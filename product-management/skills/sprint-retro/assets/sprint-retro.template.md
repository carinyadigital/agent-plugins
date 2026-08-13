<!--
DRAFTING AIDE — DELETE THIS BLOCK BEFORE SAVING THE OUTPUT FILE.
DO NOT INCLUDE in a retrospective:
  - Acceptance criteria verification against code → validate
  - Edits to plan.md — it is the historical record of what was committed
  - Task Gherkin, new work items, architecture changes → record a routed action
  - Any finding attributed to a named individual → describe the system
  - Any action without an owner
-->
---
type: Sprint Retrospective
sprint_id: <!-- e.g. sprint-3 -->
version: '0.1'
owner: <!-- squad -->
status: Draft
last_updated: <!-- YYYY-MM-DD -->
related:
  - docs/work/sprint-{id}/plan.md
---

# Sprint retrospective — {Sprint id}

**Dates:** <!-- YYYY-MM-DD to YYYY-MM-DD -->

## Sprint goal

**Goal:** <!-- as stated in plan.md -->

**Verdict:** Met | Not met

<!-- Binary. "Mostly" is not a result. If the goal was met while committed
     tasks were missed — or missed while every task shipped — explain that gap
     here; it is usually the most interesting finding in the sprint. -->

## Commitment versus actual

| Measure            | Committed | Delivered |
| ------------------ | --------- | --------- |
| Tasks              |           |           |
| Points             |           |           |

| Work item | Task ID | Title | Committed | Outcome | Evidence |
| --------- | ------- | ----- | --------- | ------- | -------- |

<!-- Outcome: delivered / partial / not started / descoped mid-sprint.
     Evidence: task status in TASKS.local.md, MR, CI run, date. -->

## Definition of done

**Held | Waived**

<!-- Did delivered work actually meet the sprint DoD from plan.md, or was it
     waived under time pressure? Waived DoD is a finding, not admin. -->

## Prior actions

| Action ID | Action | Status | Notes |
| --------- | ------ | ------ | ----- |

<!-- Status: done / open / abandoned (with reason). An action carried three
     sprints without progress is itself a finding — raise it below. -->

## What went well

<!-- Each item needs evidence. A theme supported by one anecdote is an
     anecdote. -->

## What did not go well

<!-- Describe systems and decisions, never individuals. -->

## Actions

| ID | Finding | Action | Owner | Track |
| -- | ------- | ------ | ----- | ----- |

<!-- Track: backlog | tasks | architecture | docs | roadmap | delivery | process -->

## Routing

| Track | Actions | Actioned by |
| ----- | ------- | ----------- |
| backlog |  | **backlog-refine** |
| tasks |  | **tasks** |
| architecture |  | **solution**, **adr** |
| docs |  | **docs-review** |
| roadmap |  | **roadmap** |
| delivery |  | **code-review** |
| process |  | the team |

<!-- Drop rows with no actions. -->

## Carry-over into the next sprint

<!-- What sprint-planning must account for before committing new work. -->

| Work item | Task ID | Title | Estimate | Why it carried |
| --------- | ------- | ----- | -------- | -------------- |
