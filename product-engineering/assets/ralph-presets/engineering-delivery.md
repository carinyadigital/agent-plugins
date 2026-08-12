## Preset: engineering delivery

Drive work item `{{WORK_ID}}` to a merge request on branch `{{BRANCH}}`, one
task per iteration.

### Sources

- Tasks and acceptance criteria: `{{TASKS_PATH}}`
- Work item technical design: `{{TDD_PATH}}`
- Run context (task order, validation commands, tracker): `{{RUN_DIR}}/context.md`

### Sub-agent rule

Every skill step (`/implement`, `/code-review`, `/ux-design-review`,
`/validate`, `/merge-request`) MUST run in a fresh sub-agent. Never inline.
Context isolation per step is what stops the orchestrator's context degrading
across a long run.

### Commit rule

All commits target `{{BRANCH}}`. Verify with `git branch --show-current`
before every commit. Message format `{TASK_ID}: <imperative summary>` with a
`Work-item: {{WORK_ID}}` trailer. No `Co-authored-by` trailers, no emojis.

### Per-task steps

Resolve `{TASK_ID}` from `current_item` and run only the step named by
`current_step`.

#### task-start

1. Read the entry for `{TASK_ID}` in `{{TASKS_PATH}}`: title, Gherkin
   acceptance criteria, dependencies.
2. Run the tracker start action from `context.md` (skip if none).
3. Set `current_step: implement`.

#### implement

1. Launch a sub-agent: `/implement {TASK_ID}`.
2. Do not commit in this step.
3. Set `current_step: review`, reset `fix_count: 0`.

#### review

1. Launch a sub-agent: `/code-review`, writing to
   `{{RUN_DIR}}/review-{TASK_ID}.md`.
2. If there are no `[blocking]` findings, or `fix_count` has reached 3, set
   `current_step: ux_review` (record any unresolved findings under `## Notes`
   when the budget is exhausted).
3. Otherwise set `current_step: review_fix`.

#### review_fix

1. Launch a sub-agent: `/code-review-fix`.
2. Increment `fix_count`.
3. Set `current_step: review`.

#### ux_review

Only when the diff touches UI, per the UI signals in `context.md`. Otherwise
set `current_step: validate_and_commit` and end the turn.

1. Launch a sub-agent: `/ux-design-review`, writing to
   `{{RUN_DIR}}/ux-review-{TASK_ID}.md`.
2. If there are no `[blocking]` findings, or `fix_count` has reached 2, set
   `current_step: validate_and_commit`.
3. Otherwise set `current_step: ux_review_fix`.

#### ux_review_fix

1. Launch a sub-agent: `/ux-design-fix blocking`.
2. Increment `fix_count`.
3. Set `current_step: ux_review`.

#### validate_and_commit

1. Run the fast validation commands from `context.md` inline (lint,
   typecheck). If they fail, fix them here and re-run.
2. Verify the branch, then commit.
3. Run the tracker progress action.
4. Append `{TASK_ID}` to `completed_items`, set `current_item` to the next
   task in the sequence, and set `current_step: task-start`.
5. When no tasks remain, set `current_item: final` and
   `current_step: final_review`.

### Final phase

Runs once, after every task is committed.

#### final_review

1. Launch a sub-agent reviewing the whole work item's branch diff, not one
   task. Use the strongest model available for sub-agents.
2. If there are no `[blocking]` findings, or `fix_count` has reached 3, set
   `current_step: final_validation`. Otherwise set
   `current_step: final_review_fix`.

#### final_review_fix

Fix blocking findings (a cheaper model is fine here), increment `fix_count`,
set `current_step: final_review`.

#### final_validation

Run the full validation command list from `context.md` (install, format, lint,
typecheck, build, test). All must pass before setting
`current_step: final_validate`. On failure, fix and re-run; this step does not
advance until green.

#### final_validate

Launch a sub-agent: `/validate {{WORK_ID}}`. This checks Gherkin acceptance
criteria and, for an epic, roadmap exit criteria.

If there are no gaps, set `current_step: create_mr`. Any gap stops the loop
instead: record it under `## Notes` and do NOT advance. Gaps are never
promised over.

#### create_mr

Launch a sub-agent: `/merge-request --draft`. Record the MR URL under
`## Notes`, then set `current_step: done`.

#### done

Verify every one of these before finishing:

- every task in the sequence appears in `completed_items`
- `final_validate` passed with no gaps
- the merge request exists and its URL is recorded

If all three hold, emit the completion promise. If any does not, record why
under `## Notes` and do not advance.
