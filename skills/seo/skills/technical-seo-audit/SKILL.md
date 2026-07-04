---
name: technical-seo-audit
description: >
  Use when auditing production SEO — metadata, canonical/OG, sitemap, robots,
  structured data, and Core Web Vitals signals. Creates GitHub issues labelled
  type:seo-recommendation with owning squad. Do NOT implement fixes — hand to
  engineering squads.
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Shell
argument-hint: "[--url base-url] [--focus metadata|sitemap|structured-data|cwv]"
---

# Technical SEO audit

Audit the production site and file prioritized recommendations as GitHub issues.

## Scope

Check via **playwright** connector (live site) and repo files:

| Area | Repo / live |
| ---- | ----------- |
| Title, meta description, canonical | Live pages |
| Open Graph / Twitter cards | Live pages |
| `robots.txt`, `sitemap.xml` | `apps/site/public/` + live |
| JSON-LD structured data | Live recipe/post pages |
| Core Web Vitals | Live (lab signals via playwright where available) |

## Issue format

Each finding becomes a GitHub issue:

- **Title:** `[SEO] {short description}`
- **Labels:** `type:seo-recommendation`, `squad:{site|blog|recipes}` (owning squad)
- **Body:** evidence, impact, recommended fix, page URL

## Router

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Default production URL: `https://carinyaparc.com.au` (override with `--url`).

## Boundaries

- Do not open PRs or edit code
- Do not publish content
- Hand implementation to Squads A/B/C via issue labels
