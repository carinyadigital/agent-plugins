# Technical SEO audit

## Before running

1. Confirm target: read `.carinyaparc/target.json`.
2. Default audit URL: `https://carinyaparc.com.au` (or `--url` override).
3. Read `apps/site/public/robots.txt` and sitemap config in repo.
4. Read Squad E charter for label conventions.

## Audit checklist

### Metadata (sample key pages)

- `/` homepage
- `/blog/` index
- `/blog/{sample-post}/`
- `/recipes/` index
- `/recipes/{sample-recipe}/`

For each page check:
- `<title>` unique and under ~60 chars
- `<meta name="description">` present, unique, under ~160 chars
- `<link rel="canonical">` correct
- Open Graph: `og:title`, `og:description`, `og:image`, `og:url`

### Sitemap and robots

- `robots.txt` allows indexing of public content
- Sitemap reachable and lists published posts/recipes
- No stale or 404 URLs in sitemap

### Structured data

- Recipe pages: Recipe schema with name, image, times, ingredients
- Blog posts: Article or BlogPosting where applicable
- Validate with Google Rich Results test approach (note errors in issues)

### Core Web Vitals (lab)

- Note LCP/CLS/INP concerns from playwright performance metrics if available
- Flag render-blocking or missing image dimensions as recommendations

## Output

Create GitHub issues via **github** connector. Priority order:

1. **P1** — indexing blockers, missing canonicals, broken sitemap
2. **P2** — missing OG tags, incomplete structured data
3. **P3** — CWV improvements, metadata polish

Also write a summary to `docs/work/seo/technical-seo-audit-{YYYY-MM-DD}.md` if
no issues were created (audit trail).

## Review criteria

- Each issue has evidence (URL, screenshot note, or HTML snippet)
- Owning squad label assigned
- Actionable fix description for engineering squads
