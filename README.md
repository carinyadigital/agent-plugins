# Carinya Plugins

**Product delivery plugins for your IDE — strategy, engineering, design, and validation in one marketplace, with optional brand, content, and SEO plugins for teams that need them. Each plugin bootstraps its own instance profile and ships MCP connectors for the tools you already use.**

## Install in one command

In [Claude Code](https://claude.com/product/claude-code), [Claude Cowork](https://claude.com/product/cowork), or **Cursor** (Settings → Plugins):

```bash
/plugin marketplace add <path-to-this-repo>
```

Restart, then run `/<practice>:setup`. It bootstraps a git-versioned instance workspace (`config/`, `brand/`, `squads/`) and recommends your first practice plugin. Full walkthrough: [brand-creative/README.md](./brand-creative/README.md).

> [!IMPORTANT]
> **Every output is a draft for your review — not production-ready deliverables or code without review, not a substitute for qualified professional judgment.** Agents and skills draft work products; you verify accuracy, brand fit, accessibility, security, and compliance before anything ships.

## Who this is for

**Primary audience:** product teams shipping software — product managers, engineers, designers, and delivery leads working from specs through implementation, review, and validation.

**Adjacent plugins:** `brand-creative`, `content-marketing`, and `search-optimisation` serve brand, editorial, and SEO workflows. They are genuinely disjoint buyers from the engineering core — install them when you need them, not because you run an agency.

This repo is **not** a promise to "run a full-service digital agency from your IDE." It is a plugin catalogue for structured product delivery, with optional go-to-market plugins on the side.

## Plugins at a glance

Install the practice plugins that match your work. The first practice `setup` writes `config/instance.json` if absent.

| Plugin | Best for | First command |
|---|---|---|
| [brand-creative](./brand-creative) | Brand voice and visual identity | `/brand-creative:setup` |
| [product-management](./product-management) | Product strategy, roadmap, specs, research, metrics, backlog, sprint cadence, validation | `/product-management:setup` |
| [content-marketing](./content-marketing) | Editorial calendar, social curation, CMS seed drafts | `/content-marketing:setup` |
| [design](./design) | Wireframes, live UX review, and UX design fix | `/design:setup` |
| [search-optimisation](./search-optimisation) | Keyword research, technical SEO audits, on-page review | `/search-optimisation:setup` |
| [architecture](./architecture) | Solution design and ADRs | `/architecture:setup` |
| [engineering](./engineering) | Technical design (tdd), implementation, code review, QA, platform ops | `/engineering:setup` |
| [ralph-loop](./ralph-loop) | Self-referential delivery loops (ad-hoc / custom; engineering preset from engineering) | `/ralph-loop-setup` |
| [skills-index](./skills-index) | Install-aware skill router | `/skills-index:find` |
| [plugin-management](./plugin-management) | Create/customize plugins + skill quality gates | `/plugin-management:create-plugin` |

**Which plugin first?** After `setup`, the interview recommends a starting practice. Common paths:

| If you are… | Install next |
|---|---|
| Standing up a new client or product | `brand-creative` → `product-management` |
| Shipping a website or app | `product-management` + `architecture` + `engineering` (+ `design` for new UI) |
| Running content and social | `brand-creative` → `content-marketing` (+ `search-optimisation` for SEO) |
| SEO-only engagement | `search-optimisation` (+ `product-management` for competitive brief) |

## Worked examples

Each example produces a **draft artefact for your review** — run the command, then verify assumptions, numbers, and brand fit before client delivery.

### 1. Bootstrap a client instance

**You have:** a new engagement — business name, one website target, no instance repo yet.

**Run:** `/brand-creative:setup --quick` (or any practice `setup`) — answers business name and writes `config/instance.json` if absent, then the practice interview.

**You get:** a bound instance profile and a practice profile ready for the next skill.

### 2. Sprint plan from an existing backlog (Product Management)

**You have:** `docs/product/backlog.md` with epics in the Now phase and open risks.

**Run:** `/product-management:sprint-planning 3` — point at the backlog and name sprint goals.

**You get:** a sprint plan with scoped work, dependencies, and stakeholder-facing summary — aligned to your practice profile cadence and escalation model.

### 3. Implement a UI task against design and AC (Engineering)

**You have:** approved `specs/{work-short-name}/tdd.md`, `TASKS.local.md` with Gherkin AC, and a bound target repo.

**Run:** `/engineering:implement CHK01-01` — the skill reads the target repo's own `AGENTS.md` / `CLAUDE.md` before changing code.

**You get:** implemented code on a feature branch, ready for `/engineering:code-review` and your normal PR workflow.

More commands and personas: [Entry points by team role](#entry-points-by-team-role) · [Extended persona catalog](#extended-persona-catalog) · [Skill & command reference](#skill--command-reference).

---

## Entry points by team role

Personas are **job titles that map to slash commands** inside practice plugins — not separate agent plugins. Install the plugin, run its `setup`, then invoke the command.

### Product team core

| Role | What it does | Command |
|---|---|---|
| **Product Manager** | Product strategy, roadmap, specs from problem statements | `/product-management:product` |
| **Delivery Lead** | Tasks/backlog decomposition, sprint planning, validation | `/product-management:sprint-planning` |
| **Architect** | System architecture and ADRs | `/architecture:solution` |
| **Engineer** | Implement tasks against approved design and AC | `/engineering:implement` |
| **Reviewer** | Peer code review against design docs and AC | `/engineering:code-review` |
| **Release gate** | Final technical sign-off on open PRs | `/engineering:final-code-review` |
| **UX Designer** | Wireframes, live UX review, UX fixes | `/design:wireframe` |
| **QA** | QA deploy, automated suite, exploratory pass | `/engineering:exploratory-pass` |

Engineering skills share one library in `engineering`. Architecture (`solution`, `adr`) lives in `architecture`. Seniority labels (peer review vs final gate) reflect review depth, not separate plugins.

### Adjacent practices (optional)

| Role | What it does | Command |
|---|---|---|
| **Brand Lead** | Voice lifecycle and visual identity guide | `/brand-creative:brand-voice write` |
| **Content Strategist** | Editorial calendar and social inventory curation | `/content-marketing:content-calendar write` |
| **Content Writer** | Blog posts, recipes, captions for CMS import | `/content-marketing:draft-post` |
| **SEO Specialist** | Keyword research, technical audits, on-page review | `/search-optimisation:keyword-research` |

Run each plugin's `setup` before first use — every skill reads your instance profile and practice profile. Skipping setup is the most common reason output stays generic.

## Extended persona catalog

Each persona below is named for the job it does. Start with [entry points by team role](#entry-points-by-team-role), then tune the underlying skill, practice profile, and connectors to how your team works.

| Persona | What it does | Plugin | Command |
|---|---|---|---|
| **Backlog Owner** | Epic breakdown, Now-phase scope, delivery risks | `product-management` | `/product-management:tasks --product` |
| **Task Decomposer** | Gherkin acceptance criteria per epic | `product-management` | `/product-management:tasks` |
| **Epic Validator** | Final sign-off against AC and roadmap gates | `product-management` | `/product-management:validate` |
| **Research Synthesizer** | Themes from interviews, surveys, and tickets | `product-management` | `/product-management:synthesize-research` |
| **Competitive Analyst** | Competitive analysis brief | `product-management` | `/product-management:competitive-brief` |
| **Spec Writer** | Feature spec or PRD from a problem statement | `product-management` | `/product-management:write-spec` |
| **Voice Enforcer** | On-brand copy check against brand voice | `brand-creative` | `/brand-creative:brand-voice enforce` |
| **Visual Identity Author** | Colors, type, logo, UI tokens | `brand-creative` | `/brand-creative:brand-guide write` |
| **Media Analyst** | Vision analysis — subjects, season, mood, quality | `content-marketing` | `/content-marketing:analyse-media` |
| **Caption Writer** | Caption variants and channel copy | `content-marketing` | `/content-marketing:write-captions` |
| **Technical SEO Auditor** | Production audit → tracked issues | `search-optimisation` | `/search-optimisation:technical-seo-audit` |
| **ADR Author** | Architecture decision register and ADR files | `architecture` | `/architecture:adr write` |
| **Epic Designer** | Work-item technical design (TDD) | `engineering` | `/engineering:tdd` |
| **MR Author** | Merge request description from the branch | `engineering` | `/engineering:merge-request` |
| **Docs Steward** | Document-set quality and consistency review | `engineering` | `/engineering:docs-review` |
| **Debugger** | Reproduce, isolate, diagnose, fix | `engineering` | `/engineering:debug` |
| **Tech Debt Prioritizer** | Prioritize remediation work | `engineering` | `/engineering:tech-debt` |
| **WebOps Engineer** | CI/CD, deployment, platform health | `engineering` | `/engineering:platform-health` |

Everything here ships as Claude Cowork, Claude Code, or Cursor plugins.

What's in the repo:

- **Practice plugins** — product management, engineering, design, and optional brand/content/SEO — each with a `setup` interview, a living `CLAUDE.md` practice profile every skill reads, and **propose profile update** so conventions can be recorded mid-engagement without re-running setup.
- **Instance bootstrap** — whichever plugin you install first writes `config/instance.json` if absent; no install-order dependency.
- **MCP connectors** — a minimal default per practice in `.mcp.json`; add more for your stack (source control, hosting, chat, trackers, analytics).
- **[Entry points by team role](#entry-points-by-team-role)** — primary commands plus the [extended catalog](#extended-persona-catalog) below.

## Repository layout

```
brand-creative/           # brand voice + visual identity
product-management/       # product, roadmap, specs, research, metrics, backlog, sprint, validate
architecture/             # solution, adr
engineering/      # tdd, implement, review, QA, platform
design/           # wireframes, ux-design-review, ux-design-fix
content-marketing/        # calendar, curation, media analysis, CMS seeds
search-optimisation/      # keyword research, technical audit, content SEO review
ralph-loop/               # ralph-loop + ralph-loop-setup (+ hooks)
skills-index/             # install-aware skill router
plugin-management/        # create/customize plugins + skills-qa / skill-review
scripts/                  # validate.py · validate_plugins.py · validate_skills.py · sync-references.py
references/               # canonical meta-framework (synced into practice plugins)
.claude-plugin/marketplace.json   # plugin registry (name: carinya-plugins)
.cursor-plugin/marketplace.json
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

1. Install a practice plugin from the marketplace (e.g. `brand-creative` or `product-management`).
2. Run **`/<practice>:setup`** — creates or binds your instance repo.
3. Install the **practice plugins** recommended during setup.
4. Run each practice's **`/<practice>:setup`** (e.g. `/brand-creative:setup`).
5. Bind targets — website pointer (`config/target.json` in target repos), credentials when ready.

**Run practice setup first.** Every other skill in a plugin reads from the profile it writes. The interview takes 10–20 minutes per plugin; **`--quick`** is available when you want to be productive in two minutes and refine later.

### Claude Cowork

1. Open the **Cowork** tab.
2. Click **Customize** in the left sidebar.
3. Click **Browse plugins** and install from `https://github.com/carinyaparc/carinya-plugins`, **or** upload a custom plugin (zip any practice directory).

After install, skills fire automatically when relevant; slash commands are available via `/`.

### Claude Code

```bash
/plugin marketplace add carinyaparc/carinya-plugins

/plugin install brand-creative@carinya-plugins
/plugin install product-management@carinya-plugins
/plugin install engineering@carinya-plugins
/plugin install design@carinya-plugins
/plugin install content-marketing@carinya-plugins
/plugin install search-optimisation@carinya-plugins
/plugin install ralph-loop@carinya-plugins
/plugin install skills-index@carinya-plugins
/plugin install plugin-management@carinya-plugins

/brand-creative:setup
/product-management:setup
```

Updates: `/plugin update`.

### Cursor

In **Settings → Plugins → Add plugin**:

- **Paste this repo URL** — `https://github.com/carinyaparc/carinya-plugins` — then pick practice plugins from the marketplace list, or
- **Upload a zip** — zip any practice directory (e.g. `engineering/`) and drop it in.

### skills.sh (skill files only)

Install individual skills without the full plugin surface (no hooks, MCP, or practice profiles):

```bash
# All skills from the monorepo
npx skills add carinyaparc/carinya-plugins

# One skill
npx skills add carinyaparc/carinya-plugins/engineering/skills/code-review
```

## How it fits together

| | What it is | Where it lives |
|---|---|---|
| **Practice plugins** | Self-contained service bundles — skills, hooks, MCP, and a template practice profile. Install the ones you need. | `<practice>/` |
| **Skills** | Domain expertise Claude draws on automatically — and slash actions you trigger explicitly: `/product-management:tasks --product`, `/engineering:implement`. | `<practice>/skills/<skill>/SKILL.md` |
| **Personas** | Job titles that map to skills — shared libraries inside each practice, not separate plugins. | Each practice's `README.md` |
| **Instance profile** | Git-versioned org facts, brand path, target bindings, squad charters. | `<instance-repo>/config/instance.json`, `brand/`, `squads/` |
| **Practice profile** | Per-practice conventions — stack defaults, persona preference, output formats, review gates. | `~/.claude/plugins/config/digital-agency/<practice>/CLAUDE.md` |
| **Connectors** | [MCP servers](https://modelcontextprotocol.io/) that wire agents to your data — repos, hosting, design, trackers, chat. | `<practice>/.mcp.json` |
| **Artefact consumption** | Downstream practices read upstream outputs by path — brand voice, brand guide, wireframes — without hard install dependencies. | Resolved via instance/target pointers |

Everything is markdown and JSON. No build step.

## Delivery artefacts (target repo)

Strategy and delivery skills write into the **bound target repo**, not the plugin. Hierarchy is fixed:

**Product → Solution → Roadmap → Backlog** → work-item design / tasks → review → validate.

| Stage | Skill | Writes |
| ----- | ----- | ------ |
| Product | `/product-management:product` | `docs/product/product.md` |
| Solution | `/architecture:solution` | `docs/architecture/solution.md` |
| Roadmap | `/product-management:roadmap` | `docs/product/roadmap.md` (does **not** require backlog) |
| Backlog | `/product-management:tasks --product` | `docs/product/backlog.md` (or tracker epics) |

Default layout the skills expect:

```text
docs/product/                 product.md, roadmap.md, backlog.md
docs/architecture/            solution.md, decisions/
specs/{work-short-name}/          tdd.md; TASKS.local.md when required
specs/{work-short-name}/reviews/  code-review-{nn}.local.md, ux-design-review-{nn}.local.md
docs/work/sprint-{id}/        plan.md, retrospective.md
reviews/                      code-review.local.json, ux-design-review.local.json,
                              review-learnings.local.md (gitignored — never committed)
docs/reviews/                 agent byproducts (competitor-scan, metrics, digests)
TASKS.local.md                repo-root tracker-pointer cache (gitignored locally)
.ux-review/                   UX capture scratch (agent-local)
.claude/loop/                 Ralph run state on Claude Code (or .cursor/loop/ on Cursor)
```

Canonical detail: [`product-management/references/delivery-conventions.md`](./product-management/references/delivery-conventions.md).

## Practice plugins by service line

Grouped by where the work sits. Each plugin's **`setup`** is what tailors it to your firm — start there.

### Strategy & delivery

| Plugin | What it adds |
|---|---|
| **[product-management](./product-management)** | Product strategy, roadmap, feature specs and PRDs, research, competitive briefs, metrics, stakeholder updates, backlog/tasks decomposition, sprint planning and retro, and work-item validation. Personas: Product Manager and Delivery Lead. |

### Brand, creative & content

| Plugin | What it adds |
|---|---|
| **[brand-creative](./brand-creative)** | Brand voice lifecycle (discover, write, enforce) and visual identity guide (colors, type, logo, UI tokens). Writes to instance `brand/` when bound. |
| **[content-marketing](./content-marketing)** | Editorial calendar, social curation, media analysis, captions, and CMS seed drafting (posts and recipes). Two personas (Content Strategist, Content Writer). Reads brand voice from resolved brand path. |
| **[design](./design)** | Wireframes, live-browser UX design review, and UX design fix. Writes to instance `design/` when bound; `engineering` reads wireframes via artefact consumption. |

### Growth & search

| Plugin | What it adds |
|---|---|
| **[search-optimisation](./search-optimisation)** | Keyword research, production technical SEO audits, and on-page content SEO review. One persona (SEO Specialist). Optional pairing with `content-marketing` for seed review. |

### Engineering & platform

| Plugin | What it adds |
|---|---|
| **[architecture](./architecture)** | Solution design (`solution`) and architecture decision records (`adr`). One persona (Principal Architect). Companion to `engineering` for work-item `tdd` and implementation. |
| **[engineering](./engineering)** | Technical design (`tdd`), implementation, peer and final code review, merge requests, documentation passes, debugging, tech debt, QA deploy and exploratory validation, platform health. Five personas share one library; `architecture` and `product-management` are recommended companions. |

### Platform

| Plugin | What it adds |
|---|---|
| **[ralph-loop](./ralph-loop)** | Self-referential delivery loops — ad-hoc and custom presets; engineering-delivery preset contributed by engineering. Ships hooks. |
| **[skills-index](./skills-index)** | Install-aware skill router — `/skills-index:find` |
| **[plugin-management](./plugin-management)** | Create/customize plugins, component authoring, marketplace registration, and skill quality gates (`skills-qa`, `skill-review`) |

**Companion practices:** `content-marketing` invokes `/product-management:tasks --product` and `/product-management:synthesize-research`; `search-optimisation` invokes `/product-management:competitive-brief` rather than bundling duplicates. `architecture` invokes `/engineering:tdd` and `/engineering:docs-review` for work-item design and doc quality. `engineering` invokes `/architecture:solution` / `/architecture:adr` and `/product-management:tasks` for architecture and planning cadence. No direction requires the companion installed — skills degrade gracefully and document the pairing.

## MCP connectors

Each practice plugin bundles a **minimal default** — one or two MCP servers most relevant to that practice — in its `.mcp.json`. Add more entries for your stack; skills produce usable output when no connector is configured.

| Practice | Default bundled | Primary categories |
|---|---|---|
| **brand-creative** | Fireflies | meeting transcription |
| **product-management** | Atlassian, Amplitude | project tracker, product analytics |
| **content-marketing** | Canva | creative / design |
| **design** | Figma, Playwright | design, browser automation |
| **search-optimisation** | Ahrefs | SEO intelligence |
| **architecture** | GitHub | source control (ADR harvest) |
| **engineering** | GitHub, Playwright, Context7 | source control, browser automation, framework docs |

No server is duplicated across plugins. Co-install companion practices or edit `.mcp.json` to add Slack, Notion, Vercel, Sentry, and other common servers — see each practice's CONNECTORS.md for the full placeholder map and suggested additions.

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
| `/<practice>:setup` | Instance repo + handoff to first practice |
| `/<practice>:setup` | Practice profile for that service line |

Framework: [`brand-creative/references/agency-setup-framework.md`](./brand-creative/references/agency-setup-framework.md) and [`practice-setup-framework.md`](./brand-creative/references/practice-setup-framework.md) and synced [`setup-framework.md`](./product-management/references/practice-setup-framework.md) copies in each practice.

**Living profile.** Every skill except `setup` uses **propose profile update** — show the exact diff, ask, write on yes. No skill auto-writes a full profile without confirmation.

## Making it yours

These are reference templates. They get better when you tune them to how your firm works — and the customization mechanism is the plugin itself.

- **Run instance and practice setup.** `setup` and `setup` **are** the customization mechanism. They interview you, read seed documents, and write profiles after you confirm the summary.
- **Edit profiles directly.** Instance facts live in your instance repo; practice conventions at `~/.claude/plugins/config/digital-agency/<practice>/CLAUDE.md`. They survive plugin updates.
- **Propose profile updates from any skill.** When a stable convention surfaces mid-engagement (tone corrections, sprint length, MR template), skills show the exact change and ask before writing.
- **Swap connectors.** Point `.mcp.json` at your source control, hosting, design, and tracker stack. Skills fall back gracefully when a connector is not configured.
- **Bring your brand and templates.** Drop terminology, house style, and branded templates into the instance `brand/` directory and practice profiles.
- **Fork skills for house style.** Every skill is a markdown file under `skills/`. Edit steps, gates, and output formats.

No build step. Everything is markdown and JSON.

## Skill & command reference

The full map across all practice plugins. Run `setup` in each plugin before other commands.

### brand-creative

| Command | Skill | What it does |
|---|---|---|
| `/brand-creative:setup` | setup | Learns voice strictness, channels, seed material; writes practice profile |
| `/brand-creative:brand-voice` | brand-voice | discover, write, review, refine, enforce — `brand/brand-voice.md` |
| `/brand-creative:brand-guide` | brand-guide | write, review, refine — visual identity and UI tokens |

### product-management

| Command | Skill | What it does |
|---|---|---|
| `/product-management:setup` | setup | Learns cadence, audiences, discovery, escalation, sprint length; writes practice profile |
| `/product-management:product` | product | write — `docs/product/product.md` (review via `/engineering:docs-review`) |
| `/product-management:roadmap` | roadmap | write — `docs/product/roadmap.md` after product (+ solution when present); does not require backlog |
| `/product-management:write-spec` | write-spec | Feature spec or PRD from a problem statement |
| `/product-management:product-brainstorming` | product-brainstorming | Sparring partner for ideas (no deliverable) |
| `/product-management:synthesize-research` | synthesize-research | Themes and insights from user research |
| `/product-management:competitive-brief` | competitive-brief | Competitive analysis brief |
| `/product-management:metrics-review` | metrics-review | Product metrics review with actions |
| `/product-management:stakeholder-update` | stakeholder-update | Status update tailored to audience |
| `/product-management:tasks` | tasks | `--product` → backlog after roadmap; `{work-id}` → `specs/{work-short-name}/TASKS.local.md` |
| `/product-management:backlog-refine` | backlog-refine | Groom backlog or judge sprint readiness |
| `/product-management:sprint-planning` | sprint-planning | Sprint plan — `docs/work/sprint-{id}/plan.md` |
| `/product-management:sprint-retro` | sprint-retro | Sprint retrospective — `docs/work/sprint-{id}/retrospective.md` |
| `/product-management:validate` | validate | Work-item completion sign-off against AC and roadmap gates |

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

### design

| Command | Skill | What it does |
|---|---|---|
| `/design:setup` | setup | Learns in-scope pages/flows and reference sources |
| `/design:wireframe` | wireframe | Low-fidelity layout and interaction spec from a brief |
| `/design:ux-design-review` | ux-design-review | Read-only UX review of implemented UI |
| `/design:ux-design-fix` | ux-design-fix | Address UX review findings or direct UI fixes |

### search-optimisation

| Command | Skill | What it does |
|---|---|---|
| `/search-optimisation:setup` | setup | Learns target site, keyword themes, audit cadence |
| `/search-optimisation:keyword-research` | keyword-research | Topic keyword docs with intent and content opportunities |
| `/search-optimisation:technical-seo-audit` | technical-seo-audit | Production audit → tracked issues |
| `/search-optimisation:content-seo-review` | content-seo-review | On-page SEO review of content seeds |

### architecture

| Command | Skill | What it does |
|---|---|---|
| `/architecture:setup` | setup | Learns target binding, architecture scope, companions |
| `/architecture:solution` | solution | write — `docs/architecture/solution.md`; review via `/engineering:docs-review` |
| `/architecture:adr` | adr | plan, write, review — `docs/architecture/decisions/` |

### engineering

| Command | Skill | What it does |
|---|---|---|
| `/engineering:setup` | setup | Learns stack, personas, target binding, connectors |
| `/engineering:tdd` | tdd | write — `specs/{work-short-name}/tdd.md`; review via `docs-review` |
| `/engineering:implement` | implement | Implement a task against approved tdd.md and AC |
| `/engineering:code-review` | code-review | Read-only peer review against tdd.md and tasks |
| `/engineering:code-review-fix` | code-review-fix | Address code-review findings without behaviour change |
| `/engineering:final-code-review` | final-code-review | Final technical gate on open PRs |
| `/engineering:merge-request` | merge-request | Open merge request for implemented work |
| `/engineering:merge-request-babysit` | merge-request-babysit | Drive an open MR/PR to merge-ready |
| `/engineering:merge-request-review` | merge-request-review | Review an MR/PR as its reviewer |
| `/ralph-loop:ralph-loop-setup` | ralph-loop-setup | Seed and configure an autonomous delivery loop |
| `/ralph-loop:ralph-loop` | ralph-loop | Run an autonomous work-item delivery loop |
| `/engineering:docs-review` | docs-review | Read-only document-set quality and consistency review |
| `/engineering:debug` | debug | Bug investigation and fix |
| `/engineering:tech-debt` | tech-debt | Technical debt audit and prioritization |
| `/engineering:deploy-qa` | deploy-qa | Prepare QA workspace |
| `/engineering:run-automated-suite` | run-automated-suite | Run automated tests in QA workspace |
| `/engineering:exploratory-pass` | exploratory-pass | AC-driven exploratory validation |
| `/engineering:document-defects` | document-defects | Record defects from QA pass |
| `/engineering:platform-health` | platform-health | CI/CD, deployment, and platform health check |

## Contributing

Everything here is markdown and JSON. Fork, edit, PR. See [CONTRIBUTING.md](./CONTRIBUTING.md) for design principles and the validation checklist.

- **New skill** → add `<practice>/skills/<skill-name>/SKILL.md` with `name` and `description` frontmatter. Invokable as `/<practice>:<skill-name>`.
- **New persona row** → add the skill under the owning practice and a row in that practice's README Agents/Personas table mapping the job title to the slash command.
- **Shared meta-framework edits** → run `python3 scripts/sync-references.py` after changing `instance-profile-template.md` or `setup-framework.md`.
- **Validate before opening a PR** — `python3 scripts/validate.py` lints manifests, verifies cross-file references, and validates evals schema. See [AGENTS.md](./AGENTS.md) for repo conventions.

## License

Licensed under the [MIT License](./LICENSE).

Copyright 2026 Carinya Parc Pty Ltd.
