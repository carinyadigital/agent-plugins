---
name: analyse-media
description: >
  Use when analysing image or video media for structured tags: subjects, season, mood,
  content type, alt text, description, quality score. Reads brand and taxonomy from
  resolved brand path. Do NOT use for writing captions (write-captions) or selecting
  posts (curate-content).
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
argument-hint: "<image path or media reference>"
metadata:
  version: "0.1.0"
  owner: content-marketing
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: structured-data
---

# Analyse media

## When to use

Produce structured vision analysis for a single image or video in content pipelines.

## What this skill does not do

- Does not write captions (`write-captions`)
- Does not select posts from inventory (`curate-content`)
- Does not schedule or publish to social channels

## Preconditions

- Read [../../references/content-conventions.md](../../references/content-conventions.md)
- Load `brand-voice.md`, `taxonomy.md`, and `seasonal-calendar.md` from resolved brand path when present
- See [../../references/prompt-refinement.md](../../references/prompt-refinement.md) for quality checks

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Brand safety | Season cues from brand seasonal calendar or user-stated geography; honest tone |
| DoD bypass | qualityScore rubric and publishable criteria per prompt-refinement |
| Blast radius | Read-only — structured JSON output, no repo writes |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md). Pass image path or media reference after the skill name.

## Outputs

JSON with: `subjects`, `season`, `moods`, `contentType`, `altText`, `description`,
`qualityScore`, `publishable`, `publishNotes` (if not publishable).

Quality assertions sourced from [../../references/prompt-refinement.md](../../references/prompt-refinement.md):
specific subjects, season cues consistent with brand calendar, specific alt text, score 0.0–1.0.
