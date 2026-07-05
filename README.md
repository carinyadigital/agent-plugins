# Digital Agency by Carinya Parc

Reference agents, skills, and data connections for a full-service digital agency workflows - digital strategy & growth, creative & content, web development & technical, and operations.

Each agent plugin is designed to be provider-agnostic: they can be deployed behind your own workflow orchestration engine as a Claude (Code, Cowork, Managed Agent), or Cursor (IDE, Cloud Agent) - you choose where it runs.

> [!IMPORTANT]
> Like any workforce, these agents require oversight and governance. They draft work products for review by qualified professionals. You are responsible for verifying outputs and for compliance with the laws and regulations that apply to your business.

What's included

- **[Agents](#agents)** — named, end-to-end workflow agents across engineering, product, and operations (Frontend Engineer through Delivery Lead). Each ships as a plugin **and** as a [Managed Agents](./managed-agents) you deploy via `/v1/agents`.
- **[Skill plugins](#skill-plugins)** — the underlying skills and commands, bundled by discipline. Install these on their own if you just want the skills without a full agent.
- **[Connectors](#mcp-integrations)** — MCP data connections bundled in each practice plugin's `.mcp.json`. Install the practice that matches your workflow; edit `.mcp.json` to swap providers.

## Agents

Each agent is named for the workflow it runs. They're starting points: install the ones that match your work, then tune the prompts, skills, and connectors to how your firm does it.

Each agent plugin is **self-contained** — it bundles the skills it uses, so installing the agent is all you need.

| Practice | Agent | What it does |
|---|---|---|
| **Engineering** | **[Frontend Engineer](./agents/frontend-engineer)** | Builds React/Next.js UI — components, client state, styling, and page composition. Reads the target repo's conventions before changing anything. |
| **Engineering** | **[Senior Frontend Engineer](./agents/senior-frontend-engineer)** | Peer code reviewer for React/Next.js UI changes. Reviews diffs against design docs and acceptance criteria; produces blocking/non-blocking verdicts. Read-only — does not write code. |
| **Engineering** | **[Principal Frontend Engineer](./agents/principal-frontend-engineer)** | Final technical gate on open PRs/MRs after peer review — architecture, security, and AC coverage. Tech-lead role; maps to delivery-review crew gate. |
| **Engineering** | **[QA Engineer](./agents/qa-engineer)** | Validates changes after CI — QA workspace deploy, automated tests, AC-driven exploratory pass, defect documentation. Maps to delivery-qa crew flow. |
| **Engineering** | **[Webops Engineer](./agents/webops-engineer)** | CI/CD, deployment, dependency hygiene, and platform health. Resolves frontend-engineer infra boundary. |
| **Product** | **[Product Manager](./agents/product-manager)** | Full product delivery lifecycle — strategy, roadmap, backlog, sprint planning, task decomposition, specs, stakeholder updates, research synthesis, and epic validation. |
| **Operations** | **[Delivery Lead](./agents/delivery-lead)** | Cross-cutting delivery steward — routes work to agents/skills, sprint planning, backlog tracking, stakeholder updates, epic validation. Maps to crew orchestration layer. |
| **Engineering** | **[Principal Architect](./agents/principal-architect)** | System architecture — solution.md, ADRs, epic-level design, documentation alignment. Owns the Architecture track upstream of implementation. |

For Managed Agent deployment — `agent.yaml`, leaf-worker subagents, steering-event examples, and per-agent security notes — see **[managed-agents/](./managed-agents)**.

## Repository Layout

```
agents/                # Named agents — one self-contained plugin each
skills/                # Skill + command bundles by discipline
managed-agents/        # Managed Agent cookbooks — one dir per agent
scripts/               # validate.py · plugin-check.py · sync-references.py · deploy-squad-agents.sh
```

## Getting Started

**First install:** add **`agency-hub`** from the marketplace and run `/agency-hub:agency-setup` to bootstrap your instance workspace (`config/`, `brand/`, `squads/`). Then install practice plugins and agents.

See [agency-hub/README.md](./agency-hub/README.md) for the full bootstrap flow.

### Cowork

In Cowork, open **Settings → Plugins → Add plugin** and either:

- **Paste this repo URL** — `https://github.com/carinyaparc/digital-agency` — then pick the agents and skills you want from the marketplace list, or
- **Upload a zip** — zip any agent directory (e.g. `agents/product-manager/`) or any practice plugin directory (e.g. `delivery-practice/`) and drop it in.

### Claude Managed Agents

Coming soon.

### Cursor

In Cursor, open **Settings → Plugins → Add plugin** and either:

- **Paste this repo URL** — `https://github.com/carinyaparc/digital-agency` — then pick the agents and skills you want from the marketplace list, or
- **Upload a zip** — zip any agent directory (e.g. `agents/product-manager/`) or any practice plugin directory (e.g. `delivery-practice/`) and drop it in.

### Cursor Cloud Agents

Coming soon.

## How It Fits Together

| | What it is | Where it lives |
|---|---|---|
| **Agents** | Self-contained plugins that own a workflow end to end — system prompt plus the skills it uses. Cowork and the Managed Agent wrapper both reference the same directory. | `agents/<slug>/` |
| **Skills** | Domain expertise, conventions, and step-by-step methods Claude draws on automatically when relevant. Authored once per discipline; each agent bundles a synced copy of the ones it needs. | `skills/<discipline>/skills/` (source) · `agents/<slug>/skills/` (bundled) |
| **Commands** | Slash actions you trigger explicitly (`/implement`). | `skills/<discipline>/commands/` |
| **Connectors** | [MCP servers](https://modelcontextprotocol.io/) that wire agents to your data — source code, code reviews, hosting, observability, analytics. | `<practice>/.mcp.json` |
| **Managed-agent wrappers** | `agent.yaml` + depth-1 subagents + steering examples for headless deployment. | `managed-agents/<slug>/` |

Everything is file-based — markdown and JSON, no build step.

## Skill Plugins

Install skill plugins for the disciplines you need.

| Plugin | What it adds |
|---|---|
| **[engineering](./skills/engineering)** | Architecture, epic design, implementation, code review, debugging, and technical debt. |
| **[product-management](./skills/product-management)** | Product strategy, roadmap, backlog, tasks, sprint planning, validation, specs, stakeholder updates, research, competitive analysis, metrics, and brainstorming. |
| **[brand-creative](./brand-creative)** | Complete brand practice — practice-setup, brand-voice lifecycle, and brand-guide visual identity. Writes to instance `brand/` when bound. |
| **[content-marketing](./content-marketing)** | Complete content practice — editorial calendar, social curation, media analysis, and CMS seed drafting. Content Strategist and Content Writer personas; reads brand voice from resolved brand path. |

## MCP Integrations

Each practice plugin bundles recommended MCP servers in its `.mcp.json`. Edit that file to swap providers or add stack-specific servers.

| Practice | Bundled providers (examples) |
|---|---|
| **web-development** | GitHub, GitLab, Vercel, Slack, Linear, Datadog, Playwright, Context7, Next.js DevTools |
| **delivery-practice** | Slack, Linear, Asana, Atlassian, Notion, Figma, Amplitude, Intercom, Fireflies, GitHub, GitLab, Vercel, Playwright, Context7, Next.js DevTools |
| **content-marketing** | GitHub, GitLab, Notion, Slack |
| **brand-creative** | Slack, Notion, Atlassian, Figma, Fireflies |
| **ux-design** | Figma |
| **search-optimisation** | GitHub, GitLab, Playwright |
| **agency-hub** | GitHub |

See each practice's `CONNECTORS.md` for category placeholders and skill usage.

> MCP access may require authentication, subscription, or an API key from the provider.

## Making It Yours

These are reference templates — they get better when you tune them to how your firm works.

- **Swap connectors** — edit the practice plugin's `.mcp.json` to point at your data providers and internal systems.
- **Add firm context** — drop your terminology, processes, and formatting standards into skill files.
- **Bring your brand voice** — install `brand-creative`, run `/brand-creative:practice-setup`, then `/brand-creative:brand-voice enforce` and `/brand-creative:brand-guide write` as needed.
- **Adjust agent scope** — edit `agents/<slug>.md` to match how your team actually runs the workflow.
- **Add your own** — copy the structure for workflows we haven't covered.

## Skill & Command Reference

<details>
<summary><b>engineering</b> — solution, adr, design, implement, code review, final-code-review, docs, debug, tech-debt, deploy-qa, run-automated-suite, exploratory-pass, document-defects</summary>

See [engineering README](./skills/engineering/README.md) for full detail.

| Skill | Modes | Description | Artefact |
| ----- | ----- | ----------- | -------- |
| **solution** | write, review, refine | System architecture (stub or full) | `docs/architecture/solution.md` |
| **adr** | plan, write, review | Architecture decision register and ADR files | `register.md`, `ADR-NNNN.md` |
| **design** | write, review | Epic-level technical design | `docs/work/{epic}/design.md` |
| **implement** | — | Implement a task against approved design and tasks | code |
| **code-review** | review, fix | Review a branch or PR; fix addresses findings | code review / code |
| **create-mr** | run | Merge request description from the branch | MR / PR |
| **docs** | review, refine | Pre-sprint or sprint-end documentation pass | review / `refine-session.md` |
| **debug** | run | Reproduce, isolate, diagnose, and fix bugs | debug report |
| **tech-debt** | run | Prioritize technical debt remediation | remediation plan |

</details>

<details>
<summary><b>product-management</b> — product, roadmap, backlog, tasks, sprint, validate, write-spec, stakeholder-update, synthesize-research, competitive-brief, metrics-review, product-brainstorming, skills-index</summary>

See [product-management README](./skills/product-management/README.md) for full detail.

| Skill | Modes | Description | Artefact |
| ----- | ----- | ----------- | -------- |
| **product** | write, review, refine | Product strategy doc, PRD, pitch, vision, personas | `docs/product/product.md` |
| **roadmap** | write, review, refine | Outcome-based delivery phases with exit criteria | `docs/product/roadmap.md` |
| **backlog** | write, review, refine | Epic breakdown, Now-phase scope, delivery risks | `docs/product/backlog.md` |
| **tasks** | write, review, refine | Gherkin acceptance criteria per epic | `docs/work/{epic}/tasks.md` |
| **sprint** | plan, retrospective | Sprint plan and retrospective | `docs/work/sprint-{id}/plan.md` / `retrospective.md` |
| **validate** | run | Final epic sign-off against AC and roadmap gates | validation report |
| **write-spec** | run | Feature spec or PRD from a problem statement | feature spec |
| **stakeholder-update** | run | Status update tailored to audience | stakeholder update |
| **synthesize-research** | run | Themes and insights from user research | research synthesis |
| **competitive-brief** | run | Competitive analysis brief | competitive brief |
| **metrics-review** | run | Product metrics review with actions | metrics report |
| **product-brainstorming** | run | Sparring partner for ideas (no deliverable) | conversation |
| **skills-index** | run | Routes vague requests to the right skill | skill routing |

</details>

<details>
<summary><b>brand-creative</b> — practice-setup, brand-guide, brand-voice</summary>

See [brand-creative README](./brand-creative/README.md) for full detail.

| Skill | Modes | Description | Artefact |
| ----- | ----- | ----------- | -------- |
| **brand-guide** | write, review, refine | Visual identity — colors, type, logo, UI tokens | `docs/brand/brand-guide.md` |
| **brand-voice** | discover, write, review, refine, enforce | Voice lifecycle and on-brand copy | `docs/brand/brand-voice.md`, `discovery-report.md`, inline content |

</details>

## Contributing

Everything here is markdown and YAML. Fork, edit, PR. For new content:

- New skill → add it under the owning practice plugin's `skills/<name>/` directory (e.g. `delivery-practice/skills/backlog/`).
- After editing shared meta-framework references, run `python3 scripts/sync-references.py`.
- Skill evals → add `evals/evals.json` and `evals/trigger-queries.json`; run `python3 scripts/validate.py` (evals schema and `--strict` frontmatter checks). See [agency-hub/references/agency-skill-design-framework.md](./agency-hub/references/agency-skill-design-framework.md) for skill design conventions.
- Run `python3 scripts/validate.py` before pushing — lints manifests, verifies cross-file references, and validates evals schema. See [CONTRIBUTING.md](./CONTRIBUTING.md#validation).

## License

[MIT](./LICENSE)

(c) 2026 Carinya Parc Pty Ltd.
