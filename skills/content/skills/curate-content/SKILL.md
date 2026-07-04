---
name: curate-content
description: >
  Use when selecting the best assets to post next from an approved media inventory.
  Reads brand from carinyaparc instance config. Do NOT use for
  analysing single images (analyse-media) or writing captions (write-captions).
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
argument-hint: "<inventory json> [--date YYYY-MM-DD]"
---

# Curate content

Rank assets from inventory for upcoming posts. Generalized from steward curator-agent.

## Brand resolution

Read [../../references/brand-resolution.md](../../references/brand-resolution.md).

## Router

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Pass inventory JSON; optional `--date` for curation date (default today).
