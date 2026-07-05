# Digital Agency Plugins

Claude and Cursor plugins and Managed Agent templates for digital agency workflows. Each named agent ships two ways from one source.

## Repository Structure

```
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
└── scripts/                         # sync-agent-skills.py, validate.py (+ orchestrate.py, deploy-managed-agent.sh — coming soon)
```

Run `python3 scripts/sync-agent-skills.py` after editing a skill under `skills/` — it propagates bundled copies into every agent under `agents/` that uses that skill. **Edit skills in `skills/`**, not in agent bundles.

Run `python3 scripts/validate.py` before opening a PR — it lints marketplace and plugin manifests, checks MCP connector wiring, validates SKILL.md frontmatter, resolves markdown cross-references, detects bundled-skill drift against `skills/`, and validates `evals/` JSON schema. Use `--format json` for CI; `--strict` once skills ship full agency-framework frontmatter. CI runs the same check on every PR via `.github/workflows/validate.yml`. Install the local pre-commit hook with `scripts/install-git-hooks.sh`. A `version-bump` GitHub Action (coming soon) will patch-bump each plugin's `plugin.json` `version` so a branch ends up exactly one patch ahead of `main`.

## Agency Hub (install first)

| Plugin | Skills (v1) | Status |
| ------ | ----------- | ------ |
| `agency-hub` | `agency-setup` + marketplace skills (ported from strategy-builder-hub) | Shipped; skills-qa alignment with agency framework — refine later |

Bootstraps a git-versioned instance repo (`config/instance.json`, `config/targets/`, `squads/`, `brand/`). See `agency-hub/README.md` and `agency-hub/references/agency-setup-framework.md`.

## Agents (current roster)

| Slug | Practice | Bundled skills | Status |
| ---- | -------- | -------------- | ------ |
| `frontend-engineer` | Engineering | `implement`, `code-review`, `create-mr`, `brand-guide`, `component-scaffold` (agent-local) | Shipped; not yet operationally proven |
| `senior-frontend-engineer` | Engineering | `code-review`, `design` | Shipped; not yet operationally proven |
| `product-manager` | Product | All 13 product-management skills (`product`, `roadmap`, `backlog`, `tasks`, `sprint`, `validate`, `write-spec`, `stakeholder-update`, `synthesize-research`, `competitive-brief`, `metrics-review`, `product-brainstorming`, `skills-index`) | Shipped; not yet operationally proven |
| `principal-frontend-engineer` | Engineering | `final-code-review`, `code-review`, `design`, `validate` | Shipped; not yet operationally proven |
| `qa-engineer` | Engineering | `deploy-qa`, `run-automated-suite`, `exploratory-pass`, `document-defects` | Shipped; not yet operationally proven |
| `webops-engineer` | Engineering | `deploy-qa`, `debug`, `platform-health` | Shipped; not yet operationally proven |
| `content-strategist` | Content | `content-calendar`, `curate-content`, `synthesize-research`, `brand-voice`, `backlog` | Shipped; not yet operationally proven |
| `content-writer` | Content | `draft-post`, `draft-recipe`, `write-captions`, `edit-content`, `brand-voice` | Shipped; not yet operationally proven |
| `seo-specialist` | SEO | `keyword-research`, `technical-seo-audit`, `content-seo-review`, `competitive-brief` | Shipped; not yet operationally proven |
| `delivery-lead` | Operations (cross-cutting) | `skills-index`, `backlog`, `tasks`, `sprint`, `validate`, `stakeholder-update`, `metrics-review` | Shipped; not yet operationally proven |
| `principal-architect` | Engineering (Architecture) | `solution`, `adr`, `design`, `docs` | Shipped; not yet operationally proven |

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
