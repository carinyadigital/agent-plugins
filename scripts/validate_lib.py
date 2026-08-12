#!/usr/bin/env python3
"""Shared validation helpers for Digital Agency plugin monorepo scripts."""
from __future__ import annotations

import json
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

try:
    import yaml
except ImportError:  # pragma: no cover - CI installs PyYAML
    yaml = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[1]

MARKETPLACE_PATHS = (
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / ".cursor-plugin" / "marketplace.json",
)

PLUGIN_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
SOURCE_UNSAFE_RE = re.compile(r"[;&|`$()<>]|\\.\\.")
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_HEADING_RE = re.compile(r"^## .+$", re.MULTILINE)

SKILL_NAME_MAX = 64
SKILL_DESC_MAX = 1024
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

MODEL_TIERS = frozenset({"fast", "standard"})

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

SKIP_DRIFT_NAMES = frozenset({"references", "setup"})
IGNORE_DRIFT_FILES = frozenset({".DS_Store"})

SKIP_AGENT_BUNDLES: dict[str, frozenset[str]] = {
    "frontend-engineer": frozenset({"brand-guide"}),
}

PRACTICE_PLUGIN_DIRS = (
    "brand-creative",
    "content-marketing",
    "product-design",
    "engineering",
    "product-management",
    "search-optimisation",
    "architecture",
    "ralph-loop",
    "skills-index",
    "skill-authoring",
)

ORPHAN_SKILL_EXCLUDES = frozenset(
    {
        "skill-authoring/template",
    }
)


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


class Reporter:
    """Issue tracking + pretty/json reporting shared by plugin and skill validators."""

    def __init__(self, fmt: str, strict: bool = False, skip_drift: bool = False) -> None:
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

    def error_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "error")

    def warning_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "warning")

    def print_summary(self, title: str | None = None) -> int:
        error_count = self.error_count()
        warn_count = self.warning_count()
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
            if title:
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

    def merge_from(self, other: Reporter) -> None:
        self.issues.extend(other.issues)
        self.check_results.extend(other.check_results)
        self.metrics.extend(other.metrics)
        self.check_count += other.check_count
        self.drifted_bundles.extend(other.drifted_bundles)


def strip_scalar(value: str) -> str | None:
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


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str, list[str]]:
    """Parse YAML frontmatter via PyYAML when available; else a minimal fallback."""
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None, text, ["missing YAML frontmatter delimiters (---)"]
    raw = match.group(1)
    if not raw.strip():
        return None, text[match.end() :], ["empty frontmatter block"]
    if yaml is None:
        return None, text[match.end() :], [
            "PyYAML is required (pip install pyyaml) to parse frontmatter"
        ]
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return None, text[match.end() :], [f"invalid YAML frontmatter: {exc}"]
    if data is None:
        return None, text[match.end() :], ["empty frontmatter block"]
    if not isinstance(data, dict):
        return None, text[match.end() :], ["frontmatter must be a YAML mapping"]
    return data, text[match.end() :], []


def plugin_dirs() -> list[Path]:
    dirs: set[Path] = set()
    for manifest in ROOT.glob("**/.claude-plugin/plugin.json"):
        if ".git" in manifest.parts:
            continue
        dirs.add(manifest.parent.parent)
    return sorted(dirs)


def marketplace_entries(reporter: Reporter) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for marketplace_path in MARKETPLACE_PATHS:
        data = reporter.load_json(marketplace_path)
        if isinstance(data, dict):
            plugins = data.get("plugins")
            if isinstance(plugins, list):
                entries.extend(plugins)
    return entries


def plugin_dir_from_source(source: str) -> Path | None:
    if not source.startswith("./"):
        return None
    return ROOT / source.removeprefix("./")


def plugin_manifest_paths(plugin_dir: Path) -> tuple[Path, Path]:
    return (
        plugin_dir / ".claude-plugin" / "plugin.json",
        plugin_dir / ".cursor-plugin" / "plugin.json",
    )


def skill_sources() -> dict[str, Path]:
    sources: dict[str, Path] = {}
    for skill_dir in ROOT.glob("skills/*/skills/*"):
        if skill_dir.is_dir() and skill_dir.name not in SKIP_DRIFT_NAMES:
            sources[skill_dir.name] = skill_dir
    for practice in PRACTICE_PLUGIN_DIRS:
        practice_skills = ROOT / practice / "skills"
        if practice_skills.is_dir():
            for skill_dir in practice_skills.iterdir():
                if skill_dir.is_dir() and skill_dir.name not in SKIP_DRIFT_NAMES:
                    sources[skill_dir.name] = skill_dir
    return sources


def source_skill_paths() -> list[Path]:
    paths = sorted(ROOT.glob("skills/*/skills/*/SKILL.md"))
    for practice in PRACTICE_PLUGIN_DIRS:
        paths.extend(sorted(ROOT.glob(f"{practice}/skills/*/SKILL.md")))
    return sorted(set(paths))


def agent_paths() -> list[Path]:
    """All agent definition markdown files under practice plugins."""
    found: list[Path] = []
    for practice in PRACTICE_PLUGIN_DIRS:
        practice_root = ROOT / practice
        if not practice_root.is_dir():
            continue
        found.extend(sorted(practice_root.glob("agents/*.md")))
        found.extend(sorted(practice_root.glob("skills/*/agents/*.md")))
    return sorted(set(found))


def normalize_tools(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    if isinstance(value, list):
        tools: list[str] = []
        for item in value:
            if isinstance(item, str):
                tools.append(item.strip())
            else:
                tools.append(str(item))
        return [t for t in tools if t]
    return [str(value)]


def has_bare_bash(tools: list[str]) -> bool:
    """True when tools include unscoped Bash (not Bash(pattern:*) forms)."""
    return any(t.strip() == "Bash" for t in tools)


def file_digest(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_tree_files(directory: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    if not directory.is_dir():
        return files
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.name not in IGNORE_DRIFT_FILES:
            files[str(path.relative_to(directory))] = path
    return files


def resolve_markdown_target(base: Path, target: str) -> Path | None:
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


# Back-compat alias used by tests that historically called Validator
class Validator(Reporter):
    """Alias for Reporter with parse helpers bound as methods (test compatibility)."""

    def strip_scalar(self, value: str) -> str | None:
        return strip_scalar(value)

    def parse_frontmatter(self, text: str) -> tuple[dict[str, Any] | None, str, list[str]]:
        return parse_frontmatter(text)

    def skill_sources(self) -> dict[str, Path]:
        return skill_sources()

    def source_skill_paths(self) -> list[Path]:
        return source_skill_paths()

    def marketplace_entries(self) -> list[dict[str, Any]]:
        return marketplace_entries(self)

    def plugin_dir(self, source: str) -> Path | None:
        return plugin_dir_from_source(source)

    def plugin_manifest_paths(self, plugin_dir: Path) -> tuple[Path, Path]:
        return plugin_manifest_paths(plugin_dir)

    def plugin_dirs(self) -> list[Path]:
        return plugin_dirs()

    def file_digest(self, path: Path) -> str:
        return file_digest(path)

    def collect_tree_files(self, directory: Path) -> dict[str, Path]:
        return collect_tree_files(directory)

    def resolve_markdown_target(self, base: Path, target: str) -> Path | None:
        return resolve_markdown_target(base, target)

    def run(self) -> int:
        raise NotImplementedError("Use validate_plugins / validate_skills / validate.py")
