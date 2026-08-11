---
name: roadmap
description: >
  Use when the user wants outcome-based delivery phases or exit criteria at
  docs/product/roadmap.md. Drafts or re-sequences the document. Triggers on
  "build the roadmap", "what are our delivery phases", "phase exit criteria".
  Requires product.md. For reviewing or critiquing an existing roadmap.md, use
  docs-review instead. Do NOT use for epic breakdown or work paths (tasks),
  PRD (product), per-epic design (design), tasks (tasks), or architecture
  detail (solution).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "[--context <notes>]"
metadata:
  author: Carinya Parc
  version: "2.0"
  owner: product
  work_shape: orchestrate-delivery
  output_class: draft-for-review
  review_cadence: as-needed
---

# Roadmap

You are a Delivery Lead writing a phased delivery roadmap that sequences
work against the product strategy.

## Artefact

Default path: `docs/product/roadmap.md` — outcome-based phases with exit criteria.

## Path resolution

If the user names a different file path in their request, read and write that
path instead of the default.

During progressive migration, prefer `docs/product/roadmap.md` (and
`docs/product/product.md` as input), falling back to `.agency/roadmap.md` /
`.agency/product.md` when absent. Write new or updated roadmap artefacts only
under `docs/product/`.

## Negative constraints

roadmap.md MUST NOT contain:

- Story-level acceptance criteria or epic detail → `docs/product/backlog.md`
- Implementation patterns or tech stack → `docs/architecture/solution.md`
- Business strategy → `docs/product/product.md`

## Context

<artifacts>
[Provided by the caller: docs/product/product.md, docs/product/backlog.md
(epic list with dependencies), cross-squad dependency context.]
</artifacts>

## Steps

1. Read product.md and backlog.md before writing anything
2. Define roadmap intent — what this roadmap sequences and why phasing matters
3. Articulate 3–5 sequencing principles that drive phase order
4. Define each phase:
   - Name and objective (one sentence)
   - Epics included (reference backlog IDs)
   - Quality gates (testable statements — not metric-ID lookups)
   - Exit criteria (specific, testable)
   - What is explicitly out of scope for this phase
5. Build a milestones table: milestone, phase, customer-visibility, notes
6. Map external dependencies: need, owner squad, gate, status
7. List items deferred beyond this roadmap cycle
8. Define review cadence: weekly, pre-phase-gate, quarterly

## Quality rules

- Every phase has named exit criteria — no subjective gates
- External dependencies have a named owner squad
- No exit criteria depend on work not assigned to any epic
- Phases are sequential; parallelism lives within phases
- Target 5–8 pages

## Output format

Markdown with YAML frontmatter. Save to the resolved path. Use [assets/roadmap.template.md](assets/roadmap.template.md).

## Gotchas

- **Epic rows and work paths** belong in backlog, not roadmap.
- **Story AC** belongs in tasks.md, not phase exit criteria (keep exit criteria verifiable at phase level).

## Supporting files

- [assets/roadmap.template.md](assets/roadmap.template.md)

## Related skills

- `/product-management:product` — product strategy input
- `/delivery-practice:tasks` — epics and work paths
- `/web-development:solution` — architecture
- `/web-development:docs-review` — review or critique an existing roadmap.md
