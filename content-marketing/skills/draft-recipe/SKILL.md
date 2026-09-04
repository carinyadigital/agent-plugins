---
name: draft-recipe
description: >
  Draft a recipe seed JSON for CMS import at the target repo's resolved recipe
  seed path, with structured-data fields (times, servings, difficulty). Use when
  writing a recipe seed from a calendar brief or slug. Match brand-voice.md before
  finishing. Do NOT merge or publish — seed PR only. Do NOT plan the calendar
  (content-calendar) or audit site-wide structured data (technical-seo-audit).
license: Apache-2.0
allowed-tools: Read Write Glob Grep
argument-hint: "<slug> [--brief from calendar]"
metadata:
  author: Carinya Digital
  version: "0.1.0"
  owner: content-marketing
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Draft recipe

You draft a recipe seed JSON for the CMS import pipeline. Pass the recipe slug
after the skill name.

Read [content-conventions.md](../../references/content-conventions.md) to resolve
brand and seed paths. Read `<resolved-brand-path>/brand-voice.md` and match tone
on excerpt and instruction steps. Read the target CMS recipe collection config
before drafting.

## Inputs

| Input              | Location                                       | Required   |
| ------------------ | ---------------------------------------------- | ---------- |
| Slug / brief       | Argument or calendar brief                     | Yes        |
| Brand voice        | `<resolved-brand-path>/brand-voice.md`         | Yes        |
| Seasonal calendar  | `<resolved-brand-path>/seasonal-calendar.md`   | If present |
| CMS schema         | Target recipe collection + ingredient fields   | Yes        |
| Existing seeds     | Resolved recipe seed directory                 | Check dupes|

## Steps

1. Resolve brand and recipe seed directory per content-conventions.
2. Read the calendar brief for this slug if present.
3. Read the CMS recipe collection schema and ingredient field definitions.
4. Check existing seeds — do not duplicate slugs.
5. Write `{recipe-seed-dir}/{slug}.json` with the schema below.
6. Prefer seasonal ingredients from the seasonal calendar; use farm produce when
   on-brand and honest about establishing phase. Clear, testable steps; Australian
   English; metric quantities preferred.
7. Ensure ISO 8601 durations are valid; `totalTime` equals prep + cook when both set;
   ingredients as full lines in `item`.

## Schema

| Field           | Type                         | Required     |
| --------------- | ---------------------------- | ------------ |
| `slug`          | string                       | yes          |
| `title`         | string                       | yes          |
| `date`          | ISO date                     | yes          |
| `author`        | author slug                  | yes          |
| `difficulty`    | `easy` \| `medium` \| `hard` | no           |
| `servings`      | number                       | no           |
| `prepTime`      | ISO 8601 duration            | no, e.g. `PT20M` |
| `cookTime`      | ISO 8601 duration            | no           |
| `totalTime`     | ISO 8601 duration            | no           |
| `excerpt`       | string, max 500              | yes          |
| `description`   | string, max 300              | no           |
| `image`         | public path                  | no           |
| `tags`          | tag slug array               | no           |
| `ingredients`   | `[{ "item": "..." }]`        | yes, min 1   |
| `instructions`  | `[{ "step": "..." }]`        | yes, min 1   |

## Quality rules

- Valid JSON; all required fields present
- ISO 8601 durations valid; structured data complete for Recipe schema.org
- Brand voice: warm, practical, not overclaiming farm output
- Seed PR only — do not merge, publish, or run import scripts

## Output format

```json
{
  "slug": "winter-root-vegetable-stew",
  "title": "Winter Root Vegetable Stew",
  "date": "2026-07-20",
  "author": "author-slug",
  "difficulty": "easy",
  "servings": 4,
  "prepTime": "PT15M",
  "cookTime": "PT45M",
  "totalTime": "PT60M",
  "excerpt": "Hearty winter stew using seasonal root vegetables.",
  "description": "A warming stew recipe featuring seasonal root vegetables.",
  "image": "/images/recipes/winter-stew.jpg",
  "tags": ["dinner", "vegetables", "winter"],
  "ingredients": [{ "item": "500 g mixed root vegetables, diced" }],
  "instructions": [{ "step": "Heat olive oil in a heavy pot over medium heat." }]
}
```
