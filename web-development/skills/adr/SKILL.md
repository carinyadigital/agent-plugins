---
name: adr
description: >
  Use when the user wants ADR register planning, writing ADR-NNNN files, or ADR
  review under .agency/architecture/decisions/. Triggers on "do we need an ADR",
  "write ADR-0007", "record this decision", "what decisions need making",
  "harvest ADRs from this epic". Do NOT use for full architecture
  narrative (solution), epic design (design), or product strategy (product).
  Proposals stay in register.md only until accepted.
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: plan|write|review> [epic|target] [flags]"
metadata:
  author: Carinya Parc
  version: "1.0"
  owner: architecture
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

# ADR

## Paths

| Artefact | Default path |
| -------- | ------------ |
| Register | `.agency/architecture/decisions/register.md` |
| ADR document | `.agency/architecture/decisions/ADR-{NUMBER}-{short-title}.md` |

## Path resolution

If the user names a different directory or file path in their request, use it
for read/write instead of the defaults. Keep `ADR-####` numbering sequential
within the register the user targets.

## Supporting files

- [assets/register.template.md](assets/register.template.md)
- [assets/adr.template.md](assets/adr.template.md)

## Router

1. Mode: `plan`, `write`, or `review`.
2. Resolve paths (default or user override).
   **plan** takes an optional epic: `adr plan <epic>` harvests decisions already
   made in `.agency/work/{epic}/design.md` and triages them into the register.
   Without an epic it surveys product.md and solution.md for decisions still to
   be made.
3. [prompts/plan.prompt.md](prompts/plan.prompt.md) | [prompts/write.prompt.md](prompts/write.prompt.md) | [prompts/review.prompt.md](prompts/review.prompt.md).
