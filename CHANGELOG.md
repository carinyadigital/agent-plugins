# Changelog

All notable changes to this project are documented here. Version numbers match
Git tags and the `version` field in `.cursor-plugin/plugin.json` and
`.claude-plugin/plugin.json`.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### delivery-practice / web-development — skills parity with carinyaparc/skills 2.1.0

Breaking skill reshape aligned with upstream [carinyaparc/skills](https://github.com/carinyaparc/skills) 2.1.0. Artefact paths remain under `.agency/`.

#### delivery-practice

- **BREAKING:** `backlog` removed — merged into `tasks` (`tasks --product` → `.agency/backlog.md`)
- **BREAKING:** `sprint` → `sprint-planning` + `sprint-retro`
- **Added:** `backlog-refine`
- **BREAKING:** `refine` mode removed from `product` and `roadmap` (use `review`)

#### web-development

- **BREAKING:** `code-review fix` → `code-review-fix`; reviews are read-only
- **BREAKING:** `ux-design-review fix` → `ux-design-fix`
- **BREAKING:** `merge-request babysit` → `merge-request-babysit`
- **BREAKING:** `docs` → `docs-review` (read-only)
- **BREAKING:** `ralph` → `ralph-loop` + `ralph-loop-setup`; hooks under `hooks/{claude,cursor}/`; seed via `scripts/seed-ralph-loop.sh`
- **BREAKING:** `refine` mode removed from `solution`

## [2026-07-05] — Connector integrations

New bundled MCP connectors and updated connector documentation across five
practice plugins.

### content-marketing — v0.2.0

- Bundled Canva MCP (`https://mcp.canva.com/mcp`) for social graphics and
  template autofill
- Updated CONNECTORS.md and practice-setup integration check to include Canva

### search-optimisation — v0.2.0

- Bundled Ahrefs MCP for SEO intelligence (keyword volume, difficulty,
  backlink data)
- Updated CONNECTORS.md, README, and practice-setup skill for Ahrefs and
  optional Semrush / Search Console guidance

### web-development — v0.2.0

- Bundled Sentry MCP (`https://mcp.sentry.dev/mcp`) for error tracking
- Updated CONNECTORS.md and practice-setup integration check to include Sentry

### brand-creative — v0.1.1

- CONNECTORS.md: document Canva, Google Drive, and SharePoint as design and
  file-storage options

### ux-design — v0.1.1

- CONNECTORS.md: document Canva as an optional design reference for social-sized
  layouts

## [2026-07-05] — Practice plugins v0.1.0

First tagged release of the MECE practice-plugin catalogue: seven
independently versioned plugins, each tagged individually
(`<plugin>-v0.1.0`) and installed as a complete practice — a practice-setup
interview plus an owned skill library — rather than the earlier standalone
agent-plugin architecture.

### agency-hub — v0.1.0

- Bootstraps a git-versioned instance workspace (`config/`, `brand/`,
  `squads/`) via `setup`
- Skills: agency-setup, auto-updater, disable, registry-browser,
  related-skills-surfacer, skill-installer, skill-manager, skills-qa,
  uninstall

### brand-creative — v0.1.0

- Complete brand practice — setup interview, brand-voice lifecycle,
  brand-guide visual identity
- Writes to the instance `brand/` directory when bound; standalone Try tier
  uses `docs/brand/`
- Skills: brand-guide, brand-voice, practice-setup

### content-marketing — v0.1.0

- Complete content practice — setup interview, editorial calendar,
  social curation, media analysis, CMS seed drafting
- Two personas (Content Strategist, Content Writer); reads brand voice from
  resolved brand path; invokes delivery-practice for backlog and research
- Skills: analyse-media, content-calendar, curate-content, draft-post,
  draft-recipe, edit-content, practice-setup, write-captions

### delivery-practice — v0.1.0

- Complete delivery practice — setup interview, product strategy,
  backlog and sprint cadence, validation, operational skills
- Two personas (Product Manager, Delivery Lead)
- Skills: backlog, competitive-brief, metrics-review, practice-setup,
  product, product-brainstorming, roadmap, skills-index, sprint,
  stakeholder-update, synthesize-research, tasks, validate, write-spec

### search-optimisation — v0.1.0

- Complete search and technical SEO practice — setup interview,
  keyword research, technical audits, content SEO review
- One persona (SEO Specialist); retires the standalone seo-specialist agent
  plugin; invokes delivery-practice for competitive brief
- Skills: content-seo-review, keyword-research, practice-setup,
  technical-seo-audit

### ux-design — v0.1.0

- Minimal UX practice — setup interview and wireframe skill for
  low-fidelity layout and interaction specs
- Writes to the instance `design/` directory when bound; standalone Try tier
  uses `docs/design/`
- Skills: practice-setup, wireframe

### web-development — v0.1.0

- Complete web engineering practice — setup interview, architecture,
  epic design, implementation, code review, QA, platform operations
- Six personas (Frontend Engineer through WebOps); consolidates the former
  frontend-engineer, senior-frontend-engineer, principal-frontend-engineer,
  qa-engineer, principal-architect, and webops-engineer agent plugins, plus
  the standalone `skills/engineering` plugin, into one owned skill library
- Reads brand-guide from resolved brand path; invokes delivery-practice for
  planning cadence
- Skills: adr, code-review, create-mr, debug, deploy-qa, design, docs,
  document-defects, exploratory-pass, final-code-review, implement,
  platform-health, practice-setup, run-automated-suite, solution, tech-debt

### Repository infrastructure

- **MCP connectors decentralised to practice plugins** — standalone connector
  plugins removed from marketplace; provider definitions now live in each
  practice's `.mcp.json` (root `connectors/` deleted)
- **`.agents/` local maintainer tooling removed** — steering and epic work
  moved to `carinyaparc-space`; the canonical Agency Skill Design Framework
  now lives at `agency-hub/references/agency-skill-design-framework.md`;
  structural checks remain in `scripts/validate.py`
- **`scripts/validate.py`** — structural validation for marketplace
  manifests, plugin.json, MCP connectors, SKILL.md frontmatter, markdown
  cross-references, bundled-skill drift, and evals schema (`--format json`,
  `--strict`, `--skip-drift`)
- **`scripts/plugin-check.py`** — fast, plugin-scoped manifest/MCP/SKILL.md
  check used as the release fast gate
- **`.github/workflows/validate.yml`** — CI gate running `validate.py` and
  unit tests on PRs
- **`tests/test_validate.py`** — unit tests for `validate.py` frontmatter
  parsing and repo validation
- **`scripts/sync-agent-skills.py`** and **`scripts/install-git-hooks.sh`**
  removed — practice plugins own skills outright; CI runs validation on
  push/PR instead of a local pre-commit hook
- `agency-builder-hub` marketplace plugin and **eval-grader** agent removed —
  superseded by `.agents/` tooling and the **plugin-eval** skill (both since
  folded into `agency-hub`)
- `agency-core` practice plugin removed — MCP connectors moved into each
  practice's own `.mcp.json`

## [0.1.0] - 2026-06-21

Initial release of Carinya Parc Digital Agency

## Added

- Functional plugins: `agency-core`, `engineering`
- Agent plugins: `frontend-engineer`
