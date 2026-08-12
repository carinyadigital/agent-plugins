# Changelog

All notable changes to this project are documented here. Version numbers match
Git tags and the `version` field in `.cursor-plugin/plugin.json` and
`.claude-plugin/plugin.json`.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Architecture practice split

- **New `architecture` plugin (v0.5.0):** `setup`, `solution`, `adr` — owns `docs/architecture/`.
- **BREAKING (`product-engineering` v0.5.0):** `solution` and `adr` moved to `architecture`. Invoke `/architecture:solution` and `/architecture:adr`. `tdd`, `docs-review`, and `tech-debt` stay in `product-engineering`. Principal Architect persona moves to `architecture`; engineering keeps five personas.
- Companions, `skills-index:find`, and `docs/CROSS-PLUGIN-CONTRACTS.md` updated for the new edge.

### Migration verification complete

- Phase 0 authoring tooling ported to `skill-authoring`; Ralph hook tests in `ralph-loop/scripts/`.
- `scripts/verify-migration.py` + CI gates (`validate.py`, `validate_skills.py`, mutation tests).
- `docs/MIGRATION.md` removed — see `docs/CROSS-PLUGIN-CONTRACTS.md`.

## [2026-08-12] — Phase 3 cutover + skills sync (v0.4.0)

All nine catalogue plugins reset to **v0.4.0** after Phase 2 restructuring
(`product-engineering`, `product-design`, `product-management` merge,
`ralph-loop` extract, `skills-index` / `skill-authoring` new). See
`docs/CROSS-PLUGIN-CONTRACTS.md`.

- **BREAKING (product-engineering):** `design` → `tdd`; artefact `design.md` → `tdd.md` (legacy accepted); modes `walking-skeleton|tdd` → `skeleton|full`. Invoke `/product-engineering:tdd`.
- Consumers (`implement`, `tasks`, `validate`, `adr`, `ralph-loop*`, sprint skills) read `tdd.md` with legacy fallback.
- Ralph-loop hooks/seed: completion-promise anchoring, turn-boundary detection, `{{TDD_PATH}}` / `{{WORK_ID}}`.
- `product-management` / `skills-index` synced with [carinyaparc/skills](https://github.com/carinyaparc/skills); `find` routes to `tdd`.
- `product` / `roadmap`: write-only posture clarified (`docs-review` = writing quality, not strategy).

## [2026-07-25] — web-development v0.3.1

- **Fixed:** `ralph-loop` / `ralph-loop-setup` — setup reports expected branch only; `start` creates/checks it out before iteration 1.

## [2026-07-24] — Product split and skills 2.1.0 alignment

Aligned with [carinyaparc/skills](https://github.com/carinyaparc/skills) 2.1.0. Artefact paths remain under `.agency/`.

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
- Added `scripts/validate.py`, `plugin-check.py`, CI (`validate.yml`), `tests/test_validate.py`.
- Removed skill sync hooks, `agency-builder-hub`, `agency-core` (MCP folded into practices).

## [0.1.0] - 2026-06-21

Initial release — `agency-core`, `engineering`, `frontend-engineer`.
