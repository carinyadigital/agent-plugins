# Work item schema

The three levels of the decomposition ladder, and the legal value of every
field. Referenced by **tasks** when writing and by **backlog-refine** when
grooming.

---

## Epic

A body of work that delivers one phase objective or crosses one integration
boundary. Lives as a row in `.agency/backlog.md`; its stories and tasks
live in `.agency/work/{epic}/tasks.md`.

| Field | Required | Legal values |
| ----- | -------- | ------------ |
| Epic ID | Yes | `{PREFIX}{nn}` — 2–4 uppercase letters + two digits (`CHK01`, `AUTH03`) |
| Title | Yes | Noun phrase naming the outcome (`Checkout Foundation`) |
| Slug | Yes | kebab-case from the title, **at most two words** (`checkout-foundation`) |
| Work path | Yes | `.agency/work/{slug}/` |
| Phase | Yes | Matches a phase name in `roadmap.md` (`Now`, `Next`, `Later`, or named) |
| Status | Yes | `not started` · `in progress` · `blocked` · `done` |
| Priority | Yes | `P0`–`P3` (see below) |
| Estimate | Yes | Story points, Fibonacci: 1, 2, 3, 5, 8, 13, 21. `TBD` only with a spike noted |
| Depends on | No | Epic IDs, comma separated. Must be acyclic |
| Outcome | Yes | The `product.md §7` outcome this epic serves |

An epic that cannot name a product outcome is either undocumented value or
scope the product strategy would not support — say so rather than writing it.

---

## Story

A user-visible outcome inside an epic. **Carries the acceptance criteria.**

| Field | Required | Legal values |
| ----- | -------- | ------------ |
| Story ID | Yes | `{EPIC-ID}-S{n}` (`CHK01-S2`) |
| Statement | Yes | *As a {role}, I want {capability}, so that {benefit}* |
| Independent test criterion | Yes | One sentence: what a reviewer can demonstrate to confirm it is done |
| Priority | Yes | `P0`–`P3` |
| Acceptance | Yes | ≥1 Gherkin scenario; EARS where a rule is clearer (see [acceptance-criteria.md](acceptance-criteria.md)) |
| Design | Recommended | Link to the `design.md` section it implements |

**Story 1 is the MVP** — the thinnest slice that proves the epic works. Mark it.

A story is wrong if you cannot write its independent test criterion. That is
the test for a vertical slice: "all the API endpoints" has no demonstration,
"a customer can reach the checkout page and see their cart" does.

---

## Task

The engineering work under one story. Inherits its story's acceptance criteria.

| Field | Required | Legal values |
| ----- | -------- | ------------ |
| Task ID | Yes | `{EPIC-ID}-{nn}`, sequential across the whole epic (`CHK01-04`) |
| Story label | Yes, unless foundational | `[S{n}]` matching its parent story |
| Parallel marker | No | `[P]` — different files from its siblings, no incomplete dependency |
| Title | Yes | Imperative, specific (`Build checkout page shell`, not `Frontend work`) |
| Deliverable | Yes | What exists when it is done, with **at least one concrete file path** |
| Status | Yes | `not started` · `in progress` · `blocked` · `done` |
| Estimate | Yes | Points, Fibonacci. Roughly a day of work. `TBD` is not acceptable on a task |
| Owner | No | `TBD` acceptable for an unassigned queue |
| Depends on | No | Task IDs, comma separated. Must be acyclic |
| Labels | No | `phase:{phase}`, `type:{type}`, plus free tags |
| Design | Recommended | `./design.md#section` |

### Foundational tasks

A task with no parent story — a shared prerequisite every story needs
(scaffolding, module layout, a client, a migration). It carries **its own
Gherkin**, since no story covers it. No `[S{n}]` label. Lives in §3, before the
stories.

Keep these genuinely shared. A "foundational" task that only one story needs
belongs to that story.

---

## Shared vocabularies

### Priority

| Value | Meaning |
| ----- | ------- |
| `P0` | Blocks other work or the phase exit criteria. Do first |
| `P1` | Required for the phase objective |
| `P2` | Wanted in this phase; droppable under pressure |
| `P3` | Opportunistic |

### Type

`feature` · `integration` · `scaffold` · `migration` · `spike` · `chore` ·
`fix`

A `spike` is time-boxed and produces a decision or a document, never shipped
code. It is the only work item allowed a `TBD` estimate on what follows it.

### Status

`not started` · `in progress` · `blocked` · `done`

`blocked` requires a named blocker. Status is updated by **validate** (against
acceptance criteria) and by **backlog-refine** (against delivery evidence) —
not by this skill after the initial write.

---

## ID stability

Task IDs are the contract with **implement**, **sprint-planning**, and
**validate**. Once written and committed, an ID is never reused or renumbered.
Adding work appends the next number; removing work marks the item as removed
rather than freeing the ID.
