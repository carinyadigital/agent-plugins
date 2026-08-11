---
name: design
description: >
  Use when the user wants technical design for any work item — epic, story,
  bug, or spike — at docs/work/{work-id}/design.md, walking-skeleton or TDD
  design. Pass a work item ID (CHK01, or a Linear/Jira/GitHub key like
  JIRA-123). Resolves the source system and writes at whatever level the ID
  names — a story gets its own design.md beside its parent epic's, not
  nested inside it. Cite solution.md — do not re-narrate architecture.
  Triggers on "design CHK01", "design JIRA-123", "write the epic design",
  "how should we build this story". For reviewing an existing design.md, use
  docs-review instead. Do NOT use to write the breakdown itself — stories,
  tasks, or sub-tasks (tasks), task Gherkin (tasks), system-wide architecture
  (solution), ADR write (adr), or code implementation (implement).
license: MIT
compatibility: Tracker resolution uses Linear, Atlassian (Jira), or GitHub/GitLab MCP tools when available, or `git remote`/`gh`/`glab`; falls back to the filesystem when none are reachable.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash(git remote:*)
  - Bash(gh:*)
  - Bash(glab:*)
argument-hint: "<work-id> [--mode walking-skeleton|tdd] [--context <notes>]"
metadata:
  author: Carinya Parc
  version: "3.0"
  owner: architecture
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

# Design

You are a Software Architect writing technical design at
`docs/work/{work-id}/design.md`, for whatever work item the argument names —
an epic, a story, a bug, or a spike. Read
[work-item-resolution.md](../../references/work-item-resolution.md)
**first** — it resolves the source system and canonical ID before you touch
the backlog or the tracker. If the ID resolves to a story, bug, or spike, also
read its parent epic's context (backlog row or tracker epic, and its
`design.md` if one exists) — cite it by ID rather than re-narrating it.

## Conventions

Read [delivery-conventions.md](../../references/delivery-conventions.md)
when resolving `{work-id}` or checking artefact boundaries.

## Artefact

`docs/work/{work-id}/design.md` — implementation specification for one work
item (walking-skeleton or TDD), keyed by *that item's own* canonical ID. A
story's design sits at `docs/work/{story-id}/design.md`, alongside its parent
epic's folder, not inside it.

## Path resolution

Default: `docs/work/{work-id}/design.md`. User-named paths under `docs/work/` override.

During progressive migration, prefer `docs/work/{work-id}/design.md` (and
`docs/architecture/solution.md`, `docs/product/backlog.md` as inputs), falling
back to `.agency/work/{work-id}/design.md`, `.agency/architecture/solution.md`,
and `.agency/backlog.md` when absent. Write new or updated design artefacts
only under `docs/work/`.

## Mode (`--mode`)

- `walking-skeleton` — Phase 0, 2–4 pages
- `tdd` — Sprint 2+, 5–10 pages

## Negative constraints

Do NOT put in design.md:

- Architecture-wide patterns already in solution.md — cite `solution.md §{N.M}`
- Business strategy → `docs/product/product.md`
- Phase sequencing → `docs/product/roadmap.md`
- Task-level Gherkin → `docs/work/{work-id}/tasks.md` via **tasks**

## Context

[Work item row in backlog.md or the tracker, solution.md, parent epic's
design.md if this is a story/bug/spike, existing design.md if updating,
codebase]

## Steps (walking-skeleton)

1. Read solution.md and the work item's row (backlog.md or the tracker); if
   it is a story, bug, or spike, also read its parent epic's design.md
2. Draft §1–§6 per template
3. §4 must list what this work item did **not** ship

## Steps (TDD)

1. Read all context
2. Draft §1–§12 per template

## Pre-save validation

- [ ] Work item resolved per work-item-resolution.md — asked the user on any
  ambiguity in source system or ID
- [ ] Path is `docs/work/{work-id}/design.md` keyed by this item's own
  canonical ID (filesystem-only: correct slug, ≤2 words, not the internal ID)
- [ ] A story/bug/spike design cites its parent epic by ID rather than
  duplicating its design.md
- [ ] Solution cited by section; no duplicated architecture narrative
- [ ] No Gherkin task scenarios (gates/slice only)
- [ ] Mode-appropriate sections only (walking-skeleton vs tdd)
- [ ] DRAFTING AIDE block removed

## Output format

Save to `docs/work/{work-id}/design.md`. Use [assets/design.template.md](assets/design.template.md).

## Gotchas

- **Do not copy solution.md** — cite `solution.md §{N.M}` instead.
- **Task Gherkin** belongs in `tasks.md`, not design (gates/slice scope only).
- **`walking-skeleton`** is 2–4 pages; **`tdd`** is 5–10 — do not mix section sets.
- **§4 Out of scope** must list what this work item explicitly did not ship.

## ADR candidates

Decisions recorded in `design.md` do not reach the architecture register on
their own. After the work item ships, run `adr plan <work-id>` to harvest
them — it triages each candidate into promote, inline, or defer, and hands
the promoted ones to **adr write**.

## Supporting files

- [assets/design.template.md](assets/design.template.md)
- [examples/checkout-foundation.md](examples/checkout-foundation.md)

## Related skills

- `tasks`, `solution`, `adr`
- `docs-review` — review or critique an existing design.md
