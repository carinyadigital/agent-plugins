---
name: write-story
description: >
  Author a single user story with statement, independent test criterion, and
  Gherkin (or EARS) acceptance criteria for markdown, Linear, or Jira. Use when
  drafting one story under an epic. Triggers on "write a story", "draft this
  user story", "create a story for…", "add a story with AC". Do NOT use for
  feature PRDs (write-spec), full epic breakdown (tasks), a single epic
  (write-epic), initiatives (write-initiative), or grooming (backlog-refine).
license: Apache-2.0
compatibility: >
  Tracker apply uses Linear or Atlassian (Jira) MCP when available; filesystem
  appends to specs/{work-short-name}/TASKS.local.md under the parent epic.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
argument-hint: "<capability or story idea> [--epic <id>] [--ears] [--context <notes>]"
metadata:
  author: Carinya Digital
  version: "1.0"
  owner: product-management
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

# Write story

You are a Business Analyst authoring **one user story** — the primary holder of
acceptance criteria inside an epic.

Read [../../references/issue-writing.md](../../references/issue-writing.md)
first. Read
[../tasks/references/work-items.md](../tasks/references/work-items.md) for story
fields and ID rules. Read
[../tasks/references/acceptance-criteria.md](../tasks/references/acceptance-criteria.md)
for Gherkin and EARS.

## When to use

- Drafting one story (with AC) before adding it to an epic
- Creating a Linear/Jira Story under a parent epic
- Appending one `### S{n}` block to an existing `TASKS.local.md`

## What this skill does not do

| Intent | Use instead |
| ------ | ----------- |
| Feature PRD / multi-story requirements | `/product-management:write-spec` |
| Decompose an epic into many stories/tasks | `/product-management:tasks {epic}` |
| Author the epic itself | `/product-management:write-epic` |
| Strategic multi-epic bet | `/product-management:write-initiative` |
| Groom / split / readiness check | `/product-management:backlog-refine` |
| Implement the story | `/engineering:implement` |

## Preconditions

| Input | If missing |
| ----- | ---------- |
| Capability or problem the story addresses | Ask once |
| Parent epic (ID, slug, or tracker key) | Ask before apply; draft can proceed with a labelled assumption |
| Destination | Resolve per issue-writing.md |
| `--ears` | Optional; add EARS only when requested or a rule is clearer than a scenario |

## Trust spine

- Draft for review before writes.
- Stories carry AC — do not leave Gherkin empty or push it to the epic.
- Canonical ID from the tracker when resolved; filesystem IDs use
  `{EPIC-ID}-S{n}` after reading the parent `TASKS.local.md`.
- Writes limited to the parent epic's `TASKS.local.md` (or the story's own
  work-dir when it has a separate design) or one tracker story.

## Workflow

### 1. Understand the slice

Accept a capability, bug-shaped request (reframe as story only if appropriate),
or "As a…". Confirm it is a **vertical slice** with one independent test
criterion. If it spans two integration boundaries, propose a split rather than
one oversized story.

### 2. Gather context

Read parent epic (tracker or `backlog.md` / `epic.md`),
`specs/{work-short-name}/design.md` when present, and existing stories so
numbering and MVP status stay coherent.

### 3. Draft the story

Use [assets/story.template.md](assets/story.template.md):

| Field | Rule |
| ----- | ---- |
| Statement | *As a {role}, I want {capability}, so that {benefit}* |
| Independent test criterion | One sentence a reviewer can demonstrate |
| Priority | `P0`–`P3` |
| Acceptance | ≥1 Gherkin scenario; observable `Then` clauses |
| EARS | Only with `--ears` or when a rule is clearer than a scenario |
| Design | Link to `design.md` section when it exists |
| Parent | Epic ID / key |

Story 1 of an epic is the MVP when no stories exist yet — say so explicitly.

### 4. Apply (on confirmation)

| Destination | Action |
| ----------- | ------ |
| Markdown | Append under Stories in `specs/{work-short-name}/TASKS.local.md` (create from the tasks template if missing and the user wants a local breakdown) |
| Linear | Create Story (or issue) with parent = epic; put statement + AC in description |
| Jira | Create Story with Epic Link / parent; AC in description or AC field |
| Sub-tasks | Do not invent a full task breakdown — offer `tasks` for that |

## Outputs

- Chat draft always.
- On apply: story ID, parent epic, path or tracker URL.

## Quality rules

- Wrong if you cannot write the independent test criterion.
- No implementation detail in `Then` clauses.
- One behaviour per Gherkin scenario.
