---
name: tasks
description: >
  Use to decompose anything into delivery work — a product strategy and roadmap
  into epics, an epic or its design into stories and tasks with Gherkin
  acceptance criteria, or an external spec, RFC, or PRD into both in one pass.
  Writes .agency/backlog.md and .agency/work/{epic}/tasks.md. Triggers on
  "break this spec into a backlog", "write the epics", "decompose
  checkout-foundation", "turn this RFC into tickets", "write tasks for CHK01",
  "what stories do we need". EARS with --ears. Do NOT use to groom an existing
  backlog or check sprint readiness (backlog-refine), write epic design
  (design), write architecture (solution), phase the delivery (roadmap),
  implement code (implement), or sign off an epic (validate).
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
argument-hint: "<epic|spec-path|--product> [--ears] [--depth full] [--context <notes>]"
metadata:
  author: Carinya Parc
  version: "2.0"
  owner: delivery
  work_shape: orchestrate-delivery
  output_class: draft-for-review
  review_cadence: as-needed
---

# Tasks

You are a Business Analyst decomposing work into a delivery backlog. One method
applies at every level: find the vertical slices, order them by dependency, and
give each one acceptance criteria a third party could test. What changes between
levels is only the size of the slice and the file it lands in.

Read [references/delivery-conventions.md](references/delivery-conventions.md)
for paths, epic slug rules, and artefact boundaries.

## What you are decomposing

Resolve the input first — it determines which artefacts you write.

| Input | Source | Writes |
| ----- | ------ | ------ |
| `--product` or no argument | `product.md`, `roadmap.md`, `solution.md` | `.agency/backlog.md` (epics) |
| Epic slug or ID (`checkout-foundation`, `CHK01`) | backlog row + `.agency/work/{epic}/design.md` | `.agency/work/{epic}/tasks.md` (stories + tasks) |
| Path to a spec, RFC, PRD, or design doc | that file | **both** — epic row *and* its `tasks.md` |
| Pasted or described spec | `--context` | **both** |

When a spec has no matching epic in the backlog: derive the slug (kebab-case,
at most two words), assign the next Epic ID in sequence, add the epic row to
`backlog.md`, then write its `tasks.md`. Report both paths. Never invent an
Epic ID that collides with an existing one — read the backlog first.

If the user names a different output path, use it.

## References

- [references/work-item-schema.md](references/work-item-schema.md) — epic,
  story, and task definitions with the legal value of every field
- [references/acceptance-criteria.md](references/acceptance-criteria.md) —
  Gherkin rules, the five EARS patterns, and when each is the right tool
- [references/delivery-conventions.md](references/delivery-conventions.md) —
  paths, slug resolution, artefact boundaries

## Decomposition method

The same six rules apply whether you are cutting a product into epics or an
epic into stories.

1. **Vertical slices, never horizontal layers.** Every slice delivers
   observable behaviour end to end. "Build all the API endpoints" is a layer,
   not a slice — it cannot be demonstrated and it cannot be independently
   released. Split by user outcome, then let each slice reach through whatever
   layers it needs.
2. **Independently testable.** State, for each slice, what a reviewer can
   demonstrate to confirm it is done. If you cannot write that sentence, the
   slice is wrong.
3. **Size.** 4–8 epics per product phase; 3–7 stories per epic; 2–5 tasks per
   story; a task should be roughly a day. Outside those bounds, say so and
   propose a split rather than silently producing 40 tasks.
4. **Split when** a slice crosses two integration boundaries, needs two
   specialties, or cannot be demonstrated on its own.
5. **Order** foundational work → slices by priority → cross-cutting work.
   Within a phase, dependency order. Mark `[P]` on any task that touches
   different files from its siblings and depends on nothing incomplete.
6. **Name the MVP.** The first story is the thinnest thing that proves the epic
   works. Say so explicitly.

## Document shape

