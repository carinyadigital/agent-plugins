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
---

# Draft recipe

Create a recipe seed file for the Payload import pipeline.

## Brand resolution

Read [../../references/brand-resolution.md](../../references/brand-resolution.md).
Run `brand-voice` **enforce** on excerpt and instruction steps.

## Artefact

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

## Structured data requirements

- `prepTime`, `cookTime`, `totalTime` must be valid ISO 8601 durations when set
- `totalTime` should equal prep + cook when both provided
- Ingredients use full lines in `item` (quantity + ingredient)
- Instructions are numbered steps in separate array entries

## Router

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

## Related skills

- `content-seo-review` — SEO review on seed PR
- `keyword-research` — target keywords for recipe SEO
