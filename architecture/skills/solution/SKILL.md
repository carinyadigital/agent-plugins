---
name: solution
description: >
  Use when the user wants to write system architecture at
  docs/architecture/solution.md (stub or full arc42-lite). Drafts or
  re-authors the document. Triggers on "write the architecture", "solution
  design", "arc42". Re-authoring is also how an existing solution.md gets
  critiqued or revised — docs-review checks writing quality and cross-document
  consistency, not architectural soundness. Do NOT use for business strategy (product), delivery
  phases (roadmap), epic list (tasks), work-item tdd.md (tdd), task
  Gherkin (tasks), or ADR files (adr write). Story AC belongs in
  docs/work/{work-id}/tasks.md.
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "[--stage stub|full] [--context <notes>]"
metadata:
  author: Carinya Parc
  version: "2.0"
  owner: architecture
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

Prefer `docs/architecture/`; fall back to `.agency/architecture/` when reading legacy artefacts. Write only under `docs/architecture/`.

# Solution

You are a Solution Architect writing arc42-lite solution design.

## Artefact

Default path: `docs/architecture/solution.md` — arc42-lite architecture (stub or full).

## Path resolution

If the user names a different file path in their request, read and write that
path instead of the default.

## Stage (`--stage`)

- `stub` — Phase 0: fill §1–§2 only; scaffold §3–11 as `[NEEDS CLARIFICATION]`. ≤2 pages.
- `full` — Phase 2+: all eleven sections. 8–12 pages.

## Negative constraints

solution.md MUST NOT contain:

- Commercial rationale, personas, positioning → `docs/product/product.md`
- Story-level acceptance criteria → `docs/work/{work-id}/tasks.md`
- Phase sequencing → `docs/product/roadmap.md`

## Context

<artifacts>
[Stub: docs/product/product.md, architecture principles, system boundary
Full: product.md, docs/work/{work-id}/tdd.md (skeleton mode), ADR register,
accepted ADRs]
</artifacts>

## Steps (stub)

1. Read product.md and architecture principles
2. §1 Context and scope — boundary, C4 L1 (ASCII), owns / does not own
3. §2 Quality goals and constraints — top 3–5 NFRs, constraints
4. Scaffold §3–11 with `[NEEDS CLARIFICATION]`
5. Delete the `<!-- DO NOT INCLUDE -->` comment block before saving

## Steps (full)

1. Read all context
2. §1 Context and scope
3. §2 Quality goals and constraints
4. §3 Solution strategy — style, key choices, principles vs quality goals
5. §4 Building block view — C4 L2/L3, module layout
6. §5 Runtime view — 2–5 key sequences
7. §6 Data model and ubiquitous language
8. §7 Cross-cutting concepts — observability, errors, security, testing
9. §8 Deployment and environments
10. §9 Architectural decisions — links to ADRs in `docs/architecture/decisions/`; mark gaps as "_(Not yet written)_"
11. §10 Risks, technical debt, open questions
12. §11 Graduation candidates — patterns that may lift org-wide when reused
13. Delete the `<!-- DO NOT INCLUDE -->` comment block before saving

## Quality rules

- §1 includes text-based C4 L1 diagram
- §3 names trade-offs, not only choices
- §9 does not invent full ADR bodies — link or mark candidates
- Do not repeat business context from product.md — link instead

## Gotchas

- **Per-work-item files/APIs** → cite from `docs/work/{work-id}/tdd.md`, don't duplicate full specs.
- **Story-level Gherkin** → `tasks.md`, not solution.
- **Closed ADRs** → `ADR-NNNN-*.md`; proposals stay in register only.

## Output format

Markdown with YAML frontmatter. Save to the resolved path. Use
[assets/solution.template.md](assets/solution.template.md).

## Supporting files

- [assets/solution.template.md](assets/solution.template.md)

## Related skills

- `/architecture:adr` — architecture decisions
- `/product-management:product` — product strategy
- `/product-management:tasks` — epics and work paths
- `/product-engineering:tdd` — work-item technical design
- `/product-engineering:docs-review` — writing quality / cross-doc consistency
