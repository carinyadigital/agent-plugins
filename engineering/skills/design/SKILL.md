---
name: design
description: >
  Use when the user wants a work-item Solution Design (epic, story, bug, or
  spike) in skeleton or full mode. Pass a work-item ID (CHK01, JIRA-123).
  Writes {work-dir}/design.md; cite ARCHITECTURE.md, do not re-narrate
  architecture. Triggers on "design CHK01", "write the solution design",
  "write the technical design", "design the epic", "how should we build this
  story". Do NOT use for test-driven development (implement),
  breakdown/Gherkin (tasks), system architecture (solution), ADRs (adr), UX
  review (ux-design-review), code (implement), or Ready for Development
  review (discovery-review).
license: Apache-2.0
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
  version: "6.0"
  owner: engineering
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

Work directory `{work-dir}/`; default (if not specified or unknown): `specs/{work-short-name}/`. Read artefacts from `{work-dir}/`, `ARCHITECTURE.md`, and `docs/architecture/decisions/`.

# Solution Design

You are a Software Architect writing a Solution Design at
`{work-dir}/design.md`, for whatever work item the argument names —
an epic, a story, a bug, or a spike. Read
[work-item-resolution.md](../../references/work-item-resolution.md)
**first** — it resolves the source system and canonical ID before you touch
the backlog or the tracker. If the ID resolves to a story, bug, or spike, also
read its parent epic's context (backlog row or tracker epic, and its
`design.md` if one exists) — cite it by ID rather than re-narrating it.

This skill writes a work-item Solution Design. It is **not** system
architecture (`ARCHITECTURE.md` belongs to
`/architecture:solution`) and **not** test-driven development — requests to
write a failing test first, or to drive code through red/green/refactor,
belong to **implement**.

## Conventions

Read [delivery-conventions.md](../../references/delivery-conventions.md)
when resolving `{work-id}` or checking artefact boundaries.

## Artefact

`{work-dir}/design.md` — implementation specification for one work
item (skeleton or full). A story's Solution Design sits in its own `{work-dir}/`
folder, alongside its parent epic's folder, not inside it.

If `{work-dir}/design.md` is missing and `{work-dir}/tdd.md` exists, rename
`tdd.md` to `design.md` (`git mv` when the repo is git) before updating —
do not keep both files.

## Path resolution

Resolve `{work-dir}` per delivery-conventions.md. Default (if not specified
or unknown): `specs/{work-short-name}/`. `{work-short-name}` is at most two
words; fall back to `{work-id}`. Prefer an existing folder that already holds
this work item's `design.md` or legacy `tdd.md`.

## Mode (`--mode`)

- `skeleton` — walking skeleton, Phase 0, 2–4 pages
- `full` — Sprint 2+, 5–10 pages

## Negative constraints

Do NOT put in design.md:

- Architecture-wide patterns already in `ARCHITECTURE.md` — cite `ARCHITECTURE.md §{N}`
- Business strategy → `docs/product/product.md`
- Phase sequencing → `docs/product/roadmap.md`
- Task-level Gherkin → `{work-dir}/TASKS.local.md` via **/product-management:tasks**

## Context

[Work item row in backlog.md or the tracker, ARCHITECTURE.md, parent epic's
design.md if this is a story/bug/spike, existing design.md (or legacy tdd.md)
if updating, codebase]

## Steps (skeleton)

1. Read ARCHITECTURE.md and the work item's row (backlog.md or the tracker); if
  it is a story, bug, or spike, also read its parent epic's design.md
2. Draft §1–§6 per template
3. §4 must list what this work item did **not** ship

## Steps (full)

1. Read all context
2. Draft §1–§12 per template

## Pre-save validation

- [ ] Work item resolved per work-item-resolution.md — asked the user on any
  ambiguity in source system or ID
- [ ] Path is `{work-dir}/design.md` (default `specs/{work-short-name}/design.md`)
- [ ] A story/bug/spike Solution Design cites its parent epic by ID rather than
  duplicating its design.md
- [ ] Solution cited by section; no duplicated architecture narrative
- [ ] No Gherkin task scenarios (gates/slice only)
- [ ] Mode-appropriate sections only (skeleton vs full)
- [ ] DRAFTING AIDE block removed
- [ ] Legacy `{work-dir}/tdd.md` is not left beside `design.md`

## Output format

Save to `{work-dir}/design.md`. Use [assets/design.template.md](assets/design.template.md).

## Gotchas

- **Do not copy ARCHITECTURE.md** — cite `ARCHITECTURE.md §{N}` instead.
- **Task Gherkin** belongs in `TASKS.local.md`, not the Solution Design (gates/slice scope only).
- **`skeleton`** is 2–4 pages; **`full`** is 5–10 — do not mix section sets.
- **§4 Out of scope** must list what this work item explicitly did not ship.

## ADR candidates

Decisions recorded in `design.md` do not reach the architecture register on
their own. After the work item ships, run `/architecture:adr plan <work-id>` to
harvest them — it triages each candidate into promote, inline, or defer, and
hands the promoted ones to `/architecture:adr write`.

## Supporting files

- [assets/design.template.md](assets/design.template.md)
- [examples/checkout-foundation.md](examples/checkout-foundation.md)

## Related workflow

- `discover` agent — orchestrates this skill plus `/product-management:tasks` and `discovery-review` until Ready
- `/product-management:tasks` — stories and AC
- `/architecture:solution` — system architecture (if not installed: `Install: /plugin install architecture@carinya-plugins`)
- `/architecture:adr` — ADR harvest / write after delivery (if not installed: `Install: /plugin install architecture@carinya-plugins`)
- `implement` — test-driven development, i.e. actually writing the tests and code
- `discovery-review` — Ready for Development gate on design.md + tasks + solution
- `docs-review` — review or critique an existing design.md
- `deliver` agent — implement the approved Solution Design end to end
