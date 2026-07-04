---
name: draft-post
description: >
  Use when drafting a blog post seed JSON for Payload import. Output at
  website/apps/site/content/seeds/posts/{slug}.json with body as markdown.
  Run brand-voice enforce before finishing. Do NOT merge or publish — seed PR only.
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<slug> [--brief from calendar]"
metadata:
  version: "0.1.0"
  owner: digital-agency
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Draft post

## When to use

Draft a blog post seed JSON for the Payload import pipeline when a calendar brief or
user request specifies a post slug and topic.

## What this skill does not do

- Does not plan the monthly calendar (`content-calendar`)
- Does not merge, publish, or run `import-content-seed.ts`
- Does not perform SEO review (`content-seo-review` runs on the seed PR)

## Preconditions

- Website target repo with `apps/site/src/collections/Posts.ts`
- Read [../../references/brand-resolution.md](../../references/brand-resolution.md)
- Run `brand-voice` **enforce** on excerpt and body before finishing

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Direct apply vs draft | Seed JSON in PR only; human merges then imports as Payload draft |
| Brand safety | brand-voice enforce; reads `carinyaparc/brand/`, never `website/docs/brand/` |
| Blast radius | Writes only under `apps/site/content/seeds/posts/` |
| DoD bypass | Does not mark content published |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

## Outputs

`apps/site/content/seeds/posts/{slug}.json` on the **website** target repo.

Schema derived from `apps/site/src/collections/Posts.ts`:

| Field | Type | Required |
| ----- | ---- | -------- |
| `slug` | string | yes |
| `title` | string | yes, max 200 |
| `date` | ISO date `YYYY-MM-DD` | yes |
| `author` | author slug | yes |
| `category` | category slug | no |
| `tags` | tag slug array | no |
| `featured` | boolean | no, default false |
| `excerpt` | string, max 500 | yes |
| `description` | string, max 300 | no (SEO meta) |
| `image` | public path | no |
| `body` | markdown string | yes |

## Related skills

- `content-seo-review` — SEO review on seed PR
- `content-calendar` — slot briefs that feed drafts
