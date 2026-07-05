---
name: final-code-review
description: >
  Use when the user wants a final technical gate on an open PR or MR after
  peer review — architecture boundaries, security, and acceptance-criteria
  coverage against docs/work/{epic}/tasks.md. Do NOT use for pre-PR peer
  review (code-review), business stakeholder sign-off (validate), or
  implementation (implement).
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
  - Shell
argument-hint: "[branch-or-pr-or-mr-url]"
---

# Final code review

Post-MR final gate: architecture, security, and technical AC coverage. The MR
is open and CI is expected green. This is not defect-finding peer review —
that happens before the MR opens.

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Pass branch, PR, or MR URL after the skill name.
