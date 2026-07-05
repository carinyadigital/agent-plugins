#!/usr/bin/env python3
"""
Structural validation for the Digital Agency plugin monorepo.

Checks marketplace manifests, plugin.json completeness, MCP connectors,
SKILL.md frontmatter, cross-file references, bundled-skill drift, and
evals.json schema.

Usage: python3 scripts/validate.py [options]
  --format pretty|json   Output format (default: pretty)
  --strict               Treat agency-framework frontmatter gaps as errors
  --skip-drift           Skip bundled skill drift detection
  --help                 Print usage and exit

Exits 0 on success, non-zero on failure.

See CONTRIBUTING.md#validation for the full check list.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]

MARKETPLACE_PATHS = (
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / ".cursor-plugin" / "marketplace.json",
)

PLUGIN_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
SOURCE_UNSAFE_RE = re.compile(r"[;&|`$()<>]|\\.\\.")
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_FRONTMATTER_KEY_RE = re.compile(r"^(\s*)([A-Za-z0-9_-]+):\s*(.*)$")
_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_HEADING_RE = re.compile(r"^## .+$", re.MULTILINE)

WORK_SHAPES = (
    "implement-and-ship",
    "review-and-gate",
    "generate-draft",
    "orchestrate-delivery",
    "monitor-and-report",
)
OUTPUT_CLASSES = (
    "draft-for-review",
    "decision-support",
    "structured-data",
    "tracking-update",
    "applied-change",
)
AGENCY_METADATA_FIELDS = ("version", "owner", "review_cadence", "work_shape", "output_class")
AGENCY_HEADINGS = (
    "## When to use",
    "## What this skill does not do",
    "## Preconditions",
    "## Trust spine",
    "## Workflow",
    "## Outputs",
)
PLUGIN_REQUIRED_FIELDS = ("name", "version", "description")
MARKETPLACE_SYNC_FIELDS = ("name", "description")

SKIP_DRIFT_NAMES = frozenset({"references", "practice-setup"})
IGNORE_DRIFT_FILES = frozenset({".DS_Store"})

# Agents that must not bundle a skill even when a source exists (MECE ownership)
SKIP_AGENT_BUNDLES: dict[str, frozenset[str]] = {
    "frontend-engineer": frozenset({"brand-guide"}),
}


@dataclass
class Issue:
    code: str
    severity: str  # "error" | "warning"
    message: str
    check: str
    file: str | None = None
    line: int | None = None
    hint: str | None = None


@dataclass
class CheckResult:
    name: str
    label: str
    status: str  # pass | fail | warn
    duration_ms: int
    error_count: int
    warning_count: int


@dataclass
class ValidationReport:
    version: int
    timestamp: str
    summary: dict[str, int]
    check_results: list[CheckResult]
    metrics: list[dict[str, Any]]
    issues: list[Issue]
    drifted_bundles: list[str] = field(default_factory=list)


class Validator:
    def __init__(self, fmt: str, strict: bool, skip_drift: bool) -> None:
        self.fmt = fmt
        self.strict = strict
        self.skip_drift = skip_drift
        self.issues: list[Issue] = []
        self.check_results: list[CheckResult] = []
        self.metrics: list[dict[str, Any]] = []
        self.check_count = 0
        self.current_check = "unknown"
        self.drifted_bundles: list[str] = []

    def rel(self, path: Path) -> str:
        try:
            return str(path.relative_to(ROOT))
        except ValueError:
            return str(path)

    def fail(
        self,
        code: str,
        message: str,
        *,
        file: str | None = None,
        line: int | None = None,
        hint: str | None = None,
    ) -> None:
        self.issues.append(
            Issue(code, "error", message, self.current_check, file, line, hint)
        )
        if self.fmt == "pretty":
            print(f"  ✗ {message}", file=sys.stderr)

    def warn(
        self,
        code: str,
        message: str,
        *,
        file: str | None = None,
        line: int | None = None,
        hint: str | None = None,
    ) -> None:
        self.issues.append(
            Issue(code, "warning", message, self.current_check, file, line, hint)
        )
        if self.fmt == "pretty":
            print(f"  ⚠ {message}")

    def pass_(self, message: str) -> None:
        if self.fmt == "pretty":
            print(f"  ✓ {message}")

    def section(self, label: str) -> None:
        self.check_count += 1
        if self.fmt == "pretty":
            print(f"\n{label}")

    def timed(self, name: str, label: str, fn: Callable[[], None]) -> None:
        self.current_check = name
        before = len(self.issues)
        start = time.perf_counter()
        fn()
        duration_ms = round((time.perf_counter() - start) * 1000)
        self.metrics.append({"name": name, "durationMs": duration_ms})
        check_issues = self.issues[before:]
        error_count = sum(1 for i in check_issues if i.severity == "error")
        warning_count = sum(1 for i in check_issues if i.severity == "warning")
        status = "fail" if error_count else ("warn" if warning_count else "pass")
        self.check_results.append(
            CheckResult(name, label, status, duration_ms, error_count, warning_count)
        )

    def load_json(self, path: Path) -> Any | None:
        try:
            with path.open(encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError:
            self.fail("JSON_MISSING", f"{self.rel(path)} not found", file=self.rel(path))
        except json.JSONDecodeError as exc:
            self.fail(
                "JSON_INVALID",
                f"{self.rel(path)} is not valid JSON: {exc}",
                file=self.rel(path),
                hint="Fix JSON syntax errors",
            )
        return None

    def strip_scalar(self, value: str) -> str | None:
        value = value.strip()
        if not value:
            return None
        if value in {"|", ">"}:
            return value
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            return value[1:-1]
        return value

    def parse_frontmatter(self, text: str) -> tuple[dict[str, Any] | None, str, list[str]]:
        match = _FRONTMATTER_RE.match(text)
        if not match:
            return None, text, ["missing YAML frontmatter delimiters (---)"]
        raw = match.group(1)
        if not raw.strip():
            return None, text[match.end() :], ["empty frontmatter block"]

        root: dict[str, Any] = {}
        metadata: dict[str, str] = {}
        in_metadata = False
        lines = raw.splitlines()
        index = 0

        while index < len(lines):
            line = lines[index]
            key_match = _FRONTMATTER_KEY_RE.match(line)
            if not key_match:
                index += 1
                continue

            indent, key, rest = key_match.groups()
            level = len(indent)
            scalar = self.strip_scalar(rest)
            index += 1

            if level == 0 and key == "metadata":
                in_metadata = True
                root["metadata"] = metadata
                continue

            if level == 0:
                in_metadata = False

            target = metadata if in_metadata and level >= 2 else root if level == 0 else None
            if target is None:
                continue

            if scalar in (">", "|"):
                block_lines: list[str] = []
                while index < len(lines):
                    next_line = lines[index]
                    if next_line.strip() == "":
                        block_lines.append("")
                        index += 1
                        continue
                    next_match = _FRONTMATTER_KEY_RE.match(next_line)
                    if next_match and len(next_match.group(1)) <= level:
                        break
                    if next_match and not in_metadata and len(next_match.group(1)) == 0:
                        break
                    block_lines.append(next_line.strip())
                    index += 1
                folded = " ".join(part for part in block_lines if part).strip()
                if folded:
                    target[key] = folded
                elif key == "allowed-tools":
                    target[key] = []
                continue

            if scalar is None and rest.strip() == "":
                list_items: list[str] = []
                while index < len(lines):
                    next_line = lines[index]
                    item_match = re.match(r"^\s+-\s+(.*)$", next_line)
                    if not item_match:
                        break
                    item = self.strip_scalar(item_match.group(1))
                    if item:
                        list_items.append(item)
                    index += 1
                if list_items:
                    target[key] = list_items
                continue

            if scalar is not None and scalar not in {"|", ">"}:
                target[key] = scalar

        return root, text[match.end() :], []

    def skill_sources(self) -> dict[str, Path]:
        sources: dict[str, Path] = {}
        for skill_dir in ROOT.glob("skills/*/skills/*"):
            if skill_dir.is_dir() and skill_dir.name not in SKIP_DRIFT_NAMES:
                sources[skill_dir.name] = skill_dir
        brand_creative_skills = ROOT / "brand-creative" / "skills"
        if brand_creative_skills.is_dir():
            for skill_dir in brand_creative_skills.iterdir():
                if skill_dir.is_dir() and skill_dir.name not in SKIP_DRIFT_NAMES:
                    sources[skill_dir.name] = skill_dir
        delivery_practice_skills = ROOT / "delivery-practice" / "skills"
        if delivery_practice_skills.is_dir():
            for skill_dir in delivery_practice_skills.iterdir():
                if skill_dir.is_dir() and skill_dir.name not in SKIP_DRIFT_NAMES:
                    sources[skill_dir.name] = skill_dir
        content_marketing_skills = ROOT / "content-marketing" / "skills"
        if content_marketing_skills.is_dir():
            for skill_dir in content_marketing_skills.iterdir():
                if skill_dir.is_dir() and skill_dir.name not in SKIP_DRIFT_NAMES:
                    sources[skill_dir.name] = skill_dir
        return sources

    def source_skill_paths(self) -> list[Path]:
        paths = sorted(ROOT.glob("skills/*/skills/*/SKILL.md"))
        paths.extend(sorted(ROOT.glob("agency-hub/skills/*/SKILL.md")))
        paths.extend(sorted(ROOT.glob("brand-creative/skills/*/SKILL.md")))
        paths.extend(sorted(ROOT.glob("delivery-practice/skills/*/SKILL.md")))
        paths.extend(sorted(ROOT.glob("content-marketing/skills/*/SKILL.md")))
        return sorted(set(paths))

    def marketplace_entries(self) -> list[dict[str, Any]]:
        entries: list[dict[str, Any]] = []
        for marketplace_path in MARKETPLACE_PATHS:
            data = self.load_json(marketplace_path)
            if isinstance(data, dict):
                plugins = data.get("plugins")
                if isinstance(plugins, list):
                    entries.extend(plugins)
        return entries

    def plugin_dir(self, source: str) -> Path | None:
        if not source.startswith("./"):
            return None
        return ROOT / source.removeprefix("./")

    def plugin_manifest_paths(self, plugin_dir: Path) -> tuple[Path, Path]:
        return (
            plugin_dir / ".claude-plugin" / "plugin.json",
            plugin_dir / ".cursor-plugin" / "plugin.json",
        )

    # ------------------------------------------------------------------
    # Checks
    # ------------------------------------------------------------------

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
                    self.fail("MARKETPLACE_ENTRY_INVALID", f"{rel} has non-object plugin entry", file=rel)
                    continue

                name = entry.get("name")
                source = entry.get("source")
                description = entry.get("description", "")

                if not isinstance(name, str) or not name:
                    self.fail("MARKETPLACE_NAME_MISSING", f"{rel} plugin entry missing name", file=rel)
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
                        f"{rel} plugin name {name!r} must match ^[a-z0-9][a-z0-9-]{{1,63}}$ (I11)",
                        file=rel,
                    )

                if not isinstance(description, str) or not (10 <= len(description.strip()) <= 2000):
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
                        f"{rel} plugin {name!r} source contains unsafe characters (I9): {source!r}",
                        file=rel,
                    )

                plugin_dir = self.plugin_dir(source)
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

                claude_manifest, cursor_manifest = self.plugin_manifest_paths(plugin_dir)
                if not claude_manifest.is_file():
                    self.fail(
                        "PLUGIN_MANIFEST_MISSING",
                        f"{self.rel(claude_manifest)} not found for marketplace plugin {name!r}",
                        file=self.rel(claude_manifest),
                    )
                if not cursor_manifest.is_file():
                    self.fail(
                        "PLUGIN_MANIFEST_MISSING",
                        f"{self.rel(cursor_manifest)} not found for marketplace plugin {name!r}",
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
                    f"plugins only in .claude-plugin/marketplace.json: {sorted(only_claude)!r}",
                    file=".claude-plugin/marketplace.json",
                )
            if only_cursor:
                self.fail(
                    "MARKETPLACE_PARITY",
                    f"plugins only in .cursor-plugin/marketplace.json: {sorted(only_cursor)!r}",
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

            plugin_dir = self.plugin_dir(source)
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
                        f"{name}.{field_name}: marketplace={marketplace_value!r} plugin={plugin_value!r}",
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
        for entry in self.marketplace_entries():
            if not isinstance(entry, dict):
                continue
            source = entry.get("source")
            if not isinstance(source, str):
                continue
            plugin_dir = self.plugin_dir(source)
            if plugin_dir is None or not plugin_dir.is_dir():
                continue
            rel_source = self.rel(plugin_dir)
            if rel_source in checked:
                continue
            checked.add(rel_source)

            for manifest_path in self.plugin_manifest_paths(plugin_dir):
                manifest = self.load_json(manifest_path)
                if not isinstance(manifest, dict):
                    continue
                for field_name in PLUGIN_REQUIRED_FIELDS:
                    if manifest.get(field_name):
                        self.pass_(
                            f'{self.rel(manifest_path)} has "{field_name}"'
                        )
                    else:
                        self.fail(
                            "PLUGIN_FIELD_MISSING",
                            f'{self.rel(manifest_path)} missing required field "{field_name}"',
                            file=self.rel(manifest_path),
                        )

    def check_mcp_connectors(self) -> None:
        connectors_dir = ROOT / "connectors"
        if not connectors_dir.is_dir():
            self.warn("CONNECTORS_DIR_MISSING", "connectors/ directory not found")
            return

        for connector_dir in sorted(connectors_dir.iterdir()):
            if not connector_dir.is_dir():
                continue
            mcp_path = connector_dir / ".mcp.json"
            mcp = self.load_json(mcp_path)
            if mcp is None:
                continue
            if not isinstance(mcp, dict) or not mcp:
                self.fail(
                    "MCP_EMPTY",
                    f"{self.rel(mcp_path)} must define at least one MCP server",
                    file=self.rel(mcp_path),
                )
            else:
                self.pass_(f"{self.rel(mcp_path)} defines {len(mcp)} server(s)")

            for manifest_path in self.plugin_manifest_paths(connector_dir):
                manifest = self.load_json(manifest_path)
                if not isinstance(manifest, dict):
                    continue
                mcp_ref = manifest.get("mcpServers")
                if mcp_ref != "./.mcp.json":
                    self.fail(
                        "MCP_REF_MISSING",
                        f'{self.rel(manifest_path)} must set "mcpServers": "./.mcp.json"',
                        file=self.rel(manifest_path),
                    )
                else:
                    self.pass_(f"{self.rel(manifest_path)} references .mcp.json")

    def check_skill_frontmatter(self) -> None:
        for skill_path in self.source_skill_paths():
            rel = self.rel(skill_path)
            skill_name = skill_path.parent.name
            try:
                text = skill_path.read_text(encoding="utf-8")
            except OSError as exc:
                self.fail("SKILL_UNREADABLE", f"{rel}: cannot read file: {exc}", file=rel)
                continue

            frontmatter, body, parse_errs = self.parse_frontmatter(text)
            for msg in parse_errs:
                severity = self.fail if self.strict else self.warn
                severity("FM_PARSE", f"{rel}: {msg}", file=rel)

            if frontmatter is None:
                continue

            if not frontmatter.get("name"):
                self.fail("FM_NO_NAME", f"{rel} missing frontmatter name", file=rel)
            elif frontmatter["name"] != skill_name:
                self.fail(
                    "FM_NAME_MISMATCH",
                    f"{rel} frontmatter name {frontmatter['name']!r} != directory {skill_name!r}",
                    file=rel,
                )
            else:
                self.pass_(f'{rel} name matches directory "{skill_name}"')

            if not frontmatter.get("description"):
                self.fail("FM_NO_DESC", f"{rel} missing frontmatter description", file=rel)
            else:
                self.pass_(f"{rel} has description")

            if not frontmatter.get("allowed-tools"):
                msg_fn = self.fail if self.strict else self.warn
                msg_fn(
                    "FM_NO_ALLOWED_TOOLS",
                    f"{rel} missing allowed-tools (agency framework §11)",
                    file=rel,
                    hint="Add allowed-tools list to frontmatter",
                )

            metadata = frontmatter.get("metadata")
            metadata_dict = metadata if isinstance(metadata, dict) else {}
            for meta_field in AGENCY_METADATA_FIELDS:
                value = metadata_dict.get(meta_field)
                if value is None or (isinstance(value, str) and not value.strip()):
                    msg_fn = self.fail if self.strict else self.warn
                    msg_fn(
                        "FM_METADATA_MISSING",
                        f"{rel} missing metadata.{meta_field}",
                        file=rel,
                        hint="See .agents/references/agency-skill-design-framework.md §11",
                    )

            work_shape = metadata_dict.get("work_shape")
            if work_shape and work_shape not in WORK_SHAPES:
                self.fail(
                    "FM_WORK_SHAPE_INVALID",
                    f"{rel} invalid metadata.work_shape {work_shape!r}",
                    file=rel,
                    hint=f"Valid values: {', '.join(WORK_SHAPES)}",
                )

            output_class = metadata_dict.get("output_class")
            if output_class and output_class not in OUTPUT_CLASSES:
                self.fail(
                    "FM_OUTPUT_CLASS_INVALID",
                    f"{rel} invalid metadata.output_class {output_class!r}",
                    file=rel,
                    hint=f"Valid values: {', '.join(OUTPUT_CLASSES)}",
                )

            if self.strict:
                headings = _HEADING_RE.findall(body)
                for heading in AGENCY_HEADINGS:
                    if heading not in headings:
                        self.fail(
                            "SKILL_HEADING_MISSING",
                            f"{rel} missing required heading {heading!r}",
                            file=rel,
                            hint="See agency-skill-design-framework.md §11",
                        )

    def resolve_markdown_target(self, base: Path, target: str) -> Path | None:
        target = target.strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            return None
        if target.startswith("<") and target.endswith(">"):
            inner = target[1:-1]
            if inner.startswith(("http://", "https://", "mailto:", "#")):
                return None
            target = inner
        path_part = target.split("#", 1)[0]
        if not path_part:
            return None
        return (base / path_part).resolve()

    def check_markdown_references(self) -> None:
        patterns = [
            (ROOT / "skills", "skills/*/skills/*/SKILL.md"),
            (ROOT / "agents", "agents/*/agents/*.md"),
            (ROOT / "agency-hub", "agency-hub/skills/*/*.md"),
            (ROOT / "brand-creative", "brand-creative/skills/*/*.md"),
            (ROOT / "delivery-practice", "delivery-practice/skills/*/*.md"),
            (ROOT / "content-marketing", "content-marketing/skills/*/*.md"),
        ]

        checked_files: list[Path] = []
        for base, pattern in patterns:
            if base.name == "skills":
                checked_files.extend(sorted(base.glob("*/skills/*/*.md")))
            elif base.name in {"agency-hub", "brand-creative", "delivery-practice", "content-marketing"}:
                checked_files.extend(sorted(base.glob("skills/*/*.md")))
            else:
                checked_files.extend(sorted(base.glob("*/*/*.md")))

        broken = 0
        for md_path in checked_files:
            rel = self.rel(md_path)
            try:
                content = md_path.read_text(encoding="utf-8")
            except OSError:
                continue

            for match in _MD_LINK_RE.finditer(content):
                target = match.group(1)
                resolved = self.resolve_markdown_target(md_path.parent, target)
                if resolved is None:
                    continue
                if not resolved.exists():
                    broken += 1
                    self.fail(
                        "MD_LINK_BROKEN",
                        f"{rel} broken link {target!r} → {self.rel(resolved)}",
                        file=rel,
                        hint="Fix the relative path or add the missing file",
                    )

        if broken == 0:
            self.pass_(f"All markdown links resolve in {len(checked_files)} checked file(s)")

    def check_agent_prompts(self) -> None:
        for agent_dir in sorted((ROOT / "agents").glob("*")):
            if not agent_dir.is_dir():
                continue
            slug = agent_dir.name
            prompt_path = agent_dir / "agents" / f"{slug}.md"
            if not prompt_path.is_file():
                self.fail(
                    "AGENT_PROMPT_MISSING",
                    f"agents/{slug}/agents/{slug}.md not found",
                    file=f"agents/{slug}/agents/{slug}.md",
                    hint="Add canonical system prompt at agents/<slug>/agents/<slug>.md",
                )
                continue
            self.pass_(f"agents/{slug}/agents/{slug}.md exists")

    def file_digest(self, path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def collect_tree_files(self, directory: Path) -> dict[str, Path]:
        files: dict[str, Path] = {}
        if not directory.is_dir():
            return files
        for path in sorted(directory.rglob("*")):
            if path.is_file() and path.name not in IGNORE_DRIFT_FILES:
                files[str(path.relative_to(directory))] = path
        return files

    def check_bundled_skill_drift(self) -> None:
        if self.skip_drift:
            self.pass_("Bundled skill drift check skipped via --skip-drift")
            return

        sources = self.skill_sources()
        drift_count = 0
        agent_local = 0

        for agent_dir in sorted((ROOT / "agents").glob("*")):
            skills_dir = agent_dir / "skills"
            if not skills_dir.is_dir():
                continue

            skip_bundles = SKIP_AGENT_BUNDLES.get(agent_dir.name, frozenset())

            for bundled_dir in sorted(skills_dir.iterdir()):
                if not bundled_dir.is_dir() or bundled_dir.name in SKIP_DRIFT_NAMES:
                    continue

                rel_bundle = self.rel(bundled_dir)
                if bundled_dir.name in skip_bundles:
                    self.fail(
                        "SKILL_DRIFT",
                        f"{rel_bundle} must not bundle {bundled_dir.name!r} — MECE owned by brand-creative only",
                        file=rel_bundle,
                        hint="Remove the bundled copy; frontend-engineer reads brand-guide.md from the resolved path",
                    )
                    drift_count += 1
                    continue

                source_dir = sources.get(bundled_dir.name)
                if source_dir is None:
                    agent_local += 1
                    self.pass_(f"{rel_bundle} is agent-local (no skills/ source)")
                    continue

                bundled_files = self.collect_tree_files(bundled_dir)
                source_files = self.collect_tree_files(source_dir)

                bundle_rel_paths = set(bundled_files)
                source_rel_paths = set(source_files)
                missing_in_bundle = source_rel_paths - bundle_rel_paths
                extra_in_bundle = bundle_rel_paths - source_rel_paths

                for rel_path in sorted(missing_in_bundle | extra_in_bundle):
                    drift_count += 1
                    self.drifted_bundles.append(rel_bundle)
                    self.fail(
                        "SKILL_DRIFT",
                        f"{rel_bundle} drift: file {rel_path!r} differs from {self.rel(source_dir)}",
                        file=rel_bundle,
                        hint="Run python3 scripts/sync-agent-skills.py",
                    )

                for rel_path in sorted(bundle_rel_paths & source_rel_paths):
                    if self.file_digest(bundled_files[rel_path]) != self.file_digest(
                        source_files[rel_path]
                    ):
                        drift_count += 1
                        self.drifted_bundles.append(rel_bundle)
                        self.fail(
                            "SKILL_DRIFT",
                            f"{rel_bundle} drift: {rel_path} content differs from source",
                            file=rel_bundle,
                            hint="Run python3 scripts/sync-agent-skills.py",
                        )

        practice_drift = self.check_practice_plugin_skill_drift(sources)
        drift_count += practice_drift

        if drift_count == 0:
            self.pass_(
                f"No bundled skill drift detected ({agent_local} agent-local skill dir(s) skipped)"
            )

    def check_practice_plugin_skill_drift(self, sources: dict[str, Path]) -> int:
        """Practice plugins own their skills outright — no vendoring drift to check."""
        self.pass_("Practice plugins own skills outright (no discipline vendoring drift check)")
        return 0

    def _compare_bundled_tree(
        self, rel_bundle: str, bundled_dir: Path, source_dir: Path
    ) -> int:
        drift_count = 0
        bundled_files = self.collect_tree_files(bundled_dir)
        source_files = self.collect_tree_files(source_dir)

        bundle_rel_paths = set(bundled_files)
        source_rel_paths = set(source_files)
        missing_in_bundle = source_rel_paths - bundle_rel_paths
        extra_in_bundle = bundle_rel_paths - source_rel_paths

        for rel_path in sorted(missing_in_bundle | extra_in_bundle):
            drift_count += 1
            self.drifted_bundles.append(rel_bundle)
            self.fail(
                "SKILL_DRIFT",
                f"{rel_bundle} drift: file {rel_path!r} differs from {self.rel(source_dir)}",
                file=rel_bundle,
                hint="Run python3 scripts/sync-agent-skills.py",
            )

        for rel_path in sorted(bundle_rel_paths & source_rel_paths):
            if self.file_digest(bundled_files[rel_path]) != self.file_digest(
                source_files[rel_path]
            ):
                drift_count += 1
                self.drifted_bundles.append(rel_bundle)
                self.fail(
                    "SKILL_DRIFT",
                    f"{rel_bundle} drift: {rel_path} content differs from source",
                    file=rel_bundle,
                    hint="Run python3 scripts/sync-agent-skills.py",
                )
        return drift_count

    def check_evals_schema(self) -> None:
        eval_dirs = sorted(ROOT.glob("skills/*/skills/*/evals"))
        if not eval_dirs:
            self.warn("EVALS_NONE", "No evals/ directories found under skills/")
            return

        for eval_dir in eval_dirs:
            rel_dir = self.rel(eval_dir)
            evals_path = eval_dir / "evals.json"
            triggers_path = eval_dir / "trigger-queries.json"

            evals = self.load_json(evals_path)
            if isinstance(evals, dict):
                skill_name = evals.get("skill_name")
                cases = evals.get("evals")
                if not skill_name:
                    self.fail(
                        "EVALS_SKILL_NAME",
                        f"{self.rel(evals_path)} missing skill_name",
                        file=self.rel(evals_path),
                    )
                if not isinstance(cases, list) or not cases:
                    self.fail(
                        "EVALS_EMPTY",
                        f"{self.rel(evals_path)} must contain a non-empty evals array",
                        file=self.rel(evals_path),
                    )
                else:
                    for index, case in enumerate(cases, start=1):
                        if not isinstance(case, dict):
                            self.fail(
                                "EVALS_CASE_INVALID",
                                f"{self.rel(evals_path)} eval #{index} is not an object",
                                file=self.rel(evals_path),
                            )
                            continue
                        for field_name in ("id", "prompt", "expected_output", "assertions"):
                            if field_name not in case:
                                self.fail(
                                    "EVALS_CASE_FIELD",
                                    f"{self.rel(evals_path)} eval #{index} missing {field_name!r}",
                                    file=self.rel(evals_path),
                                )
                        assertions = case.get("assertions")
                        if assertions is not None and (
                            not isinstance(assertions, list) or not assertions
                        ):
                            self.fail(
                                "EVALS_ASSERTIONS",
                                f"{self.rel(evals_path)} eval #{index} assertions must be a non-empty array",
                                file=self.rel(evals_path),
                            )
                    self.pass_(f"{self.rel(evals_path)} schema OK ({len(cases)} eval(s))")

            triggers = self.load_json(triggers_path)
            if isinstance(triggers, list):
                if not triggers:
                    self.warn(
                        "TRIGGERS_EMPTY",
                        f"{self.rel(triggers_path)} is empty",
                        file=self.rel(triggers_path),
                    )
                else:
                    for index, entry in enumerate(triggers, start=1):
                        if not isinstance(entry, dict):
                            self.fail(
                                "TRIGGERS_ENTRY_INVALID",
                                f"{self.rel(triggers_path)} entry #{index} is not an object",
                                file=self.rel(triggers_path),
                            )
                            continue
                        if "query" not in entry or "should_trigger" not in entry:
                            self.fail(
                                "TRIGGERS_ENTRY_FIELD",
                                f"{self.rel(triggers_path)} entry #{index} missing query or should_trigger",
                                file=self.rel(triggers_path),
                            )
                    self.pass_(
                        f"{self.rel(triggers_path)} schema OK ({len(triggers)} trigger(s))"
                    )
            elif triggers_path.is_file():
                self.fail(
                    "TRIGGERS_INVALID",
                    f"{self.rel(triggers_path)} must be a JSON array",
                    file=self.rel(triggers_path),
                )

            if evals_path.is_file() and not triggers_path.is_file():
                self.fail(
                    "TRIGGERS_MISSING",
                    f"{rel_dir} has evals.json but missing trigger-queries.json",
                    file=rel_dir,
                )

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
        hooks = self.load_json(hooks_path)
        if isinstance(hooks, dict):
            self.pass_("hooks/hooks.json is valid JSON")
            if hooks.get("hooks") is None:
                self.warn(
                    "HOOKS_EMPTY",
                    "hooks/hooks.json has no hooks registered",
                    file="hooks/hooks.json",
                )

    def parse_cookbook_yaml(self, text: str) -> dict[str, Any]:
        data: dict[str, Any] = {}
        catalogue: dict[str, str] = {}
        current_list_key: str | None = None
        for line in text.splitlines():
            if not line.strip() or line.strip().startswith("#"):
                continue
            list_match = re.match(r"^\s+-\s+(.+)$", line)
            if list_match and current_list_key:
                item = self.strip_scalar(list_match.group(1).strip()) or list_match.group(1).strip()
                data.setdefault(current_list_key, []).append(item)
                continue
            key_match = re.match(r"^(\s*)([A-Za-z0-9_-]+):\s*(.*)$", line)
            if not key_match:
                continue
            indent, key, rest = key_match.groups()
            scalar = self.strip_scalar(rest)
            if indent:
                if key in ("plugin", "prompt", "mcp") and scalar:
                    catalogue[key] = scalar
                continue
            current_list_key = None
            if scalar:
                data[key] = scalar
            elif rest.strip() == "":
                data[key] = []
                current_list_key = key
        if catalogue:
            data["catalogue"] = catalogue
        return data

    def marketplace_plugin_names(self) -> set[str]:
        names: set[str] = set()
        for entry in self.marketplace_entries():
            name = entry.get("name")
            if isinstance(name, str):
                names.add(name)
        return names

    def check_managed_agent_cookbooks(self) -> None:
        managed_dir = ROOT / "managed-agents"
        if not managed_dir.is_dir():
            self.warn(
                "COOKBOOKS_MISSING",
                "managed-agents/ directory not found",
                file="managed-agents/",
            )
            return

        cookbook_dirs = sorted(
            path for path in managed_dir.iterdir() if path.is_dir() and path.name != ".git"
        )
        if not cookbook_dirs:
            self.fail(
                "COOKBOOKS_EMPTY",
                "managed-agents/ has no agent cookbooks",
                file="managed-agents/",
            )
            return

        plugin_names = self.marketplace_plugin_names()
        valid_platforms = {"cursor", "claude-cma", "either"}
        checked = 0

        for cookbook_dir in cookbook_dirs:
            agent_yaml = cookbook_dir / "agent.yaml"
            rel_dir = self.rel(cookbook_dir)
            if not agent_yaml.is_file():
                self.fail(
                    "COOKBOOK_MISSING_YAML",
                    f"{rel_dir} missing agent.yaml",
                    file=rel_dir,
                )
                continue

            text = agent_yaml.read_text(encoding="utf-8")
            data = self.parse_cookbook_yaml(text)
            slug = data.get("slug")
            platform = data.get("platform")
            catalogue = data.get("catalogue", {})

            if not isinstance(slug, str) or slug != cookbook_dir.name:
                self.fail(
                    "COOKBOOK_SLUG",
                    f"{rel_dir}/agent.yaml slug must match directory name",
                    file=self.rel(agent_yaml),
                )
                continue

            if platform not in valid_platforms:
                self.fail(
                    "COOKBOOK_PLATFORM",
                    f"{rel_dir}/agent.yaml has invalid platform '{platform}'",
                    file=self.rel(agent_yaml),
                )

            plugin = catalogue.get("plugin") if isinstance(catalogue, dict) else None
            if plugin not in plugin_names:
                self.fail(
                    "COOKBOOK_PLUGIN",
                    f"{rel_dir}/agent.yaml references unknown plugin '{plugin}'",
                    file=self.rel(agent_yaml),
                    hint="Register the agent in marketplace manifests",
                )

            prompt = catalogue.get("prompt") if isinstance(catalogue, dict) else None
            if isinstance(prompt, str):
                prompt_path = (cookbook_dir / prompt).resolve()
                if not prompt_path.is_file():
                    self.fail(
                        "COOKBOOK_PROMPT",
                        f"{rel_dir}/agent.yaml prompt path does not resolve: {prompt}",
                        file=self.rel(agent_yaml),
                    )

            mcp = catalogue.get("mcp") if isinstance(catalogue, dict) else None
            if isinstance(mcp, str):
                mcp_path = (cookbook_dir / mcp).resolve()
                if not mcp_path.is_file():
                    self.fail(
                        "COOKBOOK_MCP",
                        f"{rel_dir}/agent.yaml mcp path does not resolve: {mcp}",
                        file=self.rel(agent_yaml),
                    )

            skills = data.get("skills", [])
            if isinstance(skills, list):
                agent_skill_dir = ROOT / "agents" / slug / "skills"
                for skill_slug in skills:
                    if skill_slug in SKIP_DRIFT_NAMES:
                        continue
                    bundled = agent_skill_dir / skill_slug / "SKILL.md"
                    source = self.skill_sources().get(skill_slug)
                    if not bundled.is_file() and source is None:
                        self.fail(
                            "COOKBOOK_SKILL",
                            f"{rel_dir}/agent.yaml references unknown skill '{skill_slug}'",
                            file=self.rel(agent_yaml),
                        )

            connectors = data.get("connectors", [])
            if isinstance(connectors, list):
                for connector in connectors:
                    if connector not in plugin_names:
                        self.fail(
                            "COOKBOOK_CONNECTOR",
                            f"{rel_dir}/agent.yaml references unknown connector '{connector}'",
                            file=self.rel(agent_yaml),
                        )

            checked += 1

        if checked:
            self.pass_(f"{checked} managed-agent cookbook(s) OK")

    # ------------------------------------------------------------------
    # Main
    # ------------------------------------------------------------------

    def run(self) -> int:
        if self.fmt == "pretty":
            print("Digital Agency — Structural Validation\n" + "=" * 40)

        checks: list[tuple[str, str, Callable[[], None]]] = [
            ("marketplaceManifests", "Marketplace manifest validity", self.check_marketplace_manifests),
            ("marketplaceParity", "Claude ↔ Cursor marketplace parity", self.check_marketplace_parity),
            ("marketplacePluginSync", "Marketplace ↔ plugin.json sync", self.check_marketplace_plugin_sync),
            ("pluginManifests", "Per-plugin manifest completeness", self.check_plugin_manifests),
            ("mcpConnectors", "MCP connector definitions", self.check_mcp_connectors),
            ("skillFrontmatter", "SKILL.md YAML frontmatter", self.check_skill_frontmatter),
            ("markdownReferences", "Markdown cross-reference resolution", self.check_markdown_references),
            ("agentPrompts", "Agent canonical prompt files", self.check_agent_prompts),
            ("bundledSkillDrift", "Agent bundled skill drift", self.check_bundled_skill_drift),
            ("evalsSchema", "evals.json and trigger-queries.json schema", self.check_evals_schema),
            ("jsonFiles", "Repository JSON sanity", self.check_json_files),
            ("hooksJson", "hooks/hooks.json validity", self.check_hooks_json),
            ("managedAgentCookbooks", "Managed-agent cookbook definitions", self.check_managed_agent_cookbooks),
        ]

        for name, label, fn in checks:
            self.section(f"[{self.check_count + 1}] {label}")
            self.timed(name, label, fn)

        error_count = sum(1 for issue in self.issues if issue.severity == "error")
        warn_count = sum(1 for issue in self.issues if issue.severity == "warning")

        if self.fmt == "json":
            report = ValidationReport(
                version=1,
                timestamp=datetime.now(timezone.utc).isoformat(),
                summary={
                    "errors": error_count,
                    "warnings": warn_count,
                    "checks": self.check_count,
                },
                check_results=self.check_results,
                metrics=self.metrics,
                issues=self.issues,
                drifted_bundles=sorted(set(self.drifted_bundles)),
            )
            print(json.dumps(asdict(report), indent=2))
        else:
            print("\n" + "=" * 40)
            if error_count > 0:
                print(
                    f"\nFAILED — {error_count} error(s)"
                    + (f", {warn_count} warning(s)" if warn_count else "")
                    + "\n",
                    file=sys.stderr,
                )
            elif warn_count > 0:
                print(f"\nPASSED with {warn_count} warning(s)\n")
            else:
                print("\nPASSED — all checks OK\n")

        return 1 if error_count > 0 else 0


def print_usage() -> None:
    print(__doc__.strip())


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--format", choices=("pretty", "json"), default="pretty")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat agency-framework frontmatter and heading gaps as errors",
    )
    parser.add_argument(
        "--skip-drift",
        action="store_true",
        help="Skip bundled skill drift detection",
    )
    parser.add_argument("--help", action="store_true")
    args = parser.parse_args()

    if args.help:
        print_usage()
        return 0

    validator = Validator(args.format, args.strict, args.skip_drift)
    return validator.run()


if __name__ == "__main__":
    raise SystemExit(main())
