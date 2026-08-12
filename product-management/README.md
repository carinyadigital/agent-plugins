# product-management

Root-level **practice plugin** — one install delivers the complete product and
delivery service: setup interview, product strategy and PRDs, roadmap, feature
specs, user research synthesis, competitive analysis, product metrics,
stakeholder updates, brainstorming, tasks/backlog decomposition, sprint planning
and retro, and epic validation. Self-contained under the MECE practice model:
edit skills here only; nothing is vendored from elsewhere.

Install standalone or after practice `setup` (writes `config/instance.json` if absent) recommends it.

## Personas

Two personas share this skill library:

| Persona | Focus | Skills |
| ------- | ----- | ------ |
| **Product Manager** | Strategy, discovery, communication | `product`, `roadmap`, `write-spec`, `product-brainstorming`, `synthesize-research`, `competitive-brief`, `metrics-review`, `stakeholder-update` |
| **Delivery Lead** | Decomposition, cadence, sign-off | `tasks`, `backlog-refine`, `sprint-planning`, `sprint-retro`, `validate` |

Invoke skills directly — there is no separate agent plugin:

```
/product-management:product
/product-management:write-spec
/product-management:roadmap
/product-management:tasks --product
/product-management:sprint-planning 3
```

## First run: setup

After instance bootstrap (or standalone):

```
/product-management:setup
```

| Flag | Behaviour |
| ---- | --------- |
| `--quick` | Reporting cadence + audience + roadmap format + escalation + sprint length; skip deep interview |
| `--full` | Full interview including discovery workflow and sprint cadence |
| `--redo` | Re-run setup only; overwrite on confirmation |
| `--resume` | Continue a paused interview |
| `--check-integrations` | Report MCP connector status only; no interview |

## Skills

| Skill | Purpose |
| ----- | ------- |
| **setup** | Interview → write practice profile and product/delivery defaults |
| **product** | write — `docs/product/product.md` (strategy, PRD, pitch, vision, personas); review via `/engineering:docs-review` |
| **roadmap** | write — `docs/product/roadmap.md` (Now/Next/Later, themes, OKR-aligned); review via `/engineering:docs-review` |
| **write-spec** | Feature spec or PRD from a problem statement — user stories, requirements, success metrics |
| **product-brainstorming** | Sparring partner for exploring a problem space (no deliverable) |
| **synthesize-research** | Themes, personas, opportunity areas from interviews, surveys, tickets |
| **competitive-brief** | Competitive analysis — feature comparison, positioning, implications |
| **metrics-review** | Metrics scorecard, trends, and recommended actions |
| **stakeholder-update** | Status update tailored by audience, launch notes, risk escalation |
| **tasks** | `--product` → `docs/product/backlog.md`; `{work-id}` → `docs/work/{work-id}/tasks.md` |
| **backlog-refine** | Groom backlog or judge sprint readiness |
| **sprint-planning** | Sprint plan — `docs/work/sprint-{id}/plan.md` |
| **sprint-retro** | Sprint retrospective — `docs/work/sprint-{id}/retrospective.md` |
| **validate** | Work-item completion sign-off |

Path and boundary rules: `references/product-conventions.md` and
`references/delivery-conventions.md`.

## Scheduled agents

| Agent | Cadence | What it does |
| ----- | ------- | ------------ |
| **competitor-scan** | weekly / monthly | Market scan; proposes backlog additions where the market surfaces a gap |
| **metrics-digest** | weekly / monthly | Metrics review vs targets; proposes follow-ups where a metric implies work |
| **stakeholder-digest** | reporting cadence | Drafts the stakeholder update for review; never sends |
| **backlog-grooming** | weekly | Groom backlog; propose splits and re-estimates |
| **daily-standup** | daily | Draft standup notes from tracker / docs |
| **sprint-planning** | sprint start | Draft sprint plan for review |
| **sprint-retrospective** | sprint end | Draft retrospective for review |

## Prerequisites

- **Instance profile** (optional) — practice `setup` (writes `config/instance.json` if absent) writes
  `config/instance.json`; setup reads cadence and risk posture without
  re-asking.
- **Connectors** (optional) — project tracker, chat, knowledge base, product
  analytics, user feedback, meeting transcription, and competitive intelligence
  MCP servers. See [CONNECTORS.md](CONNECTORS.md).

## Companion practices

| Need | Plugin | Invoke |
| ---- | ------ | ------ |
| Architecture (`solution`, `adr`) | **architecture** | `/architecture:solution`, `/architecture:adr` |
| Technical design, implementation | **engineering** | `/engineering:tdd`, `/engineering:implement` |
| Brand voice and visual identity | **brand-creative** | `/brand-creative:*` |

## Coverage

Covers the full PM workflow from Anthropic's
[product-management plugin](https://github.com/anthropics/knowledge-work-plugins/tree/main/product-management)
— write-spec, roadmap, stakeholder-update, synthesize-research, competitive-brief,
metrics-review, product-brainstorming — **plus** a dedicated `product` strategy
skill and the delivery skills (`tasks`, `backlog-refine`,
`sprint-planning`, `sprint-retro`, `validate`).
