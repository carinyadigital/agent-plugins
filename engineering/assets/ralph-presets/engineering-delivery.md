## Preset: engineering delivery

Drive work item `{{WORK_ID}}` to a merge request on branch `{{BRANCH}}`, one
task per iteration. Keep every existing issue source current. Do not create a
repo-root `TASKS.local.md` pointer or a second task list.

### Sources

List every authoritative source resolved at setup. Typical combination:

- Tracker issue(s) already in use (Jira, Linear, GitHub/GitLab)
- Local breakdown, when it already exists: `{{TASKS_PATH}}`
- Work-item Solution Design, when it exists: `{{TDD_PATH}}` (`design.md`;
  rename legacy `tdd.md` first)
- Run context (task order, validation commands, source lifecycle):
  `{{RUN_DIR}}/context.md`

Each lifecycle step updates **all** configured sources before advancing. If
one update fails, leave the step unchanged and record which source is stale.

### Sub-agent rule

Every skill step (`/engineering:implement`, `/engineering:code-review`,
`/product-management:validate`, `/engineering:merge-request`) MUST run in a
fresh sub-agent. Never inline. Context isolation per step is what stops the
orchestrator's context degrading across a long run.

UX design review and UX design fix are **not** default stages. Add
`/design:ux-design-review` / `/design:ux-design-fix` only when the user
explicitly requested them at setup.

### Commit rule

All commits target `{{BRANCH}}`. Verify with `git branch --show-current`
before every commit. Message format `{TASK_ID}: <imperative summary>` with a
`Work-item: {{WORK_ID}}` trailer. No `Co-authored-by` trailers, no emojis.

### Per-task steps

Resolve `{TASK_ID}` from `current_item` and run only the step named by
`current_step`. Branch checkout is part of `implement`, not its own continue
— a stop-hook iteration is for a skill step, not bookkeeping. Source
lifecycle updates happen inside the named steps below.

#### implement

1. Move `{TASK_ID}` to In Progress (or the exact equivalent) on **every**
   configured source. If any update fails, record it and do not advance.
2. Read the entry for `{TASK_ID}` in `{{TASKS_PATH}}` or the tracker: title,
   Gherkin acceptance criteria, dependencies.
3. Launch a sub-agent: `/engineering:implement {TASK_ID}`.
4. Do not commit in this step.
5. Set `current_step: review`, reset `fix_count: 0`.

#### review

1. Move `{TASK_ID}` to In Review (or the exact equivalent) on **every**
   configured source. If any update fails, record it and do not advance.
2. Launch a sub-agent: `/engineering:code-review`, writing to
   `{{RUN_DIR}}/review-{TASK_ID}.md`.
3. If there are no `[blocking]` findings, or `fix_count` has reached 3, set
   `current_step: validate_and_commit` (record any unresolved findings under
   `## Notes` when the budget is exhausted).
4. Otherwise set `current_step: review_fix`.

#### review_fix

1. Launch a sub-agent: `/engineering:code-review-fix`.
2. Increment `fix_count`.
3. Set `current_step: review`.

#### validate_and_commit

1. Run the fast validation commands from `context.md` inline (lint,
   typecheck). If they fail, fix them here and re-run.
2. Verify the branch, then commit.
3. Move `{TASK_ID}` to Done (or the exact equivalent) on **every** configured
   source, with a short shipped summary when the source supports comments.
   If any update fails, record it and do not advance.
4. Append `{TASK_ID}` to `completed_items`, set `current_item` to the next
   task in the sequence, and set `current_step: implement`.
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

Launch a sub-agent: `/product-management:validate {{WORK_ID}}`. This checks
Gherkin acceptance criteria and, for an epic, roadmap exit criteria.

If there are no gaps, set `current_step: create_mr`. Any gap stops the loop
instead: record it under `## Notes` and do NOT advance. Gaps are never
promised over.

#### create_mr

Launch a sub-agent: `/engineering:merge-request --draft`. Record the MR URL
under `## Notes`, then set `current_step: done`.

#### done

Verify every one of these before finishing:

- every task in the sequence appears in `completed_items`
- `final_validate` passed with no gaps
- the merge request exists and its URL is recorded
- every configured source reports Done for every task

If all hold, emit the completion promise. If any does not, record why
under `## Notes` and do not advance.
