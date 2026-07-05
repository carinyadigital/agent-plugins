#!/usr/bin/env python3
"""
Re-sync bundled skills from canonical source trees.

Agent plugins under agents/<slug>/skills/<name>/ bundle copies from:
  - skills/<discipline>/skills/<name>/  (discipline plugins)
  - brand-creative/skills/<name>/       (brand-guide, brand-voice — MECE owned here)
  - delivery-practice/skills/<name>/    (product, backlog, sprint, … — MECE owned here)

Run after editing a canonical skill to propagate into every agent that bundles it.

Usage: python3 scripts/sync-agent-skills.py
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
DISCIPLINES = ROOT / "skills"
BRAND_CREATIVE_SKILLS = ROOT / "brand-creative" / "skills"
DELIVERY_PRACTICE_SKILLS = ROOT / "delivery-practice" / "skills"
BRAND_CONVENTIONS = ROOT / "brand-creative" / "references" / "brand-conventions.md"
DELIVERY_CONVENTIONS = ROOT / "delivery-practice" / "references" / "delivery-conventions.md"

# agent slug -> skill names to skip when syncing (MECE — skill lives elsewhere only)
SKIP_AGENT_BUNDLES: dict[str, set[str]] = {
    "frontend-engineer": {"brand-guide"},
}

synced = 0
missing: list[str] = []


def build_skill_sources() -> dict[str, Path]:
    sources: dict[str, Path] = {}
    for sk in DISCIPLINES.glob("*/skills/*"):
        if sk.is_dir() and sk.name != "references":
            sources[sk.name] = sk
    if BRAND_CREATIVE_SKILLS.is_dir():
        for sk in BRAND_CREATIVE_SKILLS.iterdir():
            if sk.is_dir() and sk.name not in {"references", "practice-setup"}:
                sources[sk.name] = sk
    if DELIVERY_PRACTICE_SKILLS.is_dir():
        for sk in DELIVERY_PRACTICE_SKILLS.iterdir():
            if sk.is_dir() and sk.name not in {"references", "practice-setup"}:
                sources[sk.name] = sk
    return sources


def sync_skill_bundle(dest: Path, src: Path) -> None:
    global synced
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(src, dest)
    synced += 1


def sync_discipline_refs(dest_skills_dir: Path, discipline: str) -> None:
    refs = DISCIPLINES / discipline / "skills" / "references"
    if not refs.is_dir():
        return
    dest = dest_skills_dir / "references"
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(refs, dest)


def sync_brand_conventions(dest_skills_dir: Path) -> None:
    if not BRAND_CONVENTIONS.is_file():
        return
    dest_dir = dest_skills_dir / "references"
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BRAND_CONVENTIONS, dest_dir / "brand-conventions.md")


def sync_delivery_conventions(dest_skills_dir: Path) -> None:
    if not DELIVERY_CONVENTIONS.is_file():
        return
    dest_dir = dest_skills_dir / "references"
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DELIVERY_CONVENTIONS, dest_dir / "delivery-conventions.md")


src_by_name = build_skill_sources()

for agent_dir in sorted(AGENTS.glob("*")):
    skills_dir = agent_dir / "skills"
    if not skills_dir.is_dir():
        continue

    skip = SKIP_AGENT_BUNDLES.get(agent_dir.name, set())
    disciplines_used: set[str] = set()
    uses_brand = False
    uses_delivery = False

    for bundled in sorted(skills_dir.iterdir()):
        if not bundled.is_dir() or bundled.name == "references":
            continue
        if bundled.name in skip:
            shutil.rmtree(bundled, ignore_errors=True)
            continue
        src = src_by_name.get(bundled.name)
        if not src:
            missing.append(str(bundled.relative_to(ROOT)))
            continue
        sync_skill_bundle(bundled, src)
        practice_root = src.parent.parent.name
        if practice_root == "brand-creative":
            uses_brand = True
        elif practice_root == "delivery-practice":
            uses_delivery = True
        else:
            disciplines_used.add(practice_root)

    for discipline in disciplines_used:
        sync_discipline_refs(skills_dir, discipline)

    if uses_brand:
        sync_brand_conventions(skills_dir)

    if uses_delivery:
        sync_delivery_conventions(skills_dir)

print(f"synced {synced} bundled skill dir(s)")
if missing:
    print("WARN: no skills source found for:", file=sys.stderr)
    for m in missing:
        print(f"  - {m}", file=sys.stderr)
    sys.exit(1)
