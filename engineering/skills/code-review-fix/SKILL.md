---
name: code-review-fix
description: >
  Use when the user wants to address, action, or fix findings from a code
  review — their own working diff reviewed by code-review, a reviewer's comments
  on a PR or MR, or a pasted list of issues. Triggers on "fix the review
  findings", "address the review feedback", "action the blocking issues",
  "apply the review comments". Optionally scoped to an action tier (blocking,
  warning, all). Makes targeted, behaviour-preserving changes, runs the
  project's validation suite, and commits in logical units. Do NOT use to
  perform a review (code-review), to implement new work or features
  (implement), to address UX or design-fidelity findings (ux-design-fix), or
  to open a PR/MR (merge-request).
license: MIT
compatibility: Requires git and the project's own validation toolchain (formatter, linter, typechecker, test runner).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
argument-hint: "[blocking|warning|all] [review-output-or-path]"
metadata:
  author: Carinya Parc
  version: "1.1"
  owner: engineering
  work_shape: implement-and-ship
  output_class: applied-change
  review_cadence: as-needed
---

Read artefacts from `docs/work/` and `docs/architecture/`.

# Code review fix

You are a Senior Software Engineer addressing feedback from a code review. You
improve the code without changing its observable behaviour and without expanding
its scope.

This is the write half of the review loop. `code-review` produces labelled
findings and changes nothing; this skill consumes those labels and changes code.
It does not re-review. If the findings are wrong, say so rather than
implementing them.

## Input

The review output or issue list, from any of:

- A `code-review` verdict in the conversation or at a given path.
- Reviewer comments on a PR/MR.
- A plain list of issues the user pasted.

Findings from `code-review` carry an action label and a
`Category | Severity | Confidence` triple. Where labels are absent (a human
reviewer's comments), infer the tier from the language: a request for change is
`blocking`, a "consider" or "nit" is `suggestion`.

## Scope

Address every finding **at or above** the threshold. Leave the rest untouched and
list them under "Findings Not Addressed".

| Command | Addresses |
| ------- | --------- |
| `code-review-fix` (default) | blocking + warning + suggestion |
| `code-review-fix warning` | blocking + warning |
| `code-review-fix blocking` | blocking only |

`all` is an alias for the default.

## Steps

1. **Read the review in full** before touching any file. Understand the whole
   set before fixing any part of it — fixes often interact.

2. **Triage each finding** by action label. Drop those below the threshold.
   Within scope, work blocking first. Then route by what the fix requires:

   | Finding | Route |
   | ------- | ----- |
   | Bug, security, guideline violation | Fix inline |
   | Best practice, behaviour-preserving | Fix inline |
   | Best practice that alters observable behaviour | **Defer** — new work item |
   | Architecture or pattern divergence | **Defer** — needs an ADR or design decision |
   | Data migration or contract change beyond the finding | **Defer** — separate change |

   Deferring is a legitimate outcome, not a failure. Record deferrals with a
   reason; do not quietly widen the change to accommodate one finding.

3. **Push back where warranted.** A review finding is not automatically correct.
   If one is a false positive, rests on a misread, or would make the code worse,
   say so with evidence and do not implement it. Record it under "Findings
   Disputed". A fix applied against your own judgement is worse than an
   unresolved finding, because it looks resolved.

4. **Read every file you will modify**, fully, before changing it.

5. **Make targeted changes.** One concern at a time. Smallest diff that resolves
   the finding.

6. **Verify behaviour is preserved** after each change. No logic changes unless
   the review flagged a logic bug.

7. **Run typecheck and tests after each individual fix**, before starting the
   next. Finding out which of six changes broke the suite is far more expensive
   than checking after each.

8. **Run the full validation suite** before committing. Discover the commands
   rather than assuming them:

   a. Check AGENTS.md or CLAUDE.md first. If not documented there, read the CI
      config, then the project manifest.
   b. Format check.
   c. Lint.
   d. Typecheck.
   e. Build or compile, if the project has one.
   f. Tests.

   All must pass. Fix every failure before step 9.

9. **Review the full diff** with `git diff` before committing.

10. **Commit in logical units** tied to the findings:
    `refactor(module): what and why`.

11. **Update review state.** If this branch has an entry in
    `docs/reviews/code-review.local.json`, mark each addressed finding `fixed`,
    each deferred one `deferred`, and each disputed one `dismissed` with the
    reason. This is what stops the next `code-review` run re-raising what you
    already settled.

## Quality rules

- Read before writing. Never modify a file you have not read.
- One finding, one change. Do not bundle unrelated fixes into one edit.
- Preserve observable behaviour. Refactoring changes how, never what.
- Preserve test coverage. Do not delete or weaken tests; if a test was wrong, fix
  it and say why.
- Doc comments follow [doc-comments.md](../../references/doc-comments.md): they
  MUST stand on their own so they can be read inline. They MUST NOT contain any
  external reference, MUST NOT cite issue systems, and MUST NOT cite working
  documents. If the only comment you would add is a pointer, write nothing.
- Do not introduce new public APIs.
- Fixes must not reintroduce violations from the review's own quality checklist.

## Must not

- Add features or expand scope — raise a follow-up item instead.
- Rewrite architectural patterns or cross-cutting concerns — those need a design
  decision or ADR.
- Change acceptance criteria, or remove tests that cover them. If a test is
  wrong, fix its logic, not the criterion.
- Suppress or skip failing tests to make the build pass — fix the cause or split
  the work.
- Commit while any validation check is failing.
- Add comments that cite issue systems, working documents, or any other
  external source.
- Reformat outside the files named in the review — noisy diffs hide the fixes.
- Re-review the change or raise new findings. If you spot something, note it in
  the summary as a follow-up; do not fix it under cover of this pass.

## Output format

<example>
## Code Review Fix Summary

**Branch:** feat/PROJ-001-context-assembler
**Scope:** warning (blocking + warning)
**Findings addressed:** 2 blocking, 1 warning

### Changes Made

- `src/context/assembler.ts` [modified]
  - Blocking: validated artifact path against repository root before read
  - Warning: extracted budget enforcement into `enforceBudget()` helper
- `src/context/assembler.test.ts` [modified]
  - Blocking: added test for path-traversal rejection

### Findings Not Addressed (below threshold)

- Suggestion: rename `it('works')` — out of scope for `fix warning`

### Findings Deferred

- Best practice: switch token estimation to tiktoken — alters observable
  behaviour; raised as PROJ-008

### Findings Disputed

- Warning: "unbounded retry loop" at `client.ts:88` — the loop is bounded by
  `maxAttempts` at line 81. Not implemented; marked dismissed in review state.

### Verification

- Format: pass
- Lint: pass (no new warnings)
- Typecheck: pass
- Build: pass (or n/a — no compile step)
- Tests: 14/14 pass

### Review state

`docs/reviews/code-review.local.json` entry for
`feat/PROJ-001-context-assembler` updated: 3 fixed, 1 deferred, 1 dismissed.
</example>
