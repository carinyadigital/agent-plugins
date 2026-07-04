# Write content calendar

## Before running

1. Resolve brand per [../../references/brand-resolution.md](../../references/brand-resolution.md).
2. Load `brand/seasonal-calendar.md`, `brand/taxonomy.md`, and `brand/brand-voice.md`.
3. Check for existing `docs/product/content-calendar.md` on the carinyaparc instance.
4. Read any open keyword research in `website/docs/work/seo/` if available.

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

Write to `docs/product/content-calendar.md` on the carinyaparc instance repo.
Do not publish Payload content — calendar is planning only.

## Review criteria

- Themes align with `seasonal-calendar.md` for the month
- Cadence is realistic (typically 2 posts + 1 recipe per month for Squad D)
- Briefs are actionable for `content-writer` without further clarification
- No duplicate slugs against existing seeds or published content
