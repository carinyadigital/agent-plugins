---
name: curate-content
description: >
  Use when selecting the best assets to post next from an approved media inventory.
  Reads brand from instance repo config. Do NOT use for
  analysing single images (analyse-media) or writing captions (write-captions).
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
argument-hint: "<inventory json> [--date YYYY-MM-DD]"
metadata:
  version: "0.1.0"
  owner: content-marketing
  review_cadence: quarterly
  work_shape: orchestrate-delivery
  output_class: decision-support
---

# Curate content

## When to use

Rank assets from an approved inventory for upcoming social posts.

## What this skill does not do

- Does not analyse a single image (`analyse-media`)
- Does not write captions (`write-captions`)
- Does not schedule or publish to Instagram

## Preconditions

- Inventory JSON with approved assets and tags
- Read [../../references/content-conventions.md](../../references/content-conventions.md)
- Optional `--date` for curation date (default today)

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Accountability gap | Ranked selection with per-asset rationale |
| Brand safety | Seasonal and voice alignment in rationale |
| Scope boundaries | Selection only — captioning is downstream |

## Workflow

Follow [prompts/run.prompt.md](prompts/run.prompt.md). Pass inventory JSON; optional `--date`.

## Outputs

Ranked asset selection with rationale per pick, diversity and seasonal alignment noted.
