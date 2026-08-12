# Changelog

All notable changes to this project are documented here. Version numbers match
Git tags and the `version` field in `.cursor-plugin/plugin.json` and
`.claude-plugin/plugin.json`.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Path cleanup

- Removed dual-read / migration instructions for retired `.agency/` artefact trees.
  Delivery artefacts live under `docs/`; target binding is `config/target.json`;
  agent byproducts write under `docs/reviews/`. Work-item design is `tdd.md` only.

### Plugin management (v0.2.0)

- **New `plugin-management` plugin (v0.2.0):** ported from tempster-plugin — `create-plugin`, `customize-plugin`, and component-authoring skills (structure, skills, agents, commands, hooks, MCP, settings, portability, marketplace/release) plus four sub-agents.
- **BREAKING:** `skill-authoring` folded into `plugin-management`. Reinstall as `plugin-management@carinya-plugins`; invoke `/plugin-management:skills-qa` and `/plugin-management:skill-review` (was `/skill-authoring:…`). Scripts live under `plugin-management/scripts/`.

### Design rename (v0.5.0)

- **BREAKING:** `product-design` renamed to `design` (directory, marketplace id, slash namespace `/design:…`, conventions file `design-conventions.md`). Reinstall as `design@carinya-plugins`; update any hard-coded `/product-design:` invocations and companion docs.

### Engineering rename (v0.6.0)

- **BREAKING:** `product-engineering` renamed to `engineering` (directory, marketplace id, slash namespace `/engineering:…`, conventions file `engineering-conventions.md`). Reinstall as `engineering@carinya-plugins`; update any hard-coded `/product-engineering:` invocations and companion docs.

### Architecture practice split

- **New `architecture` plugin (v0.5.0):** `setup`, `solution`, `adr` — owns `docs/architecture/`.
- **BREAKING (`engineering` v0.5.0, formerly `product-engineering`):** `solution` and `adr` moved to `architecture`. Invoke `/architecture:solution` and `/architecture:adr`. `tdd`, `docs-review`, and `tech-debt` stay in `engineering`. Principal Architect persona moves to `architecture`; engineering keeps five personas.
- Companions, `skills-index:find`, and `docs/CROSS-PLUGIN-CONTRACTS.md` updated for the new edge.

### Migration verification complete

- Phase 0 authoring tooling ported to `skill-authoring`; Ralph hook tests in `ralph-loop/scripts/`.
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
