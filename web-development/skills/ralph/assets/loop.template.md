---
iteration: 1
max_iterations: {{MAX_ITERATIONS}}
completion_promise: "{{COMPLETION_PROMISE}}"
state_file: {{WORK_DIR}}/loop-state.md
---

You are running the {{EPIC}} epic delivery loop on branch `{{BRANCH}}`.

## Context

- Run working dir: `{{WORK_DIR}}/`
- Static context: `{{WORK_DIR}}/context.md` (task sequence, validation commands, tracker)
- Loop state: `{{WORK_DIR}}/loop-state.md`
- Epic design: `{{DESIGN_PATH}}`
- Tasks and acceptance criteria: `{{TASKS_PATH}}`
- Branch: `{{BRANCH}}`

## Loop rules

1. Read `{{WORK_DIR}}/loop-state.md` at the start of every iteration to
   determine `current_task` and `current_step`. Read `{{WORK_DIR}}/context.md`
   for the task sequence, validation commands, and tracker actions.
2. Execute exactly ONE step per iteration, then end the turn. The stop hook
   feeds this prompt back for the next iteration.
3. Every skill step (`/implement`, `/code-review`, `/code-review fix`,
   `/ux-design-review`, `/ux-design-review fix`, `/validate`,
   `/merge-request`) MUST run in a fresh sub-agent (Cursor Task tool /
   Claude Code agent) — never inline.
4. The per-task `review → review_fix` cycle runs at most 3 times per task
   (`review_fix_count`); the `ux_review → ux_review_fix` cycle at most 2
   (`ux_review_fix_count`). When a budget is exhausted, proceed to the next
   step regardless and record the unresolved findings in loop-state.md under
   `## Notes`.
5. All commits MUST target branch `{{BRANCH}}`. Verify with
   `git branch --show-current` before committing. No `Co-authored-by`
   trailers, no emojis.
6. When all tasks are complete, do NOT output the completion promise yet —
   enter the final phase (`current_task: final`) and finish it first.
7. Only output `<promise>{{COMPLETION_PROMISE}}</promise>` when the `done`
   step's conditions are genuinely true. Never output it to escape the loop.
8. If a step is blocked by something only a human can resolve (missing
   credentials, ambiguous requirement, destructive decision), write the
   blocker to `{{WORK_DIR}}/loop-state.md` under `## Notes`, report it, and
   stop WITHOUT updating `current_step` — the stall guard will end the loop.

---

## Iteration protocol — execute exactly ONE step

Resolve `{TASK_ID}` from `current_task` and `{STEP}` from `current_step` in
`{{WORK_DIR}}/loop-state.md`, then run only that step.

### STEP: task-start

1. Read the task entry for `{TASK_ID}` in `{{TASKS_PATH}}` (title, Gherkin
   acceptance criteria, dependencies).
2. Perform the **tracker start action** from `{{WORK_DIR}}/context.md`
   (skip if the Tracker section says none).
3. Update loop-state: `current_step: implement`.

### STEP: implement

1. Ensure you are on branch `{{BRANCH}}`.
2. Launch a new sub-agent with this prompt:

   ```
   Run /implement {TASK_ID} for the {{EPIC}} epic.
   Design: {{DESIGN_PATH}}
   Tasks: {{TASKS_PATH}}
   Branch: {{BRANCH}}
   Implement all acceptance criteria for {TASK_ID} fully before completing.
   Do not commit — the orchestrating loop commits after review.
   ```

3. Wait for the sub-agent to complete.
4. Update loop-state: `current_step: review`, `review_fix_count: 0`.

### STEP: review

1. Launch a new sub-agent with this prompt:

   ```
   Run /code-review for task {TASK_ID} of the {{EPIC}} epic.
   Design: {{DESIGN_PATH}}
   Tasks: {{TASKS_PATH}}
   Review the current git diff against the acceptance criteria and design
   spec for {TASK_ID}. Write the full review output to
   {{WORK_DIR}}/review-{TASK_ID}.md.
   ```

2. Wait for the sub-agent to complete, then read
   `{{WORK_DIR}}/review-{TASK_ID}.md`.
3. If the review contains `[blocking]` findings AND `review_fix_count < 3`:
   update loop-state `current_step: review_fix` and increment
   `review_fix_count`.
4. Else: decide whether this task's diff touches UI (rendered components,
   pages, styles, templates — see the UI signals in
   `{{WORK_DIR}}/context.md`). If yes, update loop-state
   `current_step: ux_review`, `ux_review_fix_count: 0`; if no,
   `current_step: validate_and_commit`.

### STEP: review_fix

1. Launch a new sub-agent with this prompt:

   ```
   Run /code-review fix for task {TASK_ID} of the {{EPIC}} epic.
   Design: {{DESIGN_PATH}}
   Tasks: {{TASKS_PATH}}
   Review findings: {{WORK_DIR}}/review-{TASK_ID}.md
   Address all blocking and warning findings. Do not change behaviour
   beyond what is needed to satisfy the review. Do not commit.
   ```

2. Wait for the sub-agent to complete.
3. Update loop-state: `current_step: review` (re-review after fix).

### STEP: ux_review

1. Launch a new sub-agent with this prompt:

   ```
   Run /ux-design-review for task {TASK_ID} of the {{EPIC}} epic.
   Design: {{DESIGN_PATH}}
   Tasks: {{TASKS_PATH}}
   Review the rendered UI touched by the current git diff against its
   design source. Write the full review output to
   {{WORK_DIR}}/ux-review-{TASK_ID}.md.
   ```

2. Wait for the sub-agent to complete, then read
   `{{WORK_DIR}}/ux-review-{TASK_ID}.md`.
