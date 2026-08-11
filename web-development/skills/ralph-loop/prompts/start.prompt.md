# Ralph loop start

Activate a seeded loop and execute iteration 1. From iteration 2 onward the
stop hook drives the loop. Your only job here is to verify the setup and run
the first step.

## Preconditions

1. **Loop file exists.** Resolve the base directory from the agent
   (`.claude/loop` for Claude Code, `.cursor/loop` for Cursor) and read
   `{base}/active.md`. If it is missing:
   - With an inline prompt (`/ralph-loop start "..."`), seed an ad-hoc loop
     first by calling `scripts/seed-ralph-loop.sh --preset ad-hoc`, then
     continue.
   - Otherwise stop and tell the user to run `/ralph-loop-setup` first.

2. **Not already mid-run.** If frontmatter `iteration > 1` the loop is already
   in progress. Resuming is fine, but say so rather than presenting it as a
   fresh start.

3. **Session ownership.** If frontmatter carries a `session_id` that is not
   this session, the loop belongs to another window. Say so and stop: starting
   it here would give the loop two drivers.

4. **Branch matches.** For presets that commit, compare
   `git branch --show-current` with the branch in the run context. On a
   mismatch, stop and report the expected branch. Do not switch branches.

5. **Hooks installed.** Confirm the plugin's hooks are active. If the external
   `ralph-loop-plugin` is also enabled, warn that two stop hooks will fire and
   ask the user to disable one first.

## Start

1. Confirm in one short block: preset, run id, branch where relevant, max
   iterations, completion promise, and the current step from the state file.
2. Execute iteration 1 by following the body of `{base}/active.md` exactly.
   ONE step only, then end the turn. The stop hook feeds the prompt back for
   iteration 2.

## Guardrails

- Only output `<promise>TEXT</promise>` when it is genuinely true.
- Do not run more than one step in this turn, even if the first is trivial.
  One step per iteration is what keeps state and context clean.
- Do not attempt to complete the whole job in the first turn. That defeats the
  loop and produces exactly the long-context degradation it exists to avoid.
