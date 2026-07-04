---
name: backlog
description: >
  Use when the user wants to write, review, or refine the product backlog,
  decompose delivery into epics, set Now-phase scope, or manage epic rows (e.g.
  CHK01). Default artefact docs/product/backlog.md. Do NOT use for business
  strategy or PRD (product), phase exit criteria (roadmap), Gherkin tasks
  (tasks), epic design.md (design), architecture (solution), sprint retro
  (sprint), or pre-sprint doc alignment (docs). Task breakdown per epic lives at
  docs/work/{epic}/ via tasks.
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: write|review|refine> [--depth full] [--stories] [--context <notes>]"
---

# Backlog

## Conventions

Read [../references/delivery-conventions.md](../references/delivery-conventions.md) when
setting work paths, resolving epic IDs, or checking artefact boundaries.

## Artefact

Default path: `docs/product/backlog.md` — product-level backlog (epics by default).

## Path resolution

If the user names a different file path in their request, read and write that
path instead of the default.

## Default shape

- **Epic-level (default):** epic breakdown table, Now-phase epic detail, dependency
  graph, delivery risks. Later phases are placeholders unless `--depth full`.
- **With stories:** when the user requests `--stories`, a small product, or
  explicitly asks — lightweight story rows only; full Gherkin → `docs/work/{epic}/tasks.md`
  via **tasks**.

## Gotchas

- **Work path slug** comes from title or short title (max two words), not Epic ID.
- **Full Gherkin** belongs in `docs/work/{epic}/tasks.md`, not in the product backlog.
- **`--stories`** adds high-level rows only; do not paste task-level AC here.
- **Architecture and APIs** stay in `solution.md`; epic detail stays in `design.md`.

## Supporting files

- [assets/backlog.template.md](assets/backlog.template.md)
- [examples/backlog.md](examples/backlog.md)
- [scripts/check-epic-paths.sh](scripts/check-epic-paths.sh) — optional slug check

## Related skills

- `product`, `roadmap`, `solution`, `tasks`, `design`, `sprint`

## Router

1. Mode: `write`, `review`, or `refine`.
2. Resolve path (default `docs/product/backlog.md`).
3. One prompt under [prompts/](prompts/).

**write** — `--depth full` for all phases; `--stories` for story-level rows in the product backlog.
