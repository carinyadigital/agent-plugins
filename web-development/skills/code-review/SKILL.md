---
name: code-review
description: >
  Use when the user wants a code review of a branch, PR, or diff against its
  acceptance criteria and declared scope (whatever form they take in this
  repo), or to address review feedback without changing behaviour
  (code-review fix, optionally scoped to a blocking or warning action tier).
  Works with any language, delivery process, or issue tracker. Do NOT use to
  implement code, sign off completion of a larger body of work, or review
  rendered UI/UX (design fidelity, accessibility — use ux-design-review).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Shell
  - WebFetch
argument-hint: "[fix [blocking|warning|all]] [branch-or-pr-or-review-output]"
---

# Code review

Review a branch, PR, or diff; or address findings from a prior review.

## Sub-agents

For large diffs or pre-PR review, spawn in parallel (Claude Code agents or Cursor Task):

| Agent | File | Focus |
| ----- | ---- | ----- |
| acceptance-criteria-reviewer | [agents/acceptance-criteria-reviewer.md](agents/acceptance-criteria-reviewer.md) | Linked acceptance criteria (any source/format) vs diff |
| design-drift-reviewer | [agents/design-drift-reviewer.md](agents/design-drift-reviewer.md) | Scope vs the discovered design/spec doc, if any |
| best-practices-reviewer | [agents/best-practices-reviewer.md](agents/best-practices-reviewer.md) | Latest library/framework docs vs diff |
| architecture-reviewer | [agents/architecture-reviewer.md](agents/architecture-reviewer.md) | Discovered architecture docs/ADRs/sibling patterns vs diff |
| bug-scan-reviewer | [agents/bug-scan-reviewer.md](agents/bug-scan-reviewer.md) | Shallow, changes-only bug + git-history scan |
| guideline-compliance-reviewer | [agents/guideline-compliance-reviewer.md](agents/guideline-compliance-reviewer.md) | AGENTS.md/CLAUDE.md/rules vs diff |

Spawn only the agents whose triggers fire — do not run all six on every diff:

| Condition | Spawn |
| --------- | ----- |
| Whenever spawning (default bug lens) | bug-scan-reviewer |
| Change has linked acceptance criteria and/or a discovered scope doc | acceptance-criteria-reviewer, design-drift-reviewer |
| Touches a framework/library | best-practices-reviewer |
| Adds modules or crosses boundaries | architecture-reviewer |
| Repo has AGENTS.md/CLAUDE.md/rules | guideline-compliance-reviewer |

Small diffs skip spawning and use the inline steps in [prompts/run.prompt.md](prompts/run.prompt.md).
Merge agent outputs into one verdict. Default review scope: `git diff` unless the user specifies files.
Gather change intent, requirements/scope, and CI status once up front (see
[references/context-resolution.md](references/context-resolution.md) and the
Context step in [prompts/run.prompt.md](prompts/run.prompt.md)) and share it
with every sub-agent — do not re-fetch per agent.

## References

- [references/context-resolution.md](references/context-resolution.md) — how to discover intent, acceptance criteria, scope, and CI signal in any repo/tracker
- [references/finding-classification.md](references/finding-classification.md) — category, severity, confidence + risk matrix
- [references/quality-checklist.md](references/quality-checklist.md) — timeless review checklist
- [references/security-checklist.md](references/security-checklist.md) — condensed security pass

## Router

1. Mode: default **review**, or `fix`.
2. One prompt under [prompts/](prompts/).

**review** (default) — [prompts/run.prompt.md](prompts/run.prompt.md).

**fix** — [prompts/fix.prompt.md](prompts/fix.prompt.md). Optional action-tier
threshold after `fix`: `blocking` (blocking only) or `warning` (blocking +
warning); default (or `all`) addresses all findings.

Pass branch, PR, diff, or review output after the mode token.
