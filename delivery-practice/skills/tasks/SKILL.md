---
name: tasks
description: >
  Use when the user wants to break an epic into tasks.md, write Gherkin acceptance
  criteria, refine sprint-ready tasks, or review task breakdown for an epic
  (checkout-foundation, CHK01, etc.). Default docs/work/{epic}/tasks.md. Do NOT use for
  epic list or work paths (backlog), product backlog stories only (backlog),
  design.md (design), code implementation (implement), PR code review
  (code-review), or epic completion sign-off (validate). EARS with --ears.
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: write|review|refine> <epic> [--ears] [--context <notes>]"
---

# Tasks

## Conventions

Read [../../references/delivery-conventions.md](../../references/delivery-conventions.md)
when resolving `{epic}` or checking where content belongs.

## Artefact

Default path: `docs/work/{epic}/tasks.md` — tasks for one epic with Gherkin acceptance
criteria by default.

## Path resolution

If the user names a different file path, use that instead of the default under
`docs/work/{epic}/`.

## Inputs

- **Preferred:** `docs/work/{epic}/design.md` and the epic row in `docs/product/backlog.md`
- **Alternative:** a spec the user provides
- **Context:** `docs/architecture/solution.md`

## Canonical task schema

Each task: Status, Priority, Estimate, Epic, Labels, Depends on, Deliverable,
Design (section link), **Acceptance (Gherkin)**.

**Required:** ≥1 Gherkin scenario per task; observable `Then` clauses.

**Optional EARS:** with `--ears` or when rules warrant it (see write prompt).

## Gotchas

- **`CHK01` is not `{epic}`** — resolve slug from backlog (e.g. `checkout-foundation`).
- **Do not add epics** here — new epics go in `docs/product/backlog.md`.
- **Design narrative** stays in `design.md`; tasks link to design sections only.
- **Gherkin `Then`** must be observable (no "should work correctly").

## Supporting files

- [assets/tasks.template.md](assets/tasks.template.md)
- [examples/checkout-foundation.md](examples/checkout-foundation.md)

## Related skills

- `backlog`, `design`, `implement`, `solution`, `sprint`

## Router

1. Mode: `write`, `review`, or `refine`.
2. Resolve `{epic}` and `docs/work/{epic}/tasks.md`.
3. One prompt under [prompts/](prompts/).

**write** — `--ears` for EARS on every task.
