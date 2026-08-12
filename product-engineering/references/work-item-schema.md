# Work item schema

The decomposition ladder — epic → story → task, plus bug and spike as
first-class leaf types — and the legal value of every field. Referenced by
**tasks** when writing, by **backlog-refine** when grooming, and by every
skill that resolves a work item argument.

Read [work-item-resolution.md](work-item-resolution.md) first: it decides
whether an ID's fields come from Linear, Jira, GitHub/GitLab, or the
filesystem tables below, and whether the ID itself is a tracker key or an
internal ID. This file defines the fields; that file decides where they live.

---

## Type

**Known set:** `epic` · `story` · `task` · `bug` · `spike`. This is a
starting vocabulary, not a whitelist — a source system's native type (Jira's
"Improvement", Linear's custom workflow labels, a GitHub `kind/*` label) is
kept verbatim in the artefact. Map it to the closest row below only to decide
skill *behaviour*; ask the user when the mapping is unclear.

| Type | Decomposes into | Carries its own AC? | Typical next skill |
| ---- | ---------------- | -------------------- | ------------------- |
| `epic` | Stories and tasks | No — AC lives on its stories | **tdd**, **tasks** |
| `story` | Tasks (sub-tasks) | Yes — the primary AC holder | **tasks**, **tdd** (if it needs its own) |
| `task` | Nothing further (it's the unit of work) | Inherits its story's AC, or carries its own if foundational | **implement** |
| `bug` | Nothing further, unless large enough to need sub-tasks | Yes — reproduction as Given/When, fix as Then | **implement** |
| `spike` | Nothing further — it is time-boxed | No — it produces a decision or document, not code | **implement** (the spike itself), then **adr** or **tasks** for what it unblocks |

`tasks` asked to decompose a `task`, `bug`, or `spike` should confirm intent
rather than refuse or silently comply — see the ask-first checklist in
work-item-resolution.md. A large bug that genuinely needs sub-tasks is a
legitimate case; a task that "needs decomposing" usually means it was sized
wrong and should go back through **backlog-refine**.

---

## Epic

A body of work that delivers one phase objective or crosses one integration
boundary. In a **filesystem-only** repo it lives as a row in
`docs/product/backlog.md`; its stories and tasks live in
`docs/work/{work-id}/tasks.md`. In a **tracker-backed** repo the tracker's
epic/initiative object is the source of truth — skills read it directly and
do not maintain a shadow `backlog.md`.

| Field | Required | Legal values |
| ----- | -------- | ------------ |
| Work item ID | Yes | Tracker key (`CHK-1`, `ENG-45`) when a tracker resolved; else internal `{PREFIX}{nn}` — 2–4 uppercase letters + two digits (`CHK01`, `AUTH03`) |
| Title | Yes | Noun phrase naming the outcome (`Checkout Foundation`) |
| Work path | Yes | `docs/work/{work-id}/` — filesystem-only repos also derive a title slug for the folder name (see delivery-conventions.md); tracker-backed repos use the key itself |
| Phase | Yes | Matches a phase name in `roadmap.md` (`Now`, `Next`, `Later`, or named) |
| Status | Yes | `not started` · `in progress` · `blocked` · `done` (or the tracker's native workflow states, mapped) |
| Priority | Yes | `P0`–`P3` (see below) |
| Estimate | Yes | Story points, Fibonacci: 1, 2, 3, 5, 8, 13, 21. `TBD` only with a spike noted |
| Depends on | No | Other work item IDs, comma separated. Must be acyclic |
| Outcome | Yes | The `product.md §7` outcome this epic serves |

An epic that cannot name a product outcome is either undocumented value or
scope the product strategy would not support — say so rather than writing it.

---

## Story

A user-visible outcome inside an epic. **Carries the acceptance criteria.**
Anything can get a `tdd.md` at story level if the work warrants it — run
`tdd {story-id}` directly; it writes to `docs/work/{story-id}/tdd.md`,
citing the parent epic by ID rather than nesting under its folder.

| Field | Required | Legal values |
| ----- | -------- | ------------ |
| Work item ID | Yes | Tracker key (`CHK-2`, `ENG-46`) when a tracker resolved; else internal `{EPIC-ID}-S{n}` (`CHK01-S2`) |
| Statement | Yes | *As a {role}, I want {capability}, so that {benefit}* |
| Independent test criterion | Yes | One sentence: what a reviewer can demonstrate to confirm it is done |
| Priority | Yes | `P0`–`P3` |
| Acceptance | Yes | ≥1 Gherkin scenario; EARS where a rule is clearer (see [acceptance-criteria.md](acceptance-criteria.md)) |
| Design | Recommended | Link to the `tdd.md` section it implements — either the parent epic's or its own |

**Story 1 is the MVP** — the thinnest slice that proves the epic works. Mark it.

A story is wrong if you cannot write its independent test criterion. That is
the test for a vertical slice: "all the API endpoints" has no demonstration,
"a customer can reach the checkout page and see their cart" does.

---

## Task

The engineering work under one story, or a standalone unit of work with no
parent story. Inherits its story's acceptance criteria when it has one.

| Field | Required | Legal values |
| ----- | -------- | ------------ |
| Work item ID | Yes | Tracker key (`CHK-15`) when a tracker resolved; else internal, sequential within the `tasks.md` it is written to: `{EPIC-ID}-{nn}` for a task under an epic (`CHK01-04`), `{STORY-ID}-{nn}` for a sub-task under a story with its own `tasks.md` (`CHK01-S2-01`) |
| Story label | Yes, unless foundational | `[S{n}]` matching its parent story |
| Parallel marker | No | `[P]` — different files from its siblings, no incomplete dependency |
| Title | Yes | Imperative, specific (`Build checkout page shell`, not `Frontend work`) |
| Deliverable | Yes | What exists when it is done, with **at least one concrete file path** |
| Status | Yes | `not started` · `in progress` · `blocked` · `done` |
| Estimate | Yes | Points, Fibonacci. Roughly a day of work. `TBD` is not acceptable on a task |
| Owner | No | `TBD` acceptable for an unassigned queue |
| Depends on | No | Other work item IDs, comma separated. Must be acyclic |
| Labels | No | `phase:{phase}`, plus free tags. Not `type:` — a task's type is the `## Type` field above, not a label |
| Design | Recommended | `./tdd.md#section` |

### Foundational tasks

A task with no parent story — a shared prerequisite every story needs
(scaffolding, module layout, a client, a migration). It carries **its own
Gherkin**, since no story covers it. No `[S{n}]` label. Lives in §3, before the
stories.

Keep these genuinely shared. A "foundational" task that only one story needs
belongs to that story.

---

## Bug

A defect against already-shipped behaviour. Usually a leaf item — implement
the fix directly. Only split into sub-tasks when the fix genuinely spans more
than one integration boundary; otherwise treat splitting as a sizing problem
for **backlog-refine**, not a default.

| Field | Required | Legal values |
| ----- | -------- | ------------ |
| Work item ID | Yes | Tracker key when resolved; else `{PREFIX}{nn}` in a filesystem-only repo |
| Title | Yes | Names the observed defect, not the fix (`Checkout total ignores discount code`) |
| Reproduction | Yes | Given/When steps that reliably trigger it |
| Expected vs actual | Yes | What should happen vs what does |
| Acceptance | Yes | The reproduction's `Then` now holds; regression coverage named |
| Priority | Yes | `P0`–`P3`, weighted by user impact |
| Design | No | Only if the fix touches architecture — cite `solution.md §{N.M}` |

## Spike

A time-boxed investigation. Never shipped code; produces a decision or a
document. The only work item allowed a `TBD` estimate on what follows it,
because its purpose is to remove that unknown.

| Field | Required | Legal values |
| ----- | -------- | ------------ |
| Work item ID | Yes | Tracker key when resolved; else `{PREFIX}{nn}` |
| Question | Yes | The single question the spike must answer |
| Timebox | Yes | A concrete duration or points ceiling |
| Output | Yes | Decision, ADR candidate, or a short findings doc — named explicitly |
| Unblocks | Recommended | The work item(s) whose estimate is currently `TBD` because of this question |

---

## Shared vocabularies

### Priority

| Value | Meaning |
| ----- | ------- |
| `P0` | Blocks other work or the phase exit criteria. Do first |
| `P1` | Required for the phase objective |
| `P2` | Wanted in this phase; droppable under pressure |
| `P3` | Opportunistic |

### Status

`not started` · `in progress` · `blocked` · `done` — or the source system's
native workflow states, mapped to these four for cross-skill reporting.

`blocked` requires a named blocker. Status is updated by **validate** (against
acceptance criteria) and by **backlog-refine** (against delivery evidence) —
not by **tasks** after the initial write.

---

## ID stability

Work item IDs are the contract with **implement**, **sprint-planning**, and
**validate**. Once written and committed, an ID is never reused or renumbered
— true whether the ID is a tracker key (the tracker enforces this itself) or
an internal ID (this schema enforces it). Adding work appends the next
number; removing work marks the item as removed rather than freeing the ID.

Never generate an internal ID for a work item that already has a tracker key,
and never renumber a tracker key to fit an internal scheme.
