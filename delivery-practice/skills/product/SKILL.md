---
name: product
description: >
  Use when the user wants a product strategy doc, PRD, pitch, vision, personas,
  or outcomes at .agency/product.md. Two modes: write (draft or re-author)
  and review (critique, update for currency, amend in place). Triggers on
  "write the PRD", "draft a product pitch", "who are our personas", "review the
  product strategy", "is this strategy still current". Do NOT use for
  phased delivery plan (roadmap), epics or backlog (tasks), architecture
  (solution), tasks or Gherkin (tasks), or implementation (implement).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: write|review> [--stage pitch|product] [--context <notes>]"
metadata:
  author: Carinya Parc
  version: "1.0"
  owner: product
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

# Product

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

- `roadmap`, `tasks`, `solution`

## Router

1. Mode: `write` or `review`.
2. Resolve target path (default or user override).
3. One prompt under [prompts/](prompts/).

**write** — `--stage pitch|product` (default: ask if unclear).
