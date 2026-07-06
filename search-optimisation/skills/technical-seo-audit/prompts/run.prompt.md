# Technical SEO audit

## Before running

1. Read `${CLAUDE_PLUGIN_ROOT}/references/search-optimisation-conventions.md`.
2. Resolve target via `.agency/target.json` or instance target config.
3. Default audit URL: production URL from target config (or `--url` override).
4. Read public `robots.txt` and sitemap config in repo when available.
5. Read squad charter for label conventions when present in the instance repo.

## Audit checklist

### Metadata (sample key pages)

Audit representative pages for the site structure — typically:

- Homepage
- Primary index pages (blog, products, recipes, etc.)
- Sample detail pages per content type

For each page check:

- `<title>` unique and under ~60 chars
- `<meta name="description">` present, unique, under ~160 chars
- `<link rel="canonical">` correct
- Open Graph: `og:title`, `og:description`, `og:image`, `og:url`

### Sitemap and robots

- `robots.txt` allows indexing of public content
- Sitemap reachable and lists published content
- No stale or 404 URLs in sitemap

### Structured data

- Content-type pages: appropriate schema (Article, Product, Recipe, etc.)
- Validate with rich-results test approach (note errors in issues)

### Core Web Vitals (lab)

- Note LCP/CLS/INP concerns from playwright performance metrics if available
- Flag render-blocking or missing image dimensions as recommendations

## Output

Create GitHub issues via **github** connector. Priority order:

1. **P1** — indexing blockers, missing canonicals, broken sitemap
2. **P2** — missing OG tags, incomplete structured data
3. **P3** — CWV improvements, metadata polish

Also write a summary to `.agency/work/seo/technical-seo-audit-{YYYY-MM-DD}.md` if
no issues were created (audit trail).

## Review criteria

- Each issue has evidence (URL, screenshot note, or HTML snippet)
- Owning squad label assigned per conventions
- Actionable fix description for engineering squads
