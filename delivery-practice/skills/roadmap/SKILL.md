---
name: roadmap
description: >
  Use when the user wants outcome-based delivery phases, exit criteria, or
  roadmap review at docs/product/roadmap.md. Requires product.md for write. Do
  NOT use for epic breakdown or work paths (backlog), PRD (product), per-epic
  design (design), tasks (tasks), or architecture detail (solution).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: write|review|refine> [--context <notes>]"
---

# Roadmap

## Conventions

Read [../../references/delivery-conventions.md](../../references/delivery-conventions.md)
when checking artefact boundaries.

## Artefact

Default path: `docs/product/roadmap.md` — outcome-based phases with exit criteria.

## Path resolution

If the user names a different file path in their request, read and write that
path instead of the default.

## Gotchas

- **Epic rows and work paths** belong in backlog, not roadmap.
- **Story AC** belongs in tasks.md, not phase exit criteria (keep exit criteria verifiable at phase level).

## Supporting files

- [assets/roadmap.template.md](assets/roadmap.template.md)

## Related skills

- `product`, `backlog`, `solution`

## Router

1. Mode: `write`, `review`, or `refine`.
2. Resolve target path (default or user override).
3. One prompt under [prompts/](prompts/).
