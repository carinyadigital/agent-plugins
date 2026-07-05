---
name: docs
description: >
  Use for pre-sprint documentation alignment (review) or sprint-end epic
  documentation pass (refine) — product, solution, and docs/work/{epic}/design.md.
  Produces refine-session.md on refine. Do NOT use for sprint retrospective
  (sprint retrospective), epic validation against AC (validate), writing backlog
  (backlog), or initial architecture (solution write). Not a substitute for code
  review (code-review).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: review|refine> <epic> [--context <notes>]"
metadata:
  version: "0.1.0"
  owner: web-development
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Docs

## Conventions

Read [../../references/web-development-conventions.md](../../references/web-development-conventions.md)
when resolving `{epic}`.

Pre-sprint and sprint-end passes on product, solution, and epic design.

## Default paths

| Artefact | Default |
| -------- | ------- |
| Product | `docs/product/product.md` |
| Solution | `docs/architecture/solution.md` |
| ADR register | `docs/architecture/decisions/register.md` |
| Epic design | `docs/work/{epic}/design.md` |
| Refine session | `docs/work/{epic}/refine-session.md` |

## Gotchas

- **Sprint retro** is `sprint retrospective`, not docs refine.
- **Task AC** stays in `tasks.md` — refine does not rewrite Gherkin.
- **ADR candidates** from design triage go to register via **adr**, not inline in solution.

## Supporting files

- [assets/refine-session.template.md](assets/refine-session.template.md)

## Router

1. Mode: `review` or `refine`.
2. Resolve `{epic}` from argument or backlog.
3. One prompt under [prompts/](prompts/).
