#!/usr/bin/env python3
"""Validate Ralph loop tooling across agent-plugins.

Usage:
    python3 plugin-management/scripts/validate_ralph.py [--quiet]

Checks Ralph shell syntax and hook suites, preset reachability, and tasks
example backlog epic-path conventions. Skill frontmatter, agent contracts,
and evals schema live in ``scripts/validate_skills.py``.

Exits 0 when everything passes, 1 otherwise.

Invoke with ``python3 plugin-management/scripts/validate_ralph.py`` rather than
relying on the executable bit — a lost +x should not be able to take CI down.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RALPH_ROOT = REPO_ROOT / "ralph-loop"

SHELL_GLOBS = ("hooks/lib/*.sh", "hooks/*/*.sh", "scripts/*.sh")
EXECUTABLE_REQUIRED = (
    "hooks/claude/stop-hook.sh",
    "hooks/cursor/ralph-stop.sh",
    "hooks/cursor/ralph-capture.sh",
    "scripts/seed-ralph-loop.sh",
)
STRUCTURAL_PLACEHOLDERS = (
    "PRESET_BODY",
    "COMPLETION_BLOCK",
    "STATE_BLOCK",
    "STUCK_BLOCK",
    "TASK_PROMPT",
    "CUSTOM_STEPS",
)


class Report:
    """Collects results so the summary reflects the whole run, not the first failure."""

    def __init__(self, quiet: bool = False) -> None:
        self.failed = False
        self.quiet = quiet

    def ok(self, message: str) -> None:
        if not self.quiet:
            print(f"ok: {message}")

    def skip(self, message: str) -> None:
        if not self.quiet:
            print(f"skip: {message}")

    def fail(self, message: str, detail: str | list[str] | None = None) -> None:
        self.failed = True
        print(f"FAIL: {message}")
        if detail:
            lines = detail.splitlines() if isinstance(detail, str) else detail
            shown = lines[:20]
            for line in shown:
                print(f"  {line}")
            remaining = len(lines) - len(shown)
            if remaining > 0:
                print(f"  ... {remaining} more line(s) truncated")


_SLUG_RE = re.compile(r"specs/([a-z0-9-]+)/")
_KEBAB_TWO_WORDS_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)?$")


def check_epic_paths(report: Report) -> None:
    """Filesystem-only backlog rows must use title slugs, not internal IDs."""
    example = REPO_ROOT / "product-management/skills/tasks/examples/backlog.md"
    if not example.is_file():
        return

    problems: list[str] = []
    for line_no, line in enumerate(example.read_text().splitlines(), start=1):
        for slug in _SLUG_RE.findall(line):
            if len(slug.split("-")) > 2:
                problems.append(
                    f"line {line_no}: '{slug}' has more than two words"
                )
            elif not _KEBAB_TWO_WORDS_RE.fullmatch(slug):
                problems.append(
                    f"line {line_no}: '{slug}' must be kebab-case with at "
                    "most one hyphen (two words)"
                )

    if problems:
        report.fail("epic work paths", problems)
    else:
        report.ok(f"epic work paths in {example.relative_to(REPO_ROOT)}")


def shell_scripts() -> list[Path]:
    found: list[Path] = []
    for pattern in SHELL_GLOBS:
        found.extend(sorted(RALPH_ROOT.glob(pattern)))
    return [p for p in found if p.is_file()]


def check_shell_syntax(report: Report) -> None:
    for script in shell_scripts():
        result = subprocess.run(
            ["bash", "-n", str(script)], capture_output=True, text=True
        )
        if result.returncode != 0:
            report.fail(
                f"{script.relative_to(REPO_ROOT)} has a syntax error", result.stderr
            )


def check_shellcheck(report: Report) -> None:
    """Absence is advisory; presence is a hard dependency."""
    if not shutil.which("shellcheck"):
        report.skip("shellcheck not installed")
        return
    scripts = [str(p) for p in shell_scripts()]
    if not scripts:
        return
    result = subprocess.run(
        ["shellcheck", "-x", "-S", "warning", *scripts],
        cwd=RALPH_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        report.fail("shellcheck reported issues", result.stdout + result.stderr)
    else:
        report.ok("shellcheck clean")


def check_executable_bits(report: Report) -> None:
    """A hook without +x fails silently and the loop dies with no diagnostic."""
    for rel in EXECUTABLE_REQUIRED:
        path = RALPH_ROOT / rel
        if path.is_file() and not os.access(path, os.X_OK):
            report.fail(f"{path.relative_to(REPO_ROOT)} is not executable (chmod +x)")


def check_template_placeholders(report: Report) -> None:
    """Templates must only use placeholders the seed script can resolve."""
    assets = RALPH_ROOT / "skills/ralph-loop/assets"
    seed = RALPH_ROOT / "scripts/seed-ralph-loop.sh"
    if not (assets.is_dir() and seed.is_file()):
        return

    seed_text = seed.read_text()
    for placeholder in STRUCTURAL_PLACEHOLDERS:
        if placeholder not in seed_text:
            report.fail(
                f"template placeholder {{{{{placeholder}}}}} is never set by "
                "seed-ralph-loop.sh"
            )

    used: set[str] = set()
    for path in assets.rglob("*"):
        if path.is_file():
            try:
                used |= set(re.findall(r"\{\{([A-Z_][A-Z0-9_]*)\}\}", path.read_text()))
            except (OSError, UnicodeDecodeError):
                continue

    unresolved = sorted(
        key
        for key in used
        if not re.search(rf"(add_default|add_kv) {key}\b|\"{key}\"", seed_text)
    )
    suffix = f" (caller-supplied: {' '.join(unresolved)})" if unresolved else ""
    report.ok(f"template placeholders resolvable{suffix}")


def _check_preset_dir(
    presets_dir: Path, problems: list[str], root_label: Path
) -> None:
    if not presets_dir.is_dir():
        return

    terminal_markers = ("emit the completion promise",)
    heading_re = re.compile(r"^####\s+(\S+)\s*$", re.M)
    transition_re = re.compile(r"current_step:\s*`?([A-Za-z0-9_-]+)`?")

    for path in sorted(presets_dir.glob("*.md")):
        text = path.read_text()
        headings = list(heading_re.finditer(text))
        if not headings:
            continue
        names = {m.group(1) for m in headings}

        for i, m in enumerate(headings):
            name = m.group(1)
            start = m.end()
            end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
            body = text[start:end]

            targets = transition_re.findall(body)
            for target in targets:
                if target not in names:
                    problems.append(
                        f"{path.relative_to(root_label)}: step '{name}' sets "
                        f"current_step: {target}, which has no #### heading "
                        "in this preset"
                    )

            is_terminal = any(marker in body for marker in terminal_markers)
            if not targets and not is_terminal:
                problems.append(
                    f"{path.relative_to(root_label)}: step '{name}' has no "
                    "current_step transition on any path and does not emit "
                    "the completion promise — the loop can enter this step "
                    "and never leave it"
                )


def check_preset_reachability(report: Report) -> None:
    problems: list[str] = []
    _check_preset_dir(
        RALPH_ROOT / "skills/ralph-loop/assets/presets",
        problems,
        REPO_ROOT,
    )

    if problems:
        report.fail("preset step graph has a dead end", problems)
    else:
        report.ok("preset step graphs have no dead-end steps")


def run_suite(report: Report, rel: str, label: str) -> None:
    """Run a Ralph shell suite via bash, so a missing +x does not skip it."""
    script = RALPH_ROOT / rel
    if not script.is_file():
        return

    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "suite.log"
        with log.open("w") as handle:
            try:
                result = subprocess.run(
                    ["bash", str(script)],
                    cwd=RALPH_ROOT,
                    stdin=subprocess.DEVNULL,
                    stdout=handle,
                    stderr=subprocess.STDOUT,
                    timeout=120,
                )
            except subprocess.TimeoutExpired:
                report.fail(label, "timed out after 120s")
                return
        output = log.read_text()

    if result.returncode == 0:
        passed = re.search(r"^passed:\s*(\d+)", output, re.M)
        count = f" ({passed.group(1)} assertions)" if passed else ""
        report.ok(f"{label}{count}")
    else:
        detail = [
            line for line in output.splitlines() if line.startswith(("  - ", "failed:"))
        ]
        report.fail(label, detail or output.splitlines()[-20:])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quiet", action="store_true", help="only print failures"
    )
    args = parser.parse_args()

    report = Report(quiet=args.quiet)

    check_epic_paths(report)
    check_shell_syntax(report)
    check_shellcheck(report)
    check_executable_bits(report)
    check_template_placeholders(report)
    check_preset_reachability(report)
    run_suite(report, "scripts/test-ralph-hooks.sh", "ralph hook tests")
    run_suite(report, "scripts/test-seed-ralph-loop.sh", "ralph seed tests")

    return 1 if report.failed else 0


if __name__ == "__main__":
    sys.exit(main())
