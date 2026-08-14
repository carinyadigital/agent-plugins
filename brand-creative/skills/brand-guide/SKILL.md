---
name: brand-guide
description: >
  Use when the user wants a visual brand guide — colors, typography, logo usage,
  imagery, and   UI tokens — at `<brand-dir>/brand-guide.md` (write, review, refine). Resolve
  `<brand-dir>` per brand-conventions.md. Do NOT use for voice, tone, or copy (brand-voice), product strategy (product),
  or component implementation (implement).
license: Apache-2.0
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: write|review|refine> [--from figma|docs|context] [--context <notes>]"
---

# Brand guide

Visual identity guide for agents building UI, slides, or formatted artefacts.

## Conventions

Read [../../references/brand-conventions.md](../../references/brand-conventions.md) when
checking artefact boundaries or resolving paths.

## Artefact

Default path: `<brand-dir>/brand-guide.md` — colors, typography, logo, imagery,
spacing, and UI tokens. Resolve `<brand-dir>` per
[../../references/brand-conventions.md](../../references/brand-conventions.md).

## Path resolution

If the user names a different file path in their request, read and write that
path instead of the default.

## Gotchas

- **No voice or messaging** — tone, terminology, and copy rules belong in
  `brand-voice.md`.
- **No component code** — cite tokens; **implement** owns code.
- **Delete DRAFTING AIDE** block before saving.
- **Figma is source of truth** when connected — extract tokens; do not invent
  hex values without evidence.

## Supporting files

- [assets/brand-guide.template.md](assets/brand-guide.template.md)

## Related skills

- `brand-voice` — voice, tone, and messaging

## Router

1. Mode: `write`, `review`, or `refine`.
2. Resolve target path (default or user override).
3. One prompt under [prompts/](prompts/).

**write** — [prompts/write.prompt.md](prompts/write.prompt.md).

**review** — [prompts/review.prompt.md](prompts/review.prompt.md).

**refine** — [prompts/refine.prompt.md](prompts/refine.prompt.md).
