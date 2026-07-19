# Design — write mode

You are a Software Architect writing epic-level `design.md` for
`.agency/work/{epic}/`. Resolve `{epic}` from the argument or `.agency/backlog.md`.

Read [SKILL.md](../SKILL.md) and
[delivery-conventions.md](../../tasks/references/delivery-conventions.md).

Parent solution: `.agency/architecture/solution.md` — cite sections; do not re-narrate.

## Mode (`--mode`)

- `walking-skeleton` — Phase 0, 2–4 pages
- `tdd` — Sprint 2+, 5–10 pages

## Negative constraints

Do NOT put in design.md:

- Architecture-wide patterns already in solution.md — cite `solution.md §{N.M}`
- Business strategy → `.agency/product.md`
- Phase sequencing → `.agency/roadmap.md`
- Task-level Gherkin → `.agency/work/{epic}/tasks.md` via **tasks**

Delete the `DRAFTING AIDE` block before saving.

## Context

[Epic row in backlog.md, solution.md, existing design.md if updating, codebase]

## Steps (walking-skeleton)

1. Read solution.md and epic in backlog.md
2. Draft §1–§6 per template
3. §4 must list what this epic did **not** ship

## Steps (TDD)

1. Read all context
2. Draft §1–§12 per template

## Pre-save validation

- [ ] Path is `.agency/work/{epic}/design.md` with correct slug (≤2 words, not Epic ID)
- [ ] Solution cited by section; no duplicated architecture narrative
- [ ] No Gherkin task scenarios (gates/slice only)
- [ ] Mode-appropriate sections only (walking-skeleton vs tdd)
- [ ] DRAFTING AIDE removed

## Output

Save to `.agency/work/{epic}/design.md`. Use [assets/design.template.md](../assets/design.template.md).

**Handoff:** suggest `tasks {epic}`.
