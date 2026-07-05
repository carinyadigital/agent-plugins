---
name: run-automated-suite
description: >
  Use when running the project's automated test suite in a prepared QA
  workspace. Do NOT use for workspace setup (deploy-qa), manual AC checks
  (exploratory-pass), or fixing failures (implement).
license: MIT
allowed-tools:
  - Read
  - Shell
  - Glob
  - Grep
argument-hint: "[test-command override]"
---

# Run automated suite

Run configured automated tests from the QA workspace root. Maps to the
**delivery-qa** crew automated suite step.

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Optionally pass a test command override after the skill name.
