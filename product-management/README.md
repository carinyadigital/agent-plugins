# product-management

Root-level **practice plugin** — one install delivers the complete product
management service: setup interview, product strategy and PRDs, roadmap, feature
specs, user research synthesis, competitive analysis, product metrics,
stakeholder updates, and brainstorming. Self-contained under the MECE practice
model: edit skills here only; nothing is vendored from elsewhere.

Install standalone or after `agency-hub:setup` recommends it. Decomposition and
sprint cadence live in the companion **delivery-practice** plugin — invoke
`/delivery-practice:tasks --product` and `/delivery-practice:sprint-planning`
when product work is ready to become a backlog.

## Persona

One persona — **Product Manager** — owns the full strategy-and-discovery skill
library. Choose defaults during `setup`.

| Focus | Skills |
| ----- | ------ |
| **Strategy — what to build and why** | `product`, `roadmap`, `write-spec` |
| **Discovery — evidence and ideas** | `product-brainstorming`, `synthesize-research`, `competitive-brief` |
| **Communication — numbers and stakeholders** | `metrics-review`, `stakeholder-update` |
| **Routing** | `skills-index` |

Invoke skills directly — there is no separate agent plugin:

```
/product-management:product
/product-management:write-spec
/product-management:roadmap write
```

## First run: setup

After instance bootstrap (or standalone):

```
/product-management:setup
```

| Flag | Behaviour |
| ---- | --------- |
| `--quick` | Reporting cadence + audience + roadmap format default; skip deep interview |
| `--full` | Full interview including discovery workflow |
| `--redo` | Re-run product setup only; overwrite on confirmation |
| `--resume` | Continue a paused interview |
| `--check-integrations` | Report MCP connector status only; no interview |

## Skills

| Skill | Purpose |
| ----- | ------- |
| **setup** | Interview → write practice profile and product defaults |
| **product** | write — `docs/product/product.md` (strategy, PRD, pitch, vision, personas); review via `/web-development:docs-review` |
| **roadmap** | write, review — `.agency/roadmap.md` (Now/Next/Later, themes, OKR-aligned) |
| **write-spec** | Feature spec or PRD from a problem statement — user stories, requirements, success metrics |
| **product-brainstorming** | Sparring partner for exploring a problem space (no deliverable) |
| **synthesize-research** | Themes, personas, opportunity areas from interviews, surveys, tickets |
| **competitive-brief** | Competitive analysis — feature comparison, positioning, implications |
| **metrics-review** | Metrics scorecard, trends, and recommended actions |
| **stakeholder-update** | Status update tailored by audience, launch notes, risk escalation |
| **skills-index** | Route vague requests to the right skill |

Path and boundary rules: `references/product-conventions.md`.

## Scheduled agents

| Agent | Cadence | What it does |
| ----- | ------- | ------------ |
| **competitor-scan** | weekly / monthly | Market scan; proposes backlog additions where the market surfaces a gap |
| **metrics-digest** | weekly / monthly | Metrics review vs targets; proposes follow-ups where a metric implies work |
| **stakeholder-digest** | reporting cadence | Drafts the stakeholder update for review; never sends |

## Prerequisites

- **Instance profile** (optional) — `agency-hub:setup` writes
  `config/instance.json`; setup reads cadence and risk posture without
  re-asking.
- **Connectors** (optional) — project tracker, chat, knowledge base, product
  analytics, user feedback, meeting transcription, and competitive intelligence
  MCP servers supercharge research synthesis, metrics review, and stakeholder
  updates. See [CONNECTORS.md](CONNECTORS.md).

## Companion practices

| Need | Plugin | Invoke |
| ---- | ------ | ------ |
| Backlog, sprints, retro, validation | **delivery-practice** | `/delivery-practice:tasks --product`, `/delivery-practice:sprint-planning` |
| Architecture, design, implementation | **web-development** | `/web-development:solution`, `/web-development:design` |
| Brand voice and visual identity | **brand-creative** | `/brand-creative:*` |

## Coverage

Covers the full PM workflow from Anthropic's
[product-management plugin](https://github.com/anthropics/knowledge-work-plugins/tree/main/product-management)
— write-spec, roadmap, stakeholder-update, synthesize-research, competitive-brief,
metrics-review, product-brainstorming — **plus** a dedicated `product` strategy
skill (PRD / vision / personas at `docs/product/product.md`) and a `skills-index`
router.
