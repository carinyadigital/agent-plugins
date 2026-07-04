---
name: analyse-media
description: >
  Use when analysing farm or property media — image or video — for structured tags:
  subjects, season, mood, content type, alt text, description, quality score. Reads brand
  and taxonomy from carinyaparc instance config. Do NOT use for writing captions (write-captions)
  or selecting posts (curate-content).
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
argument-hint: "<image path or media reference>"
metadata:
  version: "0.1.0"
  owner: digital-agency
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
- Does not publish to Instagram

## Preconditions

- Read [../../references/brand-resolution.md](../../references/brand-resolution.md)
- Load brand files from `carinyaparc/brand/` per `config/instance.json`
- See [../../references/prompt-refinement.md](../../references/prompt-refinement.md) for quality checks

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Brand safety | NSW seasonal context; honest establishing-phase descriptions |
| DoD bypass | qualityScore rubric and publishable criteria per prompt-refinement |
| Blast radius | Read-only — structured JSON output, no repo writes |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md). Pass image path or media reference after the skill name.

## Outputs

JSON with: `subjects`, `season`, `moods`, `contentType`, `altText`, `description`,
`qualityScore`, `publishable`, `publishNotes` (if not publishable).

Quality assertions sourced from [../../references/prompt-refinement.md](../../references/prompt-refinement.md):
specific subjects, NSW season cues, specific alt text, score 0.0–1.0.
