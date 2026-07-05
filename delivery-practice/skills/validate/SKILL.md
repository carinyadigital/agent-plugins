---
name: validate
description: >
  Use when the user wants final epic completion sign-off: every task in
  docs/work/{epic}/tasks.md verified against Gherkin AC and roadmap phase exit
  criteria. Pass epic slug or ID. Do NOT use for PR or branch code review
  (code-review), writing tasks (tasks), or sprint retrospective (sprint). Not
  for drafting backlog or design.
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
argument-hint: "<epic-slug|epic-id>"
metadata:
  version: "0.1.0"
  owner: delivery-practice
  review_cadence: quarterly
  work_shape: review-and-gate
  output_class: decision-support
---

# Validate

## Conventions

Read [../../references/delivery-conventions.md](../../references/delivery-conventions.md)
when resolving `{epic}`.

## Sub-agents

When the epic has many tasks (roughly >5) or complex Gherkin, spawn **ac-evidence-verifier**
([agents/ac-evidence-verifier.md](agents/ac-evidence-verifier.md)) to build the acceptance
matrix before writing the report and updating tasks.md.

For skill changes in this repo, add `evals/evals.json` and run `python3 scripts/validate.py`. See [agency-hub/references/agency-skill-design-framework.md](../../../agency-hub/references/agency-skill-design-framework.md) for design conventions.

## Gotchas

- **Code review ≠ validate** — review judges the diff; validate judges epic done-ness vs AC.
- **Resolve slug from backlog** when user passes only an Epic ID.
- **Update tasks.md status** only with evidence; do not invent new AC.
- **Epic status in backlog** updates only when all tasks for the epic are verified.

Follow [prompts/run.prompt.md](prompts/run.prompt.md).
