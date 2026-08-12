# Ralph loop cancel

Stop an active loop. The run directory is archived, never deleted: it is the
record of what happened.

## Steps

1. Resolve the base directory from the agent (`.claude/loop` or
   `.cursor/loop`) and check `{base}/active.md`.
2. **If it does not exist:** report "No active Ralph loop found." and stop.
3. **If it exists:**
   - Read `iteration`, `run_id`, and, where a `state_file` is declared,
     `current_item` and `current_step`, so the report says where the loop was
     when it stopped.
   - Remove the active loop file and its transient flags:

     ```bash
     rm -f {base}/active.md {base}/done {base}/stall
     ```

   - Archive the run directory:

     ```bash
     mkdir -p {base}/archive && mv {base}/{run_id} {base}/archive/{run_id}
     ```

   - Append a line under `## Notes` in the archived `loop-state.md` recording
     that the run was cancelled by the user, at which iteration, and on which
     step.

## Timing

Cancelling takes effect when the current turn ends and the stop hook next
fires. It does not interrupt a turn already in flight. If a sub-agent is
running it will finish; the loop simply will not be fed again.

## Output

One short confirmation:

"Cancelled at iteration 7 (was on CHK01-03 / review_fix). Run archived to
.claude/loop/archive/checkout-foundation-20260719-101500/."

Or the no-active-loop message.
