---
name: ralph
description: >
  Use when the user wants to run a Ralph loop: an autonomous, self-referential
  delivery loop that drives a whole epic through implement, code review, fix,
  UX review, validate, commit, and merge request, one task per iteration,
  until a completion promise is emitted (ralph setup, ralph start), or to
  inspect or stop a running loop (ralph status, ralph cancel). Also supports
  simple ad-hoc loops that repeat a single prompt until done. Do NOT use to
  implement a single task once (implement), review a diff (code-review), or
  sign off an epic (validate) — the loop orchestrates those skills.
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Shell
argument-hint: "[setup <epic|--prompt \"...\">|start|status|cancel] [--max-iterations N] [--completion-promise TEXT]"
---

# Ralph loop

Run an autonomous delivery loop: the plugin's stop hook re-feeds the loop
prompt after every turn, the agent executes exactly one step per iteration,
and the loop ends only when the completion promise is genuinely true (or a
safety rail fires). Implements the Ralph Wiggum technique with an epic step
machine on top.

## How the loop works

1. `ralph setup` seeds `.ralph/{work-id}/` (context + state) and generates
   the active loop file `.ralph/loop.md` — it does NOT start the loop.
2. `ralph start` verifies the seeded files and executes iteration 1.
3. The plugin hooks (`hooks/`) take over: after every turn, the stop hook
   re-feeds the body of `.ralph/loop.md`; the agent reads its own state and
   runs the next step.
4. The loop ends when the agent outputs `<promise>TEXT</promise>` matching
   the configured promise, `max_iterations` is reached, or the stall guard
   detects no state change for 3 consecutive iterations.

The step machine is canonical in
[references/loop-protocol.md](references/loop-protocol.md):
per task `implement → review → review_fix → ux_review (UI only) →
validate_and_commit → task-progress`, then a one-time final phase
(epic review → branch validation → `/validate` → `/merge-request`).
Every step runs this repo's skills in a fresh sub-agent.

## References

- [references/loop-protocol.md](references/loop-protocol.md) — the step machine: per-task cycle, final phase, budgets, guardrails
- [references/environment-resolution.md](references/environment-resolution.md) — resolve validation commands, tracker, branch, and UI detection once at setup
- [references/prompt-authoring.md](references/prompt-authoring.md) — completion promises, iteration budgets, escape hatches for ad-hoc loops

## Assets

- [assets/loop.template.md](assets/loop.template.md) — active loop file (frontmatter + step-machine body)
- [assets/context.template.md](assets/context.template.md) — per-run static context
- [assets/loop-state.template.md](assets/loop-state.template.md) — per-run mutable state

## Router

1. Mode: `setup`, `start`, **status**, or `cancel`. No default — if the mode
   is missing, infer from context: an epic argument implies `setup`; a bare
   `/ralph` with a seeded `.ralph/loop.md` implies `start`; otherwise ask.
2. One prompt under [prompts/](prompts/).

**setup** — [prompts/setup.prompt.md](prompts/setup.prompt.md). Resolve the
epic (slug, ID, or path per delivery conventions), derive a dependency-safe
task order, resolve the environment, seed `.ralph/{epic}/`, and generate
`.ralph/loop.md`. `--prompt "..."` seeds an ad-hoc loop instead (no step
machine). Never starts the loop.

**start** — [prompts/start.prompt.md](prompts/start.prompt.md). Verify the
seeded loop file (or seed an ad-hoc one from an inline prompt), confirm the
branch, execute iteration 1.

**status** — [prompts/status.prompt.md](prompts/status.prompt.md). Report
iteration, current task and step, budgets used, completed tasks, review
files.

**cancel** — [prompts/cancel.prompt.md](prompts/cancel.prompt.md). Remove
the active loop file and flags; keep the run directory as a record.

## Ground rules

- Only output `<promise>TEXT</promise>` when the statement is completely
  and genuinely true — never to escape the loop.
- Always set `max_iterations` (default 50) as a safety net.
- Exactly ONE step per iteration; state lives in files, not in memory.
- Every skill step runs in a fresh sub-agent (Cursor Task tool / Claude Code
  agents) — never inline. Context isolation is what keeps iterations sharp.
- All commits target the resolved branch; verify with
  `git branch --show-current` before committing. No `Co-authored-by`
  trailers, no emojis in commits.
- If installed, disable the external `ralph-loop-plugin` — this plugin
  ships its own hooks and running both would double-fire stop hooks.
