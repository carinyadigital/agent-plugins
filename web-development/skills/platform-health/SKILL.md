---
name: platform-health
description: >
  Use when auditing platform health — dependency updates, uptime, error rates, CI status,
  and deployment hygiene. Trigger for "dependency audit", "check Sentry errors", "platform
  health review", or scheduled maintenance. Do NOT use for feature implementation (implement)
  or debugging a single bug (debug).
license: MIT
allowed-tools:
  - Read
  - Shell
  - Glob
  - Grep
argument-hint: "[--focus deps|errors|ci|uptime]"
metadata:
  version: "0.1.0"
  owner: web-development
  review_cadence: quarterly
  work_shape: monitor-and-report
  output_class: tracking-update
---

# Platform health

Dependency audit, error review, and deployment hygiene for webops workflows.

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Optional focus: `deps`, `errors`, `ci`, `uptime`.
