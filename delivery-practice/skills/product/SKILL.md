---
name: product
description: >
  Use when the user wants a product strategy doc, PRD, pitch, vision, personas,
  or outcomes at .agency/product.md (write, review, refine). Do NOT use for
  phased delivery plan (roadmap), epics or backlog (backlog), architecture
  (solution), tasks or Gherkin (tasks), or implementation (implement).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: write|review|refine> [--stage pitch|product] [--context <notes>]"
---

# Product

## Conventions

Read [../../references/delivery-conventions.md](../../references/delivery-conventions.md)
when checking artefact boundaries.

## Artefact

Default path: `.agency/product.md` — strategy document (_why_, _who_, _what_).
Readable by a non-technical stakeholder without a glossary.

## Path resolution

If the user names a different file path in their request, read and write that
path instead of the default.

## Gotchas

- **No file paths, APIs, or schemas** — those belong in solution.md.
- **No epic tables** — roadmap and backlog own sequencing and epics.
- **Delete DRAFTING AIDE** block before saving.

## Stage (write mode)

| Stage | When | Format |
| ----- | ---- | ------ |
| `pitch` | Phase 0, pre-foundation | Shape Up, ≤2 pages |
| `product` | Phase 2+, post-walking-skeleton | Extended, ≤5 pages |

## Supporting files

- [assets/product.template.md](assets/product.template.md)
- [examples/product.md](examples/product.md)

## Related skills

- `roadmap`, `backlog`, `solution`

## Router

1. Mode: `write`, `review`, or `refine`.
2. Resolve target path (default or user override).
3. One prompt under [prompts/](prompts/).

**write** — `--stage pitch|product` (default: ask if unclear).
