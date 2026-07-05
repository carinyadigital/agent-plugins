---
name: draft-recipe
description: >
  Use when drafting a recipe seed JSON for CMS import. Output at the target repo's
  resolved recipe seed path. Include structured-data fields (times, servings,
  difficulty). Match brand-voice.md before finishing. Do NOT merge or publish — seed PR only.
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

# Draft recipe

## When to use

Draft a recipe seed JSON when a calendar brief or user request specifies a recipe slug
and topic.

## What this skill does not do

- Does not plan the monthly calendar (`content-calendar`)
- Does not merge, publish, or run `import-content-seed.ts`
- Does not audit site-wide structured data (`technical-seo-audit`)

## Preconditions

- Target repo with CMS recipe collection schema (read collection config before drafting)
- Read [../../references/content-conventions.md](../../references/content-conventions.md)
- Read `<resolved-brand-path>/brand-voice.md` and match tone on excerpt and instruction steps

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Direct apply vs draft | Seed JSON in PR only; human merges then imports as CMS draft |
| Brand safety | Reads brand-voice.md from resolved brand path; inline tone ask if missing |
| Blast radius | Writes only under resolved recipe seed directory |
| DoD bypass | Does not mark recipe live |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

## Outputs

`{recipe-seed-dir}/{slug}.json` on the target repo (resolve per content-conventions).

Schema derived from the target CMS recipe collection config:

| Field | Type | Required |
| ----- | ---- | -------- |
| `slug` | string | yes |
| `title` | string | yes |
| `date` | ISO date | yes |
| `author` | author slug | yes |
| `difficulty` | `easy` \| `medium` \| `hard` | no |
| `servings` | number | no |
| `prepTime` | ISO 8601 duration | no, e.g. `PT20M` |
| `cookTime` | ISO 8601 duration | no |
| `totalTime` | ISO 8601 duration | no |
| `excerpt` | string, max 500 | yes |
| `description` | string, max 300 | no |
| `image` | public path | no |
| `tags` | tag slug array | no |
| `ingredients` | `[{ "item": "..." }]` | yes, min 1 |
| `instructions` | `[{ "step": "..." }]` | yes, min 1 |

Structured data: valid ISO 8601 durations; `totalTime` equals prep + cook when both set;
ingredients as full lines in `item`.

## Related skills

- `content-seo-review` — SEO review on seed PR
- `keyword-research` — target keywords for recipe SEO
