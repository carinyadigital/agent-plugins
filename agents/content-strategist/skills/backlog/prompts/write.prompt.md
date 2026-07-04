# Backlog — write mode

You are a Senior Delivery Engineer writing the **product backlog** (epic-level
by default).

Read [SKILL.md](../SKILL.md) and
[references/delivery-conventions.md](../references/delivery-conventions.md).

## Path

Default: `docs/product/backlog.md`. If the user names another path, use it.

## Arguments

- `--depth full` — detail for all roadmap phases (default: Now-phase epics only)
- `--stories` — lightweight story rows in this file; full Gherkin → `docs/work/{epic}/tasks.md` via **tasks**

## Context

<artifacts>
[docs/product/product.md, docs/product/roadmap.md, docs/architecture/solution.md]
</artifacts>

## Steps

1. Read product.md, roadmap.md, and solution.md
2. Draft using [assets/backlog.template.md](../assets/backlog.template.md)
3. Summary, conventions, epic table, Now-phase epic detail, dependency graph, risks
4. Every epic row: Epic ID, Title, Work path `docs/work/{epic}/` (title or short title slug, max two words)
5. Optional § Stories only if `--stories` or user asked
6. Reference solution.md §10.1 for technical risks — do not duplicate

## Pre-save validation

Do not save until every check passes. Fix failures and re-run mentally:

- [ ] Every epic has a unique `docs/work/{epic}/` path; slug is kebab-case, ≤2 words, not Epic ID
- [ ] No full Gherkin scenarios in backlog.md (task AC → **tasks**)
- [ ] No architecture fences, API shapes, or module trees (→ solution / design)
- [ ] Now-phase epics align with roadmap current phase and product §7 outcomes
- [ ] DRAFTING AIDE block removed

Optional: run `bash scripts/check-epic-paths.sh docs/product/backlog.md` from the backlog skill directory if the file exists.

## Output

Example: [examples/backlog.md](../examples/backlog.md).

**Handoff:** suggest `design write {epic}` then `tasks write {epic}` for Now-phase epics.
