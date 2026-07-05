#!/usr/bin/env python3
"""
Re-sync bundled skills from the skills source tree.

Agent plugins under agents/<slug>/skills/<name>/ and practice plugins under
<practice>/skills/<name>/ are vendored copies of skills/<discipline>/skills/<name>/.
The skills/ tree is the source of truth; run this after editing a skill there to
propagate the change into every agent and practice plugin that bundles it.

Usage: python3 scripts/sync-agent-skills.py
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
PRACTICES = ROOT / "skills"

# Root-level practice plugins → skills/<discipline>/ source
PRACTICE_PLUGINS: dict[str, str] = {
    "brand-creative": "brand",
}

# index every skill name -> source dir in practices (skip shared refs)
src_by_name: dict[str, Path] = {}
for sk in PRACTICES.glob("*/skills/*"):
    if sk.is_dir() and sk.name != "references":
        src_by_name[sk.name] = sk

synced = 0
missing: list[str] = []


def sync_skill_bundle(dest: Path, src: Path) -> None:
    global synced
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(src, dest)
    synced += 1


def sync_discipline_refs(dest_skills_dir: Path, discipline: str) -> None:
    refs = PRACTICES / discipline / "skills" / "references"
    if not refs.is_dir():
        return
    dest = dest_skills_dir / "references"
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(refs, dest)


for agent_dir in sorted(AGENTS.glob("*")):
    skills_dir = agent_dir / "skills"
    if not skills_dir.is_dir():
        continue

    disciplines_used: set[str] = set()
    for bundled in sorted(skills_dir.iterdir()):
        if not bundled.is_dir() or bundled.name == "references":
            continue
        src = src_by_name.get(bundled.name)
        if not src:
            missing.append(str(bundled.relative_to(ROOT)))
            continue
        sync_skill_bundle(bundled, src)
        disciplines_used.add(src.parent.parent.name)

    for discipline in disciplines_used:
        sync_discipline_refs(skills_dir, discipline)

for practice_name, discipline in sorted(PRACTICE_PLUGINS.items()):
    practice_dir = ROOT / practice_name
    dest_skills = practice_dir / "skills"
    if not dest_skills.is_dir():
        missing.append(f"{practice_name}/skills/ (missing practice plugin dir)")
        continue

    src_skills_root = PRACTICES / discipline / "skills"
    for src in sorted(src_skills_root.iterdir()):
        if not src.is_dir() or src.name == "references":
            continue
        dest = dest_skills / src.name
        sync_skill_bundle(dest, src)

    sync_discipline_refs(dest_skills, discipline)

    refs = src_skills_root / "references"
    plugin_refs = practice_dir / "references"
    if refs.is_dir():
        plugin_refs.mkdir(parents=True, exist_ok=True)
        for ref_file in sorted(refs.iterdir()):
            if ref_file.is_file():
                shutil.copy2(ref_file, plugin_refs / ref_file.name)

print(f"synced {synced} bundled skill dir(s) from skills/")
if missing:
    print("WARN: no skills source found for:", file=sys.stderr)
    for m in missing:
        print(f"  - {m}", file=sys.stderr)
    sys.exit(1)
