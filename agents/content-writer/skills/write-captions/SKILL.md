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
---

# Write captions

Generate three distinct Instagram caption variants plus channel copy. Generalized from
steward caption-agent.

## Brand resolution

Read [../../references/brand-resolution.md](../../references/brand-resolution.md).

## Router

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Pass tags JSON or media context after the skill name.
