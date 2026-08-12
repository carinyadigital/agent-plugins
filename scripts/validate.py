#!/usr/bin/env python3
"""
Structural validation for the Digital Agency plugin monorepo.

Thin orchestrator — runs plugin-domain then skill-domain validators.

  python3 scripts/validate_plugins.py   # marketplace, manifests, MCP
  python3 scripts/validate_skills.py    # frontmatter, agents, orphans, drift, evals

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
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_lib import Reporter, Validator  # noqa: E402, F401
from validate_plugins import PluginValidator  # noqa: E402
from validate_skills import SkillValidator  # noqa: E402


def print_usage() -> None:
    print(__doc__.strip())


def _run_plugin_checks(v: PluginValidator) -> None:
    checks = [
        ("marketplaceManifests", "Marketplace manifest validity", v.check_marketplace_manifests),
        ("marketplaceParity", "Claude ↔ Cursor marketplace parity", v.check_marketplace_parity),
        ("marketplacePluginSync", "Marketplace ↔ plugin.json sync", v.check_marketplace_plugin_sync),
        ("pluginManifests", "Per-plugin manifest completeness", v.check_plugin_manifests),
        ("mcpConnectors", "Practice plugin MCP definitions", v.check_mcp_connectors),
        ("jsonFiles", "Repository JSON sanity", v.check_json_files),
        ("hooksJson", "hooks/hooks.json validity", v.check_hooks_json),
        ("legacyArtefactPaths", "No obsolete .digital-agency/ or .agency/ path references", v.check_legacy_artefact_paths),
        ("crossPluginPaths", "No cache-unsafe sibling-plugin ../ references", v.check_cross_plugin_paths),
    ]
    for name, label, fn in checks:
        v.section(f"[{v.check_count + 1}] {label}")
        v.timed(name, label, fn)


def _run_skill_checks(v: SkillValidator) -> None:
    checks = [
        ("skillFrontmatter", "SKILL.md YAML frontmatter", v.check_skill_frontmatter),
        ("agentContracts", "Agent frontmatter contracts", v.check_agent_contracts),
        ("orphanSkills", "No orphan SKILL.md outside skills/", v.check_orphan_skills),
        ("markdownReferences", "Markdown cross-reference resolution", v.check_markdown_references),
        ("agentPrompts", "Agent canonical prompt files", v.check_agent_prompts),
        ("bundledSkillDrift", "Agent bundled skill drift", v.check_bundled_skill_drift),
        ("evalsSchema", "evals.json and trigger-queries.json schema", v.check_evals_schema),
    ]
    for name, label, fn in checks:
        v.section(f"[{v.check_count + 1}] {label}")
        v.timed(name, label, fn)


def main(argv: list[str] | None = None) -> int:
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
    args = parser.parse_args(argv)

    if args.help:
        print_usage()
        return 0

    if args.format == "json":
        combined = Reporter("json", args.strict, args.skip_drift)
        plugins = PluginValidator("_silent", args.strict, args.skip_drift)
        skills = SkillValidator("_silent", args.strict, args.skip_drift)
        _run_plugin_checks(plugins)
        _run_skill_checks(skills)
        combined.merge_from(plugins)
        combined.merge_from(skills)
        return combined.print_summary()

    print("Digital Agency — Structural Validation\n" + "=" * 40)
    plugins = PluginValidator("pretty", args.strict, args.skip_drift)
    plugin_rc = plugins.run_full()
    skills = SkillValidator("pretty", args.strict, args.skip_drift)
    skill_rc = skills.run()
    return 1 if plugin_rc or skill_rc else 0


if __name__ == "__main__":
    raise SystemExit(main())
