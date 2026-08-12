# Web development conventions

Canonical rules for paths, target binding, artefact consumption, and skill
boundaries. All `product-engineering` skills read this file when resolving paths or
routing near-miss requests.

## Target binding

Resolve the working target before reading stack-specific config or writing code.
Apply this order — first match wins:

1. **Explicit path named by the user** in the request.
2. **Inside a target repo** — `.agency/target.json` exists at the working
   root → read the pointer, resolve instance root and target metadata.
3. **Inside an instance repo** — `config/instance.json` at working root → use
   `config/targets/{target}.json` when the user names a target slug.
4. **Standalone** — no instance or target pointer → treat the current project as
   the target; read `AGENTS.md` / `CLAUDE.md` for local conventions.

`setup` may create `.agency/target.json` on first-time binding when
the user confirms target association.

## Brand guide (artifact consumption)

Before implementing UI, read `<resolved-brand-path>/brand-guide.md` for design
tokens, colors, typography, and UI patterns. Resolve the brand directory using the
same order as `brand-creative` conventions:

1. **Explicit path named by the user** in the request.
2. **Inside an instance repo** — `config/instance.json` at working root →
   `<instance-root>/brand/`.
3. **Inside a target repo** — `.agency/target.json` at working root →
   resolve instance root, then `<instance-root>/brand/`.
4. **Standalone** — no instance or target pointer → `docs/brand/` in the current
   project.

If `brand-guide.md` does not exist, ask the user for design guidance inline — do
not require `brand-creative` to be installed. Do not bundle or invoke the
brand-guide skill; read the artefact directly.

## UX design output (artifact consumption)

When a UX design practice has produced wireframes or specs, read from
`<instance-root>/design/` (or the path named by the user). Falls back to
`docs/work/{work-id}/design.md` for work-item implementation specs (fall back to `.agency/work/` when reading legacy artefacts).

## Companion practice (delivery)

For sprint participation, backlog grooming, task writing, and epic validation during
implementation, invoke companion skills directly — do not bundle local copies:

| Need | Invoke |
| ---- | ------ |
| Epics / backlog from product | `/product-management:tasks --product` |
| Task Gherkin AC | `/product-management:tasks` |
| Groom backlog or check sprint readiness | `/product-management:backlog-refine` |
| Sprint plan | `/product-management:sprint-planning` |
| Sprint retrospective | `/product-management:sprint-retro` |
| Work-item completion sign-off | `/product-management:validate` |
| Which planning skill to use | `/skills-index:find` |

Recommend `product-management` as a co-install. Document in CONNECTORS.md.

When a companion plugin is **not installed**, do not emit a bare slash command.
State what you can do without it, then:

```text
Install: /plugin install product-management@carinya-plugins
Then run: /product-management:<skill> …
```

See `docs/CROSS-PLUGIN-CONTRACTS.md` (monorepo) for the full edge list.

## Document layout

```text
docs/product/                 product.md, roadmap.md, backlog.md
docs/architecture/            solution.md, decisions/register.md, ADR-NNNN-*.md
docs/work/{work-id}/          design.md, tasks.md
docs/work/{work-id}/reviews/  code-review / ux-design-review verdicts
docs/work/sprint-{id}/        plan.md, retrospective.md
docs/reviews/                 shared review state (*.local.json)
.agency/target.json           target binding (permanent)
.agency/reviews/              agent byproducts: competitor-scan, metrics, digests
```

Repo identity lives in `.agency/target.json` (`name`, `instance`, `target`) — not inferred from the directory name.

Override paths when the user names them explicitly in the request.

## Progressive migration bridge

Prefer `docs/` artefact paths. When reading an input missing under `docs/`,
fall back to the legacy `.agency/` equivalent if present. Write new and
updated delivery/engineering artefacts only under `docs/`. Keep
`.agency/target.json` and `.agency/reviews/` byproducts under `.agency/`.

Work-item ID resolution (any work item, not epic-only) is defined in
[work-item-resolution.md](work-item-resolution.md) and
[delivery-conventions.md](delivery-conventions.md).

## Artefact boundaries

