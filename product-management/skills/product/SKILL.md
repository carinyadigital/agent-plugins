---
name: product
description: >
  Use when the user wants a product strategy doc, PRD, pitch, vision,
  personas, or outcomes at docs/product/product.md. Drafts or re-authors the
  document. Triggers on "write the PRD", "draft a product pitch", "who are
  our personas". Re-authoring is also how an existing product.md gets
  critiqued or revised — docs-review checks writing quality and cross-document
  consistency, not strategic soundness. Do NOT use for phased delivery plan (roadmap), epics
  or backlog (tasks), architecture (solution), tasks or Gherkin (tasks), or
  implementation (implement).
license: Apache-2.0
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "[--stage pitch|product] [--context <notes>]"
metadata:
  author: Carinya Parc
  version: "1.1"
  owner: product
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

# Product

You are a Product Manager writing a product document that defines the
_why_, _who_, and _what_ of the product.

## Artefact

Default path: `docs/product/product.md` — strategy document (_why_, _who_, _what_).
Readable by a non-technical stakeholder without a glossary.

## Path resolution

If the user names a different file path in their request, read and write that
path instead of the default.

## Arguments

`--stage pitch|product` (default: ask if unclear).

## Context

<artifacts>
[Pitch: problem statement, appetite, known constraints.
Product stage: existing pitch product.md, user research, stakeholder map.]
</artifacts>

## Steps (pitch stage)

1. Read all provided context
2. §1 Problem — evidence-based bullets
3. §2 Appetite — investment and phasing
4. §3 Sketch — end-to-end outcome in plain language
5. §4 Rabbit holes — deliberate exclusions
6. §5 No-gos — out-of-scope with reasons
7. Delete the `DRAFTING AIDE` comment block before saving

## Steps (product stage)

1. Read context and existing pitch product.md if present
2. Carry forward §1–§5, updated if needed
3. §6 Target users
4. §7 Outcome metrics — reference `ARCHITECTURE.md` §1 for thresholds; do not restate numbers
5. §8 Product principles — commercial only
6. §9 Stakeholders and RACI
7. §10 Dependencies and sequencing
8. Delete the `DRAFTING AIDE` comment block before saving

## Quality rules

- Readable without a glossary; pitch ≤2 pages, product stage ≤5 pages
- §7 no raw numeric thresholds; §8 not technical
- Derive from context — do not invent requirements
- **No file paths, APIs, or schemas** — those belong in `ARCHITECTURE.md`
- **No epic tables** — roadmap and backlog own sequencing and epics

## Output

Markdown with YAML frontmatter. Use [assets/product.template.md](assets/product.template.md).

## Supporting files

- [assets/product.template.md](assets/product.template.md)
- [examples/product.md](examples/product.md)

## Related skills

- `/product-management:roadmap` — sequencing and phases
- `/product-management:tasks` — epics and backlog decomposition
- `/architecture:solution` — architecture (companion; if not installed: `/plugin install architecture@carinya-plugins`)
- `/engineering:docs-review` — writing quality / cross-doc consistency (not strategic soundness)
