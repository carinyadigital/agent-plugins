---
name: edit-content
description: >
  Use when reviewing caption variants and selecting or lightly editing the best one for
  publication. Reads brand voice from carinyaparc instance config. Does not append hashtags.
  Do NOT use for initial caption generation (write-captions).
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
argument-hint: "<caption variants json>"
---

# Edit content

Editorial review — select strongest caption variant or produce a light edit. Generalized
from steward editor-agent.

## Brand resolution

Read [../../references/brand-resolution.md](../../references/brand-resolution.md).

## Router

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

Pass caption variants JSON after the skill name.
