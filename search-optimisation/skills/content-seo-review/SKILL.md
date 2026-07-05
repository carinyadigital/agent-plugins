---
name: content-seo-review
description: >
  Use when reviewing content seed PRs for SEO — titles, meta descriptions,
  heading structure, keyword usage, and internal linking opportunities.
  Produces PR review comments. Do NOT use for technical site audits
  (technical-seo-audit) or drafting content (/content-marketing:draft-post).
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
argument-hint: "<pr-url or seed path>"
metadata:
  version: "0.1.0"
  owner: search-optimisation
  review_cadence: quarterly
  work_shape: review-and-gate
  output_class: decision-support
---

# Content SEO review

## When to use

Review content seed JSON or pasted draft content for on-page SEO before merge or publish.

## What this skill does not do

- Does not rewrite seed files — PR review comments only
- Does not run site-wide technical audit (`technical-seo-audit`)
- Does not draft content (`/content-marketing:draft-post`, `draft-recipe`)

## Preconditions

Read `${CLAUDE_PLUGIN_ROOT}/references/search-optimisation-conventions.md`.

- Seed paths resolved per target config or user input
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
- `/content-marketing:draft-post`, `draft-recipe` — optional authors of seeds under review
