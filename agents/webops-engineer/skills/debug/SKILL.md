---
name: debug
description: >
  Use when investigating bugs, errors, or unexpected behavior — reproduce,
  isolate, diagnose, and fix. Trigger with an error message, stack trace,
  "works in staging but not prod", or "broke after deploy". Do NOT use for
  incident response workflows, code review (code-review), or implementation
  (implement).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Shell
argument-hint: "<error message or problem description>"
---

# Debug

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Pass the error message, stack trace, or problem description after the skill name.
