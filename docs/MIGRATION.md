# Migration plan: `carinya-plugins`

Consolidating `carinyaparc/skills` into `carinyaparc/digital-agency-plugins`, restructuring the
plugin set, and dissolving `agency-hub`.

**Status:** proposed — not started
**Decisions locked:** repo `carinya-plugins` · marketplace `carinya-plugins` · no hub · 8 plugins

---

## Target state

| Plugin | Contents | Connectors | Ships hooks |
|---|---|---|---|
| `product-management` | product-management + delivery-practice (~14 skills) | atlassian, amplitude | no |
| `product-design` | wireframe + ux-design-review + ux-design-fix (~4) | figma, playwright | no |
| `product-engineering` | web-development − ux − ralph (~19) | github, playwright, context7 | no |
| `ralph-loop` | ralph-loop + ralph-loop-setup (~2) | — | **yes** |
| `skills-index` | find/route (~1) | — | no |
| `brand-creative` | unchanged (3) | fireflies | no |
| `content-marketing` | unchanged (8) | canva | no |
| `search-optimisation` | unchanged (4) | ahrefs | no |
| `skill-authoring` | skills-qa + eval-grader + validators + spec + template | — | no |

Dissolved: `agency-hub`, `delivery-practice`, `ux-design`, `web-development`.

### Why no hub

Of the hub's nine skills, six are a community-skill package manager — `registry-browser`,
`skill-installer`, `auto-updater`, `disable`, `uninstall`, `skill-manager` (~46KB). Claude Code
now ships this natively with signing, version pinning, `sha` pinning, and install scopes.
`marketplace.json` already describes it as "v2 — designed, deferred." Delete it.

The three that survive go elsewhere:

- **`setup`** (12.5KB) — instance bootstrap. Load-bearing, but doesn't need a plugin. Every
  practice `setup` currently says *"Does not write `config/instance.json` — owned by
  `agency-hub:setup`."* Invert that one contract: each practice `setup` writes the instance
  profile if absent, then runs its own interview. Whichever plugin you install first bootstraps.
  Removes the install-order dependency and cuts a product team from 5 setup interviews to 3.
  `instance-profile-template.md` and `practice-setup-framework.md` are already synced into all
  8 plugins by `sync-references.py`, so only the interview logic moves.
- **`skills-qa`** (33KB — the largest skill in the hub) — not package management at all. It's a
  skill-authoring quality gate, and it's the natural home for the tooling coming across from
  `carinyaparc/skills`. Becomes `skill-authoring`.
- **`related-skills-surfacer`** — subsumed by the install-aware `skills-index`.

### Why `skills-index` is now its own plugin

Folding it into the hub was the right call while a hub existed. With the hub gone there's no
larger meta-plugin to absorb it, and putting it in `product-management` would be arbitrary.

Scope it to what the platform doesn't already do. Claude Code surfaces every installed skill's
description to the model, so "which skill handles X" already routes natively. The router earns
its place on two things only:

1. **Discovery of uninstalled plugins** — "install `search-optimisation` to get keyword-research"
2. **Workflow sequencing** — the delivery loop has an order; the platform doesn't know it

Command: `/skills-index:find`.

---

## Phase 0 — Freeze and reconcile the fork

Both repos were committed on 12 Aug 2026, 55 minutes apart. Every overlapping `SKILL.md`
differs. Do this before any restructuring — reconciling a fork and moving directories in the
same commits is unreviewable.

### Status: bug-fix sub-phase DONE, drift-reconciliation sub-phase NOT STARTED

An independent review (`REVIEW.md`, dated 12 Aug, benchmarked against Anthropic's own
`knowledge-work-plugins`, `claude-plugins-official`, and `spec-kit`) found 9 P0 defects in
`carinyaparc/skills` — a red CI build and, more seriously, a ralph-loop stop condition an agent
could satisfy by merely *mentioning* it, plus a flagship preset that could never reach its own
final step. All 9 are fixed, tested, and verified green against the repo's real current state
(`v3.0.0`, commit `f32572b`):

