---
name: write-captions
description: >
  Use when writing Instagram caption variants and channel copy from media tags or analysis
  output. Reads brand from carinyaparc instance config. Do NOT use for
  selecting the final caption (edit-content) or vision analysis (analyse-media).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<tags json or media context>"
metadata:
  version: "0.1.0"
  owner: digital-agency
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Write captions

## When to use

Generate three distinct Instagram caption variants plus channel copy from media tags or
analyse-media output.

## What this skill does not do

- Does not select the final caption (`edit-content`)
- Does not analyse images (`analyse-media`)
- Does not schedule or publish posts

## Preconditions

- Read [../../references/brand-resolution.md](../../references/brand-resolution.md)
- Tags JSON or media context provided by caller

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Brand safety | First-person plural; cliché avoid list; no hashtags in body |
| Direct apply vs draft | Variants for editorial review — edit-content selects |
| DoD bypass | Three differentiated angles per prompt-refinement quality checks |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md). Pass tags JSON or media context after the skill name.

## Outputs

JSON with `caption_a` (storytelling), `caption_b` (short/visual, max 150 chars),
`caption_c` (educational), plus `google_post` and `email_excerpt` channel copy.

Quality checks from [../../references/prompt-refinement.md](../../references/prompt-refinement.md):
distinct opening words across variants; no embedded hashtags.
