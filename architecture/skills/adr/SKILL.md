---
name: adr
description: >
  Use when the user wants ADR register planning, writing ADR-NNNN files, or ADR
  review under docs/architecture/decisions/. Triggers on "do we need an ADR",
  "write ADR-0007", "record this decision", "what decisions need making",
  "harvest ADRs from this epic", "harvest ADRs from JIRA-123". Do NOT use for
  full architecture narrative (solution), work-item Solution Design (design, alias tdd), or
  product strategy (product). Proposals stay in register.md only until
  accepted.
license: Apache-2.0
compatibility: Tracker resolution (plan mode, when a work-id is named) uses Linear, Atlassian (Jira), or GitHub/GitLab MCP tools when available, or `git remote`/`gh`/`glab`; falls back to the filesystem when none are reachable.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git remote:*)
  - Bash(gh:*)
  - Bash(glab:*)
argument-hint: "<mode: plan|write|review> [work-id|target] [flags]"
metadata:
  author: Carinya Parc
  version: "2.0"
  owner: architecture
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

Read and write architecture artefacts under `docs/architecture/`.

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
   **plan** takes an optional work item: `adr plan <work-id>` resolves it per
   [work-item-resolution.md](../../references/work-item-resolution.md),
   harvests decisions already made in `{work-dir}/design.md`, and
   triages them into the register. Without a work item it surveys product.md
   and solution.md for decisions still to be made.
3. [prompts/plan.prompt.md](prompts/plan.prompt.md) | [prompts/write.prompt.md](prompts/write.prompt.md) | [prompts/review.prompt.md](prompts/review.prompt.md).

## Related skills

- `/architecture:solution` — system architecture narrative
- `/engineering:design` — work-item technical design (harvest source)
- `/engineering:docs-review` — writing quality / cross-doc consistency
