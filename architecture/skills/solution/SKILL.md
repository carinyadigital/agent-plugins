---
name: solution
description: >
  Use when the user wants system architecture as an arc42 ARCHITECTURE.md —
  current (as-is, default) or target (to-be, especially greenfield).
  Triggers on "write the architecture", "solution design", "arc42",
  "ARCHITECTURE.md", "target architecture", "as-is architecture",
  "document what we have". Re-authoring also covers architectural critique
  — docs-review covers writing quality only. Do NOT use for product strategy,
  roadmap phases, epic/story breakdown (tasks), work-item design (design),
  or ADRs (adr).
license: Apache-2.0
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "[--state current|target] [--context <notes>]"
metadata:
  author: Carinya Digital
  version: "3.1"
  owner: architecture
  work_shape: generate-draft
  output_class: draft-for-review
  review_cadence: as-needed
---

Read and write architecture artefacts. Default write path is `ARCHITECTURE.md`
at the target repo root.

# Architecture (arc42)

You are a Principal Architect. arc42 is both a template (where each kind of
architecture information belongs) and a method (how you produce it). Follow
both. Do not invent a parallel outline.

## Artefact

Default path: `ARCHITECTURE.md` at the target repo root.

Decisions are **not** in this file. They live in
`docs/decisions/` via `/architecture:adr`.

## Path resolution

Write (first match):

1. Path the user named in this request.
2. `ARCHITECTURE.md` at the resolved target repo root.

Read (first match, then write the default unless the user named a path):

1. Path the user named.
2. `artefactPaths.architecture` from the bound target config, if present.
3. `ARCHITECTURE.md` at the target repo root.
4. Legacy `docs/architecture/solution.md` — migrate its substance into
   `ARCHITECTURE.md`; do not keep both as live architecture.

Override only when the user names a different file.

## State (`--state`)

| Value | When | What you write |
| ----- | ---- | -------------- |
| `current` (default) | A system that already exists | What the code and running topology **are**. Ground every section in the repo. |
| `target` | Greenfield, or an explicit "intended / to-be" ask | What the architecture **should be**. Planned paths are allowed; mark assumptions. |

If `--state` is omitted:

- Substantial implementation exists → `current`.
- Little or no implementation (project start) → `target`, and say so.
- User asked for both as-is and to-be → write `current` as the document, and
  put the intended delta in Solution Strategy plus Risks — do not fork a
  second architecture file unless they named one.

Frontmatter `state:` must match the state you wrote.

## The method

