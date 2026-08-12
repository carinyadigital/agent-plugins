---
name: content-calendar
description: >
  Use when planning or reviewing the editorial content calendar — monthly themes,
  post/recipe cadence, and briefs per slot. Reads seasonal calendar from resolved brand
  path. Do NOT use for drafting individual posts (draft-post) or social curation
  (curate-content).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: write|review> [--month YYYY-MM]"
metadata:
  version: "0.1.0"
  owner: content-marketing
  review_cadence: quarterly
  work_shape: orchestrate-delivery
  output_class: draft-for-review
---

# Content calendar

## When to use

Plan or review the monthly editorial calendar for blog posts and recipes in the
instance or target repo.

## What this skill does not do

- Does not draft seed JSON (`draft-post`, `draft-recipe`)
- Does not curate Instagram inventory (`curate-content`)
- Does not publish content

## Preconditions

- Read [../../references/content-conventions.md](../../references/content-conventions.md)
- Load `brand/seasonal-calendar.md` and `brand/taxonomy.md` before planning
- Resolve month from `--month YYYY-MM` (default: current month)

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Accountability gap | Review mode produces explicit planning-ready verdict |
| Brand safety | Themes align with seasonal calendar and brand voice |
| Scope boundaries | Calendar briefs only — execution is draft-post/draft-recipe |
| Blast radius | Writes `docs/content/content-calendar.md` on instance repo |

## Workflow

1. Mode: `write` or `review`.
2. [prompts/write.prompt.md](prompts/write.prompt.md) | [prompts/review.prompt.md](prompts/review.prompt.md).

## Outputs

| Mode | Default path |
| ---- | ------------ |
| `write`, `review` | `docs/content/content-calendar.md` (instance repo) |

Path may be overridden in `config/targets/{target}.json` or user explicit path.

## Related skills

- `draft-post`, `draft-recipe` — execute calendar slots
- `curate-content` — social inventory alignment
- `keyword-research` — SEO input when search-optimisation practice is installed
