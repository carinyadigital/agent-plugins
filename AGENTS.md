# Digital Agency Plugins

Claude and Cursor plugins for digital agency workflows, organised as **MECE practice plugins** — each practice is a self-contained install unit that owns its skill library outright. Personas (Frontend Engineer, Product Manager, Content Writer, SEO Specialist, …) are invoked via slash commands on the owning practice plugin, not as separate agent plugins.

## Repository Structure

```
├── agency-hub/                      # instance bootstrap + (v2) marketplace — install first
│   ├── .claude-plugin/plugin.json
│   ├── .cursor-plugin/plugin.json
│   ├── .mcp.json                    # bundled MCP servers (e.g. GitHub for hub bootstrap)
│   ├── references/                  # agency-setup framework, instance profile template (canonical)
│   └── skills/
│       └── agency-setup/SKILL.md    # instance bootstrap; marketplace skills ported from strategy-builder-hub
├── brand-creative/                  # practice plugin — brand-guide, brand-voice, practice-setup
├── delivery-practice/               # practice plugin — product, roadmap, backlog, sprint, validate, …
├── content-marketing/               # practice plugin — calendar, drafts, captions, analyse-media, …
├── ux-design/                       # practice plugin — wireframe, practice-setup
├── search-optimisation/             # practice plugin — keyword-research, technical-seo-audit, content-seo-review
├── web-development/                 # practice plugin — solution, design, implement, code-review, deploy-qa, …
├── managed-agents/                  # CMA cookbooks (coming soon) — headless deployment definitions
├── hooks/                           # repo-level hooks.json (empty scaffold)
├── tests/                           # unit tests for the validation scripts
└── scripts/                         # sync-references.py, validate.py, plugin-check.py, deploy-squad-agents.sh
```

Every practice plugin follows the same internal layout:

```
<practice>/
├── .claude-plugin/plugin.json       # Claude manifest
├── .cursor-plugin/plugin.json       # Cursor manifest (kept identical)
├── .mcp.json                        # bundled MCP servers for this practice
├── hooks/hooks.json                 # empty scaffold
├── references/                      # <practice>-conventions.md + synced meta-framework files
└── skills/
    └── <name>/
        ├── SKILL.md                 # frontmatter: name, description, allowed-tools, metadata
        ├── assets/                  # optional templates
        └── references/              # optional skill-local references
```

Practice plugins own their skills outright — edit skills in the owning plugin's `skills/` directory (`brand-creative/skills/`, `delivery-practice/skills/`, `content-marketing/skills/`, `ux-design/skills/`, `search-optimisation/skills/`, `web-development/skills/`, `agency-hub/skills/`).

Run `python3 scripts/sync-references.py` after editing shared meta-framework files (`instance-profile-template.md` — canonical in `agency-hub/references/`; `practice-setup-framework.md` — canonical in `brand-creative/references/`). Synced copies land in every practice plugin's `references/`.

Run `python3 scripts/validate.py` before opening a PR — it lints marketplace and plugin manifests, checks practice-plugin MCP wiring, validates SKILL.md frontmatter, resolves markdown cross-references, and validates `evals/` JSON schema. Use `python3 scripts/plugin-check.py <plugin-dir>` for fast per-plugin checks while iterating.

## Plugin catalogue

