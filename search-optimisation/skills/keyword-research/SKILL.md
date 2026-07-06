---
name: keyword-research
description: >
  Use when researching keywords for a topic area — search intent, volume signals,
  and content opportunities. Output at .agency/work/seo/keyword-research-{topic}.md on
  the target repo. Do NOT use for technical site audits (technical-seo-audit) or
  competitive product analysis (/delivery-practice:competitive-brief).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<topic-slug>"
metadata:
  version: "0.1.0"
  owner: search-optimisation
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Keyword research

## When to use

Research keywords for a topic and document findings for content calendar planning.

## What this skill does not do

- Does not audit technical SEO (`technical-seo-audit`)
- Does not draft content seeds (`/content-marketing:draft-post`, `draft-recipe`)
- Does not open GitHub issues
- Does not produce a full competitive brief (`/delivery-practice:competitive-brief`)

## Preconditions

Read `${CLAUDE_PLUGIN_ROOT}/references/search-optimisation-conventions.md`.

- Target repo in workspace
- Topic slug in kebab-case for filename

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Direct apply vs draft | Research doc for human review before calendar slots |
| Blast radius | Writes only under resolved SEO work directory |
| Scope boundaries | Keyword research only — not competitive landscape brief |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md). Topic slug becomes the filename segment.

## Outputs

`.agency/work/seo/keyword-research-{topic}.md` on the **target** repo (or override path per conventions).

## Related skills

- `/content-marketing:content-calendar` — consumes keyword targets for slot briefs
- `/content-marketing:draft-post`, `draft-recipe` — apply keywords in seeds
- `/delivery-practice:competitive-brief` — broader competitive landscape (companion)
