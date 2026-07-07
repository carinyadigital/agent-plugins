# Prompt authoring for Ralph loops

Guidance for writing ad-hoc loop prompts (`/ralph setup --prompt "..."`)
and for tuning the epic templates. The loop re-feeds the same prompt every
iteration — the prompt is the whole specification.

## Completion promises

- The promise is a statement of fact, not a command: the agent outputs
  `<promise>TEXT</promise>` only when TEXT is genuinely true.
- Make it specific and verifiable: `ALL_TESTS_PASS_COVERAGE_80` beats
  `DONE`.
- Matching is exact (single tag, whitespace normalised) — one promise per
  loop. You cannot encode multiple outcomes (`SUCCESS` vs `BLOCKED`) in the
  promise; rely on `max_iterations` and the stall guard for the failure
  paths.
- Epic loops default to `{EPIC}_COMPLETE` upper-snake-cased.

## Completion criteria

Vague goals give the loop nothing to verify against.

Bad: `Build a todo API and make it good.`

Good:

```
Build a REST API for todos.

When complete:
- All CRUD endpoints working
- Input validation in place
- Tests passing (coverage > 80%)
- README documents the API
Output: <promise>TODO_API_COMPLETE</promise>
```

## Self-correction

Include the verify-fix cycle in the prompt so failures become data:

```
Follow TDD: write failing tests, implement, run the suite.
If any test fails, debug and fix before adding anything new.
```

## Escape hatches

- Always set `--max-iterations` (ad-hoc default 20, epic default 50). An
  impossible task otherwise loops forever.
- Tell the loop what to do when stuck:

  ```
  If you are blocked or the same failure repeats for 3 iterations:
  document what is blocking and what you attempted, then stop making
  changes so the loop's stall guard ends the run.
  ```

- Epic loops get this for free: blockers are recorded in `loop-state.md`
  and the stall guard stops the loop when state stops changing.

## Phasing

Break large ad-hoc goals into ordered phases inside the one prompt —
`Phase 1: auth (tests green). Phase 2: catalogue. Phase 3: cart.` — and
require phases to be completed in order. For anything with real task
structure, prefer an epic loop: tasks.md + the step machine is exactly
this, with budgets and reviews built in.

## When a Ralph loop is the wrong tool

- Tasks needing human judgment or design decisions mid-flight — do the
  design first (design, tasks skills), then loop the delivery.
- One-shot operations — just do them.
- Unclear success criteria — the loop will either spin or lie; sharpen the
  criteria first.
