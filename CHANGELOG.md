# Changelog

All notable changes to this project are documented here. Version numbers match
Git tags and the `version` field in `.cursor-plugin/plugin.json` and
`.claude-plugin/plugin.json`.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [2026-08-14] — Apache-2.0 license

Patch release of every catalogue plugin. Relicense MIT → Apache-2.0; each
plugin now ships a `LICENSE` file at plugin root so the text travels with an
independently installed plugin.

### architecture 0.6.2

- License: MIT → Apache-2.0. Ships `LICENSE` at plugin root.

### brand-creative 0.4.3

- License: MIT → Apache-2.0. Ships `LICENSE` at plugin root.

### content-marketing 0.4.3

- License: MIT → Apache-2.0. Ships `LICENSE` at plugin root.

### design 0.6.2

- License: MIT → Apache-2.0. Ships `LICENSE` at plugin root.

### engineering 0.7.2

- License: MIT → Apache-2.0. Ships `LICENSE` at plugin root.

### plugin-management 0.2.3

- License: MIT → Apache-2.0. Ships `LICENSE` at plugin root.
- `plugin-structure` and `plugin-scaffolder` now copy `LICENSE` into new plugins.

### product-management 0.5.2

- License: MIT → Apache-2.0. Ships `LICENSE` at plugin root.

### ralph-loop 0.5.2

- License: MIT → Apache-2.0. Ships `LICENSE` at plugin root.

### search-optimisation 0.4.3

- License: MIT → Apache-2.0. Ships `LICENSE` at plugin root.

### skills-index 0.4.2

- License: MIT → Apache-2.0. Ships `LICENSE` at plugin root.

### Repository

- Root `LICENSE` and README updated to Apache License 2.0.

## [2026-08-14] — author + SMB catalogue positioning

Patch release of every catalogue plugin. Author metadata and README positioning
only — no skill or path changes.

### architecture 0.6.1

- Author metadata: Digital Agency → Carinya Parc.

### brand-creative 0.4.2

- Author metadata: Digital Agency → Carinya Parc.

### content-marketing 0.4.2

- Author metadata: Digital Agency → Carinya Parc.

### design 0.6.1

- Author metadata: Digital Agency → Carinya Parc.

### engineering 0.7.1

- Author metadata: Digital Agency → Carinya Parc.

### plugin-management 0.2.2

- Author metadata: Digital Agency → Carinya Parc.

### product-management 0.5.1

- Author metadata: Digital Agency → Carinya Parc.

### ralph-loop 0.5.1

- Author metadata: Digital Agency → Carinya Parc.

### search-optimisation 0.4.2

- Author metadata: Digital Agency → Carinya Parc.

### skills-index 0.4.1

- Author metadata: Digital Agency → Carinya Parc.

### Repository

- README repositioned for small and medium business owners: full-service digital agency work delivered agentically in Claude Cowork, Claude Code, Cursor, or another agent. Brand, content, design, and search are first-class; engineering is optional when you ship a product or site.
- Marketplace owner: Carinya Digital Services → Carinya Parc.

## [2026-08-14] — specs/reviews paths + catalogue catch-up

First tagged release of the renamed catalogue. Breaking path changes and earlier
untagged catalogue moves ship together. 0.x minors used for breaking changes;
no 1.0.0 yet.

### engineering 0.7.0

