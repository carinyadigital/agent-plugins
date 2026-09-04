# Digital Agency Plugins

Claude and Cursor plugins for digital agency workflows.

## Repository Structure

```
├── brand-creative/                  # practice plugin — brand-guide, brand-voice, setup (MECE owned)
│   ├── references/                  # brand-conventions + synced meta-framework files
│   └── skills/
├── product-management/              # practice plugin — product + delivery skills (MECE owned)
│   ├── references/                  # product-conventions, delivery-conventions + synced meta-framework files
│   └── skills/
├── content-marketing/               # practice plugin — calendar, drafts, captions, analyse-media (MECE owned)
│   ├── references/                  # content-conventions + synced meta-framework files
│   └── skills/
├── architecture/                    # practice plugin — solution, adr, setup (MECE owned)
├── design/                          # practice plugin — wireframe, ux-design-review, ux-design-fix (MECE owned)
│   ├── references/                  # design-conventions + synced meta-framework files
│   └── skills/
├── engineering/                     # practice plugin — design, implement, review, QA, WebOps (MECE owned)
├── ralph-loop/                      # ralph-loop + ralph-loop-setup + hooks
├── skills-index/                    # find + related-skills-surfacer
├── plugin-management/               # create/customize plugins + skills-qa / skill-review
│   ├── references/                  # agency-skill-design-framework
│   └── skills/
├── search-optimisation/             # practice plugin — keyword-research, technical-seo-audit, content-seo-review (MECE owned)
│   ├── references/                  # search-optimisation-conventions + synced meta-framework files
│   └── skills/
├── brand-creative/                      # instance bootstrap + (v2) marketplace — install first
│   ├── .claude-plugin/plugin.json
│   ├── .cursor-plugin/plugin.json
│   ├── .mcp.json                    # bundled MCP servers (e.g. GitHub for hub bootstrap)
│   ├── references/                  # instance profile template, setup framework
│   └── skills/
│       └── setup/SKILL.md    # instance bootstrap; marketplace skills ported from strategy-builder-hub
├── agents/                          # named agents — one self-contained plugin each
│   └── <slug>/
│       ├── .claude-plugin/plugin.json
│       ├── .cursor-plugin/plugin.json
│       ├── agents/<slug>.md         #   ← canonical system prompt (one source, two wrappers)
│       └── skills/                  #   ← bundled copies, synced from skills/
├── skills/                          #   skill plugins — skill sources, commands
│   └── <discipline>/
│       ├── .claude-plugin/plugin.json
│       ├── .cursor-plugin/plugin.json
│       ├── commands/
│       └── skills/
│           └── <name>/
│               ├── SKILL.md
│               ├── prompts/
│               ├── agents/      #   sub-agents for this skill
│               ├── evals/       #   evals.json + trigger-queries.json
│               └── scripts/     #   optional helper scripts
└── scripts/                         # sync-references.py, validate.py, validate_plugins.py, validate_skills.py
```

Practice plugins own their skills outright — edit skills in the owning plugin's `skills/` directory (`brand-creative/skills/`, `product-management/skills/`, `content-marketing/skills/`, `design/skills/`, `search-optimisation/skills/`, `engineering/skills/`, `architecture/skills/`).

Run `python3 scripts/sync-references.py` after editing shared meta-framework files in `references/` (`instance-profile-template.md`, `practice-setup-framework.md`).

Run `python3 scripts/validate.py` before opening a PR — it runs plugin-domain and skill-domain validators (marketplace/plugin manifests, MCP wiring, SKILL.md frontmatter + budgets, every `**/agents/*.md` contract, orphan SKILL.md, markdown cross-references, evals schema). Use `python3 scripts/validate_plugins.py <plugin-dir>` for fast per-plugin checks while iterating.


