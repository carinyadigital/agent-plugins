# Write content calendar

## Before running

1. Resolve brand per [../../../references/content-conventions.md](../../../references/content-conventions.md).
2. Load `brand/seasonal-calendar.md`, `brand/taxonomy.md`, and `brand/brand-voice.md` when present.
3. Read existing `docs/content/content-calendar.md` in the instance or target repo when present.
4. Read any open keyword research in target repo docs when available.

## Task

Produce or update the monthly content calendar for the requested month.

### Calendar structure

```markdown
# Content calendar — {Month YYYY}

## Monthly theme
{1–2 sentences tying seasonal events to brand narrative}

## Cadence
| Channel | Target |
| ------- | ------ |
| Blog posts | {n} |
| Recipes | {n} |

## Slots

| Week | Type | Slug (proposed) | Brief | Status |
| ---- | ---- | --------------- | ----- | ------ |
| W1 | post | ... | ... | planned |
| W2 | recipe | ... | ... | planned |
```

Each brief must include:
- Target audience and intent (inform, inspire, convert)
- Key message aligned with brand voice
- Suggested hero image subject or path
- Tags/category hints from taxonomy
- SEO keyword target when known

## Output

Write to `docs/content/content-calendar.md` in the instance or target repo (or path from
`config/targets/{target}.json`). Do not publish CMS
content — calendar is planning only.

## Review criteria

- Themes align with `seasonal-calendar.md` for the month when present
- Cadence is realistic for the team's stated rhythm
- Briefs are actionable for Content Writer skills without further clarification
- No duplicate slugs against existing seeds or published content
