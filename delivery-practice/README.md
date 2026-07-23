# delivery-practice

Root-level **practice plugin** — one install delivers the complete delivery service:
setup interview, tasks/backlog decomposition, sprint planning and retro, and epic
validation. Self-contained under the MECE practice model: edit skills here only;
nothing is vendored from elsewhere.

Install standalone or after `agency-hub:setup` recommends it. Other
practices (content-marketing, web-development, search-optimisation) declare this
as a **companion practice** and invoke skills directly — e.g.
`/delivery-practice:tasks --product`, `/delivery-practice:sprint-planning`.
Product strategy, roadmap, specs, research, metrics, and stakeholder updates live
in the companion **product-management** plugin.

## Persona

One persona — **Delivery Lead** — owns the execution skill library: turning
strategy into a backlog, running sprint cadence, and signing off epics.

| Focus | Skills |
| ----- | ------ |
| **Decomposition** | `tasks`, `backlog-refine` |
| **Cadence** | `sprint-planning`, `sprint-retro` |
| **Sign-off** | `validate` |
| **Routing** | `skills-index` |

Invoke skills directly — there is no separate agent plugin:

```
/delivery-practice:tasks --product
/delivery-practice:sprint-planning 3
/delivery-practice:backlog-refine
```

## First run: setup

After instance bootstrap (or standalone):

```
/delivery-practice:setup
```

| Flag | Behaviour |
| ---- | --------- |
| `--quick` | Reporting cadence default + escalation model; skip deep interview |
| `--full` | Full interview including sprint cadence |
| `--redo` | Re-run delivery setup only; overwrite on confirmation |
| `--resume` | Continue a paused interview |
| `--check-integrations` | Report MCP connector status only; no interview |

## Skills

| Skill | Purpose |
| ----- | ------- |
| **setup** | Interview → write practice profile and delivery defaults |
| **tasks** | `--product` → `.agency/backlog.md`; `{epic}` → `.agency/work/{epic}/tasks.md` |
| **backlog-refine** | Groom backlog or judge sprint readiness |
| **sprint-planning** | Sprint plan — `.agency/sprints/sprint-{id}/plan.md` |
| **sprint-retro** | Sprint retrospective — `.agency/sprints/sprint-{id}/retrospective.md` |
| **validate** | Epic completion sign-off |
| **skills-index** | Route vague requests to the right skill |

Path and boundary rules: `references/delivery-conventions.md`.

`tasks --product` consumes `.agency/product.md` and `.agency/roadmap.md`, which
are produced by the companion **product-management** plugin.

## Prerequisites

- **Instance profile** (optional) — `agency-hub:setup` writes
  `config/instance.json`; setup reads cadence and risk posture without
  re-asking.
- **Connectors** (optional) — project tracker, chat, knowledge base, analytics,
  and competitive intelligence MCP servers supercharge stakeholder updates,
  research synthesis, and metrics review.

## After setup

1. Decompose strategy into a backlog with `tasks`, then run sprint cadence.
2. Re-run `/delivery-practice:setup --redo` to refresh delivery defaults.
3. Companion practices invoke shared skills here — do not duplicate `tasks` or
   `backlog-refine` in other plugins. Strategy and research skills live in
   `product-management`.

## References

- `references/practice-setup-framework.md` — invocation, config paths, interview structure
- `references/delivery-conventions.md` — path resolution and artefact boundaries
- `references/instance-profile-template.md` — Tier 1 schema (owned by agency-hub; synced copy)

Meta-framework files (`instance-profile-template.md`, `setup-framework.md`)
are kept in sync across practice plugins via `python3 scripts/sync-references.py`.
