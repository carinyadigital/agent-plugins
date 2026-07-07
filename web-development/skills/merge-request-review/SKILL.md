---
name: merge-request-review
description: >
  Use when the user is the reviewer of a merge request or pull request and
  wants it reviewed and the verdict published to the provider — inline
  comments on the right lines, threads resolved or replied to, and an
  approve / request-changes / comment decision. Handles first reviews and
  re-review rounds after the author pushes. Works with any codebase and any
  git provider — GitHub, GitLab, or Bitbucket — using MCP tools where
  available, provider CLIs otherwise. Do NOT use to review your own working
  diff before opening an MR (code-review), to open or babysit an MR
  (merge-request), or to implement changes (implement).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Shell
  - WebFetch
argument-hint: "[mr-url-or-number] [--verdict-only] [--no-publish]"
---

# Merge request review

Review an MR/PR as its reviewer and publish the outcome to the provider.

This is the reviewer side of the delivery loop. It differs from
**code-review** (author side, judges a local diff, verdict lands in chat) in
what it produces: a published review — inline comments anchored to diff
lines, thread replies, and a merge verdict — plus re-review rounds as the
author pushes fixes.

## Router

One mode, one prompt: [prompts/run.prompt.md](prompts/run.prompt.md).

- Argument: an MR/PR URL or number. Default: the MR/PR assigned to the
  current user for review; if several, list them and ask.
- `--verdict-only`: skip inline comments; publish a single summary review.
- `--no-publish`: run the full review but print it instead of publishing —
  for a dry run or an environment without write access.

## References

- [references/review-workflow.md](references/review-workflow.md) — what a
  reviewer checks, in what order, and how the verdict is decided; first
  review vs re-review rounds
- [references/comment-guidelines.md](references/comment-guidelines.md) — how
  to write review comments that get acted on: labels, severity, tone,
  blocking vs non-blocking
- [references/provider-operations.md](references/provider-operations.md) —
  per-provider mechanics for reading MR state and publishing reviews:
  MCP → CLI, pending reviews, inline anchoring, approvals

## Ground rules

- **Publishing is outward-facing.** Show the user the composed review
  (verdict + every comment) and get confirmation before publishing, unless
  they have already told you to publish without asking.
- Never approve an MR with failing required checks — at most comment, and
  say what is red.
- Never merge. Approval is the reviewer's output; merging is a separate
  human decision.
- Review the diff, not the author. Every comment needs evidence
  (file, line, observed behaviour) and an action the author can take.
- Do not re-litigate previous rounds: on re-review, judge what changed since
  your last review and the threads you opened — not the whole MR again.
- Stay in role: you are the reviewer, not a co-author. Do not push commits
  to the author's branch; request changes instead.
