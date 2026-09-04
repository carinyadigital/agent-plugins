# Changelog

All notable changes to this project are documented here. Version numbers match
Git tags and the `version` field in `.cursor-plugin/plugin.json` and
`.claude-plugin/plugin.json`.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [2026-09-04] — live copy to Carinya Digital / agent-plugins

Install commands, skill authors, and catalogue docs now use
`carinyadigital/agent-plugins` and `@agent-plugins`. Skill frontmatter author is
**Carinya Digital**. Legal copyright remains Carinya Parc Pty Ltd.

### architecture 0.8.1 / content-marketing 0.4.4 / design 0.6.4 / document-management 0.1.3 / engineering 0.8.4 / plugin-management 0.2.4 / product-management 0.5.5 / ralph-loop 0.7.1 / search-optimisation 0.4.4 / skills-index 0.4.5

- Companion install strings: `@carinya-plugins` → `@agent-plugins`.
- Skill `metadata.author`: Carinya Parc → Carinya Digital.

## [2026-09-04] — engineering-delivery in ralph-loop

Marketplace identity: `carinya-plugins` → `agent-plugins`. Display name and
plugin author are **Carinya Digital**; owner URL is
`https://github.com/carinyadigital`. Catalogue repo:
`https://github.com/carinyadigital/agent-plugins`.

### ralph-loop 0.7.0

- `engineering-delivery` ships in `ralph-loop/skills/ralph-loop/assets/presets/`.
  Seed no longer looks up sibling `engineering/assets/ralph-presets/`.

### engineering 0.8.3

- Removed plugin-level `assets/ralph-presets/`. `deliver` invokes
  `/ralph-loop:ralph-loop-setup` when that plugin is installed, then reads
  loop artefacts from `.claude/loop/` or `.cursor/loop/`.

## [2026-09-04] — ADRs at docs/decisions/

### architecture 0.8.0

- **BREAKING:** `/architecture:adr` writes the register and `ADR-NNNN` files
  under `docs/decisions/` (was `docs/architecture/decisions/`). Leftover files
  at the old path are a read fallback; `adr` migrates them into
  `docs/decisions/`.
- Merged `work-item-resolution.md` into `references/work-items.md` (resolution
  plus schema in one file).

### engineering 0.8.2

- Cite ADRs under `docs/decisions/` instead of `docs/architecture/decisions/`.
- Merged `work-item-resolution.md` and `work-item-schema.md` into
  `references/work-items.md`.
- Removed plugin-level `assets/tasks-local.template.md`. The repo-root
  `TASKS.local.md` pointer template lives in the `tasks` skill.

### product-management 0.5.4

- Delivery conventions place ADRs at `docs/decisions/`.
- Merged task work-item resolution and schema into
  `skills/tasks/references/work-items.md`.

### document-management 0.1.2

- Default `protected_paths` protect `docs/decisions/` (ADRs) instead of
  `docs/architecture/`. Leftover `docs/architecture/` is still reported, never
  auto-moved.

### design 0.6.3 / brand-creative 0.4.4

- Read ADRs from `docs/decisions/`. Instance/target layout templates list
  `docs/decisions/` instead of `docs/architecture/`.

### ralph-loop 0.6.1

- Read ADRs from `docs/decisions/`.
- Setup reuses existing issue sources and never writes a root
  `TASKS.local.md` pointer. Generated engineering-delivery runs keep every
  configured source synchronized through In Progress, In Review, and Done.
  UX review is no longer a default stage.

## [2026-09-04] — ARCHITECTURE.md at repo root

### architecture 0.7.0

- **BREAKING:** `/architecture:solution` writes arc42 `ARCHITECTURE.md` at the
  target repo root (current/as-is by default; `--state target` for intended
  architecture, including greenfield). Architecture decisions stay in
  `docs/architecture/decisions/` via `/architecture:adr` — they are no longer
  a section of the architecture narrative. Legacy
  `docs/architecture/solution.md` is a read fallback only.

### engineering 0.8.1

- Cite `ARCHITECTURE.md` (repo root) instead of
  `docs/architecture/solution.md`. ADRs remain under
  `docs/architecture/decisions/`.
- **BREAKING:** Renamed work-item Solution Design skill `tdd` → `design`
  (artefact `design.md`). The `tdd` alias skill is removed — invoke
  `/engineering:design`. Added `discover` and `deliver` as agent-only
  entry points and `discovery-review` as the Ready for Development gate.
- **BREAKING:** Renamed `merge-request-babysit` → `merge-request-watch`.
- **BREAKING:** Removed `final-code-review` and `merge-request-review`. Use
  `code-review` for PR/MR review (including as assigned reviewer). Use
  `/product-management:validate` for work-item sign-off.
- `code-review` collapses overlapping lenses into `bug-scan-reviewer`,
  `requirements-reviewer`, and `code-reviewer`.
- **BREAKING:** `code-review` co-locates tracking JSON with the verdict
  (`specs/{work-short-name}/reviews/code-review-{nn}.local.json` next to the
  `.md`). It no longer writes repo-root `reviews/`. `code-review-fix` reads
  and updates the sibling JSON.

### product-management 0.5.3

- Roadmap, tasks, and product artefacts cite `ARCHITECTURE.md` at the repo
  root instead of `docs/architecture/solution.md`.
- **BREAKING:** `validate` no longer writes a validation report. It discovers
  the AC source (tracker description or a local tasks/spec file), checks off
  passed criteria, records evidence as a tracker comment or description
  update, and marks the item done when every criterion passes.

### document-management 0.1.1

- Treat repo-root `ARCHITECTURE.md` as read-only context (like `README.md`).
  `docs/architecture/` remains protected for ADRs.

### skills-index 0.4.4

- Route `/architecture:solution` to system architecture at `ARCHITECTURE.md`.

## [2026-09-04] — document-management

### document-management 0.1.0

- First release. Utility plugin for the `docs/` tree lifecycle: `docs-setup`
  (scaffold or reorganise to Diátaxis) and `docs-improve` (score, drift vs
  code, voice, then apply approved fixes). Two agents (`docs-reviewer`
  read-only, `docs-writer` gated). Writes stay inside `docs_root`; default
  `protected_paths` leave practice-owned trees alone. Coexists with
  `/engineering:docs-review` for set-quality review.

## [2026-08-15] — engineering-delivery + multi-root loop

### engineering 0.7.3

- `engineering-delivery` preset: fold `task-start` into `implement` so branch
  checkout and tracker start do not consume a stop-hook continue.

### ralph-loop 0.5.3

- Cursor stop and capture hooks search `workspace_roots` for
  `.cursor/loop/active.md`. A multi-root window no longer misses a loop
  seeded in a sibling checkout when `CURSOR_PROJECT_DIR` points elsewhere.
- Seed default `FIRST_STEP` for `engineering-delivery` is `implement`.

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
