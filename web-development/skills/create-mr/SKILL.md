---
name: create-mr
description: >
  Creates a merge request or pull request for the current branch with generated
  title, description, labels, and reviewer suggestions. Use after implementation.
  Do NOT use for code review (code-review) or task implementation (implement).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Shell
argument-hint: "[story-id]"
metadata:
  version: "0.1.0"
  owner: web-development
  review_cadence: quarterly
  work_shape: implement-and-ship
  output_class: tracking-update
---

# Create MR

## When to use

Open a pull request or merge request after implementation on the current branch.

## What this skill does not do

- Does not implement code (`implement`)
- Does not review code (`code-review`)
- Does not merge the PR

## Preconditions

- Implementation branch with committed changes
- Task id or story id for PR description

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Blast radius | Opens PR only — does not merge or deploy |
| DoD bypass | Description links task id and epic — not merge-ready sign-off |
| Accountability gap | Suggested reviewers — human approves merge |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

## Outputs

Pull request with title, description referencing task id and epic path, suggested labels
and reviewers.
