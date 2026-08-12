---
name: tech-debt
description: >
  Identify, categorize, and prioritize technical debt. Use for "tech debt
  audit", "what should we refactor", "code health", or refactoring priorities.
  Do NOT use for code review (code-review), architecture decisions (adr), or bug
  investigation (debug).
license: MIT
allowed-tools: Read Glob Grep
argument-hint: "[scope or area]"
metadata:
  author: Carinya Parc
  version: "0.1.0"
  owner: product-engineering
  review_cadence: quarterly
  work_shape: review-and-gate
  output_class: decision-support
---

# Tech debt

Systematically identify, categorize, and prioritize technical debt. Pass scope
(service, module, epic) after the skill name when provided; otherwise scan the
area the user describes.

## Categories

| Type | Examples | Risk |
| ---- | -------- | ---- |
| **Code debt** | Duplicated logic, poor abstractions, magic numbers | Bugs, slow development |
| **Architecture debt** | Monolith that should be split, wrong data store | Scaling limits |
| **Test debt** | Low coverage, flaky tests, missing integration tests | Regressions ship |
| **Dependency debt** | Outdated libraries, unmaintained dependencies | Security vulns |
| **Documentation debt** | Missing runbooks, outdated READMEs, tribal knowledge | Onboarding pain |
| **Infrastructure debt** | Manual deploys, no monitoring, no IaC | Incidents, slow recovery |

## Prioritization

Score each item:

- **Impact** (1–5) — how much it slows the team
- **Risk** (1–5) — cost of not fixing
- **Effort** (1–5) — lower effort → higher priority

Priority = (Impact + Risk) × (6 − Effort)

## Steps

1. Confirm scope (repo area, service, or epic) or default to the user's described area.
2. Scan for debt across the categories above.
3. Score and rank items.
4. Produce a prioritized list with estimated effort, business justification, and a
   phased remediation plan that can run alongside feature work.

## Output format

Prioritized markdown list with: item, category, scores, justification, and suggested
phase for remediation.
