---
name: implement
description: >
  Use when the user wants to implement a task in code against approved
  design.md and .agency/work/{epic}/tasks.md. Do NOT use for code review (code-review),
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
---

# Implement

Implements a task with approved requirements and design, against `design.md`
and `tasks.md`.

Follow [prompts/implement.prompt.md](prompts/implement.prompt.md).

Pass task id and context after the skill name (e.g. `/implement CHK01-01`).
