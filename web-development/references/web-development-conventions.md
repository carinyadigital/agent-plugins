# Web development conventions

Canonical rules for paths, target binding, artefact consumption, and skill
boundaries. All `web-development` skills read this file when resolving paths or
routing near-miss requests.

## Target binding

Resolve the working target before reading stack-specific config or writing code.
Apply this order — first match wins:

1. **Explicit path named by the user** in the request.
2. **Inside a target repo** — `.digital-agency/target.json` exists at the working
   root → read the pointer, resolve instance root and target metadata.
3. **Inside an instance repo** — `config/instance.json` at working root → use
   `config/targets/{target}.json` when the user names a target slug.
4. **Standalone** — no instance or target pointer → treat the current project as
   the target; read `AGENTS.md` / `CLAUDE.md` for local conventions.

`setup` may create `.digital-agency/target.json` on first-time binding when
the user confirms target association.

## Brand guide (artifact consumption)

Before implementing UI, read `<resolved-brand-path>/brand-guide.md` for design
tokens, colors, typography, and UI patterns. Resolve the brand directory using the
same order as `brand-creative` conventions:

1. **Explicit path named by the user** in the request.
2. **Inside an instance repo** — `config/instance.json` at working root →
   `<instance-root>/brand/`.
3. **Inside a target repo** — `.digital-agency/target.json` at working root →
   resolve instance root, then `<instance-root>/brand/`.
4. **Standalone** — no instance or target pointer → `docs/brand/` in the current
   project.

If `brand-guide.md` does not exist, ask the user for design guidance inline — do
not require `brand-creative` to be installed. Do not bundle or invoke the
brand-guide skill; read the artefact directly.

## UX design output (artifact consumption)

When a UX design practice has produced wireframes or specs, read from
`<instance-root>/design/` (or the path named by the user). Falls back to
`docs/work/{epic}/design.md` for epic-level implementation specs.

## Companion practice (delivery)

For sprint participation, backlog grooming, task writing, and epic validation during
implementation, invoke companion skills directly — do not bundle local copies:

| Need | Invoke |
| ---- | ------ |
| Epic registry, backlog alignment | `/delivery-practice:backlog` |
| Task Gherkin AC | `/delivery-practice:tasks` |
| Sprint plan or retro | `/delivery-practice:sprint` |
| Epic completion sign-off | `/delivery-practice:validate` |
| Which planning skill to use | `/delivery-practice:skills-index` |

Recommend `delivery-practice` as a co-install. Document in CONNECTORS.md.

## Document layout

```text
docs/product/          product.md, roadmap.md, backlog.md
docs/architecture/     solution.md, decisions/register.md, ADR-NNNN-*.md
docs/work/{epic}/      design.md, tasks.md, refine-session.md
docs/work/sprint-{id}/ plan.md, retrospective.md
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
- **EARS:** optional via `/delivery-practice:tasks write --ears` or when rules are clearer than scenarios.
- **Backlog:** epic scope only; no full Gherkin in `backlog.md` (use **tasks** companion skill).

## Design modes

| Mode | When | Size |
| ---- | ---- | ---- |
| `walking-skeleton` | Phase 0 | 2–4 pages |
| `tdd` | Sprint 2+ | 5–10 pages |

Cite `solution.md §{N.M}` — do not re-narrate architecture in `design.md`.

## Personas

Six personas share one skill library. Choose the default persona during
`setup` (merged for one-person shops; distinct for larger teams).

| Persona | Primary skills | Focus |
| ------- | -------------- | ----- |
| **Frontend Engineer** | `implement`, `code-review`, `create-mr` | Build — UI, client state, styling |
| **Senior Frontend Engineer** | `code-review`, `design` | Peer review — diffs vs design and AC |
| **Principal Frontend Engineer** | `final-code-review`, `code-review`, `design` | Final gate — architecture and AC on open PRs |
| **Principal Architect** | `solution`, `adr`, `design`, `docs` | Architecture — solution, ADRs, epic design |
| **QA Engineer** | `deploy-qa`, `run-automated-suite`, `exploratory-pass`, `document-defects` | Validation — automated and exploratory QA |
| **WebOps Engineer** | `deploy-qa`, `debug`, `platform-health` | Platform — CI/CD, deploy, health |

Epic sign-off uses `/delivery-practice:validate` (companion skill), not a local copy.

## Skill routing (near-misses)

| User intent | Skill | Persona |
| ----------- | ----- | ------- |
| System architecture | **solution** | Principal Architect |
| ADR write/review | **adr** | Principal Architect |
| `design.md` for one epic | **design** | Senior FE / Principal FE / Architect |
| Implement code | **implement** | Frontend Engineer |
| PR / branch code review | **code-review** | Senior FE / Principal FE |
| Address review feedback | **code-review** `fix` | Frontend Engineer |
| Final PR gate | **final-code-review** | Principal Frontend Engineer |
| Open merge request | **create-mr** | Frontend Engineer |
| Pre/post-sprint doc pass | **docs** | Principal Architect |
| Bug investigation | **debug** | WebOps Engineer |
| Technical debt audit | **tech-debt** | Principal Architect |
| QA workspace prep | **deploy-qa** | QA / WebOps |
| Run automated tests | **run-automated-suite** | QA Engineer |
| Exploratory AC pass | **exploratory-pass** | QA Engineer |
| Document defects | **document-defects** | QA Engineer |
| Platform health check | **platform-health** | WebOps Engineer |
| PRD, phases, backlog, tasks, sprint, validate | `/delivery-practice:*` | Companion — any persona |
