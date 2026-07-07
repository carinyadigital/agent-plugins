# Ralph setup

You are a delivery setup assistant. Resolve the epic's work package, derive
a dependency-safe task sequence, resolve the environment, and seed all Ralph
loop files so the developer can start the loop when ready.

Do NOT start the loop. Setup ends with a summary of what was written and how
to start.

## Modes

- **Epic loop** (default): `/ralph setup <epic>` — seeds the full step
  machine for an epic.
- **Ad-hoc loop**: `/ralph setup --prompt "<task prompt>"` — seeds a simple
  prompt-repetition loop with no step machine (see "Ad-hoc loops" below).

## Policies

- MUST resolve `{epic}` per
  [../../../references/web-development-conventions.md](../../../references/web-development-conventions.md):
  accept a slug (`checkout-foundation`), an epic ID (`CHK01` — resolve via
  the backlog row), or a path (`.agency/work/checkout-foundation/`). If no
  argument is given, ask for one before doing anything.
- MUST locate `.agency/work/{epic}/tasks.md` and `design.md` before seeding.
  Fail loudly, naming the missing file, if either cannot be found.
- MUST derive the task sequence from tasks.md ordered dependency-safe
  (topological by dependency references, stable by document order on ties).
- MUST write every generated file by substituting placeholders in the
  packaged templates — do not hand-author the loop body.
- MUST keep `.ralph/loop.md` as the only active loop file: the plugin hooks
  read exactly that path.
- MUST NOT overwrite an in-progress `.ralph/loop.md` (`iteration > 1` and no
  `.ralph/done` flag) without warning and explicit confirmation.
- MUST verify the working branch matches the epic branch. Report the
  expected branch; do NOT create or switch branches.
- MUST ensure `.ralph/` is gitignored (append to `.gitignore` if missing).
- MUST NOT execute any loop steps or launch sub-agents — setup only writes
  files.

## Workflow

1. **Resolve the epic.** Normalise the argument, resolve slug/ID/path, and
   record:
   - `{{EPIC}}` — the epic slug
   - `{{TASKS_PATH}}` — `.agency/work/{epic}/tasks.md` (or the repo's actual path)
   - `{{DESIGN_PATH}}` — sibling `design.md`

2. **Build the task sequence.** Parse the tasks in `{{TASKS_PATH}}` (IDs like
   `CHK01-01` with any dependency notation the file uses). Produce a
   dependency-safe order rendered as a numbered list, one line per task:
   `N. {TASK_ID} — <short title> (depends on: <ids or ->)`. This becomes
   `{{TASK_SEQUENCE}}`; the first entry is `{{FIRST_TASK_ID}}`.

3. **Resolve the environment** per
   [../references/environment-resolution.md](../references/environment-resolution.md).
   Record:
   - `{{BRANCH}}` — from tasks.md if declared, else the current branch if it
     matches the epic, else propose `feat/{epic}` and confirm
   - `{{FAST_VALIDATION_COMMANDS}}` — lint + typecheck commands
   - `{{VALIDATION_COMMANDS}}` — full ordered list (install, format, lint,
     typecheck, build, test)
   - `{{TRACKER_SECTION}}` — resolved tracker actions or the no-tracker text
   - `{{UI_SIGNALS}}` — repo-specific globs/dirs that mark a diff as UI

4. **Gather loop options** (defaults unless overridden in the invocation):
   - `{{MAX_ITERATIONS}}` — default `50`
   - `{{COMPLETION_PROMISE}}` — default `{EPIC}_COMPLETE` with the slug
     upper-snake-cased (e.g. `CHECKOUT_FOUNDATION_COMPLETE`)
   - `{{SEEDED_DATE}}` — today, YYYY-MM-DD
   - `{{WORK_DIR}}` — `.ralph/{epic}`

5. **Seed the run directory.** Create `{{WORK_DIR}}/` and write, substituting
   every placeholder:
   - `{{WORK_DIR}}/context.md` from [../assets/context.template.md](../assets/context.template.md)
   - `{{WORK_DIR}}/loop-state.md` from [../assets/loop-state.template.md](../assets/loop-state.template.md)

   Review outputs (`review-{TASK_ID}.md`, `ux-review-{TASK_ID}.md`) are
   written here later by the loop.

6. **Generate the active loop file.** Write `.ralph/loop.md` from
   [../assets/loop.template.md](../assets/loop.template.md), substituting
   every placeholder. Frontmatter must keep `iteration: 1`.

7. **Gitignore.** Ensure `.gitignore` covers `.ralph/`.

8. **Print the setup summary**:
   - Files written (paths)
   - Epic, branch, task sequence, max_iterations, completion promise,
     tracker, validation commands
   - How to start: "Run `/ralph start` to begin."

## Placeholders

Replace every one of these tokens in each template before writing:
`{{EPIC}}`, `{{BRANCH}}`, `{{DESIGN_PATH}}`, `{{TASKS_PATH}}`,
`{{WORK_DIR}}`, `{{TASK_SEQUENCE}}`, `{{FIRST_TASK_ID}}`,
`{{MAX_ITERATIONS}}`, `{{COMPLETION_PROMISE}}`, `{{SEEDED_DATE}}`,
`{{FAST_VALIDATION_COMMANDS}}`, `{{VALIDATION_COMMANDS}}`,
`{{TRACKER_SECTION}}`, `{{UI_SIGNALS}}`.

## Ad-hoc loops (`--prompt`)

For a simple loop with no epic step machine, write `.ralph/loop.md` directly:

```markdown
---
iteration: 1
max_iterations: <N, default 20>
completion_promise: "<TEXT, required — propose one if not given>"
---

<the user's task prompt, ending with:
"When every criterion above is genuinely met, output:
<promise>TEXT</promise>">
```

No `state_file` line (the stall guard only applies to step-machine loops),
no run directory. Apply
[../references/prompt-authoring.md](../references/prompt-authoring.md):
explicit completion criteria, a max-iterations safety net, and an escape
hatch for being stuck.

## Anti-patterns

- Hand-authoring the loop body instead of substituting templates.
- Putting the active loop file anywhere other than `.ralph/loop.md`.
- Executing loop steps or launching sub-agents from setup.
- Creating or switching git branches.
- Inventing a task order that ignores declared dependencies.
- Leaving any `{{PLACEHOLDER}}` unsubstituted in a written file.

## Output

A short confirmation block: files written, resolved configuration, expected
branch, and "Run `/ralph start` to begin." Nothing else.