- **BREAKING:** Work-item artefacts move from `docs/work/{work-id}/` to `specs/{work-short-name}/`. `{work-short-name}` is kebab-case, at most two words, from the title (`specs/cart/`); fall back to `{work-id}` when a short name cannot be discovered. Writes `tdd.md` and, when a local task breakdown is required, `TASKS.local.md`. Numbered review verdicts move to `specs/{work-short-name}/reviews/`. Sprint plan/retro stay at `docs/work/sprint-{id}/`. Repo-root `TASKS.local.md` remains the Linear/Jira tracker pointer. No dual-read of the old `docs/work/{id}/tdd.md` or `tasks.md` paths.
- **BREAKING:** Review tracking JSON moves from `docs/reviews/{skill}.local.json` to `reviews/{skill}.local.json` (`code-review` / `code-review-fix`). Fallback branch-level reports and `review-learnings.local.md` move with it. `reviews/` is gitignored (`/reviews/`) and must never be committed. Agent byproducts stay under `docs/reviews/`.
- **BREAKING:** `product-engineering` renamed to `engineering` (directory, marketplace id, slash namespace `/engineering:…`, conventions file `engineering-conventions.md`). Reinstall as `engineering@carinya-plugins`.
- **BREAKING:** `solution` and `adr` moved to `architecture`. Invoke `/architecture:solution` and `/architecture:adr`. `tdd`, `docs-review`, and `tech-debt` stay in `engineering`. Principal Architect persona moves to `architecture`; engineering keeps five personas.
- Removed dual-read / migration instructions for retired `.agency/` artefact trees.

### design 0.6.0

- **BREAKING:** Work-item review verdicts move to `specs/{work-short-name}/reviews/` (`ux-design-review` / `ux-design-fix`).
- **BREAKING:** Review tracking JSON moves from `docs/reviews/{skill}.local.json` to `reviews/{skill}.local.json`. `reviews/` is gitignored.
- **BREAKING:** `product-design` renamed to `design` (directory, marketplace id, slash namespace `/design:…`, conventions file `design-conventions.md`). Reinstall as `design@carinya-plugins`.
- Removed dual-read / migration instructions for retired `.agency/` artefact trees.

### architecture 0.6.0

- **BREAKING:** Work-item artefacts for `adr` / `solution` move to `specs/{work-short-name}/`.
- **New plugin:** `setup`, `solution`, `adr` — owns `docs/architecture/`. Principal Architect persona lives here.

### product-management 0.5.0

- **BREAKING:** Work-item artefacts for `tasks` / `validate` / `backlog-refine` / sprint skills move from `docs/work/{work-id}/` to `specs/{work-short-name}/`. Sprint plan/retro stay at `docs/work/sprint-{id}/`.
- Removed dual-read / migration instructions for retired `.agency/` artefact trees.

### ralph-loop 0.5.0

- **BREAKING:** Work-item artefacts move to `specs/{work-short-name}/`.

### plugin-management 0.2.1

- **New plugin:** ported from tempster-plugin — `create-plugin`, `customize-plugin`, and component-authoring skills (structure, skills, agents, commands, hooks, MCP, settings, portability, marketplace/release) plus four sub-agents.
- **BREAKING:** `skill-authoring` folded into `plugin-management`. Reinstall as `plugin-management@carinya-plugins`; invoke `/plugin-management:skills-qa` and `/plugin-management:skill-review` (was `/skill-authoring:…`). Scripts live under `plugin-management/scripts/`.

### brand-creative 0.4.1

- Removed dual-read / migration instructions for retired `.agency/` artefact trees. Delivery artefacts live under `docs/`; target binding is `config/target.json`.

### content-marketing 0.4.1

- Removed dual-read / migration instructions for retired `.agency/` artefact trees.

### search-optimisation 0.4.1

- Removed dual-read / migration instructions for retired `.agency/` artefact trees. SEO research stays at `docs/work/seo/`.

### skills-index 0.4.0

- Catch-up tag for the Phase 3 cutover version (never tagged under the current plugin name). Companions and `find` updated for the architecture / engineering edge.

### Repository

- Phase 0 authoring tooling ported (now in `plugin-management`); Ralph hook tests in `ralph-loop/scripts/`.
- CI gates: `validate.py` (plugins + skills), `validate_ralph.py`, mutation tests.
- Validator split: `scripts/validate_plugins.py` + `scripts/validate_skills.py` + `validate_lib.py`; agent contracts + orphan SKILL.md enforced.
- `docs/MIGRATION.md` removed — see `docs/CROSS-PLUGIN-CONTRACTS.md`.

## [2026-08-12] — Phase 3 cutover + skills sync (v0.4.0)

