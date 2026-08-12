<!--
DRAFTING AIDE — DELETE THIS BLOCK BEFORE SAVING THE OUTPUT FILE.
DO NOT INCLUDE in a sprint plan:
  - Gherkin acceptance criteria → docs/work/{work-id}/tasks.md
  - New or re-prioritised epics → docs/product/backlog.md
  - Phase re-sequencing or exit criteria → docs/product/roadmap.md
  - Architecture or design detail → solution.md / tdd.md
  - Committed scope beyond capacity minus carry-over → make it Stretch
-->
---
type: Sprint Plan
sprint_id: <!-- e.g. sprint-3 -->
version: '0.1'
owner: <!-- squad -->
status: Draft
last_updated: <!-- YYYY-MM-DD -->
related:
  - docs/product/backlog.md
  - docs/product/roadmap.md
---

# Sprint plan — {Sprint id}

**Dates:** <!-- YYYY-MM-DD to YYYY-MM-DD -->

## Sprint goal

<!-- One sentence, one outcome. A third party must be able to tell at sprint
     end whether it was met. Two goals joined by "and" are two sprints. -->

## Capacity

| Measure                  | Points | Source                        |
| ------------------------ | ------ | ----------------------------- |
| Available capacity       |        | <!-- derived from sprint-N, or supplied --> |
| Consumed by carry-over   |        |                               |
| Remaining for new work   |        |                               |

<!-- If no velocity history exists, record TBD and say so. Do not invent it. -->

## Carry-over

<!-- Tasks from the prior plan not marked done in their tasks.md. These consume
     capacity before any new work is considered. -->

| Work item | Task ID | Title | Estimate | Owner | Why it carried |
| --------- | ------- | ----- | -------- | ----- | -------------- |

## Retrospective actions

<!-- Every action from the prior retrospective is either committed here or
     deferred with a reason. Silence means it was dropped. -->

| Action ID | Action | Committed / Deferred | Reason if deferred |
| --------- | ------ | -------------------- | ------------------ |

## Scope

| Work item | Title | Work path | Phase |
| --------- | ----- | --------- | ----- |

## Committed tasks

<!-- Every task must already exist in a work item's tasks.md with ≥1 Gherkin
     scenario. Total points must fit within remaining capacity. -->

| Work item | Task ID | Title | Estimate | Owner |
| --------- | ------- | ----- | -------- | ----- |

**Committed total:** <!-- points -->

## Stretch

<!-- Pulled only if committed work finishes early. Not a commitment. -->

| Work item | Task ID | Title | Estimate |
| --------- | ------- | ----- | -------- |

## Dependencies

<!-- Anything a committed task needs that the team does not control. An
     unnamed dependency becomes an invisible blocker mid-sprint. -->

| Dependency | Needed by | Owner | Status | Gates |
| ---------- | --------- | ----- | ------ | ----- |

## Risks

| Risk | Likelihood | Impact | Mitigation | Owner |
| ---- | ---------- | ------ | ---------- | ----- |

## Out of scope

<!-- Name the tempting adjacent work the team is deliberately not doing. An
     empty section means the boundary was never drawn. -->

## Sprint definition of done

<!-- What must be true of every committed task before the sprint can close.
     Verifiable by someone who was not in the room. -->

- [ ]
