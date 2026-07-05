---
name: draft-post
description: >
  Use when drafting a blog post seed JSON for CMS import. Output at the target repo's
  resolved post seed path with body as markdown. Match brand-voice.md before finishing.
  Do NOT merge or publish — seed PR only.
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<slug> [--brief from calendar]"
metadata:
  version: "0.1.0"
  owner: content-marketing
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Draft post

## When to use

Draft a blog post seed JSON for the CMS import pipeline when a calendar brief or user
request specifies a post slug and topic.

## What this skill does not do

- Does not plan the monthly calendar (`content-calendar`)
- Does not merge, publish, or run `import-content-seed.ts`
- Does not perform SEO review (`content-seo-review` runs on the seed PR)

## Preconditions

- Target repo with CMS post collection schema (read collection config before drafting)
- Read [../../references/content-conventions.md](../../references/content-conventions.md)
- Read `<resolved-brand-path>/brand-voice.md` and match tone on excerpt and body before finishing

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Direct apply vs draft | Seed JSON in PR only; human merges then imports as CMS draft |
| Brand safety | Reads brand-voice.md from resolved brand path; inline tone ask if missing |
| Blast radius | Writes only under resolved post seed directory |
| DoD bypass | Does not mark content published |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

## Outputs

`{post-seed-dir}/{slug}.json` on the target repo (resolve per content-conventions).

Schema derived from the target CMS post collection config:

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
