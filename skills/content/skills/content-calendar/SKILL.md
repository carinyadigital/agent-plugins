---
name: content-calendar
description: >
  Use when planning or reviewing the editorial content calendar — monthly themes,
  post/recipe cadence, and briefs per slot. Reads seasonal calendar from carinyaparc
  brand. Do NOT use for drafting individual posts (draft-post) or social curation
  (curate-content).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: write|review> [--month YYYY-MM]"
---

# Content calendar

Monthly editorial plan for blog posts and recipes. Output lives on the **carinyaparc**
instance repo, not the target website repo.

## Brand resolution

Read [../../references/brand-resolution.md](../../references/brand-resolution.md).
Load `brand/seasonal-calendar.md` and `brand/taxonomy.md` before planning.

## Artefacts

| Mode | Default path |
| ---- | ------------ |
| `write`, `review` | `docs/product/content-calendar.md` (carinyaparc instance) |

Path may be overridden in `config/targets/{target}.json` or Squad D charter.

## Router

1. Mode: `write` or `review`.
2. Resolve month from `--month YYYY-MM` (default: current month).
3. [prompts/write.prompt.md](prompts/write.prompt.md) | [prompts/review.prompt.md](prompts/review.prompt.md).

## Related skills

- `draft-post`, `draft-recipe` — execute calendar slots
- `curate-content` — social inventory alignment
- `keyword-research` — SEO input from Squad E
