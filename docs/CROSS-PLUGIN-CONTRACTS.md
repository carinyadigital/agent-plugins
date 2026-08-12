# Cross-plugin contracts

Live edges between plugins after Phase 2 restructuring. Each edge must **gracefully
degrade** when the companion plugin is not installed: state what the user can do
without it, then give an explicit install command — never a dangling
`/namespace:skill` with no context.

**Marketplace:** `carinyaparc/carinya-plugins` (`carinya-plugins`)

**Standard install message:**

```text
Install: /plugin install <plugin>@carinya-plugins
Then run: /<plugin>:<skill> …
```

**Standard artefact consumption:** When a skill reads another practice's output
from disk (`brand-guide.md`, `design.md`, wireframes), it does **not** require
that plugin to be installed. Missing artefacts → ask the user inline; do not
fail with a slash-command reference.

---

## Contract index

| From | To | Mechanism | Required? |
| ---- | -- | --------- | --------- |
| `ralph-loop` | `product-engineering` | engineering-delivery preset invokes implement, code-review, code-review-fix, merge-request | Yes for that preset |
| `ralph-loop` | `product-design` | engineering-delivery preset invokes ux-design-review, ux-design-fix | Optional (UI tasks only) |
| `ralph-loop` | `product-management` | engineering-delivery preset invokes validate | Yes for that preset |
| `product-engineering` | self | implement reads tdd.md from tdd skill | Internal |
| `product-management` | `product-engineering` | product/roadmap recommend solution, docs-review | Companion |
| `product-management` | `product-engineering` | delivery skills route design/implement/review | Companion |
| `product-engineering` | `product-management` | planning cadence, validate sign-off | Companion |
| `product-engineering` | `product-design` | ux-design-review, ux-design-fix | Companion |
| `product-design` | `product-engineering` | wireframe → implement; tdd.md for specs | Companion |
| `content-marketing` | `product-management` | tasks, synthesize-research | Companion |
| `search-optimisation` | `product-management` | competitive-brief | Companion |
| `product-engineering` | `ralph-loop` | autonomous delivery loop | Companion |
| `skills-index` | all catalogue plugins | install-aware routing | Optional meta-plugin |
| any practice | `brand-creative` | read brand-guide.md / brand-voice.md from resolved path | Artefact only |

---

## ralph-loop → product-engineering / product-design / product-management

**Preset:** `engineering-delivery` (contributed by `product-engineering` at
`product-engineering/assets/ralph-presets/engineering-delivery.md`)

**Resolution at seed time:** `ralph-loop/scripts/seed-ralph-loop.sh` looks for
contributed presets in:

1. `RALPH_PRESET_DIRS` (colon-separated list — set by the agent when both plugins
   are installed)
2. Sibling plugin cache:
   `${CLAUDE_PLUGIN_ROOT}/../product-engineering/assets/ralph-presets/` (or
   `CURSOR_PLUGIN_ROOT` equivalent)

This sibling lookup is intentional — marketplace installs place plugins as
siblings in the plugin cache. It is **not** a general pattern for skill markdown
links.

### engineering-delivery preset steps → skills

| Step | Skill | Plugin |
| ---- | ----- | ------ |
| implement | `/product-engineering:implement` | product-engineering |
| review | `/product-engineering:code-review` | product-engineering |
| review_fix | `/product-engineering:code-review-fix` | product-engineering |
| ux_review | `/product-design:ux-design-review` | product-design |
| ux_review_fix | `/product-design:ux-design-fix` | product-design |
| final_validate | `/product-management:validate` | product-management |
| create_mr | `/product-engineering:merge-request` | product-engineering |

### Graceful degradation

| Missing plugin | Behaviour |
| -------------- | --------- |
| `product-engineering` | **Refuse** `engineering-delivery` preset at setup. Offer `ad-hoc` or `custom`, or: `Install: /plugin install product-engineering@carinya-plugins` |
| `product-design` | Loop continues; skip `ux_review` / `ux_review_fix` when UI signals absent or plugin not installed. Note in run context. |
| `product-management` | Loop can implement and review but cannot run `final_validate`. Stop before final sign-off with install message for `product-management`. |

**ad-hoc** and **custom** presets ship inside `ralph-loop` and run with no
companion plugins.

---

## product-engineering:implement → tdd.md

**Internal edge** (same plugin). `implement` reads `docs/work/{work-id}/tdd.md`
written by the `tdd` skill.

