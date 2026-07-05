---
name: edit-content
description: >
  Use when reviewing caption variants and selecting or lightly editing the best one for
  publication. Reads brand voice from instance repo config. Does not append hashtags.
  Do NOT use for initial caption generation (write-captions).
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
argument-hint: "<caption variants json>"
metadata:
  version: "0.1.0"
  owner: content-marketing
  review_cadence: quarterly
  work_shape: review-and-gate
  output_class: decision-support
---

# Edit content

## When to use

Editorial review — select the strongest caption variant or produce a light edit from
write-captions output.

## What this skill does not do

- Does not generate caption variants from scratch (`write-captions`)
- Does not append hashtags
- Does not publish to Instagram

## Preconditions

- Caption variants JSON from `write-captions`
- Read [../../references/content-conventions.md](../../references/content-conventions.md)

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Accountability gap | Selection includes editorial rationale |
| Brand safety | Voice check against brand-voice avoid list |
| DoD bypass | Does not treat selection as published — pipeline continues |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md). Pass caption variants JSON after the skill name.

## Outputs

JSON with selected caption, rationale, and optional light edits. No hashtag appending.
