# Content SEO review

## Before running

1. Read `${CLAUDE_PLUGIN_ROOT}/references/search-optimisation-conventions.md`.
2. Load the seed JSON file(s) in the PR diff or path named by the user.
3. Read relevant `docs/work/seo/keyword-research-*.md` for target keywords.
4. Check slug uniqueness and URL structure against the target site's routing.

## Review checklist

### Posts and articles

- [ ] Title includes primary keyword naturally; under 60 chars ideal
- [ ] `description` or `excerpt` works as meta description (under 160 chars)
- [ ] Slug is short, kebab-case, keyword-relevant
- [ ] Body has logical H2 structure (maps to headings on import)
- [ ] Internal linking opportunities noted (suggest anchor text + target slug)
- [ ] Image path set; alt text guidance if hero image referenced in body

### Structured content types (recipes, products, etc.)

- [ ] Title and description optimised for search intent
- [ ] Structured data fields complete per content type
- [ ] Seasonal or topical keyword alignment where applicable

## Output

PR review comments grouped as:

- **Blocking** — must fix before merge (duplicate slug, missing description, keyword stuffing)
- **Suggestion** — optional improvements (internal links, heading tweaks)

Verdict: **approve**, **approve with suggestions**, or **request changes**.

## Review criteria

- Comments cite specific JSON fields or content sections
- Keyword usage reads naturally (no stuffing)
- Recommendations actionable by content authors without a full SEO re-run