- CI red (shellcheck SC2034 + misleading docstring + silent truncation) — **fixed**
- Promise matcher fulfillable by mention, not just genuine completion — **fixed**, 4 new tests
- Stale promise from an earlier iteration killing a fresh loop at iteration 1 — **fixed**, 2 new tests
- `final_validate → create_mr` unreachable in the flagship preset — **fixed** + new validator check
- `done` sentinel docs wrongly implied a primary/fallback relationship that doesn't hold — **fixed**
- `adr`/`tdd` missing `Edit` despite being told to edit files in place — **fixed**
- Two wrong sibling references + one eval note certifying the broken route — **fixed**
- Empty `"Epic delivery"` group in `skills.sh.json` — **removed**
- `product`/`roadmap`/`solution` promising a `docs-review` critique mode that skill explicitly
  declines — **fixed** (removed the false promise rather than building the new mode)

10 new negative-boundary tests + 3 new mutants added; `validate_skills.py` (now with a new
`check_preset_reachability` check), the 112-assertion hook suite, and the full mutation suite
are all green. Delivered as a patch + git bundle (see chat) — verified to apply cleanly and pass
validation from a fresh checkout of the real current `main`.

**Deferred, not fixed:** the fourth wrong sibling reference (`skill-review` naming a nonexistent
`create-skill`) — fixing it requires resolving §3.1 of the review first (promote `skill-review`
into `skills/` proper, or delete it), which is a structural/behavioural call on a write-capable,
self-modifying skill, not a one-line reference correction. Needs your decision before either
repo touches it.

**Not started:** the fork-reconciliation this phase is actually named for — the drift table
below, porting `skills`-ahead work into `dap`, and porting the authoring tooling into a
`skill-authoring` plugin skeleton. The bug fixes above were real defects worth fixing regardless
of which repo ends up canonical; they don't substitute for the reconciliation.

- [ ] Freeze commits on `carinyaparc/skills`. Announce in its README.
- [ ] Resolve the five systematic drifts (decide once, apply everywhere):

| Drift | `skills` | `digital-agency-plugins` | Decision |
|---|---|---|---|
| Skill name | `tdd` / `tdd.md` | `design` / `design.md` | ? |
| `work_shape` | `authoring`, `targeted-change` | `generate-draft`, `implement-and-ship` | ? |
| `output_class` | `delivery-artefact`, `code-change` | `draft-for-review`, `applied-change` | ? |
| `review_cadence` | absent | present | ? |
| `allowed-tools` | inline string | YAML list | YAML list |
| Legacy paths | none | `.agency/` fallbacks | drop after migration window |
| Cross-refs | bare (`solution`) | namespaced (`/web-development:solution`) | namespaced |

  The `tdd`/`design` split is the urgent one — `/implement` reads `tdd.md` in one repo and
  `design.md` in the other. That chain is broken across repos today.

- [ ] Port work where `skills` is ahead:
  - `docs/reviews/` review-state migration (dap still has `.agency/` fallbacks)
  - `references/work-item-resolution.md` improvements
  - "any work item, not just epics" resolution logic
- [ ] Port authoring tooling `dap` lacks, into the new `skill-authoring` plugin:
  - `agents/eval-grader.md`
  - `agents/skills/skill-review/`
  - `scripts/validate_skills.py`
  - `scripts/mutation-test.py`
  - `spec/agent-skills-spec.md`
  - `template/SKILL.md`
- [ ] Green: `scripts/validate.py`, `scripts/plugin-check.py`

**Exit:** every skill exists once, in `dap`, with one metadata vocabulary and one naming scheme.

---

## Phase 1 — Rename

### Status: DONE

Two names change; only one redirects.

- [x] Repo `digital-agency-plugins` → `carinya-plugins`. GitHub redirects old URLs and clones —
      low risk, do it first.
- [x] Marketplace `carinya-digital` → `carinya-plugins` in both
      `.claude-plugin/marketplace.json` and `.cursor-plugin/marketplace.json`.
      **No redirect.** Anyone installed must `/plugin marketplace remove carinya-digital` then
      `/plugin marketplace add carinyaparc/carinya-plugins`. Do it now, at ~1 user.
