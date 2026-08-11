<!--
DRAFTING AIDE — DELETE THIS BLOCK BEFORE SAVING THE OUTPUT FILE.
This template covers the filesystem-only fallback (no Linear/Jira resolved).
See references/work-item-resolution.md — tracker-backed repos use the
tracker's own key as the work-id and may create sub-tasks as tracker
sub-issues instead of markdown lines.
Used at two levels: an epic's own tasks.md (stories + tasks, §4 present), or
a story's own tasks.md when it gets further breakdown (sub-tasks only — omit
§4 Stories and go straight from §3 to a flat sub-task list shaped like §5).
DO NOT INCLUDE in tasks.md:
  - Architecture narrative → cite solution.md §N.M
  - Design narrative → cite ./design.md#section
  - New epics → docs/product/backlog.md via tasks --product
  - Business rationale → product.md
  - Definition-of-Done items inside story acceptance criteria
Every story needs: statement, independent test criterion, ≥1 Gherkin scenario.
Every task needs: deliverable with a concrete file path, estimate, status.
-->
---
type: Tasks
epic_slug: <!-- kebab-case, max two words — filesystem-only folder name -->
work_id: <!-- e.g. CHK01, or the tracker key if one exists -->
version: '0.1'
owner: <!-- squad -->
status: Draft
last_updated: <!-- YYYY-MM-DD -->
source: <!-- design.md | path to the spec this was decomposed from -->
related:
  - docs/product/backlog.md
  - docs/work/{work-id}/design.md
  - docs/architecture/solution.md
---

# Tasks — {Work item title} ({WORK-ID})

## 1. Summary

**Work item:** {WORK-ID} | **Phase:** | **Priority:** | **Estimate:** {n} points across {n} stories / {n} tasks
<!-- Writing a story's own tasks.md instead of an epic's: drop stories/tasks
     counts for a single sub-task count, and inherit Phase from the parent
     epic. -->

**Source.** <!-- design.md, or the spec this was decomposed from -->

**Scope.**

**Out of scope (this work item).** <!-- name the adjacent work deliberately excluded -->

**MVP.** Story S1 — <!-- the thinnest slice that proves this work item works. Omit for a story's own tasks.md — there is no further MVP below a story. -->

## 2. Conventions

| Convention | Value |
| ---------- | ----- |
| Story ID (epic's tasks.md only) | `{WORK-ID}-S{n}` |
| Task / sub-task ID | `{WORK-ID}-{nn}` — sequential within this file, never reused |
| Story label | `[S{n}]` on every task with a parent story (epic's tasks.md only) |
| Parallel marker | `[P]` — different files, no incomplete dependency |
| Acceptance | Gherkin on the story, or on this work item itself when it has no stories; EARS where a rule is clearer |
| Estimate | Story points, Fibonacci |

## 3. Foundational

<!-- Shared prerequisites every story needs. No story label. These carry their
     own Gherkin, since no story covers them. Keep genuinely shared — a
     prerequisite only one story needs belongs to that story. -->

- [ ] **[{WORK-ID}-01]** {Title} — `path/to/deliverable`
  - **Status:** not started | **Estimate:** | **Owner:**
  - **Depends on:** —
  - **Deliverable:**
  - **Design:** [`./design.md`](design.md#section)
  - **Acceptance (Gherkin):**

    ```gherkin
    Scenario:
      Given
      When
      Then
    ```

## 4. Stories

<!-- One subsection per story, in priority order. S1 is the MVP. Epic's
     tasks.md only — a story's own tasks.md has no stories beneath it; go
     straight from §3 to a flat sub-task list shaped like §5, prefixed
     [{WORK-ID}-nn]. -->

### S1 — {Story title}

**As a** {role}, **I want** {capability}, **so that** {benefit}.

**Independent test criterion.** <!-- One sentence: what a reviewer can
demonstrate to confirm this story is done. If you cannot write this, the story
is not a vertical slice. -->

**Priority:** P0 | **Design:** [`./design.md`](design.md#section)

**Acceptance (Gherkin):**

```gherkin
Scenario: {Happy path}
  Given
  When
  Then

Scenario: {The edge that actually breaks}
  Given
  When
  Then
```

<!-- Optional. Include only where a rule is clearer than a scenario:
     invariants, constraints, NFRs, always/never rules. Never restate a
     scenario. Omit this heading entirely when unused. -->

**Acceptance (EARS):**

```
WHEN {trigger} THE SYSTEM SHALL {behaviour}
IF {condition} THEN THE SYSTEM SHALL {behaviour}
```

**Tasks:**

- [ ] **[{WORK-ID}-02]** [S1] {Title} — `path/to/file`
  - **Status:** not started | **Estimate:** | **Owner:**
  - **Depends on:** {WORK-ID}-01
  - **Deliverable:**
- [ ] **[{WORK-ID}-03]** [P] [S1] {Title} — `path/to/file`
  - **Status:** not started | **Estimate:** | **Owner:**
  - **Depends on:** {WORK-ID}-01
  - **Deliverable:**

### S2 — {Story title}

<!-- Same shape. -->

## 5. Cross-cutting

<!-- Polish, documentation, observability. No story label. Omit if empty. -->

- [ ] **[{WORK-ID}-nn]** {Title} — `path/to/file`
  - **Status:** not started | **Estimate:** | **Owner:**
  - **Deliverable:**

## 6. Dependencies

```text
{WORK-ID}-01 ──┬── S1: -02 ──> -03
               └── S2: -04 ──> -05
```

**Parallel opportunities.** <!-- Tasks marked [P] that can run at the same time -->

**External dependencies.** <!-- Anything outside the team's control, with owner and status -->

## 7. Traceability and Definition of Done

### Stories to design and architecture

| Story | design.md § | solution.md § |
| ----- | ----------- | ------------- |

### Definition of Done (work item-wide)

<!-- Uniform across this work item. Do not repeat these inside story
     acceptance criteria. -->

- [ ] All Gherkin scenarios pass; all stated EARS rules hold
- [ ] Tests written and CI green
- [ ] Code review approved and merged
- [ ] Documentation updated where the criteria require it

## 8. Handoff

<!-- What this work item leaves stable; what comes next -->
