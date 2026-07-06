---
name: solution
description: >
  Use when the user wants to write, review, or refine system architecture at
  .agency/architecture/solution.md (stub or full arc42-lite). Do NOT use for business
  strategy (product), delivery phases (roadmap), epic list (backlog), per-epic
  design.md (design), task Gherkin (tasks), or ADR files (adr write). Story AC
  belongs in .agency/work/{epic}/tasks.md.
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: write|review|refine> [--stage stub|full] [--context <notes>]"
---

# Solution

## Conventions

Read [../../references/web-development-conventions.md](../../references/web-development-conventions.md)
for artefact boundaries.

## Artefact

Default path: `.agency/architecture/solution.md` — arc42-lite architecture (stub or full).

## Path resolution

If the user names a different file path in their request, read and write that
path instead of the default.

## Stage (write mode)

| Stage | When | Sections |
| ----- | ---- | -------- |
| `stub` | Phase 0 | §1–§2 only; §3–11 scaffolded |
| `full` | Phase 2+ | All eleven sections |

## Gotchas

- **Per-epic files/APIs** → cite from `.agency/work/{epic}/design.md`, don't duplicate full specs.
- **Story-level Gherkin** → `tasks.md`, not solution.
- **Closed ADRs** → `ADR-NNNN-*.md`; proposals stay in register only.

## Supporting files

- [assets/solution.template.md](assets/solution.template.md)

## Related skills

- `product`, `backlog`, `tasks`, `design`, `adr`

## Router

1. Mode: `write`, `review`, or `refine`.
2. Resolve target path (default or user override).
3. One prompt under [prompts/](prompts/).

**write** — `--stage stub|full`.
