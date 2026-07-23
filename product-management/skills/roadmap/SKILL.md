---
name: roadmap
description: >
  Use when the user wants outcome-based delivery phases, exit criteria, or
  roadmap review at .agency/roadmap.md. Two modes: write (draft or
  re-sequence) and review (judge credibility, record delivery evidence, amend in
  place). Triggers on "build the roadmap", "what are our delivery phases",
  "phase exit criteria", "is this roadmap credible", "did we hit the phase
  gate". Requires product.md for write. Do
  NOT use for epic breakdown or work paths (tasks), PRD (product), per-epic
  design (design), tasks (tasks), or architecture detail (solution).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: write|review> [--context <notes>]"
metadata:
  author: Carinya Parc
  version: "1.0"
  owner: product
  work_shape: orchestrate-delivery
  output_class: draft-for-review
  review_cadence: as-needed
---

# Roadmap

## Artefact

Default path: `.agency/roadmap.md` — outcome-based phases with exit criteria.

## Path resolution

If the user names a different file path in their request, read and write that
path instead of the default.

## Gotchas

- **Epic rows and work paths** belong in backlog, not roadmap.
- **Story AC** belongs in tasks.md, not phase exit criteria (keep exit criteria verifiable at phase level).

## Supporting files

- [assets/roadmap.template.md](assets/roadmap.template.md)

## Related skills

- `product`, `tasks`, `solution`

## Router

1. Mode: `write` or `review`.
2. Resolve target path (default or user override).
3. One prompt under [prompts/](prompts/).
