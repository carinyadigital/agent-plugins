# Draft post seed

## Before running

1. Resolve brand per [../../references/brand-resolution.md](../../references/brand-resolution.md).
2. Read the content calendar brief for this slug if present.
3. Read `apps/site/src/collections/Posts.ts` to confirm field constraints.
4. Check existing seeds and published slugs — do not duplicate.

## Task

Write `apps/site/content/seeds/posts/{slug}.json`.

### Body markdown

- Use `##` for section headings (maps to Lexical headings on import)
- Australian English spelling
- First person plural (we, our) per brand voice
- No JSX or MDX components — plain markdown only
- Target 600–1200 words unless brief specifies otherwise

### Relationships

Use slugs for `author`, `category`, and `tags`. Common author slug: `jonno`.
Create plausible category/tag slugs aligned with `brand/taxonomy.md`.

## Output

Single JSON file. Example shape:

```json
{
  "slug": "example-slug",
  "title": "Example Title",
  "date": "2026-07-15",
  "author": "jonno",
  "category": "farming",
  "tags": ["soil", "winter"],
  "featured": false,
  "excerpt": "Short teaser for cards and listings.",
  "description": "SEO meta description under 300 chars.",
  "image": "/images/example.jpg",
  "body": "## Opening\\n\\nParagraph text..."
}
```

## Review criteria

- Valid JSON matching schema
- Brand voice enforced (warm, grounded, honest about establishing phase)
- Excerpt stands alone; description optimised for search when provided
- Body converts cleanly to Lexical (no custom MDX)
