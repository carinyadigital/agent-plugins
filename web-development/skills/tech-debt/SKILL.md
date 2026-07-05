---
name: tech-debt
description: >
  Use when identifying, categorizing, and prioritizing technical debt — "tech
  debt audit", "what should we refactor", "code health", or refactoring
  priorities. Do NOT use for code review (code-review), architecture decisions
  (adr), or bug investigation (debug).
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
argument-hint: "[scope or area]"
---

# Tech debt

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Pass scope (service, module, epic) after the skill name when the user provides one.
