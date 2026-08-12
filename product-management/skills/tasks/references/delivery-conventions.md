# Delivery conventions

Canonical rules for paths, work items, and artefact boundaries. Skills that
touch `docs/work/{work-id}/` should read this file when resolving a work item
argument or writing under `docs/work/`.

## Document layout

```text
docs/product/               product.md, roadmap.md, backlog.md
docs/architecture/          solution.md, decisions/register.md, ADR-*.md
docs/work/{work-id}/        tdd.md, tasks.md — one folder per resolved work item
docs/work/{work-id}/reviews/  code-review-{nn}.local.md, ux-design-review-{nn}.local.md
                            ({nn} sequential per skill prefix, not across skills)
docs/work/sprint-{id}/      plan.md, retrospective.md
docs/reviews/               code-review.local.json, ux-design-review.local.json,
                             review-learnings.local.md, and the latest-only
                             {skill}-{branch}.local.md when no work item
                             resolved
```

Override paths when the user names them explicitly in the request.

## Work item ID (`{work-id}`)

Any work item — epic,
story, task, bug, spike, or whatever type the source system defines — can be
the target of `tasks`, `tdd`, `validate`, `backlog-refine`,
`ralph-loop-setup`, and `implement`. What changes is the *behaviour* for that
type, not whether the ID is accepted.

Read [work-item-resolution.md](work-item-resolution.md) in full before
resolving `{work-id}` — it covers:

- Detecting the source system (Linear, Jira, GitHub/GitLab issues, or
  filesystem) and the `TASKS.local.md` pointer that caches Linear/Jira
  detection
- The **golden rule**: ask the user on any ambiguity in system, ID, or type —
  never guess
- Why the canonical ID is the tracker's own key when one exists, and why
  internal IDs (`{PREFIX}{nn}`, `{PREFIX}{nn}-{nn}`) are a filesystem-only
  source, never a parallel scheme alongside a tracker

| Rule | Detail |
| ---- | ------ |
| Canonical ID | Tracker key (`JIRA-123`, `ENG-45`) when a tracker resolved; internal ID only when filesystem is the source |
| Work path | `docs/work/{work-id}/` — keyed by *this* item's own canonical ID, at whatever level it sits |
| Parent linkage | By ID reference in the artefact, never by nesting one work item's folder inside another's |

**Filesystem-only source** still uses slugs for the top-level backlog
folder name when no tracker exists, exactly as before:

| Title | Internal ID | Work path |
| ----- | ----------- | ------- |
| Checkout Foundation | `CHK01` | `docs/work/checkout-foundation/` |
| Payment and Placement | `CHK02` | `docs/work/payment-placement/` |

The slug is derived from the title (kebab-case, at most two words) and is
**not** the ID — `CHK01` is the ID, `checkout-foundation` is the folder name.
This distinction disappears once a tracker is in play: the folder *is* the ID
(`docs/work/JIRA-123/`), because the tracker key is already a stable, unique,
filesystem-safe handle and slugging it again only adds a translation step.

## Artefact boundaries

| Content | Belongs in | Not in |
| ------- | ---------- | ------ |
| Business strategy, personas, outcomes | `docs/product/product.md` | backlog, solution |
| Phase sequencing, exit criteria | `docs/product/roadmap.md` | backlog, product |
| Epic list, deps, points, work paths | `docs/product/backlog.md` (filesystem-only source) | roadmap detail |
| Story/task statement, test criterion, AC | `docs/work/{work-id}/tasks.md` | backlog (titles only) |
| Architecture, NFRs, cross-epic patterns | `docs/architecture/solution.md` | the TDD (cite only) |
| ADR decisions | `register.md`, `ADR-NNNN-*.md` | solution narrative |
| Work item implementation spec | `docs/work/{work-id}/tdd.md` | solution, backlog |
| Task Gherkin (and optional EARS) | `docs/work/{work-id}/tasks.md` | backlog, the TDD |
| Sprint plan / retro | `docs/work/sprint-{id}/` | product backlog |
| Human-readable review verdict | `docs/work/{work-id}/reviews/{skill}-{nn}.local.md` | shared JSON state |
| Review tracking state (per branch, incremental) | `docs/reviews/{skill}.local.json` | human-readable verdicts |

`docs/product/backlog.md` is a filesystem-only artefact: it exists only
in repos with no external tracker resolved. When Linear or Jira is the
source, the tracker itself is the backlog — skills read epic/initiative lists
from it directly rather than maintaining a parallel `backlog.md`.

## Acceptance criteria

- **Default:** Gherkin in `docs/work/{work-id}/tasks.md`, on the **story** (or
  on the work item itself when it carries its own AC, e.g. a bug's repro/fix
  scenario). A foundational task with no parent story carries its own.
- **EARS:** via `tasks --ears`, or where a rule is clearer than a scenario.
  Five patterns: see `skills/tasks/references/acceptance-criteria.md`.
- **Backlog:** epic scope only; no full Gherkin in `backlog.md` (use **tasks**).
- **Schema:** field-by-field rules in `skills/tasks/references/work-item-schema.md`.

## TDD modes

The technical design document (`tdd.md`) has two modes:

| Mode | When | Size |
| ---- | ---- | ---- |
| `skeleton` | Phase 0 (walking skeleton) | 2–4 pages |
| `full` | Sprint 2+ | 5–10 pages |

Cite `solution.md §{N.M}` — do not re-narrate architecture in `tdd.md`.
The TDD applies at whatever level the user names: `tdd CHK01` writes the
epic's design; `tdd JIRA-123` writes that story's design, sitting beside
(not nested inside) its parent epic's folder and citing the parent by ID.

**Not test-driven development.** The `tdd` skill writes a design document.
Writing a failing test first, red/green/refactor, and test authoring in
general belong to **implement**.

## Skill routing (near-misses)

| User intent | Skill |
| ----------- | ----- |
| PRD, vision, why/who/what | **product** |
| Phases, exit criteria | **roadmap** |
| Epics, work paths, Now scope | **tasks --product** |
| `tdd.md` (technical design) for one work item | **tdd** |
| System architecture (`solution.md`) | **/architecture:solution** |
| ADR plan / write / review | **/architecture:adr** |
| `tasks.md`, stories, Gherkin AC | **tasks** |
| Decompose any spec or RFC into a backlog | **tasks** |
| Groom a backlog, check sprint readiness | **backlog-refine** |
| Implement code | **implement** |
| PR / branch code review | **code-review** |
| Address code review feedback | **code-review-fix** |
| Work item done vs AC + roadmap gates | **validate** |
| Sprint plan | **sprint-planning** |
| Sprint retrospective | **sprint-retro** |
| Review a set of documents for quality, boundaries, consistency | **docs-review** |