| Condition | Behaviour |
| --------- | --------- |
| tdd.md present | Proceed |
| tdd.md absent | Stop. Recommend `/product-engineering:tdd {work-id}` first. |
| Legacy `.agency/work/…/design.md` or `docs/work/…/design.md` | Read fallback only; write new artefacts under `docs/` as `tdd.md` |

Primary artefact filename is `tdd.md`. Legacy `design.md` is accepted when
reading only — the `tdd` skill migrates it to `tdd.md` on update.

---

## product-management → product-engineering:solution

Strategy skills (`product`, `roadmap`, `write-spec`) list architecture as a
companion handoff.

| Condition | Behaviour |
| --------- | --------- |
| `product-engineering` installed | Recommend `/product-engineering:solution` or `/product-engineering:docs-review` |
| Not installed | Continue product work from user input. At architecture boundaries, say: `Install: /plugin install product-engineering@carinya-plugins` then `/product-engineering:solution` |

Delivery skills route implementation to `/product-engineering:tdd`,
`/product-engineering:implement`, etc. — see
`product-management/references/delivery-conventions.md`.

---

## product-engineering ↔ product-management

See `product-engineering/references/product-engineering-conventions.md` and
`product-management/references/delivery-conventions.md`.

| Need | Invoke |
| ---- | ------ |
| Backlog / tasks / AC | `/product-management:tasks` |
| Sprint cadence | `/product-management:sprint-planning`, `sprint-retro`, `backlog-refine` |
| Sign-off | `/product-management:validate` |

When `product-management` is not installed: continue engineering work that does
not need tracker/backlog integration; recommend co-install for delivery cadence.

---

## product-engineering / product-design UX edge

| Need | Invoke |
| ---- | ------ |
| Live-browser UX review | `/product-design:ux-design-review` |
| Fix UX findings | `/product-design:ux-design-fix` |

When `product-design` is not installed: `code-review` still runs; skip UX
review steps. Recommend install before UI-heavy work.

Wireframes from `product-design` are consumed from `<instance-root>/design/` or
user-named paths — no plugin install required to **read** them.

---

## content-marketing / search-optimisation → product-management

Documented in each plugin's `CONNECTORS.md` and conventions files.

| Plugin | Companion skill | When |
| ------ | --------------- | ---- |
| content-marketing | `/product-management:tasks --product` | Backlog alignment |
| content-marketing | `/product-management:synthesize-research` | Research themes |
| search-optimisation | `/product-management:competitive-brief` | Competitive landscape |

Setup skills explicitly state they **do not install** companion plugins.

---

## brand-creative artefact consumption

`product-engineering`, `content-marketing`, and others read
`brand-guide.md` / `brand-voice.md` from the resolved brand path.

| Condition | Behaviour |
| --------- | --------- |
| Artefact exists | Read and apply |
| Artefact absent | Ask user for design/voice guidance inline |
| `brand-creative` not installed | No install required — optional recommendation to run `/brand-creative:brand-voice write` |

---

## skills-index install-aware routing

`/skills-index:find` detects installed plugins and:

1. Routes to installed skills with `/plugin:skill`
2. Offers `/plugin install <plugin>@carinya-plugins` for catalogue matches that
   are not installed

Does not invoke other plugins directly — recommendation only.

---

## Runtime path rules

Each plugin is copied to an isolated cache directory at install time.

| Allowed | Example |
| ------- | ------- |
| Paths within the same plugin | `../../references/conventions.md` |
| Sibling plugin lookup in **documented** shell contracts | `seed-ralph-loop.sh` → `../product-engineering/assets/ralph-presets/` |
| Artefact paths in the user's repo | `docs/work/{id}/design.md` |

| Forbidden in skill markdown | Why |
| --------------------------- | --- |
| `../other-plugin/references/…` | Sibling may not exist in cache |
| Repo-monorepo paths assuming checkout layout | Install is not monorepo |

Repo-root `scripts/` (validate, sync-references) may reference any path — they
run in the monorepo, not in the plugin cache.

---

## MCP bundles (Phase 3 verification)

| Plugin | Bundled MCP | Notes |
| ------ | ----------- | ----- |
| product-management | atlassian, amplitude | Unchanged after delivery-practice merge — tracker + analytics |
| product-design | figma, playwright | Playwright required for ux-design-review/fix browser work |
| product-engineering | github, playwright, context7 | Engineering tool surface |
| brand-creative | fireflies | |
| content-marketing | canva | |
| search-optimisation | ahrefs | |
| ralph-loop | — | Hooks only |
| skills-index | — | Router only |
| skill-authoring | — | QA tooling |

Skills degrade when a connector is absent — see each plugin's `CONNECTORS.md`.
