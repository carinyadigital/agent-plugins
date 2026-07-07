---
epic: {{EPIC}}
branch: {{BRANCH}}
design: {{DESIGN_PATH}}
tasks: {{TASKS_PATH}}
seeded: {{SEEDED_DATE}}
---

# {{EPIC}} Ralph loop context

Seeded by `/ralph setup {{EPIC}}`. Static reference the loop reads each
iteration. Do not edit `loop-state.md` manually while a loop is running.

## Sources

- Design: `{{DESIGN_PATH}}`
- Tasks: `{{TASKS_PATH}}`
- Branch: `{{BRANCH}}`

## Task sequence (dependency-safe order)

{{TASK_SEQUENCE}}

## Validation commands

Fast (run at `validate_and_commit`, per task):

{{FAST_VALIDATION_COMMANDS}}

Full (run once at `final_validation`):

{{VALIDATION_COMMANDS}}

## Tracker

{{TRACKER_SECTION}}

## UI signals (when to run ux_review)

{{UI_SIGNALS}}

## Step machine (per task)

```
task-start → implement → review → review_fix (max 3) → ux_review (UI only, fix max 2) → validate_and_commit → task-progress → [next task]
```

## Final phase (current_task: final — runs once, after all tasks committed)

```
final_review (strongest model) → final_review_fix (max 3) → final_validation (full commands) → final_validate (/validate {{EPIC}}) → create_mr (/merge-request create --draft) → done
```
