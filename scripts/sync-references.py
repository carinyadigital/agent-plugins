#!/usr/bin/env python3
"""Keep meta-framework reference files in sync across practice plugins."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Canonical sources for shared meta-framework files (repo-root references/)
CANONICAL = {
    "instance-profile-template.md": REPO_ROOT / "references",
    "practice-setup-framework.md": REPO_ROOT / "references",
}

# Practice plugins that carry synced copies
PRACTICE_PLUGINS = (
    "brand-creative",
    "product-management",
    "content-marketing",
    "product-design",
    "search-optimisation",
    "engineering",
    "architecture",
)


def _targets(name: str) -> list[Path]:
    return [REPO_ROOT / plugin / "references" / name for plugin in PRACTICE_PLUGINS]


def _check() -> bool:
    ok = True
    for name, canonical_dir in CANONICAL.items():
        canonical = canonical_dir / name
        if not canonical.is_file():
            print(f"missing canonical: {canonical}", file=sys.stderr)
            ok = False
            continue
        for target in _targets(name):
            if target.resolve() == canonical.resolve():
                continue
            if not target.is_file():
                print(f"missing plugin copy: {target}", file=sys.stderr)
                ok = False
            elif not filecmp.cmp(canonical, target, shallow=False):
                print(f"out of sync: {canonical} != {target}", file=sys.stderr)
                ok = False
    return ok


def _sync() -> None:
    for name, canonical_dir in CANONICAL.items():
        canonical = canonical_dir / name
        for target in _targets(name):
            if target.resolve() == canonical.resolve():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(canonical, target)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync meta-framework reference files into practice plugins."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if canonical and plugin copies differ",
    )
    args = parser.parse_args()

    if args.check:
        return 0 if _check() else 1

    _sync()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
