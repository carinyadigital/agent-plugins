---
name: draft-recipe
description: >
  Use when drafting a recipe seed JSON for Payload import. Output at
  website/apps/site/content/seeds/recipes/{slug}.json. Include structured-data
  fields (times, servings, difficulty). Do NOT merge or publish — seed PR only.
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

# Draft recipe

## When to use

Draft a recipe seed JSON when a calendar brief or user request specifies a recipe slug
and topic.

## What this skill does not do

- Does not plan the monthly calendar (`content-calendar`)
- Does not merge, publish, or run `import-content-seed.ts`
- Does not audit site-wide structured data (`technical-seo-audit`)

## Preconditions

- Website target repo with `apps/site/src/collections/Recipes.ts`
- Read [../../references/brand-resolution.md](../../references/brand-resolution.md)
- Run `brand-voice` **enforce** on excerpt and instruction steps

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Direct apply vs draft | Seed JSON in PR only; human merges then imports as Payload draft |
| Brand safety | brand-voice enforce on recipe copy |
| Blast radius | Writes only under `apps/site/content/seeds/recipes/` |
| DoD bypass | Does not mark recipe live |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

## Outputs

`apps/site/content/seeds/recipes/{slug}.json` on the **website** target repo.

Schema derived from `apps/site/src/collections/Recipes.ts`:

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
