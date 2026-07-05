---
name: design
description: >
  Use when the user wants epic-level technical design at docs/work/{epic}/design.md,
  walking-skeleton or TDD design, or design review before tasks. Pass epic slug or
  ID (CHK01). Cite solution.md — do not re-narrate architecture. Do NOT use for
  product backlog or epics (backlog), task Gherkin (tasks), system-wide
  architecture (solution), ADR write (adr), code implementation (implement), or
  doc-only sprint-end pass (docs refine).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: write|review> <epic> [--mode walking-skeleton|tdd] [--context <notes>]"
metadata:
  version: "0.1.0"
  owner: web-development
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Design

## Conventions

Read [../../references/web-development-conventions.md](../../references/web-development-conventions.md)
when resolving `{epic}` or checking artefact boundaries.

## Artefact

`docs/work/{epic}/design.md` — implementation specification for one epic (walking-skeleton or TDD).

## Path resolution

Default: `docs/work/{epic}/design.md`. User-named paths under `docs/work/` override.

## Gotchas

- **Do not copy solution.md** — cite `solution.md §{N.M}` instead.
- **Task Gherkin** belongs in `tasks.md`, not design (gates/slice scope only).
- **`walking-skeleton`** is 2–4 pages; **`tdd`** is 5–10 — do not mix section sets.
- **§4 Out of scope** must list what this epic explicitly did not ship.

## Supporting files

- [assets/design.template.md](assets/design.template.md)
- [examples/checkout-foundation.md](examples/checkout-foundation.md)

## Router

1. Mode: `write` or `review`.
2. Resolve `{epic}`.
3. [prompts/write.prompt.md](prompts/write.prompt.md) | [prompts/review.prompt.md](prompts/review.prompt.md).

**write** — `--mode walking-skeleton|tdd`.