All nine catalogue plugins reset to **v0.4.0** after Phase 2 restructuring
(`engineering`, `product-design`, `product-management` merge,
`ralph-loop` extract, `skills-index` / `skill-authoring` new). See
`docs/CROSS-PLUGIN-CONTRACTS.md`.

- **BREAKING (engineering):** `design` → `tdd`; artefact `design.md` → `tdd.md`; modes `walking-skeleton|tdd` → `skeleton|full`. Invoke `/engineering:tdd`.
- Consumers (`implement`, `tasks`, `validate`, `adr`, `ralph-loop*`, sprint skills) read `tdd.md`.
- Ralph-loop hooks/seed: completion-promise anchoring, turn-boundary detection, `{{TDD_PATH}}` / `{{WORK_ID}}`.
- `product-management` / `skills-index` synced with [carinyaparc/skills](https://github.com/carinyaparc/skills); `find` routes to `tdd`.
- `product` / `roadmap`: write-only posture clarified (`docs-review` = writing quality, not strategy).

## [2026-07-25] — web-development v0.3.1

- **Fixed:** `ralph-loop` / `ralph-loop-setup` — setup reports expected branch only; `start` creates/checks it out before iteration 1.

## [2026-07-24] — Product split and skills 2.1.0 alignment

Aligned with [carinyaparc/skills](https://github.com/carinyaparc/skills) 2.1.0. Artefact paths at this release used the agency tree (later moved to `docs/`).

- **product-management v0.1.0:** New MECE practice — PM persona owns strategy/discovery (`product`, `roadmap`, `write-spec`, brainstorming, research, competitive-brief, metrics, stakeholder-update, skills-index, setup).
- **delivery-practice v0.2.0 (BREAKING):** Product skills moved out; `backlog` → `tasks --product`; `sprint` → `sprint-planning` + `sprint-retro`; added `backlog-refine`. Delivery Lead execution only.
- **web-development v0.3.0 (BREAKING):** `code-review-fix`, `ux-design-fix`, `merge-request-babysit`, `docs-review` (read-only); `ralph` → `ralph-loop` + `ralph-loop-setup`; `solution` refine mode removed. Added parallel sub-agent review, MR skills, UX review, Ralph hooks.

## [2026-07-05] — Connector integrations

- **content-marketing v0.2.0:** Canva MCP
- **search-optimisation v0.2.0:** Ahrefs MCP (+ Semrush / Search Console guidance)
- **web-development v0.2.0:** Sentry MCP
- **brand-creative / ux-design v0.1.1:** CONNECTORS.md updates (Canva, Drive, SharePoint)

## [2026-07-05] — Practice plugins v0.1.0

First tagged MECE practice-plugin catalogue (`<plugin>-v0.1.0`): practice-setup + owned skill library per plugin, replacing standalone agent plugins.

| Plugin | Scope |
| ------ | ----- |
| `agency-hub` | Instance bootstrap (`config/`, `brand/`, `squads/`); registry, skill install/QA, auto-updater |
| `brand-creative` | Brand voice + brand-guide; writes to `brand/` |
| `content-marketing` | Calendar, curation, media, drafting; Strategist + Writer personas |
| `delivery-practice` | Product + delivery (later split); PM + Delivery Lead |
| `search-optimisation` | Keyword research, technical SEO, content SEO; SEO Specialist |
| `ux-design` | Setup + wireframe; writes to `design/` |
| `web-development` | Architecture through WebOps; consolidates six former agent plugins |

### Repository infrastructure

- MCP connectors moved into each practice's `.mcp.json` (standalone connector plugins / `connectors/` removed).
- `.agents/` maintainer tooling removed — steering/epics → `carinyaparc-space`.
- Added `scripts/validate.py`, CI (`validate.yml`), `tests/test_validate.py`.
- Removed skill sync hooks, `agency-builder-hub`, `agency-core` (MCP folded into practices).

## [0.1.0] - 2026-06-21

Initial release — `agency-core`, `engineering`, `frontend-engineer`.
