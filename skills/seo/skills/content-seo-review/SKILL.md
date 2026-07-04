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
metadata:
  version: "0.1.0"
  owner: digital-agency
  review_cadence: quarterly
  work_shape: review-and-gate
  output_class: decision-support
---

# Content SEO review

## When to use

Review blog post and recipe seed JSON for on-page SEO before merge.

## What this skill does not do

- Does not rewrite seed files — PR review comments only
- Does not run site-wide technical audit (`technical-seo-audit`)
- Does not draft content (`draft-post`, `draft-recipe`)

## Preconditions

- Seed paths under `apps/site/content/seeds/posts/` or `recipes/`
- Keyword targets from `keyword-research` when available

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Accountability gap | Review comments with blocking vs non-blocking SEO findings |
| DoD bypass | Does not approve merge — human merges after review |
| Blast radius | Read-only on seeds; comments on PR |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

## Outputs

PR review comments covering title, meta description, heading structure, keyword usage,
and internal linking opportunities.

## Related skills

- `keyword-research` — keyword targets to check against
- `draft-post`, `draft-recipe` — authors of seeds under review