| Plugin | Skills (v1) | Personas | Status |
| ------ | ----------- | -------- | ------ |
| `agency-hub` | `agency-setup` + marketplace skills (`skill-installer`, `registry-browser`, `skills-qa`, `auto-updater`, `uninstall`, `disable`, `skill-manager`, `related-skills-surfacer`) | — | Shipped; install first |
| `brand-creative` | `practice-setup`, `brand-guide`, `brand-voice` | — | Shipped |
| `delivery-practice` | `practice-setup` + 13 delivery skills (`product`, `roadmap`, `backlog`, `tasks`, `sprint`, `validate`, `write-spec`, `stakeholder-update`, `synthesize-research`, `competitive-brief`, `metrics-review`, `product-brainstorming`, `skills-index`) | Product Manager, Delivery Lead | Shipped |
| `content-marketing` | `practice-setup` + 7 content skills (`content-calendar`, `curate-content`, `analyse-media`, `write-captions`, `edit-content`, `draft-post`, `draft-recipe`) | Content Strategist, Content Writer | Shipped; reads `brand-voice.md` via artifact consumption; invokes `/delivery-practice:backlog` and `/delivery-practice:synthesize-research` as companion skills |
| `ux-design` | `practice-setup`, `wireframe` | — | Shipped; minimal v1 — writes wireframes to `<instance-root>/design/`; downstream practices read via artifact consumption |
| `search-optimisation` | `practice-setup` + 3 SEO skills (`keyword-research`, `technical-seo-audit`, `content-seo-review`) | SEO Specialist | Shipped; invokes `/delivery-practice:competitive-brief` as companion skill |
| `web-development` | `practice-setup` + 15 engineering skills (`solution`, `adr`, `design`, `implement`, `code-review`, `final-code-review`, `create-mr`, `debug`, `deploy-qa`, `run-automated-suite`, `exploratory-pass`, `document-defects`, `platform-health`, `tech-debt`, `docs`) | Frontend Engineer, Senior Frontend Engineer, Principal Frontend Engineer, QA Engineer, WebOps Engineer, Principal Architect | Shipped; not yet operationally proven — reads `brand-guide.md` from resolved brand path; invokes `/delivery-practice:backlog` and `/delivery-practice:sprint` as companion skills |

`agency-hub` bootstraps a git-versioned instance repo (`config/instance.json`, `config/targets/`, `squads/`, `brand/`). See `agency-hub/README.md` and `agency-hub/references/agency-setup-framework.md`.

**Cross-practice relationships:**

- **Artifact consumption** — read another practice's output file (e.g. `web-development` reads `brand-guide.md` and wireframes from `design/`).
- **Companion practice** — co-install and invoke skills directly (e.g. `web-development` → `/delivery-practice:backlog`; `content-marketing` → `/delivery-practice:synthesize-research`). Skills are invoked as `/<plugin>:<skill>`.

**Retired:** standalone agent plugins under `agents/` and discipline skill folders under `skills/` — skills now live only inside their owning practice plugin. `social-media` practice plugin is pending; interim: `content-marketing` skills for captions and curation.

Strategy, roadmap, backlog, and epic work for this catalogue live in the **carinyaparc-space** coordination repo under `products/digital-agency/` — not in this repo.

## Key Files

- `.claude-plugin/marketplace.json` / `.cursor-plugin/marketplace.json`: Marketplace manifests — register all plugins with source paths (keep both in sync)
- `<plugin>/.claude-plugin/plugin.json` / `<plugin>/.cursor-plugin/plugin.json`: Plugin metadata — name, description, version, and skill discovery (keep both in sync)
- `<plugin>/skills/*/SKILL.md`: Skill definitions — invoked as `/<plugin>:<skill>` or triggered automatically by description match
- `<practice>/.mcp.json`: Bundled MCP server definitions per practice plugin (GitHub, GitLab, Vercel, Figma, Linear, Playwright, Context7, Next.js DevTools, and practice-specific providers)
- `<practice>/references/<practice>-conventions.md`: Canonical path resolution and artefact boundaries for that practice
- `scripts/validate.py`: Structural validation — run before every PR
- `*.local.md`: User-specific configuration (gitignored)

## Development Workflow

1. Edit markdown files directly — changes take effect immediately
2. After editing shared meta-framework references, run `python3 scripts/sync-references.py`
3. Run `python3 scripts/validate.py` — fix errors before pushing
4. Test commands with `/plugin:skill-name` syntax (Cowork) or install via Cursor Settings → Plugins
5. Skills are invoked automatically when their trigger conditions match
