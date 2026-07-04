---
name: code-review
description: >
  Use when the user wants a code review of a branch, PR, or diff against
  design.md and tasks.md acceptance criteria, or to address review feedback
  without changing behaviour (code-review fix). Do NOT use to implement
  (implement) or epic completion sign-off (validate).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Shell
argument-hint: "[fix] [branch-or-pr-or-review-output]"
metadata:
  version: "0.1.0"
  owner: digital-agency
  review_cadence: quarterly
  work_shape: review-and-gate
  output_class: decision-support
---

# Code review

## When to use

Review a branch, PR, or diff against design and tasks AC; or address findings from a
prior review (`fix` mode).

## What this skill does not do

- Does not implement new features (`implement`) except targeted fix mode
- Does not open PRs (`create-mr`)
- Does not sign off epic completion (`validate`)

## Preconditions

- `docs/work/{epic}/design.md` and `tasks.md` in workspace
- Branch, PR, or diff specified (default: `git diff`)

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Accountability gap | Blocking vs non-blocking findings in verdict |
| DoD bypass | Does not mark epic or task complete |
| Blast radius | Fix mode addresses stated findings only |

## Workflow

1. Mode: default **review**, or `fix`.
2. **review** — [prompts/run.prompt.md](prompts/run.prompt.md).
3. **fix** — [prompts/fix.prompt.md](prompts/fix.prompt.md).

For large diffs, spawn sub-agents in parallel:

| Agent | File | Focus |
| ----- | ---- | ----- |
| tasks-ac-reviewer | [agents/tasks-ac-reviewer.md](agents/tasks-ac-reviewer.md) | Gherkin in tasks.md vs diff |
| design-drift-reviewer | [agents/design-drift-reviewer.md](agents/design-drift-reviewer.md) | Scope vs design.md |

Conventions: [../references/delivery-conventions.md](../references/delivery-conventions.md).

## Outputs

Structured review verdict with blocking and non-blocking findings mapped to AC.
Fix mode: targeted code changes addressing prior review output.
