---
name: implement
description: >
  Use when the user wants to implement a task in code against approved
  design.md and docs/work/{epic}/tasks.md. Do NOT use for code review (code-review),
  address review feedback (code-review fix), writing tasks (tasks), or design
  (design write).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Shell
argument-hint: "<task-id>"
metadata:
  version: "0.1.0"
  owner: digital-agency
  review_cadence: quarterly
  work_shape: implement-and-ship
  output_class: applied-change
---

# Implement

## When to use

Implement a committed task with approved `design.md` and Gherkin AC in `tasks.md`.

## What this skill does not do

- Does not write tasks or design (`tasks`, `design`)
- Does not open PRs (`create-mr`)
- Does not review code (`code-review`)
- Does not sign off epic completion (`validate`)

## Preconditions

- `docs/work/{epic}/design.md` approved
- Task row in `docs/work/{epic}/tasks.md` with Gherkin AC
- Pass task id after skill name (e.g. `/web-development:implement CHK01-01`)
- Before UI work: read `<resolved-brand-path>/brand-guide.md` per
  `${CLAUDE_PLUGIN_ROOT}/references/web-development-conventions.md`; ask inline if missing

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Blast radius | Scope limited to task AC and design.md files-shipped list |
| DoD bypass | Does not mark task done in tasks.md — validate or human gate |
| Escalation | Halts when design or AC missing or ambiguous |

## Workflow

Follow [prompts/implement.prompt.md](prompts/implement.prompt.md).

## Outputs

Code changes on branch implementing the task AC. Branch ready for `create-mr` and `code-review`.