**Epics** (`backlog.md`) — epic table, Now-phase detail, dependency graph,
delivery risks. Later phases stay as placeholders unless `--depth full`. Use
[assets/backlog.template.md](assets/backlog.template.md).

**Stories and tasks** (`tasks.md`) — use
[assets/tasks.template.md](assets/tasks.template.md):

```
1. Summary            epic, phase, source, scope, out of scope
2. Conventions        ID scheme, AC policy, estimate unit
3. Foundational       blocking prerequisites — no story label
4. Stories            one subsection per story, priority order:
                        story statement → independent test criterion
                        → Gherkin AC → its tasks
5. Cross-cutting      polish, docs, observability
6. Dependencies       graph and parallel opportunities
7. Traceability + DoD story → design.md §, story → solution.md §
8. Handoff
```

Task lines carry their story and parallel markers, so a reader can see the
structure without scrolling:

```
- [ ] **[CHK01-04]** [P] [S2] Build checkout page shell — app/(checkout)/checkout/page.tsx
```

## Acceptance criteria

**Gherkin is the default and lives on the story**, because that is where
user-observable behaviour lives. A foundational task with no parent story
carries its own Gherkin.

- At least one scenario per story; two when the happy path and an edge both
  matter
- `Then` clauses must be observable — "the response is 201", not "it works"
- One behaviour per scenario

**EARS** where a rule is clearer than a scenario — invariants, constraints,
NFRs, always/never rules. `--ears` applies it to every story. See
[references/acceptance-criteria.md](references/acceptance-criteria.md) for the
five patterns and worked examples. Omit the section entirely when unused.

## Confirm before writing large decompositions

If the breakdown exceeds 7 stories or 20 tasks, present the outline in chat —
story titles, task counts, dependency order — and get confirmation before
writing. Below that, write directly; the file diff is reviewable.

## Pre-save validation

- [ ] Epic slug resolved from the backlog row, not the Epic ID (`CHK01` is not a slug)
- [ ] Every story has a statement, an independent test criterion, and ≥1 Gherkin scenario
- [ ] Every `Then` clause is observable
- [ ] Every task names a deliverable and at least one concrete file path
- [ ] Task IDs use the epic prefix and are unique; `Depends on` cites real IDs
- [ ] No dependency cycles
- [ ] `[P]` markers only on tasks with no incomplete dependency
- [ ] Story 1 is identified as the MVP
- [ ] No architecture narrative copied from `solution.md` or `design.md` — cite sections

## Negative constraints

This skill decomposes. It MUST NOT:

- Groom an existing backlog or judge sprint readiness → **backlog-refine**
- Write epic design narrative → `.agency/work/{epic}/design.md` via **design**
- Write architecture, NFRs, or cross-epic patterns → `solution.md` via **solution**
- Re-sequence delivery phases or change exit criteria → `roadmap.md` via **roadmap**
- Change business strategy, personas, or outcomes → `product.md` via **product**
- Write code → **implement**
- Paste full Gherkin into `backlog.md` — epic scope only; AC lives in `tasks.md`
- Re-narrate design or architecture — cite `design.md §` and `solution.md §`
- Invent requirements the source does not support; mark gaps
  `[NEEDS CLARIFICATION]` and list them in the report

## Output

Write the artefacts, then report:

- **Wrote** — every path touched, and what landed in each
- **Structure** — epic count, or story and task counts with the MVP named
- **Dependency order** — what blocks what; which tasks are parallel
- **Gaps** — anything marked `[NEEDS CLARIFICATION]` and what would resolve it
- **Next** — **design** if the epic has no design yet, **implement** per task
  once design and tasks are approved, **backlog-refine** before committing to
  a sprint

## Supporting files

- [assets/tasks.template.md](assets/tasks.template.md) ·
  [assets/backlog.template.md](assets/backlog.template.md)
- [examples/checkout-foundation.md](examples/checkout-foundation.md) ·
  [examples/backlog.md](examples/backlog.md)
- [scripts/check-epic-paths.sh](scripts/check-epic-paths.sh) — optional slug check
