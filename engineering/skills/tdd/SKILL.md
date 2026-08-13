---
name: tdd
description: >
  Use when the user wants a technical design document for a work item (epic,
  story, bug, or spike) in skeleton or full mode. Pass a work-item ID (CHK01,
  JIRA-123). Writes specs/{work-short-name}/tdd.md; cite solution.md, do not
  re-narrate architecture. Triggers on "tdd CHK01", "write the technical
  design", "design the epic", "how should we build this story". Review an
  existing tdd.md with docs-review. Do NOT use for test-driven development
  (implement), breakdown/Gherkin (tasks), architecture (solution), ADRs
  (adr), or code (implement).
license: MIT
compatibility: Tracker resolution uses Linear, Atlassian (Jira), or GitHub/GitLab MCP tools when available, or `git remote`/`gh`/`glab`; falls back to the filesystem when none are reachable.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git remote:*)
  - Bash(gh:*)
  - Bash(glab:*)
argument-hint: "<work-id> [--mode skeleton|full] [--context <notes>]"
metadata:
  author: Carinya Parc
  version: "5.0"
  owner: engineering
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

Read artefacts from `specs/` and `docs/architecture/`.

# Technical design document

You are a Software Architect writing a technical design document at
`specs/{work-short-name}/tdd.md`, for whatever work item the argument names —
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

`specs/{work-short-name}/tdd.md` — implementation specification for one work
item (skeleton or full). `{work-short-name}` is at most two words, from the
title; fall back to `{work-id}` when a short name cannot be discovered. A
story's TDD sits in its own `specs/{work-short-name}/` folder, alongside its
parent epic's folder, not inside it.

## Path resolution

Default: `specs/{work-short-name}/tdd.md`. User-named paths under `specs/` override. Resolve `{work-short-name}` per delivery-conventions.md (at most two words; fall back to `{work-id}`).

## Mode (`--mode`)

- `skeleton` — walking skeleton, Phase 0, 2–4 pages
- `full` — Sprint 2+, 5–10 pages

## Negative constraints

Do NOT put in tdd.md:

- Architecture-wide patterns already in solution.md — cite `solution.md §{N.M}`
- Business strategy → `docs/product/product.md`
- Phase sequencing → `docs/product/roadmap.md`
- Task-level Gherkin → `specs/{work-short-name}/TASKS.local.md` via **tasks**

## Context

[Work item row in backlog.md or the tracker, solution.md, parent epic's
tdd.md if this is a story/bug/spike, existing tdd.md
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
- [ ] Path is `specs/{work-short-name}/tdd.md` — short name ≤2 words, or
  `{work-id}` when a short name cannot be discovered
- [ ] A story/bug/spike TDD cites its parent epic by ID rather than
  duplicating its tdd.md
- [ ] Solution cited by section; no duplicated architecture narrative
- [ ] No Gherkin task scenarios (gates/slice only)
- [ ] Mode-appropriate sections only (skeleton vs full)
- [ ] DRAFTING AIDE block removed

## Output format

Save to `specs/{work-short-name}/tdd.md`. Use [assets/tdd.template.md](assets/tdd.template.md).

## Gotchas

- **Do not copy solution.md** — cite `solution.md §{N.M}` instead.
- **Task Gherkin** belongs in `TASKS.local.md`, not the TDD (gates/slice scope only).
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