Six recurring, interrelated activities — no fixed order; each increment
refines the others ([arc42 method](https://arc42.org/method/)):

1. **Clarify requirements** — quality goals, constraints, stakeholders.
   Question quality requirements; categorise function; name technical risks.
2. **Design structures** — building blocks, runtime, interfaces. Structure
   along the domain (domain-driven).
3. **Design cross-cutting concepts** — quality-driven: pick the concepts that
   make the quality goals achievable (UI, persistence, errors, operations,
   test, release — only those that apply).
4. **Communicate and document** — write only what stakeholders need. The
   template is the cabinet; fill the drawers that have content.
5. **Accompany the implementation** — for `current`, look at the source.
   Record what the code does, including gold pieces that beat the original
   design. Do not document an intended shape the repo does not have.
6. **Analyze and evaluate** — do today's structures and concepts still
   achieve the quality goals? Weaknesses and risks go in §11, not as silent
   omissions.

Stances that come with the method: clarify the most important quality
requirements before anything else; structure along the domain; choose
cross-cutting concepts that actually serve those quality goals.

## Negative constraints

`ARCHITECTURE.md` MUST NOT contain:

- Architecture decision records or an "Architecture Decisions" section →
  `/architecture:adr` (`docs/decisions/`)
- Commercial rationale, personas, positioning → `docs/product/product.md`
- Story-level acceptance criteria → `specs/{work-short-name}/TASKS.local.md`
- Phase sequencing → `docs/product/roadmap.md`
- Work-item APIs and file lists → `{work-dir}/design.md` (cite this doc)

## Context

Read before writing:

- `docs/product/product.md` when present (do not copy business narrative)
- Existing `ARCHITECTURE.md` or legacy `docs/architecture/solution.md`
- `docs/decisions/` — link accepted ADRs from the sections they
  affect; do not restate the decision bodies
- For `current`: the repo (layout, deploy config, tests, CI, public APIs)
- For `target` at project start: product.md, constraints the user named,
  comparable systems they pointed at

## Steps

1. Resolve target, path, and state (above).
2. **Clarify requirements (1).** Top 3–5 architecture quality goals, ordered;
   constraints; stakeholders who must know or work with this architecture.
3. **See the system (5, then 2).** `current`: walk the repo and produce the
   context diagram, building-block whitebox, and directory tree from what
   exists. `target`: design those from domain + quality goals.
4. **Cross-cutting concepts (3).** Only concepts the quality goals require.
   Typical drawers: security (trust boundaries), persistence, observability,
   testing, build/release. Concrete behaviour, not tool names alone.
5. **Runtime and deployment (2, 3).** 2–5 sequences people debug at 3am.
   Deployment as Service / Platform / Role, mapped to building blocks.
6. **Evaluate (6).** Quality scenarios that make §1 goals testable. Risks,
   debt, open questions. Glossary of terms used in code and conversation.
7. **Write (4).** Fill
   [assets/ARCHITECTURE.template.md](assets/ARCHITECTURE.template.md).
   Omit a section only if it truly does not apply — say so in chat, do not
   leave empty headings or `[NEEDS CLARIFICATION]`.
8. Delete the drafting-aide comment block. Save to the resolved path.
9. If you migrated from `docs/architecture/solution.md`, say that the legacy
   file is superseded and should be removed in the same change set.

## What "good" looks like (agent-practical)

Stay inside the arc42 drawers. Make each drawer usable by an implementer
who was not in the room:

- **Ownership rule** at the top — which changes require updating this file
  in the same PR.
- **ASCII diagrams** for context, building-block whitebox, and trust
  boundaries. No untitled boxes.
- **Source files** after every filled section — the paths that make the
  section true. `current`: existing paths. `target`: intended paths.
- **Directory tree** under Building Block View (whitebox overall) — the
  repo layout every later epic extends.
- **Deployment table** (Service, Platform, Role) plus how building blocks
  map onto it.
- **Limits, protocols, and identities** as facts (timeouts, step caps,
  thread/session rules), not slogans.
- **Testing tiers** and **CI workflows** as cross-cutting concepts when
  they exist (`current`) or are decided (`target`).

Do not replace arc42 with a free-form "system overview / frontend / API /
CI" outline. Map those facts into §3, §5, §6, §7, and §8.

## Quality rules

- §1 quality goals are architecture qualities, not project goals; top goal
  wins on conflict
- §4 names trade-offs and what the system will **not** do
- §5 includes a text diagram and the repository layout
- §9 is absent — no decision log in this file
- `current` does not invent topology, services, or directories the repo
  does not have
- `target` does not pretend code exists; planned structure is labelled
- Do not repeat product.md — link it
- Cite ADRs by ID where a section is governed by one; do not paste them

## Gotchas

- **Per-work-item files/APIs** → `{work-dir}/design.md`; cite this document
  by section (`ARCHITECTURE.md §5`).
- **Closed ADRs** → `docs/decisions/ADR-NNNN-*.md`. A decision
  that is only a sentence in this file should be harvested with
  `/architecture:adr plan`, not expanded here.
- **Legacy `solution.md`** → read it, write `ARCHITECTURE.md`, do not edit
  both as canonical.

## Output format

Markdown with YAML frontmatter. Save to the resolved path. Use
[assets/ARCHITECTURE.template.md](assets/ARCHITECTURE.template.md).

Present the draft for review — this is not shipped fact until a human
accepts it.

## Supporting files

- [assets/ARCHITECTURE.template.md](assets/ARCHITECTURE.template.md)

## Related skills

- `/architecture:adr` — architecture decisions
- `/product-management:product` — product strategy
- `/product-management:tasks` — epics and work paths
- `/engineering:design` — work-item technical design
- `/engineering:docs-review` — writing quality / cross-doc consistency
