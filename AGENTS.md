# Digital Agency Plugins

Claude and Cursor plugins and Managed Agent templates for digital agency workflows. Each named agent ships two ways from one source.

## Repository Structure

```
├── brand-creative/                  # practice plugin — brand-guide, brand-voice, practice-setup (MECE owned)
│   ├── references/                  # brand-conventions + synced meta-framework files
│   └── skills/
├── delivery-practice/               # practice plugin — product, backlog, sprint, validate, … (MECE owned)
│   ├── references/                  # delivery-conventions + synced meta-framework files
│   └── skills/
├── content-marketing/               # practice plugin — calendar, drafts, captions, analyse-media (MECE owned)
│   ├── references/                  # content-conventions + synced meta-framework files
│   └── skills/
├── ux-design/                       # practice plugin — wireframe, practice-setup (MECE owned)
│   ├── references/                  # ux-design-conventions + synced meta-framework files
│   └── skills/
├── search-optimisation/             # practice plugin — keyword-research, technical-seo-audit, content-seo-review (MECE owned)
│   ├── references/                  # search-optimisation-conventions + synced meta-framework files
│   └── skills/
├── agency-hub/                      # instance bootstrap + (v2) marketplace — install first
│   ├── .claude-plugin/plugin.json
│   ├── .cursor-plugin/plugin.json
│   ├── .mcp.json                    # bundled MCP servers (e.g. GitHub for hub bootstrap)
│   ├── references/                  # instance profile template, setup framework
│   └── skills/
│       └── agency-setup/SKILL.md    # instance bootstrap; marketplace skills ported from strategy-builder-hub
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
├── managed-agents/                  #   CMA cookbooks (coming soon) — one dir per named agent
│   └── <slug>/
│       ├── agent.yaml               #   system + skills → ../../agents/<slug>/...
│       ├── subagents/*.yaml         #   depth-1 leaf workers
│       ├── steering-examples.json
│       └── README.md                #   security tier + handoff notes
└── scripts/                         # sync-references.py, validate.py, plugin-check.py
```

Practice plugins own their skills outright — edit skills in the owning plugin's `skills/` directory (`brand-creative/skills/`, `delivery-practice/skills/`, `content-marketing/skills/`, `ux-design/skills/`, `search-optimisation/skills/`, `web-development/skills/`, `agency-hub/skills/`).

Run `python3 scripts/sync-references.py` after editing shared meta-framework files (`instance-profile-template.md`, `practice-setup-framework.md`).

Run `python3 scripts/validate.py` before opening a PR — it lints marketplace and plugin manifests, checks practice-plugin MCP wiring, validates SKILL.md frontmatter, resolves markdown cross-references, and validates `evals/` JSON schema. Use `python3 scripts/plugin-check.py <plugin-dir>` for fast per-plugin checks while iterating.

## Agency Hub (install first)

| Plugin | Skills (v1) | Status |
| ------ | ----------- | ------ |
| `agency-hub` | `agency-setup` + marketplace skills (ported from strategy-builder-hub) | Shipped; skills-qa alignment with agency framework — refine later |
| `brand-creative` | `practice-setup`, `brand-guide`, `brand-voice` | Shipped; first MECE practice plugin |
| `delivery-practice` | `practice-setup` + 13 delivery skills (`product`, `roadmap`, `backlog`, `tasks`, `sprint`, `validate`, `write-spec`, `stakeholder-update`, `synthesize-research`, `competitive-brief`, `metrics-review`, `product-brainstorming`, `skills-index`) | Shipped; second MECE practice plugin — Product Manager and Delivery Lead personas, no separate agent plugins |
| `content-marketing` | `practice-setup` + 7 content skills (`content-calendar`, `curate-content`, `analyse-media`, `write-captions`, `edit-content`, `draft-post`, `draft-recipe`) | Shipped; third MECE practice plugin — Content Strategist and Content Writer personas, no separate agent plugins; reads `brand-voice.md` via artifact consumption; invokes `/delivery-practice:backlog` and `/delivery-practice:synthesize-research` as companion skills |
| `ux-design` | `practice-setup`, `wireframe` | Shipped; minimal v1 — no dedicated persona; writes wireframes to `<instance-root>/design/`; downstream practices read via artifact consumption |
| `search-optimisation` | `practice-setup` + 3 SEO skills (`keyword-research`, `technical-seo-audit`, `content-seo-review`) | Shipped; one persona (SEO Specialist), no separate agent plugin; invokes `/delivery-practice:competitive-brief` as companion skill |

Bootstraps a git-versioned instance repo (`config/instance.json`, `config/targets/`, `squads/`, `brand/`). See `agency-hub/README.md` and `agency-hub/references/agency-setup-framework.md`.

## Agents (current roster)

| Slug | Practice | Bundled skills | Status |
| ---- | -------- | -------------- | ------ |
| `frontend-engineer` | Engineering | `implement`, `code-review`, `create-mr`, `component-scaffold` (agent-local); reads `brand-guide.md` from resolved brand path | Shipped; not yet operationally proven |
| `senior-frontend-engineer` | Engineering | `code-review`, `design` | Shipped; not yet operationally proven |
| `principal-frontend-engineer` | Engineering | `final-code-review`, `code-review`, `design`, `validate` (synced from delivery-practice) | Shipped; not yet operationally proven |
| `qa-engineer` | Engineering | `deploy-qa`, `run-automated-suite`, `exploratory-pass`, `document-defects` | Shipped; not yet operationally proven |
| `webops-engineer` | Engineering | `deploy-qa`, `debug`, `platform-health` | Shipped; not yet operationally proven |
| `principal-architect` | Engineering (Architecture) | `solution`, `adr`, `design`, `docs` | Shipped; not yet operationally proven |

Product Manager and Delivery Lead are **personas inside `delivery-practice`**, not standalone agent plugins. Content Strategist and Content Writer are **personas inside `content-marketing`**, not standalone agent plugins. SEO Specialist is a **persona inside `search-optimisation`**, not a standalone agent plugin. Invoke skills directly: `/delivery-practice:product`, `/content-marketing:content-calendar write`, `/search-optimisation:keyword-research`, etc.

Each agent lives under `agents/<slug>/` with a canonical system prompt at `agents/<slug>.md`, bundled skills at `skills/`, and role-specific MCP in `.mcp.json`. Register new agents in both marketplace manifests.

Strategy, roadmap, backlog, and epic work for this catalogue live in the **carinyaparc-space** coordination repo under `products/digital-agency/` — not in this repo.

## Key Files

- `.claude-plugin/marketplace.json` / `.cursor-plugin/marketplace.json`: Marketplace manifests — register all plugins with source paths
- `plugin.json`: Plugin metadata — name, description, version, and component discovery settings
- `commands/*.md`: Slash commands invoked as `/plugin:command-name`
- `skills/*/SKILL.md`: Detailed knowledge and workflows for specific tasks
- `<practice>/.mcp.json`: Bundled MCP server definitions per practice plugin (GitHub, GitLab, Vercel, Figma, Linear, Playwright, Context7, Next.js DevTools, and practice-specific providers)
- `scripts/validate.py`: Structural validation — run before every PR
- `*.local.md`: User-specific configuration (gitignored)

## Development Workflow

1. Edit markdown files directly — changes take effect immediately
2. After editing shared meta-framework references, run `python3 scripts/sync-references.py`
3. Run `python3 scripts/validate.py` — fix errors before pushing
4. Test commands with `/plugin:command-name` syntax (Cowork) or install via Cursor Settings → Plugins
5. Skills are invoked automatically when their trigger conditions match
