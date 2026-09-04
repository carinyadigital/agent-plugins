# Work items

How any skill turns a bare argument (`JIRA-123`, `ENG-45`, `#812`,
`checkout-foundation`, `CHK01`) into a **source system**, a **canonical ID**,
and a **type** — then the field rules for each type. Resolve once per session
and reuse. **Never guess:** if system, ID, or type is ambiguous, stop and ask.

## 1. Pointer file

Look for `TASKS.local.md` at the **repo root** first. That file is the
Linear/Jira source-system pointer — not the work-item task list (that lives at
`{work-dir}/TASKS.local.md` when a local breakdown is required).

- **Exists and names Linear or Jira** — trust it (site, workspace/team, project
  key). Do not re-detect or re-ask.
- **Exists and names filesystem** — trust it; skip to [ID and path](#id-and-path).
- **Missing** — run [§2](#2-detect-the-source-system).
- **Stale or contradicts what you find** — say so and ask whether to keep it,
  update it, or use the filesystem.
- **Fresh Linear/Jira resolution** (not a trusted existing pointer) — write
  repo-root `TASKS.local.md` with **Source**, **Site / workspace**, **Project /
  team key**, **Resolved**, **Resolved by**. Use the `tasks` skill's
  `assets/tasks-local.template.md` when present. GitHub/GitLab and filesystem do not
  get a pointer. Tell the user it was written and should be gitignored; do not
  edit `.gitignore` unless asked.

## 2. Detect the source system

Match reachable tools against the argument's shape. A tool being available
does not mean the ID belongs to it.

| System | Available when | ID shape |
| ------ | -------------- | -------- |
| Linear | Linear MCP | `{TEAM}-{n}` (`ENG-45`) |
| Jira | Atlassian MCP | `{PROJECT}-{n}` (`CHK-123`) |
| GitHub / GitLab | GitHub/GitLab MCP, or `gh`/`glab`; remote from `git remote -v` | `#123`, or a bare number in context |
| Filesystem | Always | kebab-case slug or `{PREFIX}{nn}` matching a `docs/product/backlog.md` row |

**Jira and Linear share `PREFIX-NUMBER`.** Stop at the first that applies:

1. **User named the system** — use it.
2. **Only one of Linear/Jira has reachable MCP, and nothing in view names the
   other** — use it; say which and why.
3. **Both reachable, neither reachable, or a named system has no tool** — ask.
   Do not default.
4. **No tracker reachable and the ID matches no external shape** — filesystem.
   Confirm a `backlog.md` row or a task in some `{work-dir}/TASKS.local.md`; if
   neither, ask whether this is new work or a typo.

No `backlog.md` and no reachable tracker: ask which system they use before
writing anything — do not silently create a filesystem backlog.

## Type

Read type from the source: Jira issue type verbatim; Linear team/label type if
modelled else ask (do not default to `task`); GitHub/GitLab labels (`type:*`,
`kind/*`, `bug`, `epic`) if present else ask. Filesystem: a `backlog.md` row is
`epic`; in `TASKS.local.md`, `### S{n}` is `story` and a line under it (or
under `## Foundational` / `## Cross-cutting`) is `task`. A filesystem `bug` or
`spike` has no structural marker — ask.

**Known set:** `epic` · `story` · `task` · `bug` · `spike` — starting
vocabulary, not a whitelist. Map the source's native type to the closest row
for *behaviour* only; keep the system's own label in artefacts. If unclear, ask.

| Type | Decomposes into | Own AC? | Typical next skill |
| ---- | ---------------- | ------- | ------------------ |
| `epic` | Stories and tasks | No — AC on its stories | **design**, **tasks** |
| `story` | Tasks | Yes — primary AC holder | **tasks**, **design** if needed |
| `task` | Nothing (unit of work) | Inherits story AC, or own if foundational | **implement** |
| `bug` | Nothing, unless large enough for sub-tasks | Yes — repro as Given/When, fix as Then | **implement** |
| `spike` | Nothing — time-boxed | No — produces a decision or document | **implement** the spike, then **adr** or **tasks** |

`tasks` asked to decompose a `task`, `bug`, or `spike` should confirm intent
rather than refuse or silently comply.

## ID and path

**Canonical ID.** A tracker's native key **is** the ID. Never generate a
parallel internal ID. Internal IDs (`{PREFIX}{nn}`, `{PREFIX}{nn}-{nn}`) exist
**only** when no external tracker resolved. Once written, never reuse or
renumber — append on add, mark removed on delete. Contract with **implement**,
**sprint-planning**, and **validate**.

**Work path.** `{work-dir}/` — one folder per item. Default
`specs/{work-short-name}/` (kebab-case, ≤2 words from the title). Fall back to
`{work-id}` when unknown. See
[delivery-conventions.md](delivery-conventions.md#work-short-name-work-short-name).
Design at `{work-dir}/design.md`; local breakdown at `{work-dir}/TASKS.local.md`.
A story/bug/spike with its own design lives in its own `{work-dir}/`,
alongside — not nested inside — its parent epic. Cross-reference by ID.
Canonical ID stays in artefact ID fields; only the directory uses the short
name. If a path segment is unsafe, ask rather than substituting.

**New work, no ID yet.** Tracker: ask whether to create it (if MCP write) or
wait for the ID — never assign an internal placeholder. Filesystem: next
internal ID in sequence.

## Ask-first checklist

Ask in one batch whenever any of these is true:

- [ ] No pointer and §2 did not resolve to a single system (case 3)
- [ ] Pointer's recorded system does not match what is reachable now
- [ ] Type does not map cleanly to a known behaviour
- [ ] The action doesn't make sense for the type (decompose a `spike` or `bug`)
- [ ] The item does not exist yet and it is unclear whether to create it
- [ ] The canonical ID is unsafe as a path segment

## Schema

Filesystem-only: epic = `docs/product/backlog.md` row; stories/tasks in
`{work-dir}/TASKS.local.md` when a local breakdown is required. Tracker-backed:
the tracker is source of truth — no shadow `backlog.md`. An epic that cannot
name a `product.md §7` outcome is undocumented value or unsupported scope —
say so rather than writing it.

**Priority:** `P0` blocks other work or phase exit; `P1` required for the phase
objective; `P2` wanted this phase (droppable); `P3` opportunistic.
**Status:** `To do` · `In progress` · `In review` · `Blocked` · `Done` — or the
source's native states mapped to these five. `Blocked` requires a named
blocker. Updated by **implement** (→ `In progress`), **code-review** (→ `In
review`), **validate** (→ `Done` or back), and **backlog-refine** — not by
**tasks** after the initial write.

### Epic

| Field | Req | Legal values |
| ----- | --- | ------------ |
| Work item ID | Yes | Tracker key (`CHK-1`); else `{PREFIX}{nn}` — 2–4 uppercase + two digits (`CHK01`) |
| Title | Yes | Noun phrase naming the outcome (`Checkout Foundation`) |
| Work path | Yes | `{work-dir}/` — default `specs/{work-short-name}/`; else `{work-id}` |
| Phase | Yes | A phase name in `roadmap.md` |
| Status | Yes | `To do` · `In progress` · `In review` · `Blocked` · `Done` (or tracker states, mapped) |
| Priority | Yes | `P0`–`P3` |
| Estimate | Yes | Fibonacci: 1, 2, 3, 5, 8, 13, 21. `TBD` only with a spike noted |
| Depends on | No | Other IDs, comma separated. Must be acyclic |
| Outcome | Yes | The `product.md §7` outcome this epic serves |

### Story

User-visible outcome inside an epic. **Carries the AC.** Story 1 is the MVP.
Wrong if you cannot write its independent test criterion. Own `design.md` is fine; cite the parent by ID, do not nest folders.

| Field | Req | Legal values |
| ----- | --- | ------------ |
| Work item ID | Yes | Tracker key; else `{EPIC-ID}-S{n}` (`CHK01-S2`) |
| Statement | Yes | *As a {role}, I want {capability}, so that {benefit}* |
| Independent test criterion | Yes | One sentence a reviewer can demonstrate |
| Priority | Yes | `P0`–`P3` |
| Acceptance | Yes | ≥1 Gherkin scenario; EARS where a rule is clearer ([acceptance-criteria.md](acceptance-criteria.md)) |
| Design | Rec | Link to the `design.md` section it implements |

### Task

Engineering work under one story, or standalone. Inherits its story's AC.
**Foundational tasks** — shared prerequisites, no parent story, own Gherkin, no
`[S{n}]`, live in §3. A "foundational" task that only one story needs belongs
to that story.

| Field | Req | Legal values |
| ----- | --- | ------------ |
| Work item ID | Yes | Tracker key; else `{EPIC-ID}-{nn}` (`CHK01-04`) or `{STORY-ID}-{nn}` (`CHK01-S2-01`) |
| Story label | Yes, unless foundational | `[S{n}]` matching its parent story |
| Parallel marker | No | `[P]` — different files from siblings, no incomplete dependency |
| Title | Yes | Imperative, specific (`Build checkout page shell`) |
| Deliverable | Yes | What exists when done, with **at least one concrete file path** |
| Status | Yes | `To do` · `In progress` · `In review` · `Blocked` · `Done` |
| Estimate | Yes | Fibonacci. Roughly a day. `TBD` not acceptable |
| Owner | No | `TBD` acceptable for an unassigned queue |
| Depends on | No | Other IDs, comma separated. Must be acyclic |
| Labels | No | `phase:{phase}`, plus free tags. Not `type:` |
| Design | Rec | `./design.md#section` |

### Bug

Defect against shipped behaviour. Leaf unless the fix spans more than one integration boundary.

| Field | Req | Legal values |
| ----- | --- | ------------ |
| Work item ID | Yes | Tracker key; else `{PREFIX}{nn}` |
| Title | Yes | Names the observed defect, not the fix |
| Reproduction | Yes | Given/When steps that reliably trigger it |
| Expected vs actual | Yes | What should happen vs what does |
| Acceptance | Yes | The reproduction's `Then` now holds; regression coverage named |
| Priority | Yes | `P0`–`P3`, weighted by user impact |
| Design | No | Only if the fix touches architecture — cite `ARCHITECTURE.md §{N}` |

### Spike

Time-boxed investigation. Never shipped code. The only item allowed a `TBD` estimate on what follows it.

| Field | Req | Legal values |
| ----- | --- | ------------ |
| Work item ID | Yes | Tracker key; else `{PREFIX}{nn}` |
| Question | Yes | The single question the spike must answer |
| Timebox | Yes | A concrete duration or points ceiling |
| Output | Yes | Decision, ADR candidate, or findings doc — named |
| Unblocks | Rec | Work item(s) whose estimate is `TBD` because of this question |
