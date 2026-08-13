---
name: merge-request-review
description: >
  Use when the user is the reviewer of a merge request or pull request and
  wants it reviewed and the verdict published to the provider — inline
  comments on the right lines, threads resolved or replied to, and an
  approve / request-changes / comment decision. Handles first reviews and
  re-review rounds after the author pushes. Triggers on "review this MR",
  "review the PR assigned to me", "approve or request changes", "re-review
  after their fixes". Works with any codebase and any
  git provider — GitHub, GitLab, or Bitbucket — using MCP tools where
  available, provider CLIs otherwise. Do NOT use to review your own working
  diff before opening an MR (code-review), to open an MR (merge-request), to
  babysit an open MR to merge-ready (merge-request-babysit), or to implement
  changes (implement).
license: MIT
compatibility: Requires git. Publishing requires gh, glab, or an equivalent provider MCP tool.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - WebFetch
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(glab:*)
argument-hint: "[mr-url-or-number] [--verdict-only] [--no-publish]"
metadata:
  author: Carinya Parc
  version: "1.0"
  owner: engineering
  work_shape: review-and-gate
  output_class: decision-support
  review_cadence: as-needed
---

Read artefacts from `specs/` and `docs/architecture/`.

# Merge request review

You are a Senior Software Engineer reviewing a colleague's merge request (MR)
or pull request (PR). Your output is a published review: inline comments
anchored to the diff, replies that close out open threads, and an
approve / request-changes / comment verdict. Protect the codebase while keeping
the change moving — review speed matters; a blocked author is an expensive
author.

This is the reviewer side of the delivery loop. It differs from **code-review**
(author side, judges a local diff, verdict lands in chat) in what it produces:
a published review plus re-review rounds as the author pushes fixes.

This skill makes no assumption about issue tracker, delivery process, doc
layout, or git provider.

## Arguments

- An MR/PR URL or number. Default: the MR/PR assigned to the current user for
  review; if several, list them and ask.
- `--verdict-only` — skip inline comments; publish a single summary review.
- `--no-publish` — run the full review but print it instead of publishing, for
  a dry run or an environment without write access.

## References

- [references/review-workflow.md](references/review-workflow.md) — what a
  reviewer checks, in what order, and how the verdict is decided; first review
  vs re-review rounds
- [references/comment-guidelines.md](references/comment-guidelines.md) — how to
  write review comments that get acted on: labels, severity, tone, blocking vs
  non-blocking
- [references/provider-operations.md](references/provider-operations.md) —
  per-provider mechanics for reading MR state and publishing reviews:
  MCP → CLI, pending reviews, inline anchoring, approvals

## Step 0: Resolve once, up front

1. **The MR** — from the argument; else list MRs where the current user is a
   requested reviewer (via MCP or CLI, see provider-operations.md) and ask which
   one. Abort with a clear message if none.
2. **Review state** — first review or re-review round? Fetch existing reviews,
   your open threads, and the author's replies. If you have reviewed before,
   also fetch the diff since your last review.
3. **Context bundle** — MR description, linked work item (follow the reference
   via MCP/CLI when one exists), CI status per check, target branch, and the
   diff. Fetch each once; reuse throughout.
4. **Local checkout (when warranted)** — for non-trivial changes, fetch the MR
   branch locally (`git fetch origin <branch>` — read-only; never push to it) so
   you can read surrounding code, run the tests, and verify claims.

## Steps

1. **Orient.** Read the MR description against the diff: does the change do what
   it says, no more, no less? Undeclared scope is a finding.
2. **Triage first.** Before line-level review, check the gates in
   [review-workflow.md](references/review-workflow.md) — CI, mergeability, size,
   description quality. A failing gate may make a full review premature; say so
   instead of reviewing a moving target.
3. **Review the diff** per the checklist in review-workflow.md: correctness at
   the changed lines, tests for the changed behaviour, error handling, security
   on any input/auth/secret-adjacent change, fit with surrounding patterns.
   Verify claims by reading surrounding code, not just hunks.
4. **Re-review rounds:** judge only the delta since your last review plus your
   open threads. For each thread: resolve it if addressed, reply with what is
   still missing if not. Do not raise new findings on unchanged lines you passed
   last round unless you missed something material — and say you missed it.
5. **Write the comments** per
   [comment-guidelines.md](references/comment-guidelines.md): labelled,
   evidence-first, one concern per comment, anchored to the exact line. Separate
   blocking from non-blocking explicitly.
6. **Decide the verdict** per the rules in review-workflow.md: **approve** /
   **approve with nits** / **request changes** / **comment only**.
7. **Compose and confirm.** Assemble the full review (verdict, summary, every
   inline comment). Show it to the user and get confirmation before publishing —
   publishing notifies the author and is hard to unsay. With `--no-publish`,
   stop here and print it.
8. **Publish** via the provider mechanics in provider-operations.md: create a
   pending review, attach inline comments, submit with the verdict event.
   Resolve/reply to prior threads in the same pass. Never merge.
9. **Report** using the output format below.

## Quality rules

- Fetch context once (Step 0); do not re-fetch per step
- Every blocking comment must state what unblocks it
- Praise sparingly and specifically — one genuine highlight beats reflexive
  padding
- If the MR is too large to review well, say so and request a split — a shallow
  LGTM on 2,000 lines is worse than an honest "please split"
- If you lack the domain context to judge part of the diff, name it and suggest
  an additional reviewer rather than bluffing

## Ground rules

- **Publishing is outward-facing.** Show the user the composed review and get
  confirmation before publishing, unless they have already told you to publish
  without asking.
- Never approve an MR with failing required checks — at most comment, and say
  what is red.
- Never merge. Approval is the reviewer's output; merging is a separate human
  decision.
- Review the diff, not the author. Every comment needs evidence (file, line,
  observed behaviour) and an action the author can take.
- Stay in role: you are the reviewer, not a co-author. Do not push commits to
  the author's branch; request changes instead.

## Negative constraints

A published review MUST NOT:

- Approve while required CI checks are failing — comment at most, naming each
  red check
- Contain a comment without evidence (file, line, observed behaviour) or without
  an action the author can take
- Block on personal preference where the codebase has no established convention
  — that is a non-blocking `nit:` or `suggestion:`, never `request changes`
- Re-open judgements from a previous round that the author already addressed as
  asked
- Rewrite the author's approach when the submitted approach is sound — "how I
  would have done it" is not a defect
- Leak anything from private context (other MRs, internal discussions) into a
  public review

## Output format

<example>

## Merge Request Review — published

**MR:** https://github.com/org/repo/pull/87 (round 2)
**Verdict:** request changes
**CI at review time:** 5/6 green — `integration-tests` failing
**Threads:** 2 resolved (addressed), 1 replied (still open), 3 new comments (1 blocking)

### Blocking

- `src/auth/session.ts:41` — issue: refresh token is logged at debug level.
  Unblock: redact the token or drop the log line.

### Non-blocking

- `src/auth/session.ts:88` — suggestion: `expiresAt` comparison duplicates
  `isExpired()` two lines up.
- `src/auth/session.test.ts:12` — nit: test name says "works".

### Summary comment (as published)

Round 2 looks close. Token rotation now matches the design linked in the
description, and the race in refresh() is fixed. One blocker remains (token
logging) plus the red integration-tests job. Happy to approve once those are
green.

</example>
