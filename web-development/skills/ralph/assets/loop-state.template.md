---
current_task: {{FIRST_TASK_ID}}
current_step: task-start
review_fix_count: 0
ux_review_fix_count: 0
final_review_count: 0
completed_tasks: []
---

# {{EPIC}} loop state

Managed by the Ralph loop. Do not edit manually during a run. The stop
hook's stall guard watches this file — if it is unchanged for 3 consecutive
iterations the loop stops.

## Task sequence

{{TASK_SEQUENCE}}

## Notes

(The loop records blockers, exhausted fix budgets, unresolved findings, and
the MR/PR URL here.)
