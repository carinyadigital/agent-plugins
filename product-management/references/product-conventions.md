# Product conventions

Canonical rules for paths and artefact boundaries for product management skills.
Skills that write under `docs/product/` should read this file when resolving paths.

## Document layout

```text
docs/product/               product.md, roadmap.md, backlog.md
docs/research/              synthesis, competitive briefs, metrics reviews (optional)
docs/updates/               stakeholder updates (optional)
docs/work/{work-id}/        design.md, tasks.md — see delivery-conventions.md
docs/work/sprint-{id}/      plan.md, retrospective.md — see delivery-conventions.md
```

Override paths when the user names them explicitly in the request.

Decomposition artefacts (`docs/product/backlog.md`, `docs/work/{work-id}/`,
`docs/work/sprint-{id}/`) are owned by this plugin's delivery skills
(`tasks`, `backlog-refine`, `sprint-planning`, `sprint-retro`, `validate`).
Strategy skills read them but do not write them — see `delivery-conventions.md`.

## Progressive migration bridge

Prefer `docs/` artefact paths. When reading an input that is missing under
`docs/`, fall back to the legacy `.agency/` equivalent if present
(e.g. `.agency/product.md`, `.agency/roadmap.md`). **Write new and updated
artefacts only under `docs/`.** Do not migrate files silently.

Repo binding (`.agency/target.json`) and agency byproducts (`.agency/reviews/`)
stay under `.agency/` permanently.

## Artefact boundaries

| Content | Belongs in | Not in |
| ------- | ---------- | ------ |
| Business strategy, personas, outcomes, vision | `docs/product/product.md` | roadmap, backlog |
| Phase sequencing, exit criteria, themes | `docs/product/roadmap.md` | product, backlog |
| Feature spec, user stories, requirements, success metrics | feature spec / PRD | product (strategy only) |
| Research themes, personas, opportunity areas | research synthesis | product (cite only) |
| Competitor comparison, positioning, implications | competitive brief | product, roadmap |
| Metrics scorecard, trends, recommended actions | metrics review | stakeholder update |
| Audience-tailored status, launch notes, risk escalation | stakeholder update | metrics review |
| Epic list, deps, points, work paths | `docs/product/backlog.md` (tasks) | product, roadmap |
| Story statement, test criterion, Gherkin AC | `docs/work/{work-id}/tasks.md` (tasks) | product artefacts |

## Skill routing (near-misses)

| User intent | Skill |
| ----------- | ----- |
| PRD, vision, why/who/what | **product** |
| Feature spec from a problem statement | **write-spec** |
| Phases, exit criteria | **roadmap** |
| Explore a problem space, stress-test thinking | **product-brainstorming** |
| Themes from interviews, surveys, tickets | **synthesize-research** |
| Compare competitors, battle cards | **competitive-brief** |
| Metrics scorecard, trends, actions | **metrics-review** |
| Status for leadership, launch note, risk escalation | **stakeholder-update** |
| Decompose product/roadmap or a spec into a backlog | **tasks --product** |
| Groom a backlog, check sprint readiness | **backlog-refine** |
| Plan or review a sprint | **sprint-planning**, **sprint-retro** |
| Sign off a work item vs AC and roadmap gates | **validate** |
| Review or critique an existing product.md / roadmap.md | **/product-engineering:docs-review** |

## Companion practices (cross-plugin)

Architecture skills live in `architecture` (`/architecture:solution`,
`/architecture:adr`). Engineering skills live in `product-engineering`
(`/product-engineering:tdd`, `implement`, `code-review`, `docs-review`, …).

When companions are not installed, continue from user input. At architecture
boundaries:

```text
Install: /plugin install architecture@carinya-plugins
Then run: /architecture:solution
```

## Agency layout notes

Repo identity lives in `.agency/target.json` (`name`, `instance`, `target`) — not inferred from the directory name.

Agent byproducts (competitor scans, metrics digests, stakeholder digests) write under:

```text
.agency/reviews/
```
