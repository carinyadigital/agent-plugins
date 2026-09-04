# Web development conventions

Canonical rules for paths, target binding, artefact consumption, and skill
boundaries. All `engineering` skills read this file when resolving paths or
routing near-miss requests.

## Target binding

Resolve the working target before reading stack-specific config or writing code.
Apply this order — first match wins:

1. **Explicit path named by the user** in the request.
2. **Inside a target repo** — `config/target.json` exists at the working
   root → read the pointer, resolve instance root and target metadata.
3. **Inside an instance repo** — `config/instance.json` at working root → use
   `config/targets/{target}.json` when the user names a target slug.
4. **Standalone** — no instance or target pointer → treat the current project as
   the target; read `AGENTS.md` / `CLAUDE.md` for local conventions.

`setup` may create `config/target.json` on first-time binding when
the user confirms target association.

## Brand guide (artifact consumption)

Before implementing UI, read `<resolved-brand-path>/brand-guide.md` for design
tokens, colors, typography, and UI patterns. Resolve the brand directory using the
same order as `brand-creative` conventions:

1. **Explicit path named by the user** in the request.
2. **Inside an instance repo** — `config/instance.json` at working root →
   `<instance-root>/brand/`.
3. **Inside a target repo** — `config/target.json` at working root →
   resolve instance root, then `<instance-root>/brand/`.
4. **Standalone** — no instance or target pointer → `docs/brand/` in the current
   project.

If `brand-guide.md` does not exist, ask the user for design guidance inline — do
not require `brand-creative` to be installed. Do not bundle or invoke the
brand-guide skill; read the artefact directly.

## UX design output (artifact consumption)

When a UX design practice has produced wireframes or specs, read from
`<instance-root>/design/` (or the path named by the user). Work-item
implementation specs live at `{work-dir}/design.md` (rename legacy `tdd.md` first).

## Companion practice (architecture)

For system solution design and ADRs, invoke companion skills directly — do not
bundle local copies:

| Need | Invoke |
| ---- | ------ |
| System architecture (`ARCHITECTURE.md`) | `/architecture:solution` |
| ADR plan / write / review | `/architecture:adr` |

Recommend `architecture` as a co-install. Document in CONNECTORS.md.

When `architecture` is **not installed**, continue from existing
`ARCHITECTURE.md` / ADR artefacts when present. At write boundaries:

```text
Install: /plugin install architecture@carinya-plugins
Then run: /architecture:solution
```

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
ARCHITECTURE.md               system architecture (arc42)
docs/decisions/               register.md, ADR-NNNN-*.md
specs/{work-short-name}/          design.md; TASKS.local.md when required
specs/{work-short-name}/reviews/  code-review verdict + co-located .local.json;
                                 ux-design-review verdicts
docs/work/sprint-{id}/        plan.md, retrospective.md
reviews/                      ux-design-review shared state (*.local.json); gitignored,
                              never committed. code-review does not write here.
