---
name: deploy-qa
description: >
  Use when preparing a QA workspace — checkout a branch or MR ref, install
  dependencies, and verify the environment is ready for test execution. Do NOT
  use for running tests (run-automated-suite), exploratory validation
  (exploratory-pass), or fixing code (implement).
license: MIT
allowed-tools:
  - Read
  - Shell
  - Glob
  - Grep
argument-hint: "<branch-name-or-mr-url>"
---

# Deploy QA

Prepare an isolated QA workspace for validation. Maps to the first step of the
**delivery-qa** crew flow.

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Pass branch name or MR/PR URL after the skill name.
