# Product conventions

Canonical rules for paths and artefact boundaries for product management skills.
Skills that write under `.agency/` should read this file when resolving paths.

## Document layout

```text
.agency/          product.md, roadmap.md
.agency/research/         synthesis, competitive briefs, metrics reviews (optional)
.agency/updates/          stakeholder updates (optional)
```

Override paths when the user names them explicitly in the request.

Decomposition artefacts (`backlog.md`, `work/{epic}/`, `sprints/`) are owned by the
companion `delivery-practice` plugin — product skills read them but do not write them.

## Artefact boundaries

| Content | Belongs in | Not in |
| ------- | ---------- | ------ |
| Business strategy, personas, outcomes, vision | `.agency/product.md` | roadmap, backlog |
| Phase sequencing, exit criteria, themes | `.agency/roadmap.md` | product, backlog |
| Feature spec, user stories, requirements, success metrics | feature spec / PRD | product (strategy only) |
| Research themes, personas, opportunity areas | research synthesis | product (cite only) |
| Competitor comparison, positioning, implications | competitive brief | product, roadmap |
| Metrics scorecard, trends, recommended actions | metrics review | stakeholder update |
| Audience-tailored status, launch notes, risk escalation | stakeholder update | metrics review |
| Epic list, deps, points, work paths | `.agency/backlog.md` (delivery-practice) | product, roadmap |
| Story statement, test criterion, Gherkin AC | `.agency/work/{epic}/tasks.md` (delivery-practice) | product artefacts |

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
| Which skill to use? | **skills-index** |

## Companion practices (cross-plugin)

Decomposition and delivery cadence live in `delivery-practice`. Invoke as
`/delivery-practice:<skill>` when recommending from product-management:

| Intent | Skill |
| ------ | ----- |
| Decompose product/roadmap or a spec into a backlog | **/delivery-practice:tasks --product** |
| Groom a backlog, check sprint readiness | **/delivery-practice:backlog-refine** |
| Plan or review a sprint | **/delivery-practice:sprint-planning**, **/delivery-practice:sprint-retro** |
| Sign off an epic vs AC and roadmap gates | **/delivery-practice:validate** |

Architecture and engineering skills live in `web-development`
(`/web-development:solution`, `design`, `implement`, `code-review`, …).

## Agency layout notes

Repo identity lives in `.agency/target.json` (`name`, `instance`, `target`) — not inferred from the directory name.

Agent byproducts (competitor scans, metrics digests, stakeholder digests) write under:

```text
.agency/reviews/
```
