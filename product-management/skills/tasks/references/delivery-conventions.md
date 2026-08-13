# Delivery conventions

Canonical rules for paths, work items, and artefact boundaries. Skills that
touch `specs/{work-short-name}/` should read this file when resolving a work
item argument or writing under `specs/`.

## Document layout

```text
docs/product/               product.md, roadmap.md, backlog.md
docs/architecture/          solution.md, decisions/register.md, ADR-*.md
specs/{work-short-name}/    tdd.md; TASKS.local.md when a local task breakdown
                            is required — one folder per resolved work item
specs/{work-short-name}/reviews/  code-review-{nn}.local.md, ux-design-review-{nn}.local.md
                            ({nn} sequential per skill prefix, not across skills)
docs/work/sprint-{id}/      plan.md, retrospective.md
reviews/                    code-review.local.json, ux-design-review.local.json,
                             review-learnings.local.md, and the latest-only
                             {skill}-{branch}.local.md when no work item
                             resolved (gitignored — never committed)
docs/reviews/               agent byproducts (competitor-scan, metrics, digests)
TASKS.local.md              repo-root tracker-pointer cache (Linear/Jira only;
                            gitignored — not the work-item task list)
```

Override paths when the user names them explicitly in the request.

Sprint plans, retrospectives, and other non-work-item delivery docs stay under
`docs/work/`. Only the artefacts for a specific work item live under `specs/`.

## Work item ID (`{work-id}`)

Any work item — epic,
story, task, bug, spike, or whatever type the source system defines — can be
the target of `tasks`, `tdd`, `validate`, `backlog-refine`,
`ralph-loop-setup`, and `implement`. What changes is the *behaviour* for that
type, not whether the ID is accepted.

Read [work-item-resolution.md](work-item-resolution.md) in full before
resolving `{work-id}` — it covers:

- Detecting the source system (Linear, Jira, GitHub/GitLab issues, or
  filesystem) and the repo-root `TASKS.local.md` pointer that caches Linear/Jira
  detection
- The **golden rule**: ask the user on any ambiguity in system, ID, or type —
  never guess
- Why the canonical ID is the tracker's own key when one exists, and why
  internal IDs (`{PREFIX}{nn}`, `{PREFIX}{nn}-{nn}`) are a filesystem-only
  source, never a parallel scheme alongside a tracker

| Rule | Detail |
| ---- | ------ |
| Canonical ID | Tracker key (`JIRA-123`, `ENG-45`) when a tracker resolved; internal ID only when filesystem is the source |
| Work path | `specs/{work-short-name}/` — keyed by a short name of at most two words; fall back to `{work-id}` when a short name cannot be discovered |
| Parent linkage | By ID reference in the artefact, never by nesting one work item's folder inside another's |

## Work short name (`{work-short-name}`)

The folder under `specs/` is a **short name**, not the canonical ID.

- kebab-case, **at most two words** (one hyphen)
- derived from the work item title — the distinctive noun phrase, not a
  sentence (`Cart` → `cart`; `Checkout Foundation` → `checkout-foundation`)
- **not** the internal ID and **not** the tracker key when a short name is
  known — `CHK01` / `JIRA-123` are IDs; `cart` is the folder name

| Title | Canonical ID | Work path |
| ----- | ------------ | --------- |
| Cart | `CHK01` or `JIRA-123` | `specs/cart/` |
| Checkout Foundation | `CHK01` | `specs/checkout-foundation/` |
| Payment and Placement | `CHK02` | `specs/payment-placement/` |

Resolve `{work-short-name}` in this order — first match wins:

1. **User-named path** under `specs/` in the request.
2. **Existing `specs/` folder** whose `tdd.md` or `TASKS.local.md` names this
   work item's canonical ID.
3. **Backlog work path** (filesystem-only `backlog.md` row).
4. **Title slug** — kebab-case, at most two words, from the tracker title or
   backlog title.
5. **`{work-id}`** — when no title is available and no existing folder matches
   (`specs/JIRA-123/`, `specs/CHK01/`).

If two candidate short names are plausible, ask rather than guessing. Once a
folder exists, reuse it — do not rename on later runs.

A story, bug, or spike that gets its own design or further breakdown gets its
own `specs/{work-short-name}/` folder, alongside — not nested inside — its
parent epic's folder. Cross-reference the parent by ID in the artefact.

## Artefact boundaries

| Content | Belongs in | Not in |
| ------- | ---------- | ------ |
| Business strategy, personas, outcomes | `docs/product/product.md` | backlog, solution |
| Phase sequencing, exit criteria | `docs/product/roadmap.md` | backlog, product |
| Epic list, deps, points, work paths | `docs/product/backlog.md` (filesystem-only source) | roadmap detail |
| Story/task statement, test criterion, AC | `specs/{work-short-name}/TASKS.local.md` | backlog (titles only) |
| Architecture, NFRs, cross-epic patterns | `docs/architecture/solution.md` | the TDD (cite only) |
| ADR decisions | `register.md`, `ADR-NNNN-*.md` | solution narrative |
| Work item implementation spec | `specs/{work-short-name}/tdd.md` | solution, backlog |
| Task Gherkin (and optional EARS) | `specs/{work-short-name}/TASKS.local.md` | backlog, the TDD |
| Sprint plan / retro | `docs/work/sprint-{id}/` | product backlog, `specs/` |
| Human-readable review verdict | `specs/{work-short-name}/reviews/{skill}-{nn}.local.md` | shared JSON state |
| Review tracking state (per branch, incremental) | `reviews/{skill}.local.json` | human-readable verdicts |

`reviews/` is local review state. Skills that write it MUST ensure the target
repo's `.gitignore` contains a root-only `/reviews/` entry, and MUST NOT
commit anything under `reviews/`.

Repo-root `TASKS.local.md` is the Linear/Jira source-system pointer (see
work-item-resolution.md). `specs/{work-short-name}/TASKS.local.md` is the
work-item task list — write it only when a local breakdown is required
(filesystem-only source, or Gherkin that does not live in the tracker). Do
not confuse the two files.

`docs/product/backlog.md` is a filesystem-only artefact: it exists only
in repos with no external tracker resolved. When Linear or Jira is the
source, the tracker itself is the backlog — skills read epic/initiative lists
from it directly rather than maintaining a parallel `backlog.md`.

## Acceptance criteria

- **Default:** Gherkin in `specs/{work-short-name}/TASKS.local.md`, on the
  **story** (or on the work item itself when it carries its own AC, e.g. a
  bug's repro/fix scenario). A foundational task with no parent story carries
  its own. Skip the file when the tracker holds the breakdown and no local
  copy is needed.
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
| `TASKS.local.md`, stories, Gherkin AC | **tasks** |
| Decompose any spec or RFC into a backlog | **tasks** |
| Groom a backlog, check sprint readiness | **backlog-refine** |
| Implement code | **implement** |
| PR / branch code review | **code-review** |
| Address code review feedback | **code-review-fix** |
| Work item done vs AC + roadmap gates | **validate** |
| Sprint plan | **sprint-planning** |
| Sprint retrospective | **sprint-retro** |
| Review a set of documents for quality, boundaries, consistency | **docs-review** |
