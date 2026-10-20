---
name: technical-seo-audit
description: >
  Audit production SEO — metadata, canonical/OG, sitemap, robots, structured
  data, indexing, and Core Web Vitals signals. Use when auditing a live site or filing
  SEO recommendations. Files recommendations to the profile's tracker (GitHub issues
  labelled `type:seo-recommendation` by default, or Linear triage). Do NOT implement
  fixes — hand to engineering squads.
license: Apache-2.0
allowed-tools: Read Write Glob Grep Bash
argument-hint: "[--url base-url] [--focus metadata|sitemap|structured-data|cwv]"
metadata:
  author: Carinya Digital
  version: "0.2.0"
  owner: search-optimisation
  review_cadence: quarterly
  work_shape: monitor-and-report
  output_class: tracking-update
---

# Technical SEO audit

You audit the production site and file prioritised recommendations to the
recommendation tracker named in the practice profile. Pass optional `--url` and `--focus` after the skill name. Do not open
PRs or edit application code.

Read [search-optimisation-conventions.md](../../references/search-optimisation-conventions.md)
and [search-data-sources.md](../../references/search-data-sources.md).

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
3. Audit via browser automation (live) and repo files per the checklist below.
4. When reachable, read Search Console (Pages/indexing, Sitemaps, Core Web Vitals,
   Enhancements) and the SEO-tool site audit. Compare with the previous run when
   `docs/work/seo/agency-state.json` or an earlier audit file exists.
5. Group findings by root cause, search the tracker for open matches, then file new
   items priority-ordered per the conventions' **Recommendation tracker** rules.
6. If no items were created, write an audit trail to
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

### Indexing (Search Console, when reachable)

- Pages "not indexed" by reason; flag new reasons and sudden jumps
- Submitted sitemap status and discovered URL count
- Rich-result errors under Enhancements

### Core Web Vitals (lab)

- Note LCP/CLS/INP concerns from Playwright performance metrics when available
- Flag render-blocking or missing image dimensions as recommendations

## Issue format

| Priority | Examples |
| -------- | -------- |
| P1 | Indexing blockers, missing canonicals, broken sitemap |
| P2 | Missing OG tags, incomplete structured data |
| P3 | CWV improvements, metadata polish |

Each item:

- **Title:** `[SEO] {short description}`
- **Labels / state:** per the conventions' tracker table (recommendation label,
  owner label, triage state)
- **Body:** evidence, impact, recommended fix, page URL

## Quality rules

- Each item has evidence (URL, screenshot note, or HTML snippet)
- Owner label assigned per conventions; no duplicates of open items
- Actionable fix description for engineering — implementation is out of scope
