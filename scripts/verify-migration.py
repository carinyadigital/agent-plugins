#!/usr/bin/env python3
"""Post-migration verification for carinya-plugins.

Checks migration-specific contracts: setup bootstrap, Ralph isolation, obsolete
namespace references, and delivery-loop cross-references.

Run after ``validate.py`` and ``skill-authoring/scripts/validate_skills.py``:

    python3 scripts/verify-migration.py
    python3 scripts/verify-migration.py --with-tooling   # also run heavy suites
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PLUGIN_DIRS = (
    "architecture",
    "brand-creative",
    "content-marketing",
    "product-design",
    "product-engineering",
    "product-management",
    "search-optimisation",
    "ralph-loop",
    "skills-index",
    "skill-authoring",
)

SETUP_PLUGINS = (
    "architecture",
    "brand-creative",
    "content-marketing",
    "product-design",
    "product-engineering",
    "product-management",
    "search-optimisation",
)
SETUP_SKILLS = tuple(f"{p}/skills/setup/SKILL.md" for p in SETUP_PLUGINS)

OBSOLETE_PATTERNS = (
    re.compile(r"agency-hub"),
    re.compile(r"web-development"),
    re.compile(r"delivery-practice"),
    re.compile(r"carinya-digital"),
    re.compile(r"ux-design:"),
)

ALLOWLIST = {
    "scripts/validate.py",
    "scripts/verify-migration.py",
    "CHANGELOG.md",
    "docs/REVIEW.md",
    "docs/RESEARCH.md",
    "docs/SKILLS-MIGRATION.md",
    "docs/CROSS-PLUGIN-CONTRACTS.md",
    "docs/archive/carinyaparc-skills-README.md",
}


def run(cmd: list[str], label: str) -> bool:
    print(f"\n== {label} ==")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"FAIL: {label}")
        return False
    print(f"ok: {label}")
    return True


def check_setup_bootstrap() -> bool:
    print("\n== setup bootstrap contract ==")
    needle = "Writes `config/instance.json` if absent"
    ok = True
    for rel in SETUP_SKILLS:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        if needle not in text:
            print(f"FAIL: {rel} missing instance bootstrap contract")
            ok = False
        else:
            print(f"ok: {rel}")
    return ok


def check_ralph_isolation() -> bool:
    print("\n== ralph hook isolation ==")
    pe_hooks = ROOT / "product-engineering/hooks/hooks.json"
    data = pe_hooks.read_text(encoding="utf-8").strip()
    if data not in ("{}", '{"hooks":[]}', '{"hooks": []}'):
        print(f"FAIL: product-engineering ships hooks: {data}")
        return False
    print("ok: product-engineering has no hooks")

    ad_hoc = ROOT / "ralph-loop/skills/ralph-loop/assets/presets/ad-hoc.md"
    if not ad_hoc.is_file():
        print("FAIL: ralph-loop ad-hoc preset missing")
        return False
    print("ok: ralph-loop ad-hoc preset present")
    return True


def check_obsolete_references() -> bool:
    print("\n== obsolete namespace grep ==")
    offenders: list[str] = []
    scan_roots = [ROOT / p for p in PLUGIN_DIRS] + [ROOT / "scripts", ROOT / ".github"]
    for base in scan_roots:
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel in ALLOWLIST:
                continue
            if path.suffix not in {".md", ".json", ".py", ".sh", ".yml", ".yaml"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for pattern in OBSOLETE_PATTERNS:
                if pattern.search(text):
                    offenders.append(f"{rel}: {pattern.pattern}")
                    break

    if offenders:
        for item in offenders[:30]:
            print(f"FAIL: {item}")
        if len(offenders) > 30:
            print(f"... and {len(offenders) - 30} more")
        return False

    print("ok: no obsolete namespace references in live plugin trees")
    return True


def check_workflow_cross_refs() -> bool:
    print("\n== delivery loop cross-refs ==")
    required = [
        ("product-management/skills/product/SKILL.md", "name: product"),
        ("product-management/skills/roadmap/SKILL.md", "name: roadmap"),
        ("product-management/skills/tasks/SKILL.md", "name: tasks"),
        ("product-engineering/skills/tdd/SKILL.md", "tdd.md"),
        ("product-engineering/skills/implement/SKILL.md", "tdd.md"),
        ("product-engineering/skills/code-review/SKILL.md", "name: code-review"),
        ("product-design/skills/ux-design-review/SKILL.md", "name: ux-design-review"),
        ("product-management/skills/validate/SKILL.md", "name: validate"),
        ("skills-index/skills/find/SKILL.md", "/plugin install"),
    ]
    ok = True
    for rel, needle in required:
        path = ROOT / rel
        if needle not in path.read_text(encoding="utf-8"):
            print(f"FAIL: {rel} missing {needle!r}")
            ok = False
        else:
            print(f"ok: {rel}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--with-tooling",
        action="store_true",
        help="also run validate.py, plugin-check, validate_skills, mutation-test, and unit tests",
    )
    args = parser.parse_args()

    checks = [
        check_setup_bootstrap(),
        check_ralph_isolation(),
        check_obsolete_references(),
        check_workflow_cross_refs(),
    ]

    if args.with_tooling:
        checks = [
            run(["python3", "scripts/validate.py"], "validate.py"),
            *[
                run(["python3", "scripts/plugin-check.py", plugin], f"plugin-check {plugin}")
                for plugin in PLUGIN_DIRS
            ],
            run(
                ["python3", "skill-authoring/scripts/validate_skills.py", "--quiet"],
                "validate_skills.py",
            ),
            run(
                ["python3", "skill-authoring/scripts/mutation-test.py"],
                "mutation-test.py",
            ),
            run(
                ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
                "unit tests",
            ),
            *checks,
        ]

    if all(checks):
        print("\nAll migration verification checks passed.")
        return 0
    print("\nMigration verification failed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
