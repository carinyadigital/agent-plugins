---
name: tdd
description: >
  Use when the user wants a technical design document (TDD) for any work item —
  epic, story, bug, or spike — at docs/work/{work-id}/tdd.md, in skeleton or
  full mode. Pass a work item ID (CHK01, or a Linear/Jira/GitHub key like
  JIRA-123). Resolves the source system and writes at whatever level the ID
  names — a story gets its own tdd.md beside its parent epic's, not nested
  inside it. Cite solution.md — do not re-narrate architecture. Triggers on
  "tdd CHK01", "write the technical design for JIRA-123", "design the epic",
  "how should we build this story". For reviewing an existing tdd.md, use
  docs-review instead. Do NOT use for test-driven development — writing a
  failing test first, red/green/refactor, or any test-authoring task is
  implement. Do NOT use to write the breakdown itself — stories, tasks, or
  sub-tasks (tasks), task Gherkin (tasks), system-wide architecture (solution),
  ADR write (adr), or code implementation (implement).
license: MIT
compatibility: Tracker resolution uses Linear, Atlassian (Jira), or GitHub/GitLab MCP tools when available, or `git remote`/`gh`/`glab`; falls back to the filesystem when none are reachable.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git remote:*)
  - Bash(git mv:*)
  - Bash(gh:*)
  - Bash(glab:*)
argument-hint: "<work-id> [--mode skeleton|full] [--context <notes>]"
metadata:
  author: Carinya Parc
  version: "4.0"
  owner: product-engineering
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

Prefer `docs/work/` and `docs/architecture/`; fall back to `.agency/work/` / `.agency/architecture/` when reading legacy artefacts.

# Technical design document

You are a Software Architect writing a technical design document at
`docs/work/{work-id}/tdd.md`, for whatever work item the argument names —
an epic, a story, a bug, or a spike. Read
[work-item-resolution.md](../../references/work-item-resolution.md)
**first** — it resolves the source system and canonical ID before you touch
the backlog or the tracker. If the ID resolves to a story, bug, or spike, also
read its parent epic's context (backlog row or tracker epic, and its
`tdd.md` if one exists) — cite it by ID rather than re-narrating it.

This skill writes design documents. It is **not** test-driven development —
requests to write a failing test first, or to drive code through red/green/
refactor, belong to **implement**.

## Conventions

Read [delivery-conventions.md](../../references/delivery-conventions.md)
when resolving `{work-id}` or checking artefact boundaries.

## Artefact

`docs/work/{work-id}/tdd.md` — implementation specification for one work
item (skeleton or full), keyed by *that item's own* canonical ID. A
story's TDD sits at `docs/work/{story-id}/tdd.md`, alongside its parent
epic's folder, not inside it.

## Path resolution

Default: `docs/work/{work-id}/tdd.md`. User-named paths under `docs/work/` override.

Repos written before this skill was renamed from `design` hold the same
artefact at `docs/work/{work-id}/design.md`. When that file exists and
`tdd.md` does not, say so, `git mv` it to `tdd.md`, and update it in place —
never leave two copies of the same design side by side.

## Mode (`--mode`)

- `skeleton` — walking skeleton, Phase 0, 2–4 pages
- `full` — Sprint 2+, 5–10 pages

## Negative constraints

Do NOT put in tdd.md:

- Architecture-wide patterns already in solution.md — cite `solution.md §{N.M}`
- Business strategy → `docs/product/product.md`
- Phase sequencing → `docs/product/roadmap.md`
- Task-level Gherkin → `docs/work/{work-id}/tasks.md` via **tasks**

## Context

[Work item row in backlog.md or the tracker, solution.md, parent epic's
tdd.md if this is a story/bug/spike, existing tdd.md (or legacy design.md)
if updating, codebase]

## Steps (skeleton)

1. Read solution.md and the work item's row (backlog.md or the tracker); if
   it is a story, bug, or spike, also read its parent epic's tdd.md
2. Draft §1–§6 per template
3. §4 must list what this work item did **not** ship

## Steps (full)

1. Read all context
2. Draft §1–§12 per template

## Pre-save validation

- [ ] Work item resolved per work-item-resolution.md — asked the user on any
  ambiguity in source system or ID
- [ ] Path is `docs/work/{work-id}/tdd.md` keyed by this item's own
  canonical ID (filesystem-only: correct slug, ≤2 words, not the internal ID)
- [ ] A legacy `design.md` for this work item was moved, not duplicated
- [ ] A story/bug/spike TDD cites its parent epic by ID rather than
  duplicating its tdd.md
- [ ] Solution cited by section; no duplicated architecture narrative
- [ ] No Gherkin task scenarios (gates/slice only)
- [ ] Mode-appropriate sections only (skeleton vs full)
- [ ] DRAFTING AIDE block removed

## Output format

Save to `docs/work/{work-id}/tdd.md`. Use [assets/tdd.template.md](assets/tdd.template.md).

## Gotchas

- **Do not copy solution.md** — cite `solution.md §{N.M}` instead.
- **Task Gherkin** belongs in `tasks.md`, not the TDD (gates/slice scope only).
- **`skeleton`** is 2–4 pages; **`full`** is 5–10 — do not mix section sets.
- **§4 Out of scope** must list what this work item explicitly did not ship.

## ADR candidates

Decisions recorded in `tdd.md` do not reach the architecture register on
their own. After the work item ships, run `/architecture:adr plan <work-id>` to
harvest them — it triages each candidate into promote, inline, or defer, and
hands the promoted ones to `/architecture:adr write`.

## Supporting files

- [assets/tdd.template.md](assets/tdd.template.md)
- [examples/checkout-foundation.md](examples/checkout-foundation.md)

## Related skills

- `/product-management:tasks` — stories and AC
- `/architecture:solution` — system architecture
- `/architecture:adr` — ADR harvest / write after delivery
- `implement` — test-driven development, i.e. actually writing the tests and code
- `docs-review` — review or critique an existing tdd.md
