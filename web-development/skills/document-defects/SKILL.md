---
name: document-defects
description: >
  Use when structuring reproducible defect reports from failed QA output —
  automated suite failures, exploratory gaps, or combined validation results.
  Do NOT use to fix code (implement) or re-run tests (run-automated-suite).
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
argument-hint: "<path-to-test-output-or-paste>"
metadata:
  version: "0.1.0"
  owner: web-development
  review_cadence: quarterly
  work_shape: monitor-and-report
  output_class: tracking-update
---

# Document defects

Structure defects from failed validation output. Maps to the **delivery-qa**
crew defect documentation step.

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Pass test output path or paste after the skill name.
