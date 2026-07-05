---
type: Tasks
epic: <!-- kebab-case from title or short title, max two words -->
epic_id: <!-- e.g. CHK01 -->
version: '0.1'
owner: <!-- squad -->
status: Draft
last_updated: <!-- YYYY-MM-DD -->
related:
  - docs/product/backlog.md
  - docs/work/{epic}/design.md
  - docs/architecture/solution.md
---

<!--
DRAFTING AIDE — DELETE BEFORE SAVING.
§3 tasks: Gherkin required; EARS optional (see SKILL.md).
-->

# Tasks -- {Epic title} ({EPIC-ID})

## 1. Summary

**Epic:** {EPIC-ID} | **Phase:** | **Priority:** | **Estimate:**

**Scope.**

**Deliverables.**

**Dependencies.**

## 2. Conventions

| Convention | Value |
| ---------- | ----- |
| Task ID | `{EPIC-ID}-{nn}` |
| Acceptance | Gherkin required; EARS optional per SKILL.md |

## 3. Tasks

- [ ] **[{EPIC-ID}-01] {Title}**
  - **Status:** Not started | **Priority:** P0 | **Estimate:**
  - **Epic:** {EPIC-ID} | **Labels:** phase:{phase}, type:{type}
  - **Depends on:**
  - **Deliverable:**
  - **Design:** [`./design.md`](design.md)
  - **Acceptance (Gherkin):**

    ```gherkin
    Scenario:
      Given
      When
      Then
    ```

## 4. Traceability and DoD

### Tasks to solution sections

| Task | solution.md |
| ---- | ----------- |

### Definition of Done

- [ ] All Gherkin scenarios pass; all stated EARS hold
- [ ] Tests and CI green; review approved; PR merged

## 5. Handoff

<!-- What this epic leaves stable; what comes next -->
