# Ralph cancel

Stop an active Ralph loop. The run directory is kept as a record; only the
active loop file and its flags are removed.

## Steps

1. Check `.ralph/loop.md`.
2. **If it does not exist:** report "No active Ralph loop found." and stop.
3. **If it exists:**
   - Read the current `iteration` and, if a `state_file` is declared, the
     `current_task` / `current_step` so the report says where the loop was.
   - Remove the active loop artefacts only:

     ```bash
     rm -f .ralph/loop.md .ralph/done .ralph/stall
     ```

   - Keep `.ralph/{work-id}/` directories — they are the run record
     (context, state, review outputs) and are what `/ralph setup` reuses
     if the loop is re-seeded later.

## Output

One short confirmation: "Cancelled Ralph loop at iteration N (was on
CHK01-03 / review_fix). Run record kept at .ralph/checkout-foundation/." —
or the no-active-loop message.
