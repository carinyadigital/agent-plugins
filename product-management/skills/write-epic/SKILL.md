---
name: write-epic
description: >
  Author a single epic — title, outcome, scope, non-goals, phase, priority,
  estimate, and dependencies — for markdown backlog, Linear, or Jira. Use when
  drafting one epic, not a full backlog. Triggers on "write an epic", "draft
  this epic", "create an epic for…", "flesh out checkout-foundation as an
  epic". Do NOT use for multi-epic decomposition (tasks --product), story AC
  (write-story), initiatives (write-initiative), feature PRDs (write-spec),
  Solution Design (design), or grooming (backlog-refine).
license: Apache-2.0
compatibility: >
  Tracker apply uses Linear or Atlassian (Jira) MCP when available; filesystem
  repos upsert docs/product/backlog.md and optional specs/{slug}/epic.md.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
argument-hint: "<epic outcome or title> [--parent <initiative|phase>] [--context <notes>]"
metadata:
  author: Carinya Digital
  version: "1.0"
  owner: product-management
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

# Write epic

You are a Delivery Lead / Product Manager authoring **one epic** — a delivery
outcome for a roadmap phase, sized to decompose into stories later.

Read [../../references/issue-writing.md](../../references/issue-writing.md)
first. Read
[../tasks/references/work-items.md](../tasks/references/work-items.md) for epic
field rules and source-system resolution. Epic schema (ID, phase, estimate,
depends-on, outcome) lives there — do not invent a parallel schema.

## When to use

- Drafting or refining a single epic before or after it exists in a tracker
- Adding one epic row to a filesystem `backlog.md`
- Expanding a candidate epic from an initiative into a full epic body

## What this skill does not do

| Intent | Use instead |
| ------ | ----------- |
| Break product/roadmap into many epics | `/product-management:tasks --product` |
| Break this epic into stories + tasks | `/product-management:tasks {epic}` |
| One user story with Gherkin | `/product-management:write-story` |
| Multi-epic strategic bet | `/product-management:write-initiative` |
| Feature PRD / requirements doc | `/product-management:write-spec` |
| Solution Design | `/engineering:design` |
| Groom / split / re-estimate backlog | `/product-management:backlog-refine` |

## Preconditions

| Input | If missing |
| ----- | ---------- |
| Epic outcome or title | Ask once |
| Destination | Resolve per issue-writing.md; ask if Linear vs Jira vs markdown is unclear |
| Phase / parent initiative | Ask; required before apply to `backlog.md` |
| `product.md` outcome to cite | Prefer reading it; halt apply if no outcome can be named |

## Trust spine

- Draft for review before filesystem or tracker writes.
- Tracker key is the canonical ID when a tracker resolves — never invent a
  parallel internal ID.
- Filesystem-only: assign the next `{PREFIX}{nn}` after reading `backlog.md`.
- Writes limited to `docs/product/backlog.md`, optional
  `specs/{work-short-name}/epic.md`, or one tracker epic.

## Workflow

### 1. Understand the epic

Accept a title, outcome, initiative candidate, or vague "we need checkout
foundation". Clarify the observable outcome, phase, and what is out of scope.

### 2. Gather context

Read when present: `product.md`, `roadmap.md`, parent initiative
(`docs/product/initiatives/` or tracker), `ARCHITECTURE.md` for constraints.
Pull related tracker epics if a ~~project tracker~~ is connected.

### 3. Draft the epic

Use [assets/epic.template.md](assets/epic.template.md). Required portable
fields match work-items.md §Epic:

| Field | Rule |
| ----- | ---- |
| Title | Noun phrase naming the outcome |
| Outcome | `product.md` §7 (or equivalent) outcome served |
| Phase | Named phase from `roadmap.md` |
| Priority | `P0`–`P3` |
| Estimate | Fibonacci; `TBD` only with a spike noted |
| Depends on | Other epic IDs; must be acyclic |
| Scope / non-goals | What the epic includes and refuses |
| Success signal | How we know the epic landed (phase-level, not story Gherkin) |
| Work path | `specs/{work-short-name}/` (kebab-case ≤2 words) |

**No story-level Gherkin on the epic.** If the user asks for AC, explain AC
lives on stories and offer `write-story` or `tasks`.

### 4. Apply (on confirmation)

| Destination | Action |
| ----------- | ------ |
| Markdown | Upsert the epic row in `docs/product/backlog.md`; optionally write `specs/{work-short-name}/epic.md` for the narrative body |
| Linear | Create/update epic-type issue (or labelled epic); set parent/project when modelled |
| Jira | Create/update Epic issue type; link parent Initiative when present |
| Tracker-backed, no `backlog.md` | Tracker only — do not invent a shadow backlog |

Offer `/product-management:write-story` or `/product-management:tasks {id}` next.

## Outputs

- Chat draft always.
- On apply: epic ID, work path, and destination in a short summary.

## Quality rules

- Traces to a product outcome — undocumented value is unsupported scope.
- One phase objective; spanning two phases means two epics (say so).
- Estimate without a spike note must be a Fibonacci number.
