# Ralph status

Report the state of the Ralph loop without changing anything. Read-only:
do not modify any file under `.ralph/`.

## Steps

1. Read `.ralph/loop.md`. If missing, report "No active Ralph loop." — then
   check for past run directories under `.ralph/` and list them as history.
2. From the loop file frontmatter: `iteration`, `max_iterations`,
   `completion_promise`, `state_file`.
3. If a `state_file` is declared, read it for: `current_task`,
   `current_step`, `review_fix_count`, `ux_review_fix_count`,
   `final_review_count`, `completed_tasks`, and anything under `## Notes`.
4. List review artefacts in the run directory (`review-*.md`,
   `ux-review-*.md`) with a one-line verdict each (read only the Result
   line).
5. Check `.ralph/stall` — if present, report the consecutive-unchanged
   count (the loop stops at 3).

## Output

<example>
## Ralph loop status

**Loop:** checkout-foundation — iteration 7 of 50
**Promise:** CHECKOUT_FOUNDATION_COMPLETE
**Current:** CHK01-03 — review_fix (attempt 2 of 3)
**Completed:** CHK01-01, CHK01-02 (2 of 5 tasks)
**Stall guard:** state changed last iteration (count 1 of 3)

### Reviews
- review-CHK01-01.md — PASS
- review-CHK01-02.md — PASS after 1 fix cycle
- review-CHK01-03.md — FAIL (2 blocking)

### Notes
(from loop-state.md, if any)
</example>
