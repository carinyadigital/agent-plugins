---
name: adr
description: >
  Use when the user wants ADR register planning, writing ADR-NNNN files, or ADR
  review under docs/architecture/decisions/. Do NOT use for full architecture
  narrative (solution), epic design (design), or product strategy (product).
  Proposals stay in register.md only until accepted.
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: plan|write|review> [target] [flags]"
---

# ADR

## Paths

| Artefact | Default path |
| -------- | ------------ |
| Register | `docs/architecture/decisions/register.md` |
| ADR document | `docs/architecture/decisions/ADR-{NUMBER}-{short-title}.md` |

## Path resolution

If the user names a different directory or file path in their request, use it
for read/write instead of the defaults. Keep `ADR-####` numbering sequential
within the register the user targets.

## Supporting files

- [assets/register.template.md](assets/register.template.md)
- [assets/adr.template.md](assets/adr.template.md)

## Router

1. Mode: `plan`, `write`, or `review`.
2. Resolve paths (default or user override).
3. [prompts/plan.prompt.md](prompts/plan.prompt.md) | [prompts/write.prompt.md](prompts/write.prompt.md) | [prompts/review.prompt.md](prompts/review.prompt.md).
