# Review workflow

What a reviewer checks, in what order, and how the verdict is decided.
Self-contained: no assumption about tracker, doc layout, or provider.

## Gates (before line-level review)

Check these first; a failing gate may make a full review premature — say so
and stop rather than reviewing a moving target:

1. **CI** — required checks green? Reviewing on red wastes a round unless
   the failure is what the author asked about.
2. **Mergeable** — conflicts with the target branch are the author's to fix
   first.
3. **Size & cohesion** — one reviewable concern? Roughly 400+ changed lines
   across unrelated concerns → request a split instead of a shallow pass.
4. **Description** — does it say what changed, why, and how to verify? A
   diff without a why cannot be judged for scope; ask for the why, don't
   guess it.
5. **Draft state** — a draft gets directional feedback only, never a
   verdict.

## Line-level checklist

Judge the changed lines and what they touch — not the whole file's legacy:

- **Correctness** — does the code do what the description claims? Trace the
  main path and the failure paths. Null/empty/boundary inputs, off-by-one,
  error handling at each failure point, concurrency on shared state.
- **Tests** — do they cover the changed behaviour, including at least one
  failure path? Would they fail if the change were reverted? Weakened or
  deleted assertions are findings.
- **Security** — on any change touching input handling, auth, secrets,
  file paths, queries, or deserialisation: validate provenance before
  flagging; secrets never in code or logs.
- **Fit** — matches the surrounding patterns and naming; reuses existing
  helpers instead of re-inventing them; no new dependency where the standard
  library or an existing one serves.
- **Scope** — everything in the diff serves the stated intent; drive-by
  changes are called out (small and harmless → non-blocking note; risky →
  request a split).
- **Readability** — a future maintainer can follow it without the MR
  description in hand; comments explain why, not what.

Do **not** flag: anything a linter/typechecker/CI already catches,
pre-existing issues on untouched lines, style preferences with no codebase
convention behind them, or intentional decisions the description already
explains.

## Verdict rules

| Verdict | When |
| ------- | ---- |
| **Approve** | No blocking findings; required checks green; tests cover the change |
| **Approve with nits** | Only non-blocking findings — approve and trust the author to address them; do not hold the MR hostage to nits |
| **Request changes** | At least one blocking finding: a correctness/security defect, missing tests for changed behaviour, or undeclared scope |
| **Comment only** | You cannot responsibly judge (missing domain context, review premature per the gates) — say what you checked and what you could not |

The bar for **approve**: the codebase is better with this change than
without it — not perfection. Prefer approving with non-blocking comments
over another round for polish.

## Re-review rounds

On an MR you have reviewed before:

1. Diff **since your last review** (`git diff <last-reviewed-sha>...HEAD`,
   or the provider's compare view) — judge the delta, not the whole MR.
2. Walk **your open threads**: addressed as asked → resolve; partially →
   reply with exactly what is missing; author pushed back with a sound
   argument → concede and resolve; weak argument → one focused reply, then
   escalate to the user rather than a comment war.
3. New findings on lines you already passed are allowed only for something
   material you missed — own it ("I missed this last round") rather than
   presenting it as the author's regression.
4. Verdict per the same rules, considering only what is now true.
