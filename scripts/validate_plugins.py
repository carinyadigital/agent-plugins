#!/usr/bin/env python3
"""
Plugin-domain structural validation for the Digital Agency plugin monorepo.

Checks marketplace manifests, plugin.json completeness, practice-plugin MCP
definitions, hooks, JSON sanity, and cache-unsafe cross-plugin paths.

Scoped mode:
  python3 scripts/validate_plugins.py [PLUGIN_DIR ...]
checks one or more plugin directories without marketplace parity or repo-wide scans.

Usage: python3 scripts/validate_plugins.py [PLUGIN_DIR ...] [options]
  (no PLUGIN_DIR)        Full plugin-domain repo validation
  --format pretty|json   Output format (default: pretty)
  --scoped               Force scoped mode across every discovered plugin dir
  --help                 Print usage and exit

Exits 0 on success, non-zero on failure.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_lib import (  # noqa: E402
    MARKETPLACE_PATHS,
    MARKETPLACE_SYNC_FIELDS,
    PLUGIN_NAME_RE,
    PLUGIN_REQUIRED_FIELDS,
    SKIP_DRIFT_NAMES,
    SOURCE_UNSAFE_RE,
    Reporter,
    marketplace_entries,
    parse_frontmatter,
    plugin_dir_from_source,
    plugin_dirs,
    plugin_manifest_paths,
    skill_sources,
)

ROOT = Path(__file__).resolve().parents[1]


class PluginValidator(Reporter):
    # Delivery artefacts live under docs/ (see delivery-conventions.md).
    LEGACY_ARTEFACT_PATH_PATTERNS = (re.compile(r"\.digital-agency/"),)
    LEGACY_ARTEFACT_PATH_SKIP_PARTS = frozenset({".git", "node_modules", ".cursor"})
    LEGACY_ARTEFACT_PATH_SKIP_FILES = frozenset(
        {
            "scripts/validate.py",
            "scripts/validate_lib.py",
            "scripts/validate_plugins.py",
            "scripts/validate_skills.py",
            "CONTRIBUTING.md",
        }
    )

    CROSS_PLUGIN_SIBLING_RE = re.compile(
        r"\.\./(?P<plugin>engineering|architecture|product-management|design|"
        r"brand-creative|content-marketing|search-optimisation|ralph-loop|"
        r"skills-index|plugin-management|agency-hub|web-development|"
        r"delivery-practice|ux-design)/"
        r"(?:skills|references|assets|hooks|scripts|\.claude-plugin|\.cursor-plugin)/"
    )
    CROSS_PLUGIN_PATH_ALLOWLIST = frozenset(
        {
            "ralph-loop/scripts/seed-ralph-loop.sh",
        }
    )

    def check_marketplace_manifests(self) -> None:
        for marketplace_path in MARKETPLACE_PATHS:
            rel = self.rel(marketplace_path)
            data = self.load_json(marketplace_path)
            if not isinstance(data, dict):
                continue

            for field_name in ("name", "owner", "plugins"):
                if field_name not in data:
                    self.fail(
                        "MARKETPLACE_FIELD_MISSING",
                        f"{rel} missing required field {field_name!r}",
                        file=rel,
                    )
                else:
                    self.pass_(f'{rel} has "{field_name}"')

            plugins = data.get("plugins")
            if not isinstance(plugins, list):
                self.fail(
                    "MARKETPLACE_PLUGINS_INVALID",
                    f"{rel} plugins must be an array",
                    file=rel,
                )
                continue

            seen: set[str] = set()
            for entry in plugins:
                if not isinstance(entry, dict):
                    self.fail(
                        "MARKETPLACE_ENTRY_INVALID",
                        f"{rel} has non-object plugin entry",
                        file=rel,
                    )
                    continue

                name = entry.get("name")
                source = entry.get("source")
                description = entry.get("description", "")

                if not isinstance(name, str) or not name:
                    self.fail(
                        "MARKETPLACE_NAME_MISSING",
                        f"{rel} plugin entry missing name",
                        file=rel,
                    )
                    continue

                if name in seen:
                    self.fail(
                        "MARKETPLACE_DUPLICATE",
                        f"{rel} duplicate plugin name {name!r}",
                        file=rel,
                        hint="Each plugin name must be unique (I2)",
                    )
                seen.add(name)

                if not PLUGIN_NAME_RE.match(name):
                    self.fail(
                        "MARKETPLACE_NAME_INVALID",
                        f"{rel} plugin name {name!r} must match "
                        f"^[a-z0-9][a-z0-9-]{{1,63}}$ (I11)",
                        file=rel,
                    )

                if not isinstance(description, str) or not (
                    10 <= len(description.strip()) <= 2000
                ):
                    self.fail(
                        "MARKETPLACE_DESC_INVALID",
                        f"{rel} plugin {name!r} description must be 10–2000 chars (I3)",
                        file=rel,
                    )

                if not isinstance(source, str) or not source:
                    self.fail(
                        "MARKETPLACE_SOURCE_MISSING",
                        f"{rel} plugin {name!r} missing source",
                        file=rel,
                    )
                    continue

                if SOURCE_UNSAFE_RE.search(source):
                    self.fail(
                        "MARKETPLACE_SOURCE_UNSAFE",
                        f"{rel} plugin {name!r} source contains unsafe characters "
                        f"(I9): {source!r}",
                        file=rel,
                    )

                plugin_dir = plugin_dir_from_source(source)
                if plugin_dir is None:
                    continue
                if not plugin_dir.is_dir():
                    self.fail(
                        "MARKETPLACE_SOURCE_MISSING_DIR",
                        f"{rel} plugin {name!r} source {source} is not a directory",
                        file=rel,
                        hint=f"Create {source}/ or fix marketplace entry",
                    )
                    continue

                claude_manifest, cursor_manifest = plugin_manifest_paths(plugin_dir)
                if not claude_manifest.is_file():
                    self.fail(
                        "PLUGIN_MANIFEST_MISSING",
                        f"{self.rel(claude_manifest)} not found for marketplace "
                        f"plugin {name!r}",
                        file=self.rel(claude_manifest),
                    )
                if not cursor_manifest.is_file():
                    self.fail(
                        "PLUGIN_MANIFEST_MISSING",
                        f"{self.rel(cursor_manifest)} not found for marketplace "
                        f"plugin {name!r}",
                        file=self.rel(cursor_manifest),
                    )

            self.pass_(f"{rel}: {len(plugins)} plugin(s) enumerated")

    def check_marketplace_parity(self) -> None:
        claude = self.load_json(MARKETPLACE_PATHS[0])
        cursor = self.load_json(MARKETPLACE_PATHS[1])
        if not isinstance(claude, dict) or not isinstance(cursor, dict):
            return

        claude_plugins = claude.get("plugins", [])
        cursor_plugins = cursor.get("plugins", [])
        if not isinstance(claude_plugins, list) or not isinstance(cursor_plugins, list):
            return

        def key(entry: dict[str, Any]) -> tuple[str, str]:
            return (str(entry.get("name", "")), str(entry.get("source", "")))

        claude_set = {key(p) for p in claude_plugins if isinstance(p, dict)}
        cursor_set = {key(p) for p in cursor_plugins if isinstance(p, dict)}

        only_claude = claude_set - cursor_set
        only_cursor = cursor_set - claude_set
        if only_claude or only_cursor:
            if only_claude:
                self.fail(
                    "MARKETPLACE_PARITY",
                    f"plugins only in .claude-plugin/marketplace.json: "
                    f"{sorted(only_claude)!r}",
                    file=".claude-plugin/marketplace.json",
                )
            if only_cursor:
                self.fail(
                    "MARKETPLACE_PARITY",
                    f"plugins only in .cursor-plugin/marketplace.json: "
                    f"{sorted(only_cursor)!r}",
                    file=".cursor-plugin/marketplace.json",
                )
        else:
            self.pass_("Claude and Cursor marketplace manifests list the same plugins")

    def check_marketplace_plugin_sync(self) -> None:
        marketplace = self.load_json(MARKETPLACE_PATHS[0])
        if not isinstance(marketplace, dict):
            return

        plugins = marketplace.get("plugins", [])
        if not isinstance(plugins, list):
            return

        for entry in plugins:
            if not isinstance(entry, dict):
                continue
            name = entry.get("name", "<unnamed>")
            source = entry.get("source")
            if not isinstance(source, str):
                continue

            plugin_dir = plugin_dir_from_source(source)
            if plugin_dir is None:
                continue

            manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
            manifest = self.load_json(manifest_path)
            if not isinstance(manifest, dict):
                continue

            drift_fields: list[str] = []
            for field_name in MARKETPLACE_SYNC_FIELDS:
                marketplace_value = entry.get(field_name)
                plugin_value = manifest.get(field_name)
                if marketplace_value != plugin_value:
                    drift_fields.append(field_name)
                    self.fail(
                        "MARKETPLACE_DRIFT",
                        f"{name}.{field_name}: marketplace={marketplace_value!r} "
                        f"plugin={plugin_value!r}",
                        file=self.rel(manifest_path),
                        hint="Keep marketplace.json in sync with plugin.json",
                    )

            if not drift_fields:
                self.pass_(f"{name}: marketplace ↔ plugin.json fields aligned")

            author = manifest.get("author")
            if author is None:
                self.warn(
                    "PLUGIN_AUTHOR_MISSING",
                    f"{self.rel(manifest_path)} missing author field",
                    file=self.rel(manifest_path),
                )

    def check_plugin_manifests(self) -> None:
        checked: set[str] = set()
        for entry in marketplace_entries(self):
            if not isinstance(entry, dict):
                continue
            source = entry.get("source")
            if not isinstance(source, str):
                continue
            plugin_dir = plugin_dir_from_source(source)
            if plugin_dir is None or not plugin_dir.is_dir():
                continue
            rel_source = self.rel(plugin_dir)
            if rel_source in checked:
                continue
            checked.add(rel_source)

            for manifest_path in plugin_manifest_paths(plugin_dir):
                manifest = self.load_json(manifest_path)
                if not isinstance(manifest, dict):
                    continue
                for field_name in PLUGIN_REQUIRED_FIELDS:
                    if manifest.get(field_name):
                        self.pass_(f'{self.rel(manifest_path)} has "{field_name}"')
                    else:
                        self.fail(
                            "PLUGIN_FIELD_MISSING",
                            f'{self.rel(manifest_path)} missing required field '
                            f'"{field_name}"',
                            file=self.rel(manifest_path),
                        )

    def check_mcp_connectors(self) -> None:
        checked: set[str] = set()
        for entry in marketplace_entries(self):
            if not isinstance(entry, dict):
                continue
            source = entry.get("source")
            if not isinstance(source, str):
                continue
            plugin_dir = plugin_dir_from_source(source)
            if plugin_dir is None or not plugin_dir.is_dir():
                continue
            mcp_path = plugin_dir / ".mcp.json"
            if not mcp_path.is_file():
                continue
            rel_source = self.rel(plugin_dir)
            if rel_source in checked:
                continue
            checked.add(rel_source)

            mcp = self.load_json(mcp_path)
            if not isinstance(mcp, dict):
                continue
            servers = mcp.get("mcpServers")
            if not isinstance(servers, dict) or not servers:
                self.fail(
                    "MCP_EMPTY",
                    f"{self.rel(mcp_path)} mcpServers must define at least one server",
                    file=self.rel(mcp_path),
                )
            else:
                self.pass_(f"{self.rel(mcp_path)} defines {len(servers)} server(s)")

    def check_json_files(self) -> None:
        json_files = sorted(
            path
            for path in ROOT.rglob("*.json")
            if ".git" not in path.parts and "node_modules" not in path.parts
        )
        invalid = 0
        for json_path in json_files:
            if self.load_json(json_path) is None and json_path.exists():
                invalid += 1
        if invalid == 0:
            self.pass_(f"All {len(json_files)} JSON file(s) parse cleanly")

    def check_hooks_json(self) -> None:
        hooks_path = ROOT / "hooks" / "hooks.json"
        if not hooks_path.is_file():
            # hooks may live inside plugins only
            self.pass_("No root hooks/hooks.json (OK if hooks are plugin-local)")
            return
        hooks = self.load_json(hooks_path)
        if isinstance(hooks, dict):
            self.pass_("hooks/hooks.json is valid JSON")
            if hooks.get("hooks") is None:
                self.warn(
                    "HOOKS_EMPTY",
                    "hooks/hooks.json has no hooks registered",
                    file="hooks/hooks.json",
                )

    def check_legacy_artefact_paths(self) -> None:
        offenders: list[tuple[str, int, str]] = []
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file():
                continue
            rel = self.rel(path)
            if rel in self.LEGACY_ARTEFACT_PATH_SKIP_FILES:
                continue
            if any(part in self.LEGACY_ARTEFACT_PATH_SKIP_PARTS for part in path.parts):
                continue
            if path.suffix in {".png", ".jpg", ".gif", ".webp", ".woff", ".woff2"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                for pattern in self.LEGACY_ARTEFACT_PATH_PATTERNS:
                    if pattern.search(line):
                        offenders.append((self.rel(path), line_no, line.strip()))
                        break

        if offenders:
            for file_path, line_no, snippet in offenders[:20]:
                self.fail(
                    "LEGACY_ARTEFACT_PATH",
                    f"Legacy artefact path reference: {snippet[:120]}",
                    file=file_path,
                    line=line_no,
                    hint="Use docs/ paths per delivery-conventions.md "
                    "(.agency/target.json stays for binding)",
                )
            if len(offenders) > 20:
                self.fail(
                    "LEGACY_ARTEFACT_PATH",
                    f"... and {len(offenders) - 20} more legacy path reference(s)",
                )
        else:
            self.pass_("No obsolete .digital-agency/ path references")

    def check_cross_plugin_paths(self) -> None:
        offenders: list[tuple[str, int, str]] = []
        for plugin_dir in plugin_dirs():
            plugin_name = plugin_dir.name
            for path in sorted(plugin_dir.rglob("*")):
                if not path.is_file():
                    continue
                rel = self.rel(path)
                if rel in self.CROSS_PLUGIN_PATH_ALLOWLIST:
                    continue
                if path.suffix in {".png", ".jpg", ".gif", ".webp", ".woff", ".woff2"}:
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    continue
                for line_no, line in enumerate(text.splitlines(), start=1):
                    for match in self.CROSS_PLUGIN_SIBLING_RE.finditer(line):
                        if match.group("plugin") == plugin_name:
                            continue
                        offenders.append((rel, line_no, line.strip()))
                        break

        if offenders:
            for file_path, line_no, snippet in offenders[:20]:
                self.fail(
                    "CROSS_PLUGIN_PATH",
                    f"Sibling-plugin path (unsafe in plugin cache): {snippet[:120]}",
                    file=file_path,
                    line=line_no,
                    hint="Use slash commands + docs/CROSS-PLUGIN-CONTRACTS.md; "
                    "shell allowlist only in seed-ralph-loop.sh",
                )
            if len(offenders) > 20:
                self.fail(
                    "CROSS_PLUGIN_PATH",
                    f"... and {len(offenders) - 20} more cross-plugin path "
                    f"reference(s)",
                )
        else:
            self.pass_("No cache-unsafe sibling-plugin ../ references in plugin trees")

    # ------------------------------------------------------------------
    # Scoped (per-plugin) checks
    # ------------------------------------------------------------------

    def check_scoped_plugin(self, plugin_dir: Path) -> None:
        self.current_check = "pluginCheck"
        rel_dir = self.rel(plugin_dir)
        if self.fmt == "pretty":
            print(f"\n[{rel_dir}]")

        if not plugin_dir.is_dir():
            self.fail("PLUGIN_DIR_MISSING", f"{rel_dir} is not a directory", file=rel_dir)
            return

        self._scoped_manifests(plugin_dir)
        self._scoped_mcp(plugin_dir)
        self._scoped_hooks(plugin_dir)
        self._scoped_skill_frontmatter(plugin_dir)
        self._scoped_json_sanity(plugin_dir)

    def _scoped_manifests(self, plugin_dir: Path) -> None:
        manifest_paths = plugin_manifest_paths(plugin_dir)
        found_any = False
        for manifest_path in manifest_paths:
            if not manifest_path.is_file():
                continue
            found_any = True
            manifest = self.load_json(manifest_path)
            if not isinstance(manifest, dict):
                continue
            for field_name in PLUGIN_REQUIRED_FIELDS:
                if manifest.get(field_name):
                    self.pass_(f'{self.rel(manifest_path)} has "{field_name}"')
                else:
                    self.fail(
                        "PLUGIN_FIELD_MISSING",
                        f'{self.rel(manifest_path)} missing required field '
                        f'"{field_name}"',
                        file=self.rel(manifest_path),
                    )
            name = manifest.get("name")
            if isinstance(name, str) and not PLUGIN_NAME_RE.match(name):
                self.fail(
                    "PLUGIN_NAME_INVALID",
                    f"{self.rel(manifest_path)} name {name!r} must match "
                    f"^[a-z0-9][a-z0-9-]{{1,63}}$",
                    file=self.rel(manifest_path),
                )
            if manifest.get("author") is None:
                self.warn(
                    "PLUGIN_AUTHOR_MISSING",
                    f"{self.rel(manifest_path)} missing author field",
                    file=self.rel(manifest_path),
                )
        if not found_any:
            self.fail(
                "PLUGIN_MANIFEST_MISSING",
                f"{self.rel(plugin_dir)} has no .claude-plugin/plugin.json or "
                ".cursor-plugin/plugin.json",
                file=self.rel(plugin_dir),
            )

    def _scoped_mcp(self, plugin_dir: Path) -> None:
        mcp_path = plugin_dir / ".mcp.json"
        if not mcp_path.is_file():
            return
        mcp = self.load_json(mcp_path)
        if mcp is None:
            return
        if isinstance(mcp, dict) and "mcpServers" in mcp:
            servers = mcp.get("mcpServers")
            if not isinstance(servers, dict) or not servers:
                self.fail(
                    "MCP_EMPTY",
                    f"{self.rel(mcp_path)} mcpServers must define at least one server",
                    file=self.rel(mcp_path),
                )
            else:
                self.pass_(f"{self.rel(mcp_path)} defines {len(servers)} server(s)")
        elif isinstance(mcp, dict) and mcp:
            self.fail(
                "MCP_SHAPE_INVALID",
                f"{self.rel(mcp_path)} must use the mcpServers wrapper shape",
                file=self.rel(mcp_path),
            )
        else:
            self.fail(
                "MCP_EMPTY",
                f"{self.rel(mcp_path)} must define at least one MCP server",
                file=self.rel(mcp_path),
            )

    def _scoped_hooks(self, plugin_dir: Path) -> None:
        hooks_path = plugin_dir / "hooks" / "hooks.json"
        if not hooks_path.is_file():
            return
        hooks = self.load_json(hooks_path)
        if isinstance(hooks, (dict, list)):
            self.pass_(f"{self.rel(hooks_path)} is valid JSON")

    def _scoped_skill_frontmatter(self, plugin_dir: Path) -> None:
        skill_paths = sorted(plugin_dir.glob("**/SKILL.md"))
        for skill_path in skill_paths:
            rel = self.rel(skill_path)
            text = skill_path.read_text(encoding="utf-8")
            frontmatter, _, errors = parse_frontmatter(text)
            if errors:
                for err in errors:
                    self.fail("SKILL_FRONTMATTER", f"{rel}: {err}", file=rel)
                continue
            assert frontmatter is not None
            missing = [
                required
                for required in ("name", "description", "allowed-tools")
                if required not in frontmatter
            ]
            for required in missing:
                self.fail(
                    "SKILL_FIELD_MISSING",
                    f'{rel} frontmatter missing "{required}"',
                    file=rel,
                )
            if not missing:
                self.pass_(f"{rel} frontmatter OK")

    def _scoped_json_sanity(self, plugin_dir: Path) -> None:
        for json_path in sorted(plugin_dir.glob("**/*.json")):
            rel = self.rel(json_path)
            try:
                json.loads(json_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                self.fail("JSON_INVALID", f"{rel} is not valid JSON: {exc}", file=rel)

    def run_full(self) -> int:
        if self.fmt == "pretty":
            print("Digital Agency — Plugin Validation\n" + "=" * 40)

        checks = [
            ("marketplaceManifests", "Marketplace manifest validity", self.check_marketplace_manifests),
            ("marketplaceParity", "Claude ↔ Cursor marketplace parity", self.check_marketplace_parity),
            ("marketplacePluginSync", "Marketplace ↔ plugin.json sync", self.check_marketplace_plugin_sync),
            ("pluginManifests", "Per-plugin manifest completeness", self.check_plugin_manifests),
            ("mcpConnectors", "Practice plugin MCP definitions", self.check_mcp_connectors),
            ("jsonFiles", "Repository JSON sanity", self.check_json_files),
            ("hooksJson", "hooks/hooks.json validity", self.check_hooks_json),
            ("legacyArtefactPaths", "No obsolete .digital-agency/ path references", self.check_legacy_artefact_paths),
            ("crossPluginPaths", "No cache-unsafe sibling-plugin ../ references", self.check_cross_plugin_paths),
        ]
        for name, label, fn in checks:
            self.section(f"[{self.check_count + 1}] {label}")
            self.timed(name, label, fn)

        return self.print_summary(title="summary")

    def run_scoped(self, targets: list[Path]) -> int:
        if self.fmt == "pretty":
            print("Digital Agency — Plugin Check\n" + "=" * 40)

        for plugin_dir in targets:
            self.check_scoped_plugin(plugin_dir)

        if self.fmt == "json":
            payload: dict[str, Any] = {
                "version": 1,
                "targets": [self.rel(p) for p in targets],
                "summary": {
                    "errors": self.error_count(),
                    "warnings": self.warning_count(),
                },
                "issues": [
                    {
                        "code": i.code,
                        "severity": i.severity,
                        "message": i.message,
                        "file": i.file,
                        "hint": i.hint,
                    }
                    for i in self.issues
                ],
            }
            print(json.dumps(payload, indent=2))
            return 1 if self.error_count() else 0

        return self.print_summary(title="summary")


# Back-compat alias for tests that imported PluginChecker
class PluginChecker:
    def __init__(self, fmt: str) -> None:
        self.fmt = fmt
        self.v = PluginValidator(fmt, strict=False, skip_drift=True)

    def rel(self, path: Path) -> str:
        return self.v.rel(path)

    def check_plugin(self, plugin_dir: Path) -> None:
        self.v.check_scoped_plugin(plugin_dir)


def print_usage() -> None:
    print(__doc__.strip())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("plugin_dirs", nargs="*")
    parser.add_argument("--format", choices=("pretty", "json"), default="pretty")
    parser.add_argument(
        "--scoped",
        action="store_true",
        help="Check every discovered plugin dir in scoped mode",
    )
    parser.add_argument("--help", action="store_true")
    args = parser.parse_args(argv)

    if args.help:
        print_usage()
        return 0

    validator = PluginValidator(args.format)

    if args.plugin_dirs or args.scoped:
        if args.plugin_dirs:
            targets = [Path(p).resolve() for p in args.plugin_dirs]
        else:
            targets = plugin_dirs()
        return validator.run_scoped(targets)

    return validator.run_full()


if __name__ == "__main__":
    raise SystemExit(main())
