---
name: technical-seo-audit
description: >
  Audit production SEO — metadata, canonical/OG, sitemap, robots, structured
  data, and Core Web Vitals signals. Use when auditing a live site or filing SEO
  recommendations. Creates GitHub issues labelled `type:seo-recommendation` with
  owning squad. Do NOT implement fixes — hand to engineering squads.
license: Apache-2.0
allowed-tools: Read Write Glob Grep Bash
argument-hint: "[--url base-url] [--focus metadata|sitemap|structured-data|cwv]"
metadata:
  author: Carinya Parc
  version: "0.1.0"
  owner: search-optimisation
  review_cadence: quarterly
  work_shape: monitor-and-report
  output_class: tracking-update
---

# Technical SEO audit

You audit the production site and file prioritised recommendations as GitHub
issues. Pass optional `--url` and `--focus` after the skill name. Do not open
PRs or edit application code.

Read [search-optimisation-conventions.md](../../references/search-optimisation-conventions.md).

## Inputs

| Input          | Location                                      | Required   |
| -------------- | --------------------------------------------- | ---------- |
| Audit URL      | Target production URL or `--url`              | Yes        |
| Focus area     | `--focus` or full audit                       | No         |
| robots/sitemap | Public paths + repo config                    | If present |
| Squad labels   | Instance squad charter                        | If present |

## Steps

1. Resolve target via `config/target.json` or instance config. Default URL from
   target production URL (or `--url`).
2. Read public `robots.txt` and sitemap config in repo when available. Read squad
   charter for label conventions when present.
3. Audit via Playwright (live) and repo files per the checklist below.
4. Create GitHub issues via the github connector, priority-ordered.
5. If no issues were created, write an audit trail to
   `docs/work/seo/technical-seo-audit-{YYYY-MM-DD}.md`.

## Checklist

### Metadata (sample key pages)

Homepage, primary index pages, and sample detail pages per content type:

- `<title>` unique and under ~60 chars
- `<meta name="description">` present, unique, under ~160 chars
- `<link rel="canonical">` correct
- Open Graph: `og:title`, `og:description`, `og:image`, `og:url`

### Sitemap and robots

- `robots.txt` allows indexing of public content
- Sitemap reachable and lists published content
- No stale or 404 URLs in sitemap

### Structured data

- Content-type pages use appropriate schema (Article, Product, Recipe, etc.)
- Note rich-results errors in issues

### Core Web Vitals (lab)

- Note LCP/CLS/INP concerns from Playwright performance metrics when available
- Flag render-blocking or missing image dimensions as recommendations

## Issue format

| Priority | Examples |
| -------- | -------- |
| P1 | Indexing blockers, missing canonicals, broken sitemap |
| P2 | Missing OG tags, incomplete structured data |
| P3 | CWV improvements, metadata polish |

Each issue:

- **Title:** `[SEO] {short description}`
- **Labels:** `type:seo-recommendation`, owning squad label per conventions
- **Body:** evidence, impact, recommended fix, page URL

## Quality rules

- Each issue has evidence (URL, screenshot note, or HTML snippet)
- Owning squad label assigned per conventions
- Actionable fix description for engineering — implementation is out of scope
