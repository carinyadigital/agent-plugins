# Ralph loop status

Report the state of the loop without changing anything. Read-only: do not
modify any file under the loop base directory.

## Steps

1. Resolve the base directory from the agent (`.claude/loop` or
   `.cursor/loop`) and read `{base}/active.md`. If missing, report "No active
   Ralph loop." then list run directories under `{base}/` and
   `{base}/archive/` as history.
2. From the frontmatter: `iteration`, `max_iterations`, `completion_promise`,
   `state_file`, `preset`, `run_id`, `session_id`, `seeded_at`.
3. If a `state_file` is declared, read it for `current_step`, `current_item`,
   `completed_items`, `fix_count`, and anything under `## Notes`.
4. List artefacts in the run directory (`review-*.md`, `ux-review-*.md`) with a
   one-line verdict each. Read only the result line.
5. Check `{base}/stall`. If present, report the consecutive-unchanged count;
   the loop stops at 3.
6. Flag anything close to firing: iteration near `max_iterations`, a stall
   count of 2, an exhausted fix budget, or notes recording a blocker.

## Output

<example>
## Ralph loop status

**Run:** checkout-foundation-20260719-101500 (engineering-delivery)
**Progress:** iteration 7 of 70
**Promise:** CHECKOUT_FOUNDATION_COMPLETE
**Current:** CHK01-03 — review_fix (fix 2 of 3)
**Completed:** CHK01-01, CHK01-02 (2 of 5)
**Stall guard:** state changed last iteration (1 of 3)

### Reviews
- review-CHK01-01.md — PASS
- review-CHK01-02.md — PASS after 1 fix cycle
- review-CHK01-03.md — 2 blocking findings

### Notes
(from loop-state.md, verbatim)
</example>

Where nothing is wrong, keep it to the block above. Do not add advice unless a
rail is close to firing.
