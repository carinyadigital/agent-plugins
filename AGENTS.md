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
├── agency-hub/                      # instance bootstrap + (v2) marketplace — install first
│   ├── .claude-plugin/plugin.json
│   ├── .cursor-plugin/plugin.json
│   ├── .mcp.json
│   ├── references/                  # instance profile template, setup framework
│   └── skills/
│       └── agency-setup/SKILL.md    # instance bootstrap; marketplace skills ported from strategy-builder-hub
├── .agents/                         # local maintainer skills & tooling
│   ├── config                       #   crew runtime — steering + work paths for this repo
│   ├── steering/                    #   strategy, solution, roadmap, backlog (gitignored)
│   ├── work/                        #   epic work artefacts (gitignored)
│   ├── skills/                      #   plugin-eval, skills-qa
│   └── references/                  #   agency skill design framework
├── agents/                          # named agents — one self-contained plugin each
│   └── <slug>/
│       ├── .claude-plugin/plugin.json
│       ├── .cursor-plugin/plugin.json
│       ├── agents/<slug>.md         #   ← canonical system prompt (one source, two wrappers)
│       └── skills/                  #   ← bundled copies, synced from skills/
├── connectors/                      #   MCP connector plugins — one provider each
│   └── <slug>/
│       ├── .claude-plugin/plugin.json
│       ├── .cursor-plugin/plugin.json
│       └── .mcp.json                #   ← canonical MCP definition
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
└── scripts/                         # sync-agent-skills.py, sync-references.py, validate.py
```

Run `python3 scripts/sync-agent-skills.py` after editing a skill under `skills/`, `brand-creative/skills/`, `delivery-practice/skills/`, or `content-marketing/skills/` — it propagates bundled copies into agents that bundle those skills. **Edit discipline skills in `skills/`**, **brand skills in `brand-creative/skills/`**, **delivery skills in `delivery-practice/skills/`**, and **content skills in `content-marketing/skills/`**, not in agent bundles.

Run `python3 scripts/sync-references.py` after editing shared meta-framework files (`instance-profile-template.md`, `practice-setup-framework.md`).

Run `python3 scripts/validate.py` before opening a PR — it lints marketplace and plugin manifests, checks MCP connector wiring, validates SKILL.md frontmatter, resolves markdown cross-references, detects bundled-skill drift against canonical sources, and validates `evals/` JSON schema.

## Agency Hub (install first)

| Plugin | Skills (v1) | Status |
| ------ | ----------- | ------ |
| `agency-hub` | `agency-setup` + marketplace skills (ported from strategy-builder-hub) | Shipped; skills-qa alignment with agency framework — refine later |
| `brand-creative` | `practice-setup`, `brand-guide`, `brand-voice` | Shipped; first MECE practice plugin |
| `delivery-practice` | `practice-setup` + 13 delivery skills (`product`, `roadmap`, `backlog`, `tasks`, `sprint`, `validate`, `write-spec`, `stakeholder-update`, `synthesize-research`, `competitive-brief`, `metrics-review`, `product-brainstorming`, `skills-index`) | Shipped; second MECE practice plugin — Product Manager and Delivery Lead personas, no separate agent plugins |
| `content-marketing` | `practice-setup` + 7 content skills (`content-calendar`, `curate-content`, `analyse-media`, `write-captions`, `edit-content`, `draft-post`, `draft-recipe`) | Shipped; third MECE practice plugin — Content Strategist and Content Writer personas, no separate agent plugins; reads `brand-voice.md` via artifact consumption; invokes `/delivery-practice:backlog` and `/delivery-practice:synthesize-research` as companion skills |

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

Product Manager and Delivery Lead are **personas inside `delivery-practice`**, not standalone agent plugins. Content Strategist and Content Writer are **personas inside `content-marketing`**, not standalone agent plugins. Invoke skills directly: `/delivery-practice:product`, `/content-marketing:content-calendar write`, etc.

Each agent lives under `agents/<slug>/` with a canonical system prompt at `agents/<slug>.md`, bundled skills at `skills/`, and role-specific MCP in `.mcp.json`. Register new agents in both marketplace manifests.

## Local maintainer tooling (`.agents/`)

Repo-local skill quality tooling and crew runtime config for contributors — not published as a marketplace plugin:

| Component | Purpose |
| --- | --- |
| **config** (`.agents/config`) | Steering doc paths and work directory for this repo |
| **steering** (`.agents/steering/`) | Strategy, solution, roadmap, backlog for this repository (gitignored) |
| **plugin-eval** (`.agents/skills/plugin-eval/SKILL.md`) | Live eval sessions — grade assertions in `evals/evals.json` |
| **skills-qa** (`.agents/skills/skills-qa/SKILL.md`) | Evaluate a skill against the Agency Skill Design Framework before shipping |

## Key Files

- `.claude-plugin/marketplace.json` / `.cursor-plugin/marketplace.json`: Marketplace manifests — register all plugins with source paths
- `plugin.json`: Plugin metadata — name, description, version, and component discovery settings
- `commands/*.md`: Slash commands invoked as `/plugin:command-name`
- `skills/*/SKILL.md`: Detailed knowledge and workflows for specific tasks
- `connectors/<slug>/.mcp.json`: Canonical MCP connector definitions (GitHub, GitLab, Vercel, Figma, Linear, Playwright, Context7, Next.js DevTools)
- `scripts/validate.py`: Structural validation — run before every PR
- `*.local.md`: User-specific configuration (gitignored)

## Development Workflow

1. Edit markdown files directly — changes take effect immediately
2. After skill changes under `skills/`, run `python3 scripts/sync-agent-skills.py`
3. Run `python3 scripts/validate.py` — fix errors before pushing
4. Test commands with `/plugin:command-name` syntax (Cowork) or install via Cursor Settings → Plugins
5. Skills are invoked automatically when their trigger conditions match
