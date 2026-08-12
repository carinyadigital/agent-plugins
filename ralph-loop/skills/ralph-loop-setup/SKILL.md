---
name: ralph-loop-setup
description: >
  Use to seed or configure a Ralph loop before running it: choose a preset
  (engineering delivery for a work item, ad-hoc for a single repeating prompt,
  or custom steps), resolve the environment, set the completion promise and
  iteration budget, and write the loop files. Triggers on "set up a ralph
  loop", "configure a ralph loop", "ralph-loop-setup", or naming a work item
  to loop over. Do NOT use to start, inspect, or stop a loop (ralph-loop) —
  setup never executes loop steps.
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
argument-hint: "[<work-id>|--prompt \"...\"] [--preset NAME] [--max-iterations N] [--completion-promise TEXT]"
metadata:
  author: Carinya Parc
  version: "2.0"
  owner: ralph-loop
  work_shape: orchestrate-delivery
  output_class: draft-for-review
  review_cadence: as-needed
---

Read artefacts from `docs/work/` and `docs/architecture/`.

# Ralph loop setup

Resolve configuration and seed the loop files. **Never start the loop.** Setup
ends with a summary and an instruction to run `/ralph-loop start`.

Writing is done by `${CLAUDE_PLUGIN_ROOT}/scripts/seed-ralph-loop.sh`, not by hand. Your job is to
resolve values and call it. Hand-authoring the loop file reintroduces the
unsubstituted-placeholder failure the script exists to prevent: a stray
`{{MAX_ITERATIONS}}` in the frontmatter fails the hook's numeric validation and
silently deletes the loop.

## Interview

Ask only what you cannot resolve yourself. Use structured questions, not prose.

1. **Preset.** If not given:
   - `engineering-delivery` — contributed by **engineering** (requires that
     plugin installed). Drives a work item through implement, review, validate, and
     merge request, one task per iteration. If the preset file cannot be resolved,
     refuse and offer:
     `Install: /plugin install engineering@carinya-plugins` then re-run setup.
   - `ad-hoc` — repeat a single prompt until it is done (no companion plugins).
   - `custom` — define your own steps (no companion plugins).

2. **Target.** The work item ID for engineering delivery; the task prompt
   for ad-hoc; the step list for custom.

3. **Budgets.** Max iterations. Default 50, but for engineering delivery
   propose `tasks × 6 + 10`, since a 12-task work item will not fit in 50.

4. **Completion promise.** Propose a default and confirm it. For a work item,
   its canonical ID (or slug, in the filesystem-only source) upper-snake-cased
   with `_COMPLETE`.

5. **Environment.** Only for presets that need it, per
   [references/environment-resolution.md](references/environment-resolution.md).

## Workflow

### 1. Resolve the agent

`CLAUDE_PLUGIN_ROOT` set means `claude`; `CURSOR_PROJECT_DIR` set means
`cursor`. This determines the base directory (`.claude/loop` or
`.cursor/loop`). There is no pointer file and no `--ralph-dir` flag.

### 2. Resolve the preset inputs

**engineering-delivery**

- Resolve `{work-id}` per
  engineering `references/work-item-resolution.md` (companion plugin — required for engineering-delivery):
  detect the source system (Linear, Jira, GitHub/GitLab, or filesystem) and
  the canonical ID first — ask the user on any ambiguity, per that file's
  ask-first checklist. Never guess.
- Locate `tasks.md` and `tdd.md` under `docs/work/{work-id}/`. Fail loudly,
  naming the missing file, if either is absent.
- Derive a dependency-safe task order: topological by declared dependencies,
  stable by document order on ties. Render as
  `N. {TASK_ID} — <title> (depends on: <ids or ->)`.
- Resolve the branch. Report the expected branch; never create or switch one.
- Resolve validation commands, tracker actions, and UI signals per
  [references/environment-resolution.md](references/environment-resolution.md).

**ad-hoc**

Write the task prompt to a file and pass `--prompt-file`. Apply
[../ralph-loop/references/prompt-authoring.md](../ralph-loop/references/prompt-authoring.md):
explicit completion criteria, a verification step each iteration, and an
escape hatch for being stuck.

**custom**

Write the step definitions to a file and pass `--steps-file`. Each step needs a
name, what to do, and which step comes next. See
[../ralph-loop/references/preset-authoring.md](../ralph-loop/references/preset-authoring.md).

### 3. Seed

Call the script. Every template value goes through `--set`:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/seed-ralph-loop.sh \
  --agent claude \
  --preset engineering-delivery \
  --run-id "{work-id}-$(date -u +%Y%m%d-%H%M%S)" \
  --max-iterations 70 \
  --completion-promise CHECKOUT_FOUNDATION_COMPLETE \
  --session-id "$SESSION_ID" \
  --set WORK_ID=checkout-foundation \
  --set BRANCH=feat/checkout-foundation \
  --set TASKS_PATH=docs/work/checkout-foundation/tasks.md \
  --set TDD_PATH=docs/work/checkout-foundation/tdd.md \
  --set FIRST_ITEM=CHK01-01 \
  --set "WORK_SEQUENCE=$(cat sequence.txt)" \
  --set "GOAL=..." --set "DONE_CRITERIA=..." --set "PRESET_CONTEXT=..."
```

(`WORK_ID` is the canonical ID — a tracker key like `JIRA-123` when one
resolved, otherwise the slug shown above.)

Run with `--dry-run` first when anything is uncertain. The script refuses to
overwrite a loop past iteration 1 without `--force`, and exits non-zero on any
unresolved placeholder.

### 4. Report

Files written, resolved configuration, expected branch, and "Run
`/ralph-loop start` to begin." Nothing else.

## Policies

- MUST NOT execute loop steps or launch sub-agents. Setup only writes files.
- MUST NOT create or switch git branches.
- MUST NOT hand-author `active.md`, `loop-state.md`, or `context.md`.
- MUST fail loudly, naming the file, when a required source is missing.
- MUST NOT invent a task order that ignores declared dependencies.

## Anti-patterns

- Writing the loop file directly instead of calling the seed script.
- Starting the loop after seeding it.
- Guessing at validation commands rather than resolving them from the repo.
- Setting a completion promise the loop has no way to verify.