| Content | Belongs in | Not in |
| ------- | ---------- | ------ |
| Business strategy, personas, outcomes | `docs/product/product.md` | backlog, solution |
| Phase sequencing, exit criteria | `docs/product/roadmap.md` | backlog, product |
| Epic list, deps, points, work paths | `docs/product/backlog.md` | roadmap detail |
| Architecture, NFRs, cross-epic patterns | `docs/architecture/solution.md` | design (cite only) |
| ADR decisions | `docs/architecture/decisions/` | solution narrative |
| Work-item implementation spec | `docs/work/{work-id}/design.md` | solution, backlog |
| Task Gherkin (and optional EARS) | `docs/work/{work-id}/tasks.md` | backlog, design |
| Sprint plan / retro | `docs/work/sprint-{id}/` | product backlog |

## Acceptance criteria

- **Default:** Gherkin in `docs/work/{work-id}/tasks.md`, on the **story** (or the work item itself when it carries AC).
- **EARS:** optional via `/product-management:tasks --ears` or when rules are clearer than scenarios.
- **Backlog:** epic scope only; no full Gherkin in `backlog.md` (use **tasks**).

## Design modes

| Mode | When | Size |
| ---- | ---- | ---- |
| `walking-skeleton` | Phase 0 | 2–4 pages |
| `tdd` | Sprint 2+ | 5–10 pages |

Cite `solution.md §{N.M}` — do not re-narrate architecture in `design.md`.
Design applies at whatever level the user names (`design CHK01`, `design JIRA-123`).

## Personas

Six personas share one skill library. Choose the default persona during
`setup` (merged for one-person shops; distinct for larger teams).

| Persona | Primary skills | Focus |
| ------- | -------------- | ----- |
| **Frontend Engineer** | `implement`, `code-review-fix`, `merge-request`, `ux-design-fix` | Build — UI, client state, styling |
| **Senior Frontend Engineer** | `code-review`, `design`, `ux-design-review` | Peer review — diffs vs design and AC |
| **Principal Frontend Engineer** | `final-code-review`, `code-review`, `design` | Final gate — architecture and AC on open PRs |
| **Principal Architect** | `solution`, `adr`, `design`, `docs-review` | Architecture — solution, ADRs, epic design |
| **QA Engineer** | `deploy-qa`, `run-automated-suite`, `exploratory-pass`, `document-defects` | Validation — automated and exploratory QA |
| **WebOps Engineer** | `deploy-qa`, `debug`, `platform-health` | Platform — CI/CD, deploy, health |

Work-item sign-off uses `/product-management:validate` (companion skill), not a local copy.

## Skill routing (near-misses)

| User intent | Skill | Persona |
| ----------- | ----- | ------- |
| System architecture | **solution** | Principal Architect |
| ADR write/review | **adr** | Principal Architect |
| `design.md` for one work item | **design** | Senior FE / Principal FE / Architect |
| Implement code | **implement** | Frontend Engineer |
| PR / branch code review | **code-review** | Senior FE / Principal FE |
| Address review feedback | **code-review-fix** | Frontend Engineer |
| Final PR gate | **final-code-review** | Principal Frontend Engineer |
| Open merge request | **merge-request** | Frontend Engineer |
| Babysit MR/PR to merge-ready | **merge-request-babysit** | Frontend Engineer |
| Review MR/PR as reviewer | **merge-request-review** | Senior FE / Principal FE |
| UX review of implemented UI | **/product-design:ux-design-review** | Frontend Engineer |
| Address UX review feedback | **/product-design:ux-design-fix** | Frontend Engineer |

When `product-design` is not installed: continue with code review only; recommend
`/plugin install product-design@carinya-plugins` before UI-heavy work.
| Run autonomous delivery loop | **/ralph-loop:ralph-loop** | Frontend Engineer |
| Review a document set | **docs-review** | Principal Architect |
| Bug investigation | **debug** | WebOps Engineer |
| Technical debt audit | **tech-debt** | Principal Architect |
| QA workspace prep | **deploy-qa** | QA / WebOps |
| Run automated tests | **run-automated-suite** | QA Engineer |
| Exploratory AC pass | **exploratory-pass** | QA Engineer |
| Document defects | **document-defects** | QA Engineer |
| Platform health check | **platform-health** | WebOps Engineer |
| PRD, phases, tasks, backlog-refine, sprint-*, validate | `/product-management:*` | Companion — any persona |
