<!--
DRAFTING AIDE — DELETE THIS BLOCK BEFORE SAVING THE OUTPUT FILE.
DO NOT INCLUDE in tasks.md:
  - Architecture narrative → cite solution.md §N.M
  - Design narrative → cite ./design.md#section
  - New epics → .agency/backlog.md via tasks --product
  - Business rationale → product.md
  - Definition-of-Done items inside story acceptance criteria
Every story needs: statement, independent test criterion, ≥1 Gherkin scenario.
Every task needs: deliverable with a concrete file path, estimate, status.
-->
---
type: Tasks
epic: <!-- kebab-case slug, max two words -->
epic_id: <!-- e.g. CHK01 -->
version: '0.1'
owner: <!-- squad -->
status: Draft
last_updated: <!-- YYYY-MM-DD -->
source: <!-- design.md | path to the spec this was decomposed from -->
related:
  - .agency/backlog.md
  - .agency/work/{epic}/design.md
  - .agency/architecture/solution.md
---

# Tasks — {Epic title} ({EPIC-ID})

## 1. Summary

**Epic:** {EPIC-ID} | **Phase:** | **Priority:** | **Estimate:** {n} points across {n} stories / {n} tasks

**Source.** <!-- design.md, or the spec this was decomposed from -->

**Scope.**

**Out of scope (this epic).** <!-- name the adjacent work deliberately excluded -->

**MVP.** Story S1 — <!-- the thinnest slice that proves the epic works -->

## 2. Conventions

| Convention | Value |
| ---------- | ----- |
| Story ID | `{EPIC-ID}-S{n}` |
| Task ID | `{EPIC-ID}-{nn}` — sequential across the epic, never reused |
| Story label | `[S{n}]` on every task with a parent story |
| Parallel marker | `[P]` — different files, no incomplete dependency |
| Acceptance | Gherkin on the story; EARS where a rule is clearer |
| Estimate | Story points, Fibonacci |

## 3. Foundational

<!-- Shared prerequisites every story needs. No story label. These carry their
     own Gherkin, since no story covers them. Keep genuinely shared — a
     prerequisite only one story needs belongs to that story. -->

- [ ] **[{EPIC-ID}-01]** {Title} — `path/to/deliverable`
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

<!-- One subsection per story, in priority order. S1 is the MVP. -->

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

- [ ] **[{EPIC-ID}-02]** [S1] {Title} — `path/to/file`
  - **Status:** not started | **Estimate:** | **Owner:**
  - **Depends on:** {EPIC-ID}-01
  - **Deliverable:**
- [ ] **[{EPIC-ID}-03]** [P] [S1] {Title} — `path/to/file`
  - **Status:** not started | **Estimate:** | **Owner:**
  - **Depends on:** {EPIC-ID}-01
  - **Deliverable:**

### S2 — {Story title}

<!-- Same shape. -->

## 5. Cross-cutting

<!-- Polish, documentation, observability. No story label. Omit if empty. -->

- [ ] **[{EPIC-ID}-nn]** {Title} — `path/to/file`
  - **Status:** not started | **Estimate:** | **Owner:**
  - **Deliverable:**

## 6. Dependencies

```text
{EPIC-ID}-01 ──┬── S1: -02 ──> -03
               └── S2: -04 ──> -05
```

**Parallel opportunities.** <!-- Tasks marked [P] that can run at the same time -->

**External dependencies.** <!-- Anything outside the team's control, with owner and status -->

## 7. Traceability and Definition of Done

### Stories to design and architecture

| Story | design.md § | solution.md § |
| ----- | ----------- | ------------- |

### Definition of Done (epic-wide)

<!-- Uniform across the epic. Do not repeat these inside story acceptance
     criteria. -->

- [ ] All Gherkin scenarios pass; all stated EARS rules hold
- [ ] Tests written and CI green
- [ ] Code review approved and merged
- [ ] Documentation updated where the criteria require it

## 8. Handoff

<!-- What this epic leaves stable; what comes next -->
