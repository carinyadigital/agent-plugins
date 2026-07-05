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
metadata:
  version: "0.1.0"
  owner: search-optimisation
  review_cadence: quarterly
  work_shape: monitor-and-report
  output_class: tracking-update
---

# Technical SEO audit

## When to use

Audit the production site and file prioritized recommendations as GitHub issues.

## What this skill does not do

- Does not open PRs or edit code
- Does not publish content
- Does not replace keyword research (`keyword-research`)

## Preconditions

Read `${CLAUDE_PLUGIN_ROOT}/references/search-optimisation-conventions.md`.

- Playwright connector for live site checks
- Production URL from target config or `--url` override

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Blast radius | Issues only — implementation handed to engineering squads |
| DoD bypass | Each issue includes evidence and recommended fix |
| Brand safety | N/A — technical findings only |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Check via **playwright** connector and repo files:

| Area | Repo / live |
| ---- | ----------- |
| Title, meta description, canonical | Live pages |
| Open Graph / Twitter cards | Live pages |
| `robots.txt`, `sitemap.xml` | Public static paths + live |
| JSON-LD structured data | Live content pages |
| Core Web Vitals | Live (lab signals via playwright) |

## Outputs

GitHub issues per finding:

- **Title:** `[SEO] {short description}`
- **Labels:** `type:seo-recommendation`, owning squad label per conventions
- **Body:** evidence, impact, recommended fix, page URL
