# Delivery conventions

Canonical rules for paths, epics, and artefact boundaries. Skills that touch
`docs/work/{epic}/` should read this file when resolving `{epic}` or writing under
`docs/work/`.

## Document layout

```text
docs/product/          product.md, roadmap.md, backlog.md
docs/architecture/     solution.md, decisions/register.md, ADR-*.md
docs/work/{epic}/           design.md, tasks.md, refine-session.md
docs/work/sprint-{id}/      plan.md, retrospective.md
```

Override paths when the user names them explicitly in the request.

## Epic slug (`{epic}`)

| Rule | Detail |
| ---- | ------ |
| Source | Epic **title** or **short title** from `docs/product/backlog.md` |
| Format | kebab-case, **at most two words** |
| Not the ID | `CHK01` → resolve row → e.g. `checkout-foundation` |
| Work path | `docs/work/{epic}/` (trailing slash in tables is fine) |

| Title | Slug | Invalid |
| ----- | ---- | ------- |
| Checkout Foundation | `checkout-foundation` | `checkout-foundation-wp` |
| Payment and Placement | `payment-placement` | `payment-and-placement` (3 words) |
| Order Confirmation | `order-confirmation` | `CHK01` (ID, not slug) |

**Resolve `{epic}` when the user passes:**

- Slug: `checkout-foundation`
- Epic ID: `CHK01` → read backlog row → slug
- Path: `docs/work/checkout-foundation/` or `.../tasks.md`

## Artefact boundaries

| Content | Belongs in | Not in |
| ------- | ---------- | ------ |
| Business strategy, personas, outcomes | `docs/product/product.md` | backlog, solution |
| Phase sequencing, exit criteria | `docs/product/roadmap.md` | backlog, product |
| Epic list, deps, points, work paths | `docs/product/backlog.md` | roadmap detail |
| Architecture, NFRs, cross-epic patterns | `docs/architecture/solution.md` | design (cite only) |
| ADR decisions | `register.md`, `ADR-NNNN-*.md` | solution narrative |
| Epic implementation spec | `docs/work/{epic}/design.md` | solution, backlog |
| Task Gherkin (and optional EARS) | `docs/work/{epic}/tasks.md` | backlog, design |
| Sprint plan / retro | `docs/work/sprint-{id}/` | product backlog |

## Acceptance criteria

- **Default:** Gherkin in `docs/work/{epic}/tasks.md` (≥1 scenario per task).
- **EARS:** optional via `tasks write --ears` or when rules are clearer than scenarios.
- **Backlog:** epic scope only; no full Gherkin in `backlog.md` (use **tasks**).

## Design modes

| Mode | When | Size |
| ---- | ---- | ---- |
| `walking-skeleton` | Phase 0 | 2–4 pages |
| `tdd` | Sprint 2+ | 5–10 pages |

Cite `solution.md §{N.M}` — do not re-narrate architecture in `design.md`.

## Skill routing (near-misses)

| User intent | Skill |
| ----------- | ----- |
| PRD, vision, why/who/what | **product** |
| Phases, exit criteria | **roadmap** |
| Epics, work paths, Now scope | **backlog** |
| `design.md` for one epic | **design** |
| `tasks.md`, Gherkin AC | **tasks** |
| Implement code | **implement** |
| PR / branch code review | **code-review** |
| Address code review feedback | **code-review** `fix` |
| Epic done vs AC + roadmap gates | **validate** |
| Sprint plan or retro | **sprint** |
| Pre-sprint doc review / post-sprint doc pass | **docs** |
| Which skill to use? | **skills-index** |
| Bug investigation | **debug** |
| Technical debt audit | **tech-debt** |
| Feature spec or PRD from an idea | **write-spec** |
| Stakeholder status update | **stakeholder-update** |
| User research synthesis | **synthesize-research** |
| Competitive analysis brief | **competitive-brief** |
| Product metrics review | **metrics-review** |
| Brainstorm / spar on an idea | **product-brainstorming** |