- [x] Confirm `carinya-plugins` isn't on Anthropic's reserved marketplace list (confirmed 12 Aug
      2026 — the list is `claude-code-marketplace`, `claude-code-plugins`,
      `claude-plugins-official`, `claude-plugins-community`, `claude-community`,
      `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `anthropic-agent-skills`,
      `knowledge-work-plugins`, `life-sciences`, `claude-for-legal`, `claude-for-financial-services`,
      `financial-services-plugins`, `first-party-plugins`, `healthcare`, plus `official-*`,
      `anthropic-*`, `claude-marketplace*` impersonation patterns — but the list is re-checked on
      every marketplace load, so re-verify at cutover).
- [x] Update every install command in every README.

**Exit:** clean install from the new marketplace name in a fresh profile.

---

## Phase 2 — Restructure

One plugin per PR. Each uses `git mv` so history follows.

- [ ] **`product-management` ← `delivery-practice`**
  - `git mv delivery-practice/skills/{tasks,backlog-refine,sprint-planning,sprint-retro,validate} product-management/skills/`
  - Delete both `skills-index` copies (they have already diverged from each other)
  - Merge the two `setup` interviews into one
  - Merge `delivery-conventions.md` into `product-management/references/`
  - Rewrite the cross-plugin handoff language — these are now internal calls
- [ ] **`product-design`** (rename `ux-design`)
  - Move `ux-design-review`, `ux-design-fix` in from `web-development`
  - `.mcp.json` gains `playwright` — this plugin has an engineering tool surface
    (`ux-design-review` drives a real browser, `ux-design-fix` writes code)
- [ ] **`product-engineering`** (rename `web-development`)
  - Rename dir, `plugin.json` `name`/`displayName`/`keywords`, marketplace entry
  - Remove ux + ralph skills
  - Keep the QA cluster (`deploy-qa`, `run-automated-suite`, `exploratory-pass`,
    `document-defects`, `platform-health`) here for now — QA without engineering isn't a real
    install. Revisit as `product-qa` if this plugin gets unwieldy.
  - Consider moving `docs-review` to `skills-index` or leaving it — it reviews any doc set,
    including `product.md`, so it's cross-cutting
- [ ] **`ralph-loop`** (extract)
  - `git mv web-development/skills/{ralph-loop,ralph-loop-setup} ralph-loop/skills/`
  - `git mv web-development/hooks ralph-loop/hooks` — takes `claude/stop-hook.sh`,
    `cursor/ralph-{capture,stop}.sh`, `lib/ralph-common.sh`. Owning `lib/` outright sidesteps
    the no-`../`-across-plugins constraint.
  - Ships `ad-hoc` + `custom` presets only. `product-engineering` **contributes** the
    `engineering-delivery` preset — the loop stays domain-agnostic, the preset ships with the
    skills it calls.
  - Strip ralph references from `web-development-conventions.md`, `delivery-conventions.md`,
    both `plugin.json` keyword lists, and the READMEs
- [ ] **`skills-index`** (new)
  - Reconcile the two divergent copies into one
  - Rewrite install-aware: route to installed, offer install commands for the rest
  - Absorb `related-skills-surfacer`
- [ ] **`skill-authoring`** (new)
  - `skills-qa` + everything ported in Phase 0
- [ ] **Dissolve `agency-hub`**
  - Delete `registry-browser`, `skill-installer`, `auto-updater`, `disable`, `uninstall`,
    `skill-manager`
  - Fold `setup` into each practice's `setup` as an idempotent bootstrap
  - Flip the contract line in all 8 `setup` skills and in `practice-setup-framework.md`:
    "Does not write `config/instance.json` — owned by `agency-hub:setup`" →
    "Writes `config/instance.json` if absent"
  - `git rm -r agency-hub`, remove from both marketplace files

**Exit:** 8 plugin dirs, no `agency-hub`, `plugin-check.py` green.

---

## Phase 3 — Fix the seams

- [ ] **Cross-plugin contracts** — write them down. Live edges after restructure:
  - `ralph-loop` engineering preset → `product-engineering` (implement, code-review,
    code-review-fix, merge-request), `product-design` (ux-design-review),
    `product-management` (validate)
  - `product-engineering:implement` → reads `design.md`/`tdd.md` written by its own `design` skill
  - `product-management` → `product-engineering:solution` for architecture
  - Each edge needs: graceful degradation when the other plugin isn't installed, and a clear
    "install X" message rather than a dangling `/namespace:skill` reference
- [ ] **Update `sync-references.py`** — `PRACTICE_PLUGINS` and `CANONICAL` both hardcode the old
      set, and `practice-setup-framework.md`'s canonical source is `brand-creative`. Repoint.
- [ ] **Verify no plugin references `../` outside its own directory.** Claude Code copies each
      plugin dir to a cache; `../shared/` silently won't exist at runtime. Grep every
      `references/` link and every hook script path.
- [ ] **Version reset.** Plugins are at 0.1.1–0.3.2 with no shared scheme. Set all to `0.4.0` at
      cutover, or start renamed/new plugins at `0.1.0` and note the lineage in each README.
- [ ] **`.mcp.json` per new plugin** — `product-design` gains playwright; confirm
      `product-management` still needs both atlassian and amplitude after the merge.

---

## Phase 4 — Distribution and decommission

- [ ] **skills.sh decision.** `npx skills add carinyaparc/skills/code-review` is the one thing
      only the flat repo does today. Verify against the
      [vercel-labs/skills CLI](https://github.com/vercel-labs/skills) whether it resolves
      monorepo subpaths. If not: a CI job publishing a flattened mirror branch, or drop the
      channel. Do not hand-maintain a second library.
- [ ] **Archive `carinyaparc/skills`.** README → pointer to the new marketplace and a table
      mapping each old skill to its new `/plugin:skill` address. GitHub archive (read-only),
      don't delete — the install URLs are in the wild.
- [ ] **Rewrite the root README.** The persona tables need rework: the current twelve are a
      consultancy grade ladder (Frontend / Senior Frontend / Principal Frontend / Principal
      Architect), not a team shape. With `product-*` naming, "engineers" is more honest.
- [ ] **Decide the agency framing.** `digital-agency-plugins` → `carinya-plugins` and
      `web-development` → `product-engineering` are both moves toward product teams and away
      from client services. `brand-creative`, `content-marketing`, `search-optimisation` are
      the remaining agency-shaped plugins. That's fine — they're genuinely disjoint buyers —
      but the README should stop promising "run a full-service digital agency from your IDE"
      if that's no longer the primary story.

---

## Verification

Run before declaring cutover:

- [ ] `scripts/validate.py` and `scripts/plugin-check.py` green across all 8 plugins
- [ ] Fresh profile: add marketplace by new name, install each plugin **individually**, run its
      `setup` with **no** `config/instance.json` present — each must bootstrap standalone
- [ ] Install `product-engineering` alone and confirm no ralph stop hook fires
- [ ] Install `ralph-loop` alone and confirm `ad-hoc` preset runs without `product-engineering`
- [ ] Walk the full loop across plugin boundaries:
      `/product-management:product` → `roadmap` → `tasks` →
      `/product-engineering:design` → `implement` → `code-review` →
      `/product-design:ux-design-review` → `/product-management:validate`
- [ ] `/skills-index:find` with only two plugins installed — recommends what's installed,
      offers install commands for what isn't
- [ ] Grep for surviving references: `agency-hub`, `web-development`, `delivery-practice`,
      `carinya-digital`, `ux-design:`
- [ ] Re-run skill evals (`evals/evals.json`, `trigger-queries.json`) — namespacing changed
      every trigger phrase that names a sibling skill

---

## Sequencing

Phase 0 is the only one that's urgent — the fork drifts daily and `tdd`/`design` is already
broken across repos. Phases 1–4 can run over weeks.

Do **not** interleave Phase 0 with Phase 2. Reconciling a fork and moving directories in the
same commits produces a diff nobody can review, including you.
