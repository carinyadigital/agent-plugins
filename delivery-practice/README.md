# delivery-practice

Root-level **practice plugin** — one install delivers the complete delivery service:
setup interview, product strategy, backlog and sprint cadence, validation, and
operational skills. Self-contained under the MECE practice model: edit skills here
only; nothing is vendored from elsewhere.

Install standalone or after `agency-hub:setup` recommends it. Other
practices (content-marketing, web-development, search-optimisation) declare this
as a **companion practice** and invoke skills directly — e.g.
`/delivery-practice:backlog`, `/delivery-practice:sprint`.

## Personas

Two personas share one skill library. Choose the default persona during
`setup` (merged for one-person shops; distinct for larger teams).

| Persona | Primary skills | Focus |
| ------- | -------------- | ----- |
| **Product Manager** | `product`, `product-brainstorming`, `roadmap`, `write-spec`, `synthesize-research` | Strategy — what to build and why |
| **Delivery Lead** | `sprint`, `stakeholder-update`, `metrics-review` | Cadence — keeping work moving and stakeholders informed |
| **Shared (both)** | `backlog`, `competitive-brief`, `skills-index`, `tasks`, `validate` | Planning artefacts and routing |

Invoke skills directly — there is no separate agent plugin per persona:

```
/delivery-practice:product write
/delivery-practice:sprint plan 3
/delivery-practice:backlog review
```

## First run: setup

After instance bootstrap (or standalone):

```
/delivery-practice:setup
```

| Flag | Behaviour |
| ---- | --------- |
| `--quick` | Reporting cadence default + escalation model; skip deep interview |
| `--full` | Full interview including persona preference |
| `--redo` | Re-run delivery setup only; overwrite on confirmation |
| `--resume` | Continue a paused interview |
| `--check-integrations` | Report MCP connector status only; no interview |

## Skills

| Skill | Purpose |
| ----- | ------- |
| **setup** | Interview → write practice profile and delivery defaults |
| **product** | write, review, refine — `docs/product/product.md` |
| **roadmap** | write, review, refine — `docs/product/roadmap.md` |
| **backlog** | write, review, refine — `docs/product/backlog.md` |
| **tasks** | write, review, refine — `docs/work/{epic}/tasks.md` |
| **sprint** | plan, retrospective |
| **validate** | Epic completion sign-off |
| **write-spec** | Feature spec or PRD |
| **stakeholder-update** | Status update for sponsors |
| **synthesize-research** | Themes from interviews, surveys, tickets |
| **competitive-brief** | Competitive analysis |
| **metrics-review** | Metrics review with recommended actions |
| **product-brainstorming** | Sparring partner for ideas |
| **skills-index** | Route vague requests to the right skill |

Path and boundary rules: `references/delivery-conventions.md`.

## Prerequisites

- **Instance profile** (optional) — `agency-hub:setup` writes
  `config/instance.json`; setup reads cadence and risk posture without
  re-asking.
- **Connectors** (optional) — project tracker, chat, knowledge base, analytics,
  and competitive intelligence MCP servers supercharge stakeholder updates,
  research synthesis, and metrics review.

## After setup

1. Use Product Manager skills for strategy; Delivery Lead skills for cadence.
2. Re-run `/delivery-practice:setup --redo` to refresh delivery defaults.
3. Companion practices invoke shared skills here — do not duplicate `backlog`,
   `synthesize-research`, or `competitive-brief` in other plugins.

## References

- `references/practice-setup-framework.md` — invocation, config paths, interview structure
- `references/delivery-conventions.md` — path resolution and artefact boundaries
- `references/instance-profile-template.md` — Tier 1 schema (owned by agency-hub; synced copy)

Meta-framework files (`instance-profile-template.md`, `setup-framework.md`)
are kept in sync across practice plugins via `python3 scripts/sync-references.py`.
