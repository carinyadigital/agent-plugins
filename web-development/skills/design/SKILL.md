---
name: design
description: >
  Use when the user wants epic-level technical design at .agency/work/{epic}/design.md,
  walking-skeleton or TDD design, or design review before tasks. Pass epic slug or
  ID (CHK01). Cite solution.md — do not re-narrate architecture. Triggers on
  "design CHK01", "write the epic design", "how should we build this epic",
  "review the design before tasks". Do NOT use for
  epics or stories (tasks), task Gherkin (tasks), system-wide
  architecture (solution), ADR write (adr), code implementation (implement), or
  reviewing a set of documents for quality and consistency (docs-review).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: write|review> <epic> [--mode walking-skeleton|tdd] [--context <notes>]"
metadata:
  author: Carinya Parc
  version: "1.0"
  owner: architecture
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

# Design

## Conventions

Read [delivery-conventions.md](../tasks/references/delivery-conventions.md)
when resolving `{epic}` or checking artefact boundaries.

## Artefact

`.agency/work/{epic}/design.md` — implementation specification for one epic (walking-skeleton or TDD).

## Path resolution

Default: `.agency/work/{epic}/design.md`. User-named paths under `.agency/work/` override.

## Gotchas

- **Do not copy solution.md** — cite `solution.md §{N.M}` instead.
- **Task Gherkin** belongs in `tasks.md`, not design (gates/slice scope only).
- **`walking-skeleton`** is 2–4 pages; **`tdd`** is 5–10 — do not mix section sets.
- **§4 Out of scope** must list what this epic explicitly did not ship.

## ADR candidates

Decisions recorded in `design.md` do not reach the architecture register on
their own. After the epic ships, run `adr plan <epic>` to harvest them — it
triages each candidate into promote, inline, or defer, and hands the promoted
ones to **adr write**.

## Supporting files

- [assets/design.template.md](assets/design.template.md)
- [examples/checkout-foundation.md](examples/checkout-foundation.md)

## Router

1. Mode: `write` or `review`.
2. Resolve `{epic}`.
3. [prompts/write.prompt.md](prompts/write.prompt.md) | [prompts/review.prompt.md](prompts/review.prompt.md).

**write** — `--mode walking-skeleton|tdd`.
