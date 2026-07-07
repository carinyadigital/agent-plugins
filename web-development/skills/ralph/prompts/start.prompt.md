# Ralph start

Activate a seeded Ralph loop and execute iteration 1. From iteration 2
onward the plugin's stop hook drives the loop — your only job here is to
verify the setup and run the first step.

## Preconditions

1. **Loop file exists.** Read `.ralph/loop.md`. If it is missing:
   - If the user passed an inline prompt (`/ralph start "..."` with optional
     `--max-iterations` / `--completion-promise`), seed an ad-hoc loop file
     first per the "Ad-hoc loops" section of
     [setup.prompt.md](setup.prompt.md), then continue.
   - Otherwise stop and tell the user to run `/ralph setup <epic>` first.
2. **Not already mid-run.** If frontmatter `iteration > 1`, this loop is
   already in progress — resuming is fine, but say so rather than treating
   it as a fresh start.
3. **Branch matches.** For an epic loop, compare `git branch --show-current`
   with the branch named in the loop file. If they differ, stop and report
   the expected branch — do not switch branches without the user's say-so.
4. **Hooks present.** Confirm the plugin's `hooks/` are installed (this
   plugin ships them). If the external `ralph-loop-plugin` is also enabled,
   warn that two stop hooks will fire and ask the user to disable one before
   starting.

## Start

1. Confirm to the user, in one short block: epic (or ad-hoc prompt summary),
   branch, max iterations, completion promise, and current task/step from
   the state file (if any).
2. Execute iteration 1 by following the body of `.ralph/loop.md` exactly —
   ONE step only, then end the turn. The stop hook feeds the prompt back
   for iteration 2.

## Guardrails

- Only output `<promise>TEXT</promise>` when it is genuinely true. Never to
  escape the loop.
- Do not run more than one step in this turn, even if the first step is
  quick — the one-step-per-iteration protocol is what keeps state and
  context clean.
