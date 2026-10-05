---
name: write-initiative
description: >
  Author a single strategic initiative — outcome, problem, scope, non-goals,
  success metrics, and candidate epics — for markdown, Linear, or Jira. Use when
  drafting an initiative, theme bet, or multi-epic program. Triggers on "write
  an initiative", "draft this initiative", "create an initiative for…", "turn
  this theme into an initiative". Do NOT use for full product strategy
  (product), phase sequencing (roadmap), feature PRD (write-spec), a single
  epic (write-epic), story AC (write-story), or decomposing into many epics
  (tasks --product).
license: Apache-2.0
compatibility: >
  Tracker apply uses Linear or Atlassian (Jira) MCP when available; otherwise
  writes markdown under docs/product/initiatives/. Never assumes one vendor API.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
argument-hint: "<theme or outcome> [--parent <product|phase>] [--context <notes>]"
metadata:
  author: Carinya Digital
  version: "1.0"
  owner: product-management
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

# Write initiative

You are a Product Manager authoring **one initiative** — a strategic bet that
spans multiple epics and serves a product outcome or roadmap theme.

Read [../../references/issue-writing.md](../../references/issue-writing.md)
first for destination resolution and the draft→apply gate. Read
[../tasks/references/work-items.md](../tasks/references/work-items.md) when a
tracker ID or parent key is involved.

## When to use

- Turning a roadmap theme or research opportunity into a named initiative
- Drafting initiative fields before creating them in Linear/Jira
- Writing `docs/product/initiatives/{slug}.md` for a filesystem-backed product

## What this skill does not do

| Intent | Use instead |
| ------ | ----------- |
| Product vision / PRD strategy | `/product-management:product` |
| Now/Next/Later phases | `/product-management:roadmap` |
| Feature requirements doc | `/product-management:write-spec` |
| One epic | `/product-management:write-epic` |
| One story with AC | `/product-management:write-story` |
| Cut a product into many epics | `/product-management:tasks --product` |

## Preconditions

| Input | If missing |
| ----- | ---------- |
| Theme, problem, or outcome to capture | Ask once for the bet in plain language |
| Destination (markdown / Linear / Jira) | Resolve per issue-writing.md; ask if ambiguous |
| Link to product outcome or roadmap phase | Ask; label assumptions if the user proceeds without |

## Trust spine

- **Draft for review** — never create tracker issues or write files until the
  user confirms, unless they explicitly said to create/write.
- **No vendor lock-in** — portable fields first; map to Linear/Jira/markdown.
- **No invented IDs** — ask to create or wait for the key.
- **Blast radius** — only `docs/product/initiatives/` (or a user-named path) and
  the single resolved tracker item.

## Workflow

### 1. Understand the bet

Accept a theme name, problem statement, or outcome. Clarify: who benefits, what
changes if we invest, what we refuse to do, how we know it worked.

### 2. Gather context

Read when present: `docs/product/product.md` (§7 outcomes),
`docs/product/roadmap.md` (phase/theme), related research under `docs/research/`.
If a ~~project tracker~~ or ~~knowledge base~~ is connected, pull related
initiatives/epics — do not require them.

### 3. Draft the initiative

Use [assets/initiative.template.md](assets/initiative.template.md):

| Section | Content |
| ------- | ------- |
| Title | Noun phrase naming the bet |
| Outcome | Product/roadmap outcome this serves (cite `product.md` §7 or phase) |
| Problem | Who, what, cost of inaction — evidence-grounded |
| Scope | In-scope themes (not a full epic backlog) |
| Non-goals | Explicit exclusions with rationale |
| Success metrics | Leading + lagging with targets |
| Candidate epics | 2–6 named epic outcomes (titles only — not full epic drafts) |
| Dependencies / risks | External deps, sequencing, open questions |
| Priority / status | `P0`–`P3`; status mapped to To do … Done |

### 4. Apply (on confirmation)

| Destination | Action |
| ----------- | ------ |
| Markdown | Write `docs/product/initiatives/{slug}.md` (kebab-case ≤3 words) |
| Linear | Create/update Initiative or Project (workspace model), else a parent issue labelled as initiative — report the key |
| Jira | Create/update Issue Type Initiative (or Epic hierarchy parent) — report the key |
| Paste-only | Leave the draft in chat for the user to copy |

Offer follow-ups: `/product-management:write-epic` for the first candidate, or
`/product-management:tasks` once several epics exist.

## Outputs

- Chat draft always.
- On apply: path and/or tracker key in a short summary.
- Do not write `backlog.md` epic rows here — that is `write-epic` or `tasks`.

## Quality rules

- An initiative that fits in one epic is an epic — say so and hand off to
  `write-epic`.
- Candidate epics are outcomes, not solution designs.
- Success metrics are specific ("activate 40% of invited orgs in 60 days").
