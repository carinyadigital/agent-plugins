# Digital Agency by Carinya Parc

**Run a full-service digital agency from your IDE — practice plugins for strategy and delivery, brand and creative, content and growth, UX, search, and web engineering, with instance bootstrap and MCP connectors baked in.**

## Install in one command

In [Claude Code](https://claude.com/product/claude-code), [Claude Cowork](https://claude.com/product/cowork), or **Cursor** (Settings → Plugins):

```bash
/plugin marketplace add <path-to-this-repo>
/plugin install agency-hub@carinya-digital
```

Restart, then run `/agency-hub:setup`. It bootstraps a git-versioned instance workspace (`config/`, `brand/`, `squads/`) and recommends your first practice plugin. Full walkthrough: [agency-hub/README.md](./agency-hub/README.md).

> [!IMPORTANT]
> **Every output is a draft for your review — not client-ready deliverables, not production code without review, not a substitute for qualified professional judgment.** Agents and skills draft work products; you verify accuracy, brand fit, accessibility, security, and compliance before anything ships. You are responsible for outputs that leave your firm.

## Plugins at a glance

Install **`agency-hub` first**, then the practice plugins that match your work.

| Plugin | Best for | First command |
|---|---|---|
| [agency-hub](./agency-hub) | Instance bootstrap, target bindings, squad charters | `/agency-hub:setup` |
| [brand-creative](./brand-creative) | Brand voice and visual identity | `/brand-creative:setup` |
| [delivery-practice](./delivery-practice) | Product strategy, backlog, sprint cadence, validation | `/delivery-practice:setup` |
| [content-marketing](./content-marketing) | Editorial calendar, social curation, CMS seed drafts | `/content-marketing:setup` |
| [ux-design](./ux-design) | Low-fidelity wireframes and interaction specs | `/ux-design:setup` |
| [search-optimisation](./search-optimisation) | Keyword research, technical SEO audits, on-page review | `/search-optimisation:setup` |
| [web-development](./web-development) | Architecture, implementation, code review, QA, platform ops | `/web-development:setup` |

**Which plugin first?** After `setup`, the interview recommends a starting practice. Common paths:

| If you are… | Install next |
|---|---|
| Standing up a new client or product | `brand-creative` → `delivery-practice` |
| Shipping a website or app | `delivery-practice` + `web-development` (+ `ux-design` for new UI) |
| Running content and social | `brand-creative` → `content-marketing` (+ `search-optimisation` for SEO) |
| SEO-only engagement | `search-optimisation` (+ `delivery-practice` for competitive brief) |

## Worked examples

Each example produces a **draft artefact for your review** — run the command, then verify assumptions, numbers, and brand fit before client delivery.

### 1. Bootstrap a client instance (Agency Hub)

**You have:** a new engagement — business name, one website target, no instance repo yet.

**Run:** `/agency-hub:setup --quick` — answer business name, first practice, and target.

**You get:** a bound instance repo with `config/instance.json`, target skeletons, and a handoff to brand setup or your first practice plugin.

### 2. Sprint plan from an existing backlog (Delivery Practice)

**You have:** `.agency/backlog.md` with epics in the Now phase and open risks.

**Run:** `/delivery-practice:sprint plan 3` — point at the backlog and name sprint goals.

**You get:** a sprint plan with scoped work, dependencies, and stakeholder-facing summary — aligned to your practice profile cadence and escalation model.

### 3. Implement a UI task against design and AC (Web Development)

**You have:** approved `.agency/work/{epic}/design.md`, `tasks.md` with Gherkin AC, and a bound target repo.

**Run:** `/web-development:implement CHK01-01` — the skill reads the target repo's own `AGENTS.md` / `CLAUDE.md` before changing code.

**You get:** implemented code on a feature branch, ready for `/web-development:code-review` and your normal PR workflow.

More personas and commands: [Named personas](#named-personas) · [Extended persona catalog](#extended-persona-catalog) · [Skill & command reference](#skill--command-reference).

---

## Named personas

Twelve job-titled entry points for digital agency work. Each name maps to **exactly one** slash command under a practice plugin — personas are not separate agent plugins; they share one skill library per practice.

| Persona | What it does | Command |
|---|---|---|
| **Product Manager** | Product strategy, roadmap, specs from problem statements | `/delivery-practice:product write` |
| **Delivery Lead** | Sprint planning, stakeholder updates, metrics review | `/delivery-practice:sprint plan` |
| **Content Strategist** | Editorial calendar and social inventory curation | `/content-marketing:content-calendar write` |
| **Content Writer** | Blog posts, recipes, captions, and light edits for CMS import | `/content-marketing:draft-post` |
| **SEO Specialist** | Keyword research, technical audits, on-page content review | `/search-optimisation:keyword-research` |
| **Brand Lead** | Voice lifecycle and visual identity guide | `/brand-creative:brand-voice write` |
| **UX Designer** | Low-fidelity wireframes from a brief | `/ux-design:wireframe` |
| **Frontend Engineer** | React/Next.js UI — components, client state, styling | `/web-development:implement` |
| **Senior Frontend Engineer** | Peer code review against design docs and AC | `/web-development:code-review` |
| **Principal Frontend Engineer** | Final technical gate on open PRs — architecture, security, AC | `/web-development:final-code-review` |
| **Principal Architect** | System architecture, ADRs, epic-level design | `/web-development:solution write` |
| **QA Engineer** | QA deploy, automated suite, exploratory pass, defect docs | `/web-development:exploratory-pass` |

Run each plugin's `setup` before first use — every skill reads your instance profile and practice profile. Skipping setup is the most common reason output stays generic.

## Extended persona catalog

Each persona below is named for the job it does. Start with the [named personas](#named-personas) above, then tune the underlying skill, practice profile, and connectors to how your firm works.

| Persona | What it does | Plugin | Command |
|---|---|---|---|
| **Backlog Owner** | Epic breakdown, Now-phase scope, delivery risks | `delivery-practice` | `/delivery-practice:backlog write` |
| **Task Decomposer** | Gherkin acceptance criteria per epic | `delivery-practice` | `/delivery-practice:tasks write` |
| **Epic Validator** | Final sign-off against AC and roadmap gates | `delivery-practice` | `/delivery-practice:validate` |
| **Research Synthesizer** | Themes from interviews, surveys, and tickets | `delivery-practice` | `/delivery-practice:synthesize-research` |
| **Competitive Analyst** | Competitive analysis brief | `delivery-practice` | `/delivery-practice:competitive-brief` |
| **Spec Writer** | Feature spec or PRD from a problem statement | `delivery-practice` | `/delivery-practice:write-spec` |
| **Voice Enforcer** | On-brand copy check against brand voice | `brand-creative` | `/brand-creative:brand-voice enforce` |
| **Visual Identity Author** | Colors, type, logo, UI tokens | `brand-creative` | `/brand-creative:brand-guide write` |
| **Media Analyst** | Vision analysis — subjects, season, mood, quality | `content-marketing` | `/content-marketing:analyse-media` |
| **Caption Writer** | Caption variants and channel copy | `content-marketing` | `/content-marketing:write-captions` |
| **Technical SEO Auditor** | Production audit → tracked issues | `search-optimisation` | `/search-optimisation:technical-seo-audit` |
| **ADR Author** | Architecture decision register and ADR files | `web-development` | `/web-development:adr write` |
| **Epic Designer** | Epic-level technical design | `web-development` | `/web-development:design write` |
| **MR Author** | Merge request description from the branch | `web-development` | `/web-development:merge-request` |
| **Docs Steward** | Pre/post-sprint documentation pass | `web-development` | `/web-development:docs review` |
| **Debugger** | Reproduce, isolate, diagnose, fix | `web-development` | `/web-development:debug` |
| **Tech Debt Prioritizer** | Prioritize remediation work | `web-development` | `/web-development:tech-debt` |
| **WebOps Engineer** | CI/CD, deployment, platform health | `web-development` | `/web-development:platform-health` |

Everything here ships as Claude Cowork, Claude Code, or Cursor plugins **and** as [managed-agent cookbooks](./managed-agents/) for headless deployment — same skills and prompts, two surfaces from one source.

What's in the repo:

- **Practice plugins** covering brand, delivery, content, UX, SEO, and web engineering — each with a `setup` interview, a living `CLAUDE.md` practice profile every skill reads, and **propose profile update** so conventions can be recorded mid-engagement without re-running setup.
- **Agency Hub** for instance bootstrap — git-versioned org profile, target bindings, and (v2) community skill marketplace management.
- **MCP connectors** bundled per practice in `.mcp.json` — source control, hosting, design, project trackers, analytics, and browser automation.
- **[Named personas](#named-personas)** — twelve primary entry points plus the [extended catalog](#extended-persona-catalog) above.
- **Managed-agent cookbooks** for Cursor Cloud Agents and Claude Managed Agents — see [managed-agents/README.md](./managed-agents/README.md).

## Repository layout

```
agency-hub/               # instance bootstrap — install first
brand-creative/           # brand voice + visual identity
delivery-practice/        # product, roadmap, backlog, sprint, validate, …
content-marketing/        # calendar, curation, media analysis, CMS seeds
ux-design/                # wireframes
search-optimisation/      # keyword research, technical audit, content SEO review
web-development/          # solution, adr, design, implement, review, QA, platform
managed-agents/           # CMA + Cursor Cloud Agent cookbooks
scripts/                  # validate.py · plugin-check.py · sync-references.py · deploy-squad-agents.sh
.claude-plugin/
  marketplace.json        # plugin registry (name: carinya-digital)
.cursor-plugin/
  marketplace.json
```

Each practice plugin has the same shape:

```
<practice>/
  .claude-plugin/plugin.json
  .cursor-plugin/plugin.json
  CLAUDE.md               # template practice profile — filled in by /<practice>:setup
  README.md
  CONNECTORS.md           # category placeholders + bundled MCP providers
  .mcp.json
  skills/                 # skills — each is a /<practice>:<skill> slash command
  references/             # practice conventions + synced meta-framework files
  hooks/                  # pre- and post-tool hooks (stubs today)
```

## Getting started

### First run (all surfaces)

1. Install **`agency-hub`** from the marketplace.
2. Run **`/agency-hub:setup`** — creates or binds your instance repo.
3. Install the **practice plugins** recommended during setup.
4. Run each practice's **`/<practice>:setup`** (e.g. `/brand-creative:setup`).
5. Bind targets — website pointer (`.agency/target.json` in target repos), credentials when ready.

**Run practice setup first.** Every other skill in a plugin reads from the profile it writes. The interview takes 10–20 minutes per plugin; **`--quick`** is available when you want to be productive in two minutes and refine later.

### Claude Cowork

1. Open the **Cowork** tab.
2. Click **Customize** in the left sidebar.
3. Click **Browse plugins** and install from `https://github.com/carinyaparc/digital-agency`, **or** upload a custom plugin (zip any practice directory).

After install, skills fire automatically when relevant; slash commands are available via `/`.

### Claude Code

```bash
/plugin marketplace add <path-to-this-repo-or-github-url>

/plugin install agency-hub@carinya-digital
/plugin install brand-creative@carinya-digital
/plugin install delivery-practice@carinya-digital
/plugin install content-marketing@carinya-digital
/plugin install ux-design@carinya-digital
/plugin install search-optimisation@carinya-digital
# web-development — zip-install the web-development/ directory until marketplace registration lands

/agency-hub:setup
/brand-creative:setup
/delivery-practice:setup
```

Updates: `/plugin update`.

### Cursor

In **Settings → Plugins → Add plugin**:

- **Paste this repo URL** — `https://github.com/carinyaparc/digital-agency` — then pick practice plugins from the marketplace list, or
- **Upload a zip** — zip any practice directory (e.g. `web-development/`) and drop it in.

### Managed Agents and Cursor Cloud Agents

Headless deployment cookbooks live in [`managed-agents/`](./managed-agents/). Engineering personas deploy to **Cursor Cloud Agents**; content personas to **Claude Managed Agents**; architecture resolves at deploy time.

```bash
./scripts/deploy-squad-agents.sh --dry-run --instance ../your-instance-repo
./scripts/deploy-squad-agents.sh apply --instance ../your-instance-repo
```

See [`managed-agents/README.md`](./managed-agents/README.md) for platform matrix, security tiers, and required secrets.

## How it fits together

| | What it is | Where it lives |
|---|---|---|
| **Practice plugins** | Self-contained service bundles — skills, hooks, MCP, and a template practice profile. Install the ones you need. | `<practice>/` |
| **Skills** | Domain expertise Claude draws on automatically — and slash actions you trigger explicitly: `/delivery-practice:backlog`, `/web-development:implement`. | `<practice>/skills/<skill>/SKILL.md` |
| **Personas** | Job titles that map to skills — shared libraries inside each practice, not separate plugins. | Each practice's `README.md` |
| **Instance profile** | Git-versioned org facts, brand path, target bindings, squad charters. | `<instance-repo>/config/instance.json`, `brand/`, `squads/` |
| **Practice profile** | Per-practice conventions — stack defaults, persona preference, output formats, review gates. | `~/.claude/plugins/config/digital-agency/<practice>/CLAUDE.md` |
| **Connectors** | [MCP servers](https://modelcontextprotocol.io/) that wire agents to your data — repos, hosting, design, trackers, chat. | `<practice>/.mcp.json` |
| **Managed-agent cookbooks** | `agent.yaml` + steering examples for headless deployment. | [`managed-agents/<slug>/`](./managed-agents/) |
| **Artefact consumption** | Downstream practices read upstream outputs by path — brand voice, brand guide, wireframes — without hard install dependencies. | Resolved via instance/target pointers |

Everything is markdown and JSON. No build step.

## Practice plugins by service line

Grouped by where the work sits. Each plugin's **`setup`** is what tailors it to your firm — start there.

### Strategy & delivery

| Plugin | What it adds |
|---|---|
| **[delivery-practice](./delivery-practice)** | Product strategy, outcome-based roadmap, backlog and tasks, sprint planning, epic validation, specs, stakeholder updates, research synthesis, competitive briefs, metrics review, and skill routing. Two personas (Product Manager, Delivery Lead), one skill library. |

### Brand, creative & content

| Plugin | What it adds |
|---|---|
| **[brand-creative](./brand-creative)** | Brand voice lifecycle (discover, write, enforce) and visual identity guide (colors, type, logo, UI tokens). Writes to instance `brand/` when bound. |
| **[content-marketing](./content-marketing)** | Editorial calendar, social curation, media analysis, captions, and CMS seed drafting (posts and recipes). Two personas (Content Strategist, Content Writer). Reads brand voice from resolved brand path. |
| **[ux-design](./ux-design)** | Practice setup and wireframe skill for low-fidelity layout and interaction specs. Writes to instance `design/` when bound; `web-development` reads wireframes via artefact consumption. |

### Growth & search

| Plugin | What it adds |
|---|---|
| **[search-optimisation](./search-optimisation)** | Keyword research, production technical SEO audits, and on-page content SEO review. One persona (SEO Specialist). Optional pairing with `content-marketing` for seed review. |

### Engineering & platform

| Plugin | What it adds |
|---|---|
| **[web-development](./web-development)** | Architecture (`solution`, `adr`), epic design, implementation, peer and final code review, merge requests, documentation passes, debugging, tech debt, QA deploy and exploratory validation, platform health. Six personas share one library; `delivery-practice` is the recommended companion for backlog, tasks, sprint, and validate. |

### Platform

| Plugin | What it adds |
|---|---|
| **[agency-hub](./agency-hub)** | Instance bootstrap via `setup`. v2 adds community skill discovery, installation QA, and update management (designed, deferred — stubs exist for shape validation). |

**Companion practices:** `content-marketing` and `search-optimisation` invoke `/delivery-practice:backlog` and related skills rather than bundling duplicates. `web-development` invokes delivery skills for planning cadence during implementation. Neither direction requires the companion installed — skills degrade gracefully and document the pairing.

## MCP connectors

Each practice plugin bundles recommended MCP servers in its `.mcp.json`. Edit that file to swap providers or add stack-specific servers. Skills produce usable output when no connector is configured — connectors are enhancements, not hard dependencies unless a skill doc says otherwise.

| Practice | Bundled providers (examples) | Categories |
|---|---|---|
| **agency-hub** | GitHub | source control |
| **brand-creative** | Slack, Notion, Atlassian, Figma, Fireflies | chat, knowledge base, design, meeting transcription |
| **delivery-practice** | Slack, Linear, Asana, Atlassian, Notion, Figma, Amplitude, Intercom, Fireflies, GitHub, GitLab, Vercel, Playwright, Context7, Next.js DevTools | chat, project tracker, design, analytics, feedback, competitive intel, source control, hosting, browser automation |
| **content-marketing** | GitHub, GitLab, Notion, Slack, Canva | source control, knowledge base, chat, design |
| **ux-design** | Figma | design |
| **search-optimisation** | GitHub, GitLab, Playwright, Ahrefs | source control, browser automation, SEO intelligence |
| **web-development** | GitHub, GitLab, Vercel, Slack, Linear, Datadog, Sentry, Playwright, Context7, Next.js DevTools | source control, hosting, chat, observability, error tracking, browser automation |

Plugins use `~~category` placeholders in skill prose (e.g. `~~project tracker`, `~~hosting`) so workflows stay tool-agnostic. See each practice's [CONNECTORS.md](./delivery-practice/CONNECTORS.md) for the full placeholder map.

> Connectors marked "customer subscription" need your own account and API key. Configure them in each plugin's `.mcp.json` or via `claude mcp` in Claude Code.

## Instance bootstrap and practice profile

Two layers of configuration tailor generic skills to your firm:

| Layer | Path | Captures |
|---|---|---|
| **Instance profile** (shared, git-versioned) | `<instance-repo>/config/instance.json`, `brand/`, `squads/` | Business identity, target bindings, brand artefacts, squad charters |
| **Practice profile** (per plugin) | `~/.claude/plugins/config/digital-agency/<practice>/CLAUDE.md` | Stack defaults, persona preference, output formats, review gates, connector status |

**Run once per plugin you install:**

| Command | Writes |
|---|---|
| `/agency-hub:setup` | Instance repo + handoff to first practice |
| `/<practice>:setup` | Practice profile for that service line |

Framework: [`agency-hub/references/agency-setup-framework.md`](./agency-hub/references/agency-setup-framework.md) and synced [`setup-framework.md`](./delivery-practice/references/practice-setup-framework.md) copies in each practice.

**Living profile.** Every skill except `setup` uses **propose profile update** — show the exact diff, ask, write on yes. No skill auto-writes a full profile without confirmation.

## Making it yours

These are reference templates. They get better when you tune them to how your firm works — and the customization mechanism is the plugin itself.

- **Run instance and practice setup.** `setup` and `setup` **are** the customization mechanism. They interview you, read seed documents, and write profiles after you confirm the summary.
- **Edit profiles directly.** Instance facts live in your instance repo; practice conventions at `~/.claude/plugins/config/digital-agency/<practice>/CLAUDE.md`. They survive plugin updates.
- **Propose profile updates from any skill.** When a stable convention surfaces mid-engagement (tone corrections, sprint length, MR template), skills show the exact change and ask before writing.
- **Swap connectors.** Point `.mcp.json` at your source control, hosting, design, and tracker stack. Skills fall back gracefully when a connector is not configured.
- **Bring your brand and templates.** Drop terminology, house style, and branded templates into the instance `brand/` directory and practice profiles.
- **Fork skills for house style.** Every skill is a markdown file under `skills/`. Edit steps, gates, and output formats.
- **Deploy squads.** Bind targets, configure secrets, and apply schedules with `deploy-squad-agents.sh`.

No build step. Everything is markdown and JSON.

## Skill & command reference

The full map across all practice plugins. Run `setup` in each plugin before other commands.

### agency-hub

| Command | Skill | What it does |
|---|---|---|
| `/agency-hub:setup` | setup | Interview → bind instance repo → write config → hand off |
| `/agency-hub:setup --quick` | setup | Minimal path: business name, one practice, one target |
| `/agency-hub:setup --check-integrations` | setup | Report MCP connector status only |

v2 marketplace commands (`registry-browser`, `skill-installer`, `skills-qa`, …) are designed but not shipped — see [agency-hub/README.md](./agency-hub/README.md).

### brand-creative

| Command | Skill | What it does |
|---|---|---|
| `/brand-creative:setup` | setup | Learns voice strictness, channels, seed material; writes practice profile |
| `/brand-creative:brand-voice` | brand-voice | discover, write, review, refine, enforce — `brand/brand-voice.md` |
| `/brand-creative:brand-guide` | brand-guide | write, review, refine — visual identity and UI tokens |

### delivery-practice

| Command | Skill | What it does |
|---|---|---|
| `/delivery-practice:setup` | setup | Learns cadence, personas, escalation; writes practice profile |
| `/delivery-practice:product` | product | write, review, refine — `.agency/product.md` |
| `/delivery-practice:roadmap` | roadmap | write, review, refine — `.agency/roadmap.md` |
| `/delivery-practice:backlog` | backlog | write, review, refine — `.agency/backlog.md` |
| `/delivery-practice:tasks` | tasks | write, review, refine — `.agency/work/{epic}/tasks.md` |
| `/delivery-practice:sprint` | sprint | plan, retrospective |
| `/delivery-practice:validate` | validate | Epic completion sign-off against AC and roadmap gates |
| `/delivery-practice:write-spec` | write-spec | Feature spec or PRD from a problem statement |
| `/delivery-practice:stakeholder-update` | stakeholder-update | Status update tailored to audience |
| `/delivery-practice:synthesize-research` | synthesize-research | Themes and insights from user research |
| `/delivery-practice:competitive-brief` | competitive-brief | Competitive analysis brief |
| `/delivery-practice:metrics-review` | metrics-review | Product metrics review with actions |
| `/delivery-practice:product-brainstorming` | product-brainstorming | Sparring partner for ideas (no deliverable) |
| `/delivery-practice:skills-index` | skills-index | Routes vague requests to the right skill |

### content-marketing

| Command | Skill | What it does |
|---|---|---|
| `/content-marketing:setup` | setup | Learns channels, persona preference, seed sources |
| `/content-marketing:content-calendar` | content-calendar | write, review — editorial calendar and slot briefs |
| `/content-marketing:curate-content` | curate-content | Rank social inventory for upcoming posts |
| `/content-marketing:analyse-media` | analyse-media | Vision analysis — subjects, season, mood, quality |
| `/content-marketing:write-captions` | write-captions | Caption variants and channel copy |
| `/content-marketing:edit-content` | edit-content | Select or lightly edit best caption variant |
| `/content-marketing:draft-post` | draft-post | Blog post seed JSON for CMS import |
| `/content-marketing:draft-recipe` | draft-recipe | Recipe seed JSON for CMS import |

### ux-design

| Command | Skill | What it does |
|---|---|---|
| `/ux-design:setup` | setup | Learns in-scope pages/flows and reference sources |
| `/ux-design:wireframe` | wireframe | Low-fidelity layout and interaction spec from a brief |

### search-optimisation

| Command | Skill | What it does |
|---|---|---|
| `/search-optimisation:setup` | setup | Learns target site, keyword themes, audit cadence |
| `/search-optimisation:keyword-research` | keyword-research | Topic keyword docs with intent and content opportunities |
| `/search-optimisation:technical-seo-audit` | technical-seo-audit | Production audit → tracked issues |
| `/search-optimisation:content-seo-review` | content-seo-review | On-page SEO review of content seeds |

### web-development

| Command | Skill | What it does |
|---|---|---|
| `/web-development:setup` | setup | Learns stack, personas, target binding, connectors |
| `/web-development:solution` | solution | write, review, refine — `.agency/architecture/solution.md` |
| `/web-development:adr` | adr | plan, write, review — ADR register and decision records |
| `/web-development:design` | design | write, review — `.agency/work/{epic}/design.md` |
| `/web-development:implement` | implement | Implement a task against approved design and AC |
| `/web-development:code-review` | code-review | run, fix — peer review against design and tasks |
| `/web-development:final-code-review` | final-code-review | Final technical gate on open PRs |
| `/web-development:merge-request` | merge-request | Open merge request for implemented work |
| `/web-development:merge-request-review` | merge-request-review | Review an MR/PR as its reviewer |
| `/web-development:ux-design-review` | ux-design-review | UX review of implemented UI |
| `/web-development:ralph` | ralph | Autonomous epic delivery loop |
| `/web-development:docs` | docs | Pre/post-sprint documentation pass |
| `/web-development:debug` | debug | Bug investigation and fix |
| `/web-development:tech-debt` | tech-debt | Technical debt audit and prioritization |
| `/web-development:deploy-qa` | deploy-qa | Prepare QA workspace |
| `/web-development:run-automated-suite` | run-automated-suite | Run automated tests in QA workspace |
| `/web-development:exploratory-pass` | exploratory-pass | AC-driven exploratory validation |
| `/web-development:document-defects` | document-defects | Record defects from QA pass |
| `/web-development:platform-health` | platform-health | CI/CD, deployment, and platform health check |

## Contributing

Everything here is markdown and JSON. Fork, edit, PR. See [CONTRIBUTING.md](./CONTRIBUTING.md) for design principles and the validation checklist.

- **New skill** → add `<practice>/skills/<skill-name>/SKILL.md` with `name` and `description` frontmatter. Invokable as `/<practice>:<skill-name>`.
- **New persona row** → add the skill under the owning practice and a row in that practice's README Agents/Personas table mapping the job title to the slash command.
- **Shared meta-framework edits** → run `python3 scripts/sync-references.py` after changing `instance-profile-template.md` or `setup-framework.md`.
- **Validate before opening a PR** — `python3 scripts/validate.py` lints manifests, verifies cross-file references, and validates evals schema. See [AGENTS.md](./AGENTS.md) for repo conventions.

## License

Licensed under the [MIT License](./LICENSE).

Copyright 2026 Carinya Parc Pty Ltd.
