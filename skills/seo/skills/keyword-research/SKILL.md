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
---

# Keyword research

Research keywords for a topic and document findings for Squad D calendar planning.

## Artefact

`docs/work/seo/keyword-research-{topic}.md` on the **website** target repo.

## Router

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Topic slug becomes the filename segment (kebab-case).

## Related skills

- `content-calendar` — consumes keyword targets for slot briefs
- `draft-post`, `draft-recipe` — apply keywords in seeds
- `competitive-brief` — broader competitive landscape
