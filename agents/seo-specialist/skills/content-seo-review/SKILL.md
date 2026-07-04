---
name: content-seo-review
description: >
  Use when reviewing content seed PRs for SEO — titles, meta descriptions,
  heading structure, keyword usage, and internal linking opportunities.
  Produces PR review comments. Do NOT use for technical site audits
  (technical-seo-audit) or drafting content (draft-post).
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
argument-hint: "<pr-url or seed path>"
---

# Content SEO review

Review blog post and recipe seed JSON for on-page SEO before merge.

## Scope

Review seeds at:

- `apps/site/content/seeds/posts/*.json`
- `apps/site/content/seeds/recipes/*.json`

## Router

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

## Related skills

- `keyword-research` — keyword targets to check against
- `draft-post`, `draft-recipe` — authors of seeds under review
