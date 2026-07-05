---
name: metrics-review
description: >
  Use when running a weekly, monthly, or quarterly metrics review, investigating
  a spike or drop, or comparing performance against targets. Do NOT use for
  stakeholder status updates (stakeholder-update) or product strategy (product).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<time period or metric focus>"
metadata:
  version: "0.1.0"
  owner: delivery-practice
  review_cadence: quarterly
  work_shape: monitor-and-report
  output_class: decision-support
---

# Metrics Review

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Pass the time period or metric focus after the skill name.
