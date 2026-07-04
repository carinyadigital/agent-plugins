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
---

# Analyse media

Structured vision analysis for content pipelines. Generalized from steward vision-agent.

## Brand resolution

Read [../../references/brand-resolution.md](../../references/brand-resolution.md), then load
brand files from `carinyaparc/brand/` per `config/instance.json`.

See [../../references/prompt-refinement.md](../../references/prompt-refinement.md) for quality checks.

## Output

JSON with: subjects, season, moods, contentType, altText, description, qualityScore,
publishable, publishNotes (if not publishable).

## Router

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Pass image path or media reference after the skill name.
