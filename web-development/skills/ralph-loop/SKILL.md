---
name: ralph-loop
description: >
  Use to start, inspect, or stop a Ralph loop: an autonomous self-referential
  loop where a stop hook re-feeds the same prompt every turn until a completion
  promise is emitted or a safety rail fires (ralph-loop start, ralph-loop
  status, ralph-loop cancel). Works for any repeating multi-step job via
  presets, including full epic delivery through implement, review, validate,
  and merge request. Do NOT use to seed or configure a loop (ralph-loop-setup),
  implement a single task once (implement), review a diff (code-review), or
  sign off an epic (validate) — the loop orchestrates those skills.
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Shell
argument-hint: "[start|status|cancel] [--prompt \"...\"] [--max-iterations N] [--completion-promise TEXT]"
metadata:
  author: Carinya Parc
  version: "1.0"
  review_cadence: as-needed
  owner: web-development
  work_shape: orchestrate-delivery
  output_class: applied-change
---

# Ralph loop

Run an autonomous loop. The plugin's stop hook re-feeds the loop prompt after
every turn, the agent executes exactly one step per iteration, and the loop
ends only when the completion promise is genuinely true or a safety rail
fires.

Seeding is a separate skill: **[ralph-loop-setup](../ralph-loop-setup/SKILL.md)**.
This skill assumes a seeded loop, except for a quick inline ad-hoc start.

## How the loop works

1. `/web-development:ralph-loop-setup` resolves configuration and runs
   `scripts/seed-ralph-loop.sh`, which writes `{base}/active.md` plus a run
   directory. `{base}` is `.claude/loop` or `.cursor/loop`, resolved from the
   agent, with no pointer file.
2. `/web-development:ralph-loop start` verifies the seeded files and executes iteration 1.
3. The plugin hooks take over. After every turn the stop hook re-feeds the body
   of `active.md`; the agent reads its own state and runs the next step.
4. The loop ends when the agent emits `<promise>TEXT</promise>` matching the
   configured promise, `max_iterations` is reached, the 200-iteration hard
   ceiling is hit, or the stall guard sees no state change for 3 consecutive
   iterations.

## Safety rails

| Rail | Default | Enforced by |
| ---- | ------- | ----------- |
| max_iterations | 50 | stop hook, from frontmatter |
| hard ceiling | 200 | stop hook, applies even when unlimited |
| stall guard | 3 unchanged iterations | stop hook, watches the state file |
| session isolation | owning session only | stop hook, from `session_id` |
| fix budgets | per preset | loop state counters |

Exhausting a budget never fails the loop: the step advances and the unresolved
findings are recorded under `## Notes` so a human sees them.

## References

- [references/loop-protocol.md](references/loop-protocol.md) — the step machine, budgets, guardrails, and why one step per iteration
- [references/preset-authoring.md](references/preset-authoring.md) — how to write a preset, with a worked non-engineering example
- [references/prompt-authoring.md](references/prompt-authoring.md) — completion promises, iteration budgets, escape hatches

## Assets

- [assets/loop.core.template.md](assets/loop.core.template.md) — generic loop body, preset-agnostic
- [assets/loop-state.core.template.md](assets/loop-state.core.template.md) — per-run mutable state
- [assets/context.core.template.md](assets/context.core.template.md) — per-run static context
- [assets/presets/](assets/presets/) — `engineering-delivery`, `ad-hoc`, `custom`

## Router

Mode is `start`, `status`, or `cancel`. If no mode is given: a seeded
`{base}/active.md` implies `start`; otherwise say the loop needs seeding and
point at `/web-development:ralph-loop-setup`.

**start** — [prompts/start.prompt.md](prompts/start.prompt.md). Verify the
seeded loop, confirm the branch where the preset needs one, execute iteration
1. With `--prompt "..."` and no seeded loop, seed an ad-hoc loop first.

**status** — [prompts/status.prompt.md](prompts/status.prompt.md). Report
iteration, current step, budgets used, completed items, and artefacts.
Read-only.

**cancel** — [prompts/cancel.prompt.md](prompts/cancel.prompt.md). Stop the
loop and archive the run directory as a record.

## Ground rules

- Only output `<promise>TEXT</promise>` when the statement is completely and
  genuinely true. Never to escape the loop, never because progress is slow.
- Exactly ONE step per iteration. State lives in files, not in memory.
- Every skill step runs in a fresh sub-agent. Context isolation per step is
  what keeps a long run sharp.
- Where a preset commits, verify the branch with `git branch --show-current`
  first. No `Co-authored-by` trailers, no emojis in commits.
- If the external `ralph-loop-plugin` is installed, disable it. This plugin
  ships its own hooks and running both double-fires the stop hook.
