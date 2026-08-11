---
current_step: {{FIRST_STEP}}
current_item: {{FIRST_ITEM}}
completed_items: []
fix_count: 0
---

# Loop state: {{RUN_ID}}

Managed by the Ralph loop. Do not edit by hand while a loop is running.

The stop hook watches this file. If it is unchanged for three consecutive
iterations the loop stops, on the assumption that nothing is progressing.

## Work sequence

{{WORK_SEQUENCE}}

## Notes

Blockers, exhausted budgets, unresolved findings, and anything a human needs to
see when the loop ends. The loop appends here; nothing is ever removed.
