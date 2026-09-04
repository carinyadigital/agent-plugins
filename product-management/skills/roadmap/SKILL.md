---
name: roadmap
description: >
  Use when the user wants outcome-based delivery phases or exit criteria at
  docs/product/roadmap.md. Drafts or re-sequences the document. Triggers on
  "build the roadmap", "what are our delivery phases", "phase exit criteria".
  Requires product.md; reads solution.md when present. Does not require
  backlog.md — hierarchy is Product → Solution → Roadmap → Backlog (backlog
  comes later via tasks --product). Re-authoring is also how an existing
  roadmap.md gets critiqued or revised — docs-review checks writing quality
  and cross-document consistency, not sequencing soundness. Do NOT use for
  epic breakdown or work paths (tasks), PRD (product), per-work-item technical
  design (design), tasks (tasks), or architecture detail (solution).
license: Apache-2.0
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

## Negative constraints

roadmap.md MUST NOT contain:

- Story-level acceptance criteria or epic detail → `docs/product/backlog.md`
- Implementation patterns or tech stack → `docs/architecture/solution.md`
- Business strategy → `docs/product/product.md`

## Context

<artifacts>
[Required: docs/product/product.md.
Optional upstream: docs/architecture/solution.md (architecture constraints that
shape phasing). Optional downstream if it already exists: docs/product/backlog.md
(do not block on it — backlog is written after roadmap via tasks --product).
Cross-squad dependency context when the caller supplies it.]
</artifacts>

## Steps

1. Read product.md before writing anything. Read solution.md when present.
   Do not require backlog.md.
2. Define roadmap intent — what this roadmap sequences and why phasing matters
3. Articulate 3–5 sequencing principles that drive phase order
4. Define each phase:
   - Name and objective (one sentence)
   - Themes / candidate epics (titles; backlog IDs only if backlog.md already
     exists — otherwise leave IDs for `tasks --product`)
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
- When backlog.md exists, exit criteria must map to named epics; on first
  roadmap (no backlog yet), name themes that `tasks --product` will decompose
- Phases are sequential; parallelism lives within phases
- Target 5–8 pages

## Output format

Markdown with YAML frontmatter. Save to the resolved path. Use [assets/roadmap.template.md](assets/roadmap.template.md).

## Gotchas

- **Do not wait for backlog.md** — hierarchy is Product → Solution → Roadmap →
  Backlog. After roadmap is drafted, `/product-management:tasks --product`
  creates the epic backlog.
- **Epic rows and work paths** belong in backlog, not roadmap.
- **Story AC** belongs in TASKS.local.md, not phase exit criteria (keep exit criteria
  verifiable at phase level).

## Supporting files

- [assets/roadmap.template.md](assets/roadmap.template.md)

## Related skills

- `/product-management:product` — product strategy input (upstream)
- `/architecture:solution` — architecture (upstream companion; if not installed: `/plugin install architecture@carinya-plugins`)
- `/product-management:tasks --product` — epic backlog (downstream)
- `/engineering:docs-review` — writing quality / cross-doc consistency (not strategic soundness)
