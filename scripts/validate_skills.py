#!/usr/bin/env python3
"""
Skill- and agent-domain structural validation for the Digital Agency monorepo.

Checks SKILL.md frontmatter (YAML + name/description budgets), every
**/agents/*.md contract, orphan SKILL.md files, markdown cross-refs,
bundled-skill drift, and evals schema.

Usage: python3 scripts/validate_skills.py [options]
  --format pretty|json   Output format (default: pretty)
  --strict               Treat agency-framework frontmatter gaps as errors
  --skip-drift           Skip bundled skill drift detection
  --help                 Print usage and exit

Exits 0 on success, non-zero on failure.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_lib import (  # noqa: E402
    AGENCY_HEADINGS,
    AGENCY_METADATA_FIELDS,
    MODEL_TIERS,
    ORPHAN_SKILL_EXCLUDES,
    OUTPUT_CLASSES,
    PRACTICE_PLUGIN_DIRS,
    SKIP_AGENT_BUNDLES,
    SKIP_DRIFT_NAMES,
    SKILL_DESC_MAX,
    SKILL_NAME_MAX,
    SKILL_NAME_RE,
    WORK_SHAPES,
    Reporter,
    _HEADING_RE,
    _MD_LINK_RE,
    agent_paths,
    collect_tree_files,
    file_digest,
    has_bare_bash,
    normalize_tools,
    parse_frontmatter,
    plugin_dirs,
    resolve_markdown_target,
    skill_sources,
    source_skill_paths,
)

ROOT = Path(__file__).resolve().parents[1]


class SkillValidator(Reporter):
    def check_skill_frontmatter(self) -> None:
        for skill_path in source_skill_paths():
            rel = self.rel(skill_path)
            skill_name = skill_path.parent.name
            try:
                text = skill_path.read_text(encoding="utf-8")
            except OSError as exc:
                self.fail(
                    "SKILL_UNREADABLE",
                    f"{rel}: cannot read file: {exc}",
                    file=rel,
                )
                continue

            frontmatter, body, parse_errs = parse_frontmatter(text)
            for msg in parse_errs:
                severity = self.fail if self.strict else self.warn
                severity("FM_PARSE", f"{rel}: {msg}", file=rel)

            if frontmatter is None:
                continue

            name = frontmatter.get("name")
            if not name:
                self.fail("FM_NO_NAME", f"{rel} missing frontmatter name", file=rel)
            elif name != skill_name:
                self.fail(
                    "FM_NAME_MISMATCH",
                    f"{rel} frontmatter name {name!r} != directory {skill_name!r}",
                    file=rel,
                )
            else:
                if not isinstance(name, str) or not SKILL_NAME_RE.match(name):
                    self.fail(
                        "FM_NAME_INVALID",
                        f"{rel} name {name!r} must be lowercase alphanumeric "
                        f"with single hyphens (max {SKILL_NAME_MAX})",
                        file=rel,
                    )
                elif len(name) > SKILL_NAME_MAX:
                    self.fail(
                        "FM_NAME_TOO_LONG",
                        f"{rel} name is {len(name)} chars (max {SKILL_NAME_MAX})",
                        file=rel,
                    )
                else:
                    self.pass_(f'{rel} name matches directory "{skill_name}"')

            description = frontmatter.get("description")
            if not description:
                self.fail(
                    "FM_NO_DESC", f"{rel} missing frontmatter description", file=rel
                )
            elif not isinstance(description, str):
                self.fail(
                    "FM_DESC_INVALID",
                    f"{rel} description must be a string",
                    file=rel,
                )
            elif len(description) > SKILL_DESC_MAX:
                self.fail(
                    "FM_DESC_TOO_LONG",
                    f"{rel} description is {len(description)} chars "
                    f"(max {SKILL_DESC_MAX})",
                    file=rel,
                )
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
                        hint="See skill-authoring/references/"
                        "agency-skill-design-framework.md §11",
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

    def check_agent_contracts(self) -> None:
        """Validate every **/agents/*.md under practice plugins."""
        paths = agent_paths()
        if not paths:
            self.warn("AGENT_NONE", "No agent markdown files found under practice plugins")
            return

        for agent_path in paths:
            rel = self.rel(agent_path)
            try:
                text = agent_path.read_text(encoding="utf-8")
            except OSError as exc:
                self.fail(
                    "AGENT_UNREADABLE",
                    f"{rel}: cannot read file: {exc}",
                    file=rel,
                )
                continue

            frontmatter, _, parse_errs = parse_frontmatter(text)
            for msg in parse_errs:
                self.fail("AGENT_FM_PARSE", f"{rel}: {msg}", file=rel)
            if frontmatter is None:
                continue

            name = frontmatter.get("name")
            expected = agent_path.stem
            if not name:
                self.fail("AGENT_NO_NAME", f"{rel} missing frontmatter name", file=rel)
            elif name != expected:
                self.fail(
                    "AGENT_NAME_MISMATCH",
                    f"{rel} frontmatter name {name!r} != file stem {expected!r}",
                    file=rel,
                )

            model = frontmatter.get("model")
            if model != "inherit":
                self.fail(
                    "AGENT_MODEL",
                    f"{rel} model must be 'inherit' (got {model!r})",
                    file=rel,
                    hint="Use model: inherit; set metadata.model_tier for cost tier",
                )

            tools_raw = frontmatter.get("tools")
            if tools_raw is None:
                self.fail(
                    "AGENT_NO_TOOLS",
                    f"{rel} missing tools frontmatter",
                    file=rel,
                )
                tools: list[str] = []
            else:
                tools = normalize_tools(tools_raw)
                if not tools:
                    self.fail(
                        "AGENT_NO_TOOLS",
                        f"{rel} tools list is empty",
                        file=rel,
                    )
                elif has_bare_bash(tools):
                    self.fail(
                        "AGENT_BARE_BASH",
                        f"{rel} tools include unscoped Bash — constrain with "
                        f"Bash(command:*) forms",
                        file=rel,
                    )

            metadata = frontmatter.get("metadata")
            metadata_dict = metadata if isinstance(metadata, dict) else {}
            if not isinstance(metadata, dict):
                self.fail(
                    "AGENT_NO_METADATA",
                    f"{rel} missing metadata mapping",
                    file=rel,
                )

            tier = metadata_dict.get("model_tier")
            if tier not in MODEL_TIERS:
                self.fail(
                    "AGENT_MODEL_TIER",
                    f"{rel} metadata.model_tier must be one of "
                    f"{sorted(MODEL_TIERS)} (got {tier!r})",
                    file=rel,
                )

            budget = metadata_dict.get("budget")
            if not isinstance(budget, int) or isinstance(budget, bool) or budget < 1:
                self.fail(
                    "AGENT_BUDGET",
                    f"{rel} metadata.budget must be a positive integer "
                    f"(got {budget!r})",
                    file=rel,
                    hint="Declare a numeric reading/turn budget in metadata.budget",
                )
            else:
                self.pass_(f"{rel} agent contract OK")

    def check_orphan_skills(self) -> None:
        """Fail on SKILL.md outside skills/<name>/ (excl. template/)."""
        orphans: list[str] = []
        for skill_path in sorted(ROOT.rglob("SKILL.md")):
            if ".git" in skill_path.parts or "node_modules" in skill_path.parts:
                continue
            rel = self.rel(skill_path)
            parts = skill_path.relative_to(ROOT).parts

            excluded = any(
                rel == f"{exclude}/SKILL.md" or rel.startswith(exclude + "/")
                for exclude in ORPHAN_SKILL_EXCLUDES
            )
            if excluded:
                continue

            # Valid layout: .../skills/<name>/SKILL.md
            in_skills_tree = (
                len(parts) >= 3
                and parts[-3] == "skills"
                and parts[-1] == "SKILL.md"
            )
            if not in_skills_tree:
                orphans.append(rel)

        if orphans:
            for rel in orphans[:20]:
                self.fail(
                    "SKILL_ORPHAN",
                    f"Orphan SKILL.md outside skills/<name>/: {rel}",
                    file=rel,
                    hint="Move under a practice plugin skills/ directory "
                    "(template/ excluded)",
                )
            if len(orphans) > 20:
                self.fail(
                    "SKILL_ORPHAN",
                    f"... and {len(orphans) - 20} more orphan SKILL.md file(s)",
                )
        else:
            self.pass_("No orphan SKILL.md files outside skills/ trees")

    def check_markdown_references(self) -> None:
        checked_files: list[Path] = []
        for base_name in ("skills", *PRACTICE_PLUGIN_DIRS):
            base = ROOT / base_name
            if not base.is_dir():
                continue
            if base_name == "skills":
                checked_files.extend(sorted(base.glob("*/skills/*/*.md")))
            else:
                checked_files.extend(sorted(base.glob("skills/*/*.md")))
                checked_files.extend(sorted(base.glob("agents/*.md")))
                checked_files.extend(sorted(base.glob("skills/*/agents/*.md")))

        agents_root = ROOT / "agents"
        if agents_root.is_dir():
            checked_files.extend(sorted(agents_root.glob("*/*/*.md")))

        broken = 0
        for md_path in sorted(set(checked_files)):
            rel = self.rel(md_path)
            try:
                content = md_path.read_text(encoding="utf-8")
            except OSError:
                continue

            for match in _MD_LINK_RE.finditer(content):
                target = match.group(1)
                resolved = resolve_markdown_target(md_path.parent, target)
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
            self.pass_(
                f"All markdown links resolve in {len(checked_files)} checked file(s)"
            )

    def check_agent_prompts(self) -> None:
        agents_root = ROOT / "agents"
        if not agents_root.is_dir():
            self.pass_("No top-level agents/ directory (personas live in practice plugins)")
            return
        for agent_dir in sorted(agents_root.glob("*")):
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

    def check_bundled_skill_drift(self) -> None:
        if self.skip_drift:
            self.pass_("Bundled skill drift check skipped via --skip-drift")
            return

        sources = skill_sources()
        drift_count = 0
        agent_local = 0
        agents_root = ROOT / "agents"
        if not agents_root.is_dir():
            self.pass_("No top-level agents/ bundles to drift-check")
            return

        for agent_dir in sorted(agents_root.glob("*")):
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
                        f"{rel_bundle} must not bundle {bundled_dir.name!r} — "
                        f"MECE owned by brand-creative only",
                        file=rel_bundle,
                        hint="Remove the bundled copy; frontend-engineer reads "
                        "brand-guide.md from the resolved path",
                    )
                    drift_count += 1
                    continue

                source_dir = sources.get(bundled_dir.name)
                if source_dir is None:
                    agent_local += 1
                    self.pass_(f"{rel_bundle} is agent-local (no skills/ source)")
                    continue

                drift_count += self._compare_bundled_tree(
                    rel_bundle, bundled_dir, source_dir
                )

        self.pass_("Practice plugins own skills outright (no discipline vendoring drift check)")

        if drift_count == 0:
            self.pass_(
                f"No bundled skill drift detected ({agent_local} agent-local skill dir(s) skipped)"
            )

    def _compare_bundled_tree(
        self, rel_bundle: str, bundled_dir: Path, source_dir: Path
    ) -> int:
        drift_count = 0
        bundled_files = collect_tree_files(bundled_dir)
        source_files = collect_tree_files(source_dir)

        bundle_rel_paths = set(bundled_files)
        source_rel_paths = set(source_files)
        missing_in_bundle = source_rel_paths - bundle_rel_paths
        extra_in_bundle = bundle_rel_paths - source_rel_paths

        for rel_path in sorted(missing_in_bundle | extra_in_bundle):
            drift_count += 1
            self.drifted_bundles.append(rel_bundle)
            self.fail(
                "SKILL_DRIFT",
                f"{rel_bundle} drift: file {rel_path!r} differs from "
                f"{self.rel(source_dir)}",
                file=rel_bundle,
                hint="Edit the canonical skill under the owning practice plugin, "
                "not a bundled copy",
            )

        for rel_path in sorted(bundle_rel_paths & source_rel_paths):
            if file_digest(bundled_files[rel_path]) != file_digest(
                source_files[rel_path]
            ):
                drift_count += 1
                self.drifted_bundles.append(rel_bundle)
                self.fail(
                    "SKILL_DRIFT",
                    f"{rel_bundle} drift: {rel_path} content differs from source",
                    file=rel_bundle,
                    hint="Edit the canonical skill under the owning practice "
                    "plugin, not a bundled copy",
                )
        return drift_count

    def check_evals_schema(self) -> None:
        eval_dirs: list[Path] = []
        for plugin_dir in plugin_dirs():
            eval_dirs.extend(sorted(plugin_dir.glob("skills/*/evals")))
        if not eval_dirs:
            self.warn(
                "EVALS_NONE", "No evals/ directories found under practice plugins"
            )
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
                        for field_name in (
                            "id",
                            "prompt",
                            "expected_output",
                            "assertions",
                        ):
                            if field_name not in case:
                                self.fail(
                                    "EVALS_CASE_FIELD",
                                    f"{self.rel(evals_path)} eval #{index} missing "
                                    f"{field_name!r}",
                                    file=self.rel(evals_path),
                                )
                        assertions = case.get("assertions")
                        if assertions is not None and (
                            not isinstance(assertions, list) or not assertions
                        ):
                            self.fail(
                                "EVALS_ASSERTIONS",
                                f"{self.rel(evals_path)} eval #{index} assertions "
                                f"must be a non-empty array",
                                file=self.rel(evals_path),
                            )
                    self.pass_(
                        f"{self.rel(evals_path)} schema OK ({len(cases)} eval(s))"
                    )

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
                                f"{self.rel(triggers_path)} entry #{index} is not "
                                f"an object",
                                file=self.rel(triggers_path),
                            )
                            continue
                        if "query" not in entry or "should_trigger" not in entry:
                            self.fail(
                                "TRIGGERS_ENTRY_FIELD",
                                f"{self.rel(triggers_path)} entry #{index} missing "
                                f"query or should_trigger",
                                file=self.rel(triggers_path),
                            )
                    self.pass_(
                        f"{self.rel(triggers_path)} schema OK "
                        f"({len(triggers)} trigger(s))"
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

    def run(self) -> int:
        if self.fmt == "pretty":
            print("Digital Agency — Skill Validation\n" + "=" * 40)

        checks: list[tuple[str, str, Callable[[], None]]] = [
            ("skillFrontmatter", "SKILL.md YAML frontmatter", self.check_skill_frontmatter),
            ("agentContracts", "Agent frontmatter contracts", self.check_agent_contracts),
            ("orphanSkills", "No orphan SKILL.md outside skills/", self.check_orphan_skills),
            ("markdownReferences", "Markdown cross-reference resolution", self.check_markdown_references),
            ("agentPrompts", "Agent canonical prompt files", self.check_agent_prompts),
            ("bundledSkillDrift", "Agent bundled skill drift", self.check_bundled_skill_drift),
            ("evalsSchema", "evals.json and trigger-queries.json schema", self.check_evals_schema),
        ]
        for name, label, fn in checks:
            self.section(f"[{self.check_count + 1}] {label}")
            self.timed(name, label, fn)

        return self.print_summary(title="summary")


def print_usage() -> None:
    print(__doc__.strip())


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

    validator = SkillValidator(args.format, args.strict, args.skip_drift)
    return validator.run()


if __name__ == "__main__":
    raise SystemExit(main())
