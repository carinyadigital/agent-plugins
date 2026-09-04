---
name: tdd
description: >
  Alias for `design`. Use when the user says "tdd CHK01", "/tdd", or names
  this skill explicitly. Writes {work-dir}/design.md (a work-item Solution
  Design). Triggers on "tdd CHK01", "tdd JIRA-123". Do NOT use for
  test-driven development (implement), breakdown/Gherkin (tasks), system
  architecture (solution), or Ready for Development review (discovery-review).
license: Apache-2.0
compatibility: Tracker resolution uses Linear, Atlassian (Jira), or GitHub/GitLab MCP tools when available, or `git remote`/`gh`/`glab`; falls back to the filesystem when none are reachable.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git remote:*)
  - Bash(gh:*)
  - Bash(glab:*)
argument-hint: "<work-id> [--mode skeleton|full] [--context <notes>]"
metadata:
  author: Carinya Parc
  version: "6.0"
  owner: engineering
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

# tdd (alias)

This skill is an alias for **design**. Follow
[../design/SKILL.md](../design/SKILL.md) immediately with the same arguments.
Do not duplicate that procedure here.

Not test-driven development — that is **implement**.