3. If it contains `[blocking]` findings AND `ux_review_fix_count < 2`:
   update loop-state `current_step: ux_review_fix` and increment
   `ux_review_fix_count`.
4. Else: update loop-state `current_step: validate_and_commit`.

### STEP: ux_review_fix

1. Launch a new sub-agent with this prompt:

   ```
   Run /ux-design-review fix blocking for task {TASK_ID} of the {{EPIC}} epic.
   Review findings: {{WORK_DIR}}/ux-review-{TASK_ID}.md
   Address the blocking findings only. Do not commit.
   ```

2. Wait for the sub-agent to complete.
3. Update loop-state: `current_step: ux_review` (re-review after fix).

### STEP: validate_and_commit

1. Run the **fast validation commands** (lint, typecheck) from
   `{{WORK_DIR}}/context.md`.
2. If any fail: fix the errors inline (no sub-agent for trivial lint/type
   fixes), then re-run until they pass.
3. Stage and commit on `{{BRANCH}}`:

   ```
   {TASK_ID}: <imperative summary from the task title>

   Epic: {{EPIC}}
   ```

4. Verify the commit landed on `{{BRANCH}}`.
5. Update loop-state: `current_step: task-progress`.

### STEP: task-progress

1. Perform the **tracker progress action** from `{{WORK_DIR}}/context.md`
   (skip if none).
2. Update `{{TASKS_PATH}}`: mark `{TASK_ID}` complete if the file tracks
   task status.
3. Advance in loop-state:
   - Append `{TASK_ID}` to `completed_tasks`.
   - Set `current_task` to the next task in the sequence
     (see `{{WORK_DIR}}/context.md`), `current_step: task-start`,
     `review_fix_count: 0`, `ux_review_fix_count: 0`.
   - If every task in the sequence is in `completed_tasks`: set
     `current_task: final`, `current_step: final_review`,
     `final_review_count: 0`.

---

## Final phase — runs ONCE, after every task is committed

Reviews and validates the whole epic branch, not a single task.

### STEP: final_review

1. Ensure you are on branch `{{BRANCH}}`.
2. Launch a new sub-agent — use the strongest available model if the host
   supports per-agent model selection — with this prompt:

   ```
   Run /code-review for the {{EPIC}} epic branch.
   Design: {{DESIGN_PATH}}
   Tasks: {{TASKS_PATH}}
   Branch: {{BRANCH}}
   Review the full epic branch diff against the design spec and the
   acceptance criteria of every task. Write the full review output to
   {{WORK_DIR}}/review-{{EPIC}}.md.
   ```

3. Wait, then read `{{WORK_DIR}}/review-{{EPIC}}.md`.
4. If it contains `[blocking]` findings AND `final_review_count < 3`:
   update loop-state `current_step: final_review_fix`, increment
   `final_review_count`. Else: `current_step: final_validation`.

### STEP: final_review_fix

1. Launch a new sub-agent with this prompt:

   ```
   Run /code-review fix for the {{EPIC}} epic branch.
   Design: {{DESIGN_PATH}}
   Tasks: {{TASKS_PATH}}
   Review findings: {{WORK_DIR}}/review-{{EPIC}}.md
   Address all blocking findings across the branch. Do not change
   behaviour beyond what is needed to satisfy the review.
   ```

2. Wait for the sub-agent to complete, then commit any changes on
   `{{BRANCH}}`:

   ```
   {{EPIC}}: address epic code-review findings

   Epic: {{EPIC}}
   ```

3. Update loop-state: `current_step: final_review`.

### STEP: final_validation

1. Launch a new sub-agent with this prompt:

   ```
   Perform a full local validation of branch {{BRANCH}} for the {{EPIC}}
   epic. Run the full validation commands, in order:
   {{VALIDATION_COMMANDS}}
   Fix any failures so all steps pass, then commit any changes to
   {{BRANCH}}. Report the final status of each step.
   ```

2. Wait for the sub-agent to complete.
3. If validation could not be made to pass: record the failure in
   loop-state `## Notes`, report it, and stop WITHOUT advancing — do not
   output the completion promise.
4. Commit any remaining changes on `{{BRANCH}}` if the sub-agent did not.
5. Update loop-state: `current_step: final_validate`.

### STEP: final_validate

1. Launch a new sub-agent with this prompt:

   ```
   Run /validate {{EPIC}}.
   Design: {{DESIGN_PATH}}
   Tasks: {{TASKS_PATH}}
   Branch: {{BRANCH}}
   Verify every task in {{TASKS_PATH}} is complete against its Gherkin
   acceptance criteria and the roadmap phase exit criteria.
   ```

2. Wait for the sub-agent to complete.
3. If `/validate` confirms the epic is complete: update loop-state
   `current_step: create_mr`.
4. If it reports gaps: record them in loop-state `## Notes`, report them,
   and stop WITHOUT advancing — do not output the completion promise.

### STEP: create_mr

1. Launch a new sub-agent with this prompt:

   ```
   Run /merge-request create --draft for the {{EPIC}} epic.
   Branch: {{BRANCH}}
   Design: {{DESIGN_PATH}}
   Tasks: {{TASKS_PATH}}
   Open a draft merge request / pull request for this branch. Use the epic
   design and task list to generate the title and description.
   ```

2. Wait for the sub-agent to complete and record the MR/PR URL in
   loop-state `## Notes`.
3. Update loop-state: `current_task: done`, `current_step: done`.

### STEP: done

Every task is committed, the epic-level review is clean (or its fix budget
is exhausted with the remainder recorded), branch validation passes,
`/validate {{EPIC}}` confirms completion, and a merge request exists.

Output: `<promise>{{COMPLETION_PROMISE}}</promise>`
