# Delivery conventions

Canonical rules for paths, epics, and artefact boundaries. Skills that touch
`.agency/work/{epic}/` should read this file when resolving `{epic}` or writing under
`.agency/work/`.

## Document layout

```text
.agency/          product.md, roadmap.md, backlog.md
.agency/architecture/     solution.md, decisions/register.md, ADR-*.md
.agency/work/{epic}/           design.md, tasks.md
.agency/sprints/sprint-{id}/      plan.md, retrospective.md
```

Override paths when the user names them explicitly in the request.

## Epic slug (`{epic}`)

| Rule | Detail |
| ---- | ------ |
| Source | Epic **title** or **short title** from `.agency/backlog.md` |
| Format | kebab-case, **at most two words** |
| Not the ID | `CHK01` → resolve row → e.g. `checkout-foundation` |
| Work path | `.agency/work/{epic}/` (trailing slash in tables is fine) |

| Title | Slug | Invalid |
| ----- | ---- | ------- |
| Checkout Foundation | `checkout-foundation` | `checkout-foundation-wp` |
| Payment and Placement | `payment-placement` | `payment-and-placement` (3 words) |
| Order Confirmation | `order-confirmation` | `CHK01` (ID, not slug) |

**Resolve `{epic}` when the user passes:**

- Slug: `checkout-foundation`
- Epic ID: `CHK01` → read backlog row → slug
- Path: `.agency/work/checkout-foundation/` or `.../tasks.md`

## Artefact boundaries

| Content | Belongs in | Not in |
| ------- | ---------- | ------ |
| Business strategy, personas, outcomes | `.agency/product.md` | backlog, solution |
| Phase sequencing, exit criteria | `.agency/roadmap.md` | backlog, product |
| Epic list, deps, points, work paths | `.agency/backlog.md` | roadmap detail |
| Story statement, test criterion, AC | `.agency/work/{epic}/tasks.md` | backlog (titles only) |
| Architecture, NFRs, cross-epic patterns | `.agency/architecture/solution.md` | design (cite only) |
| ADR decisions | `register.md`, `ADR-NNNN-*.md` | solution narrative |
| Epic implementation spec | `.agency/work/{epic}/design.md` | solution, backlog |
| Task Gherkin (and optional EARS) | `.agency/work/{epic}/tasks.md` | backlog, design |
| Sprint plan / retro | `.agency/sprints/sprint-{id}/` | product backlog |

## Acceptance criteria

- **Default:** Gherkin in `.agency/work/{epic}/tasks.md`, on the **story**
  (≥1 scenario each). A foundational task with no parent story carries its own.
- **EARS:** via `tasks --ears`, or where a rule is clearer than a scenario.
  Five patterns: see `skills/tasks/references/acceptance-criteria.md`.
- **Backlog:** epic scope only; no full Gherkin in `backlog.md` (use **tasks**).
- **Schema:** field-by-field rules in `skills/tasks/references/work-item-schema.md`.

## Design modes

| Mode | When | Size |
| ---- | ---- | ---- |
| `walking-skeleton` | Phase 0 | 2–4 pages |
| `tdd` | Sprint 2+ | 5–10 pages |

Cite `solution.md §{N.M}` — do not re-narrate architecture in `design.md`.

## Skill routing (near-misses)

| User intent | Skill |
| ----------- | ----- |
| PRD, vision, why/who/what | **/product-management:product** (companion) |
| Phases, exit criteria | **/product-management:roadmap** (companion) |
| Epics, work paths, Now scope | **tasks --product** |
| `design.md` for one epic | **design** |
| `tasks.md`, stories, Gherkin AC | **tasks** |
| Decompose any spec or RFC into a backlog | **tasks** |
| Groom a backlog, check sprint readiness | **backlog-refine** |
| Implement code | **implement** |
| PR / branch code review | **code-review** |
| Address code review feedback | **code-review-fix** |
| Epic done vs AC + roadmap gates | **validate** |
| Sprint plan | **sprint-planning** |
| Sprint retrospective | **sprint-retro** |
| Review a set of documents for quality, boundaries, consistency | **docs-review** |
| Which skill to use? | **skills-index** |

## Agency layout notes

Repo identity lives in `.agency/target.json` (`name`, `instance`, `target`) — not inferred from the directory name.

Additional agency trees (not used by all skills):

```text
.agency/reviews/              agent byproducts: competitor-scan, metrics, digests
```

Cross-plugin skills live in `web-development` (design, implement, code-review, …)
and `product-management` (product, roadmap, write-spec, synthesize-research,
competitive-brief, metrics-review, stakeholder-update, product-brainstorming).
Invoke as `/web-development:<skill>` or `/product-management:<skill>` when
recommending from delivery-practice. `product.md` and `roadmap.md` are produced
by `product-management` and consumed here by `tasks --product`.