| Plugin | Skills (v1) | Status |
| ------ | ----------- | ------ |
| `brand-creative` | `setup`, `brand-guide`, `brand-voice` | Shipped; first MECE practice plugin |
| `product-management` | `setup` + PM + delivery skills (`product`, `roadmap`, `write-spec`, `product-brainstorming`, `synthesize-research`, `competitive-brief`, `metrics-review`, `stakeholder-update`, `tasks`, `backlog-refine`, `sprint-planning`, `sprint-retro`, `validate`) | Shipped; MECE practice plugin — Product Manager and Delivery Lead personas, no separate agent plugins |
| `content-marketing` | `setup` + 7 content skills (`content-calendar`, `curate-content`, `analyse-media`, `write-captions`, `edit-content`, `draft-post`, `draft-recipe`) | Shipped; MECE practice plugin — Content Strategist and Content Writer personas, no separate agent plugins; reads `brand-voice.md` via artifact consumption; invokes `/product-management:tasks --product` and `/product-management:synthesize-research` as companion skills |
| `architecture` | `setup`, `solution`, `adr` | Shipped; MECE practice — Principal Architect persona; companion to engineering for design/implement |
| `engineering` | `setup` + design, discover/deliver agents, implement, review, MR, docs-review, QA, WebOps skills | Shipped; MECE practice — five engineering personas; architecture and product-management as companions |
| `design` | `setup`, `wireframe`, `ux-design-review`, `ux-design-fix` | Shipped; writes wireframes to `<instance-root>/design/`; live-browser review/fix; downstream practices read via artifact consumption |
| `ralph-loop` | `ralph-loop`, `ralph-loop-setup` | Shipped; ships hooks; engineering-delivery preset contributed by engineering |
| `skills-index` | `find`, `related-skills-surfacer` | Shipped; install-aware router |
| `plugin-management` | `create-plugin`, `customize-plugin`, component-authoring skills, `skills-qa`, `skill-review` | Shipped; meta-plugin + former skill-authoring quality gates |
| `search-optimisation` | `setup` + 3 SEO skills (`keyword-research`, `technical-seo-audit`, `content-seo-review`) | Shipped; one persona (SEO Specialist), no separate agent plugin; invokes `/product-management:competitive-brief` as companion skill |

Practice `setup` skills bootstrap a git-versioned instance repo when `config/instance.json` is absent (`config/instance.json`, `config/targets/`, `squads/`, `brand/`). See `brand-creative/README.md` and `brand-creative/references/agency-setup-framework.md`.

## Agents (current roster)

| Slug | Practice | Bundled skills | Status |
| ---- | -------- | -------------- | ------ |
| `frontend-engineer` | Engineering | `implement`, `code-review`, `merge-request`, `component-scaffold` (agent-local); reads `brand-guide.md` from resolved brand path | Shipped; not yet operationally proven |
| `senior-frontend-engineer` | Engineering | `code-review`, `design` | Shipped; not yet operationally proven |
| `principal-frontend-engineer` | Engineering | `code-review`, `design`, `validate` (synced from product-management) | Shipped; not yet operationally proven |
| `qa-engineer` | Engineering | `deploy-qa`, `run-automated-suite`, `exploratory-pass`, `document-defects` | Shipped; not yet operationally proven |
| `webops-engineer` | Engineering | `deploy-qa`, `debug`, `platform-health` | Shipped; not yet operationally proven |
| `principal-architect` | Architecture | `solution`, `adr` (practice: `architecture`); `design` / `docs-review` via engineering companion | Persona in `architecture`; not a standalone agent plugin |

Product Manager and Delivery Lead are **personas inside `product-management`**, not standalone agent plugins. Content Strategist and Content Writer are **personas inside `content-marketing`**, not standalone agent plugins. SEO Specialist is a **persona inside `search-optimisation`**, not a standalone agent plugin. Principal Architect is a **persona inside `architecture`**, not a standalone agent plugin. Invoke skills directly: `/product-management:product`, `/architecture:solution`, `/engineering:design`, `/content-marketing:content-calendar write`, `/search-optimisation:keyword-research`, etc.

Each agent lives under `agents/<slug>/` with a canonical system prompt at `agents/<slug>.md`, bundled skills at `skills/`, and role-specific MCP in `.mcp.json`. Register new agents in both marketplace manifests.

Strategy, roadmap, backlog, and epic work for this catalogue live in the **carinyaparc-space** coordination repo under `products/digital-agency/` — not in this repo.

## Key Files

- `.claude-plugin/marketplace.json` / `.cursor-plugin/marketplace.json`: Marketplace manifests — register all plugins with source paths
- `plugin.json`: Plugin metadata — name, description, version, and component discovery settings
- `commands/*.md`: Slash commands invoked as `/plugin:command-name`
- `skills/*/SKILL.md`: Detailed knowledge and workflows for specific tasks
- `<practice>/.mcp.json`: Bundled MCP server definitions per practice plugin (GitHub, GitLab, Vercel, Figma, Linear, Playwright, Context7, Next.js DevTools, and practice-specific providers)
- `scripts/validate.py`: Structural validation orchestrator — run before every PR
- `scripts/validate_plugins.py` / `scripts/validate_skills.py`: Domain validators
- `*.local.md`: User-specific configuration (gitignored)

## Development Workflow

1. Edit markdown files directly — changes take effect immediately
2. After editing shared meta-framework references, run `python3 scripts/sync-references.py`
3. Run `python3 scripts/validate.py` — fix errors before pushing
4. Test commands with `/plugin:command-name` syntax (Cowork) or install via Cursor Settings → Plugins
5. Skills are invoked automatically when their trigger conditions match
