#!/usr/bin/env python3
"""
Fast, single-plugin structural check for the Digital Agency plugin monorepo.

The "typecheck" equivalent of `validate.py`: checks that one plugin directory
is internally well-formed — manifests, MCP connector definitions, SKILL.md
frontmatter, hooks.json, JSON sanity — without touching marketplace parity,
cross-repo references, bundled-skill drift, or evals schema. Those stay in
`validate.py`, which only makes sense once a plugin is registered in both
marketplace manifests.

Run this while iterating on a practice, skill, or connector before it's
registered anywhere, and as the per-plugin gate before a release.

Usage: python3 scripts/plugin-check.py [PLUGIN_DIR ...] [options]
  (no PLUGIN_DIR)        Check every plugin directory found in the repo
  --format pretty|json   Output format (default: pretty)
  --help                 Print usage and exit

A "plugin directory" is any directory containing .claude-plugin/plugin.json.

Exits 0 on success, non-zero on failure.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VALIDATE_PATH = Path(__file__).resolve().parent / "validate.py"


def load_validate_module():
    spec = importlib.util.spec_from_file_location("agency_validate", VALIDATE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {VALIDATE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["agency_validate"] = module
    spec.loader.exec_module(module)
    return module


validate = load_validate_module()


def discover_plugin_dirs() -> list[Path]:
    dirs: set[Path] = set()
    for manifest in ROOT.glob("**/.claude-plugin/plugin.json"):
        if ".git" in manifest.parts:
            continue
        dirs.add(manifest.parent.parent)
    return sorted(dirs)


class PluginChecker:
    def __init__(self, fmt: str) -> None:
        self.fmt = fmt
        # skip_drift / strict are irrelevant here — reused purely for
        # load_json / parse_frontmatter / fail / warn / pass_ / issue tracking
        self.v = validate.Validator(fmt, strict=False, skip_drift=True)

    def rel(self, path: Path) -> str:
        return self.v.rel(path)

    def check_plugin(self, plugin_dir: Path) -> None:
        self.v.current_check = "pluginCheck"
        rel_dir = self.rel(plugin_dir)
        if self.fmt == "pretty":
            print(f"\n[{rel_dir}]")

        if not plugin_dir.is_dir():
            self.v.fail("PLUGIN_DIR_MISSING", f"{rel_dir} is not a directory", file=rel_dir)
            return

        self._check_manifests(plugin_dir)
        self._check_mcp(plugin_dir)
        self._check_hooks(plugin_dir)
        self._check_skill_frontmatter(plugin_dir)
        self._check_json_sanity(plugin_dir)

    def _check_manifests(self, plugin_dir: Path) -> None:
        manifest_paths = (
            plugin_dir / ".claude-plugin" / "plugin.json",
            plugin_dir / ".cursor-plugin" / "plugin.json",
        )
        found_any = False
        for manifest_path in manifest_paths:
            if not manifest_path.is_file():
                continue
            found_any = True
            manifest = self.v.load_json(manifest_path)
            if not isinstance(manifest, dict):
                continue
            for field_name in validate.PLUGIN_REQUIRED_FIELDS:
                if manifest.get(field_name):
                    self.v.pass_(f'{self.rel(manifest_path)} has "{field_name}"')
                else:
                    self.v.fail(
                        "PLUGIN_FIELD_MISSING",
                        f'{self.rel(manifest_path)} missing required field "{field_name}"',
                        file=self.rel(manifest_path),
                    )
            name = manifest.get("name")
            if isinstance(name, str) and not validate.PLUGIN_NAME_RE.match(name):
                self.v.fail(
                    "PLUGIN_NAME_INVALID",
                    f"{self.rel(manifest_path)} name {name!r} must match "
                    f"^[a-z0-9][a-z0-9-]{{1,63}}$",
                    file=self.rel(manifest_path),
                )
            if manifest.get("author") is None:
                self.v.warn(
                    "PLUGIN_AUTHOR_MISSING",
                    f"{self.rel(manifest_path)} missing author field",
                    file=self.rel(manifest_path),
                )
        if not found_any:
            self.v.fail(
                "PLUGIN_MANIFEST_MISSING",
                f"{self.rel(plugin_dir)} has no .claude-plugin/plugin.json or "
                ".cursor-plugin/plugin.json",
                file=self.rel(plugin_dir),
            )

    def _check_mcp(self, plugin_dir: Path) -> None:
        mcp_path = plugin_dir / ".mcp.json"
        if not mcp_path.is_file():
            return
        mcp = self.v.load_json(mcp_path)
        if mcp is None:
            return
        # Standard Claude Code plugin-root format: {"mcpServers": {...}},
        # auto-discovered — no manifest field required for this shape.
        if isinstance(mcp, dict) and "mcpServers" in mcp:
            servers = mcp.get("mcpServers")
            if not isinstance(servers, dict) or not servers:
                self.v.fail(
                    "MCP_EMPTY",
                    f"{self.rel(mcp_path)} mcpServers must define at least one server",
                    file=self.rel(mcp_path),
                )
            else:
                self.v.pass_(f"{self.rel(mcp_path)} defines {len(servers)} server(s)")
        elif isinstance(mcp, dict) and mcp:
            # connectors/<slug>/.mcp.json legacy shape: server(s) at top level,
            # referenced explicitly from plugin.json via "mcpServers": "./.mcp.json"
            self.v.pass_(f"{self.rel(mcp_path)} defines {len(mcp)} server(s)")
            self._check_connector_manifest_ref(plugin_dir, mcp_path)
        else:
            self.v.fail(
                "MCP_EMPTY",
                f"{self.rel(mcp_path)} must define at least one MCP server",
                file=self.rel(mcp_path),
            )

    def _check_connector_manifest_ref(self, plugin_dir: Path, mcp_path: Path) -> None:
        if plugin_dir.parent.name != "connectors":
            return
        for manifest_path in (
            plugin_dir / ".claude-plugin" / "plugin.json",
            plugin_dir / ".cursor-plugin" / "plugin.json",
        ):
            if not manifest_path.is_file():
                continue
            manifest = self.v.load_json(manifest_path)
            if not isinstance(manifest, dict):
                continue
            if manifest.get("mcpServers") != "./.mcp.json":
                self.v.fail(
                    "MCP_REF_MISSING",
                    f'{self.rel(manifest_path)} must set "mcpServers": "./.mcp.json"',
                    file=self.rel(manifest_path),
                )
            else:
                self.v.pass_(f"{self.rel(manifest_path)} references .mcp.json")

    def _check_hooks(self, plugin_dir: Path) -> None:
        hooks_path = plugin_dir / "hooks" / "hooks.json"
        if not hooks_path.is_file():
            return
        hooks = self.v.load_json(hooks_path)
        if isinstance(hooks, (dict, list)):
            self.v.pass_(f"{self.rel(hooks_path)} is valid JSON")

    def _check_skill_frontmatter(self, plugin_dir: Path) -> None:
        skill_paths = sorted(plugin_dir.glob("**/SKILL.md"))
        for skill_path in skill_paths:
            rel = self.rel(skill_path)
            text = skill_path.read_text(encoding="utf-8")
            frontmatter, _, errors = self.v.parse_frontmatter(text)
            if errors:
                for err in errors:
                    self.v.fail("SKILL_FRONTMATTER", f"{rel}: {err}", file=rel)
                continue
            assert frontmatter is not None
            missing = [
                required
                for required in ("name", "description", "allowed-tools")
                if required not in frontmatter
            ]
            for required in missing:
                self.v.fail(
                    "SKILL_FIELD_MISSING",
                    f'{rel} frontmatter missing "{required}"',
                    file=rel,
                )
            if not missing:
                self.v.pass_(f"{rel} frontmatter OK")

    def _check_json_sanity(self, plugin_dir: Path) -> None:
        json_paths = sorted(plugin_dir.glob("**/*.json"))
        for json_path in json_paths:
            rel = self.rel(json_path)
            try:
                json.loads(json_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                self.v.fail("JSON_INVALID", f"{rel} is not valid JSON: {exc}", file=rel)


def print_usage() -> None:
    print(__doc__.strip())


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("plugin_dirs", nargs="*")
    parser.add_argument("--format", choices=("pretty", "json"), default="pretty")
    parser.add_argument("--help", action="store_true")
    args = parser.parse_args()

    if args.help:
        print_usage()
        return 0

    checker = PluginChecker(args.format)

    if args.plugin_dirs:
        targets = [Path(p).resolve() for p in args.plugin_dirs]
    else:
        targets = discover_plugin_dirs()

    if checker.fmt == "pretty":
        print("Digital Agency — Plugin Check\n" + "=" * 40)

    for plugin_dir in targets:
        checker.check_plugin(plugin_dir)

    v = checker.v
    error_count = sum(1 for i in v.issues if i.severity == "error")
    warn_count = sum(1 for i in v.issues if i.severity == "warning")

    if checker.fmt == "json":
        payload: dict[str, Any] = {
            "version": 1,
            "targets": [checker.rel(p) for p in targets],
            "summary": {"errors": error_count, "warnings": warn_count},
            "issues": [
                {
                    "code": i.code,
                    "severity": i.severity,
                    "message": i.message,
                    "file": i.file,
                    "hint": i.hint,
                }
                for i in v.issues
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        print("\n" + "=" * 40)
        if error_count:
            print(f"\nFAILED — {error_count} error(s), {warn_count} warning(s)\n", file=sys.stderr)
        elif warn_count:
            print(f"\nPASSED with {warn_count} warning(s)\n")
        else:
            print("\nPASSED — all checks OK\n")

    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())