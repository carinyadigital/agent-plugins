---
name: stakeholder-update
description: >
  Use when writing a weekly or monthly status for leadership, announcing a
  launch, escalating a risk, or tailoring the same progress for exec, engineering,
  or customer audiences. Do NOT use for product strategy (product) or roadmap
  updates (roadmap).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<update type and audience>"
metadata:
  version: "0.1.0"
  owner: delivery-practice
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Stakeholder Update

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Pass the update type, audience, and cadence after the skill name.
