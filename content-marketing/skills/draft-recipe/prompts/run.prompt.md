# Draft recipe seed

## Before running

1. Resolve brand per [../../references/content-conventions.md](../../references/content-conventions.md).
2. Read calendar brief for this slug if present.
3. Read `apps/site/src/collections/Recipes.ts` and `src/fields/recipeIngredient.ts`.
4. Check existing seeds — do not duplicate slugs.

## Task

Write `apps/site/content/seeds/recipes/{slug}.json`.

### Content guidelines

- Seasonal ingredients where possible (check `brand/seasonal-calendar.md`)
- Dexter beef and farm produce when on-brand; honest about establishing phase
- Clear, testable steps — a home cook should succeed
- Australian English; metric quantities preferred

## Output

Example shape:

```json
{
  "slug": "winter-root-vegetable-stew",
  "title": "Winter Root Vegetable Stew",
  "date": "2026-07-20",
  "author": "jonno",
  "difficulty": "easy",
  "servings": 4,
  "prepTime": "PT15M",
  "cookTime": "PT45M",
  "totalTime": "PT60M",
  "excerpt": "Hearty winter stew using seasonal root vegetables.",
  "description": "A warming stew recipe featuring seasonal root vegetables from the farm.",
  "image": "/images/recipes/winter-stew.jpg",
  "tags": ["dinner", "vegetables", "winter"],
  "ingredients": [{ "item": "500 g mixed root vegetables, diced" }],
  "instructions": [{ "step": "Heat olive oil in a heavy pot over medium heat." }]
}
```

## Review criteria

- Valid JSON; all required fields present
- ISO 8601 durations valid
- Structured data complete for Recipe schema.org
- Brand voice: warm, practical, not overclaiming farm output
