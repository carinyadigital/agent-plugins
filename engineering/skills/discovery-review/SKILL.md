---
name: discovery-review
description: >
  Use when the user wants to confirm discovery artefacts are complete and a
  work item is Ready for Development — design.md, TASKS.local.md, ARCHITECTURE.md,
  and related product or architecture docs for that item. Triggers on
  "ready for development", "is discovery done", "review the TDD and tasks",
  "can we start implementing", "discovery review", "are we ready to build".
  Read-only gate: verdict plus findings; does not amend artefacts. Do NOT use
  for writing the Solution Design and tasks until Ready (discover), repo docs
  quality (docs-review), code review (code-review), UX review
  (ux-design-review), writing a Solution Design (design) or tasks
  (/product-management:tasks), or completion sign-off
  (/product-management:validate).
license: Apache-2.0
compatibility: Tracker resolution uses Linear, Atlassian (Jira), or GitHub/GitLab MCP tools when available, or `git remote`/`gh`/`glab`; falls back to the filesystem when none are reachable.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write(specs/**/reviews/**)
  - Write(discovery-review-*.local.md)
  - Write(discovery-review-*.local.json)
  - Bash(git remote:*)
  - Bash(git log:*)
  - Bash(gh:*)
  - Bash(glab:*)
argument-hint: "<work-id>"
metadata:
  author: Carinya Parc
  version: "2.0"
  owner: engineering
  work_shape: review-and-gate
  output_class: decision-support
  review_cadence: as-needed
---

Work directory `{work-dir}/`; default (if not specified or unknown): `specs/{work-short-name}/`. Read artefacts from `{work-dir}/`, `ARCHITECTURE.md`, and `docs/architecture/decisions/`.

# Discovery review

You are a Tech Lead judging whether discovery is complete enough to start
implementation. You report a **Ready for Development** or **Not ready**
verdict. You do not change the artefacts.

This is the gate between `design` / `/product-management:tasks` and `implement`.
It is not a writing quality review of a docs tree — that belongs to
`docs-review`.

## Read-only contract

This skill writes exactly one co-located pair per run — same directory, same
stem:

- `specs/{work-short-name}/reviews/discovery-review-{nn}.local.md` — human-readable
  verdict
- `specs/{work-short-name}/reviews/discovery-review-{nn}.local.json` — review state
  for incremental runs

When no work item resolved, write the latest-only pair
`discovery-review-{slug}.local.md` and `discovery-review-{slug}.local.json` at the
repo root. Do not invent numbering on the fallback path.

Do not write under repo-root `reviews/`. Do not create that directory. Do not
edit `.gitignore`. These files are local (`.local.` suffix) and MUST never be
committed. The skill MUST NOT modify product, architecture, Solution Design, or
task artefacts.

Naming the next skill (`design`, `/product-management:tasks`,
`/architecture:solution`, `implement`) is not invoking it.

## Inputs

Read [work-item-resolution.md](../../references/work-item-resolution.md)
**first** — resolve source system, canonical ID, and type before judging
completeness. Read
[delivery-conventions.md](../../references/delivery-conventions.md) for paths
and artefact boundaries.

| Input | Location | Required |
| ----- | -------- | -------- |
| Work item | tracker or `docs/product/backlog.md` | Yes |
| Solution Design | `{work-dir}/design.md` | Yes for epic/story; if missing for a bug/spike, say so rather than inventing one |
| Tasks + Gherkin AC | `{work-dir}/TASKS.local.md` or the tracker | Yes when a local or tracker breakdown is how this repo carries AC — owned by `/product-management:tasks` |
| Solution architecture | `ARCHITECTURE.md` | If the work item touches architectural boundaries |
| ADRs | `docs/architecture/decisions/` | If the Solution Design cites them, or a decision is still open |
| Product / roadmap | `docs/product/product.md`, `roadmap.md` | If present — check the slice still matches |

## Steps

1. **Resolve** — work item, `{work-dir}`, type. Ask on any ambiguity.
2. **Inventory** — which discovery artefacts exist, which are missing, which
   are stubs (`[NEEDS CLARIFICATION]`, empty sections, leftover DRAFTING AIDE).
3. **Completeness** — apply
   [references/readiness-gate.md](references/readiness-gate.md) for this type.
4. **Boundaries and consistency** — the set must obey delivery-conventions
   artefact boundaries, and must not contradict itself. Apply
   [references/artefact-consistency.md](references/artefact-consistency.md).
5. **Gate** — **Ready for Development** only when there are no blocking
   findings. Warnings do not fail the gate; they travel with the verdict.
6. **Report** — persist the verdict; name the owning skill for each gap.

The discovery set for one work item is small. Review it inline. Do not spawn
sub-agents, and do not expand the review into a handbook or `docs/` tree audit.

## Do not report

- Prose polish, heading style, or house voice. Not this gate.
- Missing content outside the work item's job (a story Solution Design need not restated
  the epic's architecture — it should cite it).
- Code quality, test coverage, or whether implementation has started.
- Whether the product strategy is *right* — only whether the slice in `design.md`
  / tasks still matches what product and solution already say.

## Quality rules

- Every finding cites evidence: path, and heading or line.
- A contradiction names **every** location and which artefact is authoritative
  per delivery-conventions — or states that you could not establish it.
- Distinguish verified absence (file not found) from inferred incompleteness.
- Prefix every finding with its action tier.

| Tier | Meaning |
| ---- | ------- |
| `blocking` | `implement` would have to guess. Missing required artefact, untestable AC, unresolved clarification that changes the slice, or a contradiction between artefacts. |
| `warning` | Real gap that will slow delivery but an implementer could proceed with an explicit assumption. |
| `suggestion` | Polish or optional artefact. Harmless to defer. |

**Blocking is a high bar.** Empty flavour text is a warning. A `[NEEDS CLARIFICATION]` that decides the files shipped or the acceptance gates is blocking.

## Must not

- Amend the Solution Design, tasks, solution, ADRs, or product docs.
- Draft replacement sections. Describe the gap; do not supply the prose.
- Review `docs/` as a documentation set — route that to `docs-review`.
- Review code, a branch, or rendered UI.
- Sign off completed implementation — that is **validate**.
- Treat "the Solution Design exists" as sufficient. Existence without a slice, files, gates,
  and testable AC is **Not ready**.

## Output format

<example>
## Discovery Review

**Work item:** CHK01 Checkout Foundation (epic)
**Work dir:** `specs/checkout-foundation/`
**Verdict:** Not ready
**Gate:** Ready for Development — failed (2 blocking)

### Inventory

| Artefact | Status |
| -------- | ------ |
| `design.md` | present, skeleton |
| `TASKS.local.md` | present |
| `ARCHITECTURE.md` | present |
| ADRs | none cited |

### Blocking

- **[blocking] Untestable AC — CHK01-03**
  **Where:** `TASKS.local.md` CHK01-03
  **Why it matters:** Scenario has no Then. Implement cannot know done.
  **Owner:** `/product-management:tasks`

- **[blocking] Open clarification that changes the slice**
  **Where:** `design.md` §5 Open questions — payment provider undecided
  **Why it matters:** Files shipped and error paths depend on the answer.
  **Owner:** `design` after `/architecture:adr` or a recorded decision

### Warnings

- **[warning] Solution Design restates module layout already in `ARCHITECTURE.md` §5**
  **Where:** `design.md` §2
  **Why it matters:** Two homes; they will drift.
  **Owner:** `design` — cite `ARCHITECTURE.md` §5 instead

### Suggestions

- **[suggestion] No ADR for the provider choice once it is made**
  **Where:** set-wide
  **Owner:** `/architecture:adr plan CHK01` after the decision

### Recommended order

1. Decide the payment provider (blocking). Record it; trim `design.md` §5.
2. Give CHK01-03 a Then that a third party could test.
3. Then re-run discovery-review. Do not start `implement` until Ready.

Next: `design` and `/product-management:tasks` for the blocking items — not `implement`. Or re-run the `discover` agent to apply the blockers and re-gate.
</example>

When the verdict is Ready:

```text
Verdict: Ready for Development
Next: run the deliver agent with <work-id>  (or implement <first-task-id> for a single task)
```

## References

- [references/readiness-gate.md](references/readiness-gate.md) — required artefacts and blocking bar per work-item type
- [references/artefact-consistency.md](references/artefact-consistency.md) — boundaries, contradictions, citations
- [delivery-conventions.md](../../references/delivery-conventions.md) — paths and artefact homes
- [work-item-resolution.md](../../references/work-item-resolution.md) — ID, type, `{work-dir}`

## Related workflow

- `discover` agent — writes Solution Design + tasks and loops this gate until Ready
- `design` / `/product-management:tasks` — leaf writers this gate judges
- `deliver` agent / `implement` skill — only after Ready for Development
- `/architecture:solution` — when a missing or contradictory ARCHITECTURE.md is blocking
- `docs-review` — document-set quality, not this Ready-for-Development gate