docs/reviews/                 agent byproducts (competitor-scan, metrics, digests)
config/target.json            target binding
```

Repo identity lives in `config/target.json` (`name`, `instance`, `target`) — not inferred from the directory name.

Override paths when the user names them explicitly in the request.

Work-item ID resolution (any work item, not epic-only) is defined in
[work-items.md](work-items.md) and
[delivery-conventions.md](delivery-conventions.md).

## Artefact boundaries

| Content | Belongs in | Not in |
| ------- | ---------- | ------ |
| Business strategy, personas, outcomes | `docs/product/product.md` | backlog, architecture |
| Phase sequencing, exit criteria | `docs/product/roadmap.md` | backlog, product |
| Epic list, deps, points, work paths | `docs/product/backlog.md` | roadmap detail |
| Architecture, NFRs, cross-epic patterns | `ARCHITECTURE.md` | design (cite only) |
| ADR decisions | `docs/decisions/` | ARCHITECTURE.md narrative |
| Work-item implementation spec | `{work-dir}/design.md` | architecture, backlog |
| Task Gherkin (and optional EARS) | `specs/{work-short-name}/TASKS.local.md` | backlog, the Solution Design |
| Sprint plan / retro | `docs/work/sprint-{id}/` | product backlog |

## Doc comments

Comments written into source, tests, config, or any other repo file MUST
stand on their own so they can be read inline. They MUST NOT cite issue
systems, working documents, or any other external source. Canonical agent
instructions: [doc-comments.md](doc-comments.md).

## Acceptance criteria

- **Default:** Gherkin in `specs/{work-short-name}/TASKS.local.md`, on the **story** (or the work item itself when it carries AC).
- **EARS:** optional via `/product-management:tasks --ears` or when rules are clearer than scenarios.
- **Backlog:** epic scope only; no full Gherkin in `backlog.md` (use **tasks**).

## Solution Design modes

| Mode | When | Size |
| ---- | ---- | ---- |
| `skeleton` | Phase 0 (walking skeleton) | 2–4 pages |
| `full` | Sprint 2+ | 5–10 pages |

Cite `ARCHITECTURE.md §{N}` — do not re-narrate architecture in `design.md`.
The Solution Design applies at whatever level the user names (`design CHK01`,
`design JIRA-123`). If only a legacy `tdd.md` exists, rename it to `design.md`
before updating.

## Personas

Five personas share one skill library. Choose the default persona during
`setup` (merged for one-person shops; distinct for larger teams).

| Persona | Primary skills | Focus |
| ------- | -------------- | ----- |
| **Frontend Engineer** | `implement`, `code-review-fix`, `merge-request`, `merge-request-watch` | Build — UI, client state, styling |
| **Senior Frontend Engineer** | `code-review`, `design`, `/design:ux-design-review` | Peer review — diffs vs design and AC |
| **Principal Frontend Engineer** | `code-review`, `design`, `discovery-review` | Architecture, AC, Ready-for-Development gate |
| **QA Engineer** | `deploy-qa`, `run-automated-suite`, `exploratory-pass`, `document-defects` | Validation — automated and exploratory QA |
| **WebOps Engineer** | `deploy-qa`, `debug`, `platform-health` | Platform — CI/CD, deploy, health |

System architecture (`solution`, `adr`) lives in the **architecture** companion.
Work-item sign-off uses `/product-management:validate` (companion skill), not a local copy.

## Skill routing (near-misses)

| User intent | Skill | Persona |
| ----------- | ----- | ------- |
| System architecture | `/architecture:solution` | Companion — Principal Architect |
| ADR write/review | `/architecture:adr` | Companion — Principal Architect |
| Prepare a work item until Ready for Development | **discover agent** | Senior FE / Principal FE |
| `design.md` for one work item | **design** | Senior FE / Principal FE |
| Deliver every task through a merge-ready MR | **deliver agent** | Frontend Engineer |
| Implement code | **implement** | Frontend Engineer |
| PR / branch / MR code review | **code-review** | Senior FE / Principal FE |
| Address review feedback | **code-review-fix** | Frontend Engineer |
| Open merge request | **merge-request** | Frontend Engineer |
| Watch MR to merge-ready | **merge-request-watch** | Frontend Engineer |
| Discovery complete / Ready for Development | **discovery-review** | Senior FE / Principal FE |
| UX review of implemented UI | **/design:ux-design-review** | Frontend Engineer |
| Address UX review feedback | **/design:ux-design-fix** | Frontend Engineer |
| Run autonomous delivery loop | **/ralph-loop:ralph-loop** | Frontend Engineer |
| Review a document set | **docs-review** | Principal FE / any |
| Bug investigation | **debug** | WebOps Engineer |
| Technical debt audit | **tech-debt** | Principal FE / WebOps |
| QA workspace prep | **deploy-qa** | QA / WebOps |
| Run automated tests | **run-automated-suite** | QA Engineer |
| Exploratory AC pass | **exploratory-pass** | QA Engineer |
| Document defects | **document-defects** | QA Engineer |
| Platform health check | **platform-health** | WebOps Engineer |
| PRD, phases, tasks, backlog-refine, sprint-*, validate | `/product-management:*` | Companion — any persona |

When the `design` companion plugin is not installed: continue with code review only; recommend `/plugin install design@carinya-plugins` before UI-heavy work.
