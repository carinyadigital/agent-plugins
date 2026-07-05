---
name: exploratory-pass
description: >
  Use when performing acceptance-criteria-driven exploratory validation in a
  prepared QA workspace — manual-style checks, browser verification, or CLI
  probes against tasks.md Gherkin. Do NOT use for automated tests only
  (run-automated-suite) or defect formatting (document-defects).
license: MIT
allowed-tools:
  - Read
  - Shell
  - Glob
  - Grep
argument-hint: "<epic-slug-or-branch>"
metadata:
  version: "0.1.0"
  owner: web-development
  review_cadence: quarterly
  work_shape: review-and-gate
  output_class: decision-support
---

# Exploratory pass

AC-driven exploratory validation in the QA workspace. Maps to the
**delivery-qa** crew exploratory step.

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Pass epic slug or branch after the skill name.
