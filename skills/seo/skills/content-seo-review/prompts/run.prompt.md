# Content SEO review

## Before running

1. Load the seed JSON file(s) in the PR diff.
2. Read relevant `docs/work/seo/keyword-research-*.md` for target keywords.
3. Check slug uniqueness and URL structure (`/blog/{slug}/`, `/recipes/{slug}`).

## Review checklist

### Posts

- [ ] Title includes primary keyword naturally; under 60 chars ideal
- [ ] `description` or `excerpt` works as meta description (under 160 chars)
- [ ] Slug is short, kebab-case, keyword-relevant
- [ ] Body has logical H2 structure (maps to headings on import)
- [ ] Internal linking opportunities noted (suggest anchor text + target slug)
- [ ] Image path set; alt text guidance if hero image referenced in body

### Recipes

- [ ] Title and description optimised for recipe search intent
- [ ] Structured data fields complete (times, servings, ingredients, steps)
- [ ] Seasonal keyword alignment where applicable

## Output

PR review comments grouped as:

- **Blocking** — must fix before merge (duplicate slug, missing description, keyword stuffing)
- **Suggestion** — optional improvements (internal links, heading tweaks)

Verdict: **approve**, **approve with suggestions**, or **request changes**.

## Review criteria

- Comments cite specific JSON fields
- Keyword usage reads naturally (no stuffing)
- Recommendations actionable by content-marketing draft skills without SEO re-run
