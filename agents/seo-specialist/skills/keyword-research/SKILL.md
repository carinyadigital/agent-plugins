---
name: keyword-research
description: >
  Use when researching keywords for a topic area — search intent, volume signals,
  and content opportunities. Output at website/docs/work/seo/keyword-research-{topic}.md.
  Do NOT use for technical site audits (technical-seo-audit) or competitive product
  analysis (competitive-brief).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<topic-slug>"
metadata:
  version: "0.1.0"
  owner: digital-agency
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Keyword research

## When to use

Research keywords for a topic and document findings for Squad D calendar planning.

## What this skill does not do

- Does not audit technical SEO (`technical-seo-audit`)
- Does not draft content seeds (`draft-post`, `draft-recipe`)
- Does not open GitHub issues

## Preconditions

- Website target repo in workspace
- Topic slug in kebab-case for filename

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Direct apply vs draft | Research doc for human review before calendar slots |
| Blast radius | Writes only under `docs/work/seo/` |
| Scope boundaries | Keyword research only — not competitive landscape brief |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md). Topic slug becomes the filename segment.

## Outputs

`docs/work/seo/keyword-research-{topic}.md` on the **website** target repo.

## Related skills

- `content-calendar` — consumes keyword targets for slot briefs
- `draft-post`, `draft-recipe` — apply keywords in seeds
- `competitive-brief` — broader competitive landscape
