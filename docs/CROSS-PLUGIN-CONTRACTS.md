# Cross-plugin contracts

Live edges between plugins after Phase 2 restructuring. Each edge must **gracefully
degrade** when the companion plugin is not installed: state what the user can do
without it, then give an explicit install command — never a dangling
`/namespace:skill` with no context.

**Marketplace:** `carinyadigital/agent-plugins` (`agent-plugins`)

**Standard install message:**

```text
Install: /plugin install <plugin>@agent-plugins
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
| `ralph-loop` | `engineering` | seeded `engineering-delivery` prompt invokes implement, code-review, code-review-fix, merge-request | Yes for that preset |
| `ralph-loop` | `design` | seeded prompt may invoke ux-design-review, ux-design-fix when the user adds those stages | Optional |
| `ralph-loop` | `product-management` | seeded prompt invokes validate | Yes for that preset |
| `engineering` | self | implement reads design.md from design skill | Internal |
| `product-management` | `architecture` | product/roadmap recommend solution | Companion |
| `product-management` | `engineering` | product/roadmap recommend docs-review; delivery skills route design/implement/review | Companion |
| `architecture` | `engineering` | solution/adr hand off to design, docs-review, implement | Companion |
| `engineering` | `architecture` | design/implement cite solution; recommend solution/adr writes | Companion |
| `engineering` | `product-management` | planning cadence, validate sign-off | Companion |
| `engineering` | `design` | ux-design-review, ux-design-fix | Companion |
| `design` | `engineering` | wireframe → implement; design.md for specs | Companion |
| `content-marketing` | `product-management` | tasks, synthesize-research | Companion |
| `search-optimisation` | `product-management` | competitive-brief | Companion |
| `engineering` | `ralph-loop` | deliver invokes setup/start when installed; then reads loop artefacts from the target repo | Companion / artefact |
| `skills-index` | all catalogue plugins | install-aware routing | Optional meta-plugin |
| any practice | `brand-creative` | read brand-guide.md / brand-voice.md from resolved path | Artefact only |
| `document-management` | `brand-creative` | artefact consumption of brand-voice.md (optional) | Artefact only |
| `document-management` | `engineering` | docs-review remains the set-quality companion; this plugin owns the docs/ tree lifecycle | Optional |

---

## ralph-loop ↔ engineering / design / product-management

The `engineering-delivery` preset ships in `ralph-loop`
(`skills/ralph-loop/assets/presets/engineering-delivery.md`). Setup writes
loop artefacts into the **target repo** (`.claude/loop/` or `.cursor/loop/`).
There is no preset file in `engineering`, and seed does not look up sibling
plugin paths.

### Artefact consumption (`deliver` → loop files)

After setup, `engineering` `deliver` reads `{base}/active.md`,
`{base}/{run-id}/loop-state.md`, and `{base}/{run-id}/context.md`. Missing
files → inline fallback, or the standard install message. This does **not**
require `ralph-loop` to be installed in order to *read* leftover artefacts.

### Slash invoke (seeded prompt → companion skills)

| Step | Skill | Plugin |
| ---- | ----- | ------ |
| implement | `/engineering:implement` | engineering |
| review | `/engineering:code-review` | engineering |
| review_fix | `/engineering:code-review-fix` | engineering |
| ux_review | `/design:ux-design-review` | design — optional; add only when the user requests it |
| ux_review_fix | `/design:ux-design-fix` | design — optional; add only when the user requests it |
| final_validate | `/product-management:validate` | product-management |
| create_mr | `/engineering:merge-request` | engineering |

### Slash invoke (`deliver` → ralph-loop)

When `ralph-loop` is installed, `deliver` runs `/ralph-loop:ralph-loop-setup`
then `/ralph-loop:ralph-loop start`. It does not seed loop files itself.

### Graceful degradation

| Missing plugin | Behaviour |
| -------------- | --------- |
| `engineering` | **Refuse** `engineering-delivery` at setup. Offer `ad-hoc` or `custom`, or: `Install: /plugin install engineering@agent-plugins` |
| `ralph-loop` | `deliver` runs the same step machine inline |
| `design` | Loop continues without UX stages unless the user added them. Note in run context. |
| `product-management` | Loop can implement and review but cannot run `final_validate`. Stop before final sign-off with install message for `product-management`. |

**ad-hoc** and **custom** presets ship inside `ralph-loop` and run with no
companion plugins.

---

## engineering:implement → design.md

**Internal edge** (same plugin). `implement` reads `{work-dir}/design.md`
written by the `design` skill.

| Condition | Behaviour |
| --------- | --------- |
| design.md present | Proceed |
| design.md absent | Stop. Recommend `/engineering:design {work-id}` first. |

Primary artefact filename is `design.md`.

---

## product-management → architecture:solution

Strategy skills (`product`, `roadmap`, `write-spec`) list architecture as a
companion handoff.

| Condition | Behaviour |
| --------- | --------- |
| `architecture` installed | Recommend `/architecture:solution` |
| Not installed | Continue product work from user input. At architecture boundaries, say: `Install: /plugin install architecture@agent-plugins` then `/architecture:solution` |

Document-set quality review stays on `engineering`:

| Condition | Behaviour |
| --------- | --------- |
| `engineering` installed | Recommend `/engineering:docs-review` |
| Not installed | Continue; recommend install when a docs quality pass is needed |

Delivery skills route implementation to `/engineering:design`,
`/engineering:implement`, etc. — see
`product-management/references/delivery-conventions.md`.

---

## architecture ↔ engineering

| Need | Invoke |
| ---- | ------ |
| System architecture | `/architecture:solution` |
| ADRs | `/architecture:adr` |
| Work-item `design.md` | `/engineering:design` |
| Docs quality review | `/engineering:docs-review` |
| Implementation | `/engineering:implement` |

`implement` and `design` **read** `ARCHITECTURE.md` and ADRs via
artefact consumption — no hard install dependency. Writing or updating those
artefacts requires the `architecture` plugin (or manual edits).

When `architecture` is not installed: continue engineering from existing
architecture artefacts or user input; at write boundaries give the install
message for `architecture`.

---

## engineering ↔ product-management

See `engineering/references/engineering-conventions.md` and
`product-management/references/delivery-conventions.md`.

| Need | Invoke |
| ---- | ------ |
| Backlog / tasks / AC | `/product-management:tasks` |
| Sprint cadence | `/product-management:sprint-planning`, `sprint-retro`, `backlog-refine` |
| Sign-off | `/product-management:validate` |

When `product-management` is not installed: continue engineering work that does
not need tracker/backlog integration; recommend co-install for delivery cadence.

---

## engineering / design UX edge

| Need | Invoke |
| ---- | ------ |
| Live-browser UX review | `/design:ux-design-review` |
| Fix UX findings | `/design:ux-design-fix` |

When `design` is not installed: `code-review` still runs; skip UX
review steps. Recommend install before UI-heavy work.

Wireframes from `design` are consumed from `<instance-root>/design/` or
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

`engineering`, `content-marketing`, `document-management`, and others read
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
2. Offers `/plugin install <plugin>@agent-plugins` for catalogue matches that
   are not installed

Does not invoke other plugins directly — recommendation only.

---

## document-management ↔ brand-creative / engineering

`document-management` owns the **`docs/` tree lifecycle** (scaffold/reorganise
to Diátaxis, then score/fix including drift and voice). It writes only inside
`docs_root` (default `docs/`) and never auto-edits the default protected
practice trees (`docs/decisions/`, `docs/product/`, `docs/design/`,
`docs/brand/`).

`/engineering:docs-review` remains the **set-quality companion**: a read-only
quality/consistency review of *any* document set (`product.md`, `ARCHITECTURE.md`,
a handbook, a wiki). Practice plugins that already point at docs-review keep
those pointers.

| Need | Invoke |
| ---- | ------ |
| Scaffold or reorganise the `docs/` tree | `/document-management:docs-setup` |
| Score/fix `docs/`, drift vs code, voice | `/document-management:docs-improve` |
| "Are these docs any good / consistent?" with no tree or code-drift intent | `/engineering:docs-review` |

### brand-voice.md (artefact consumption)

| Condition | Behaviour |
| --------- | --------- |
| `<resolved-brand-path>/brand-voice.md` exists | Read and apply as the judgement layer |
| Artefact absent | Ask for tone inline; use the plugin style guide |
| `brand-creative` not installed | No install required |

### engineering:docs-review (optional companion)

| Condition | Behaviour |
| --------- | --------- |
| `engineering` installed | For pure set-quality review, recommend `/engineering:docs-review` |
| Not installed | Continue tree lifecycle work; set-quality review can wait |

When `document-management` is not installed: practices keep using
`/engineering:docs-review` for document-set quality. Missing this plugin does
not block architecture, product, or engineering work.

---

## Runtime path rules

Each plugin is copied to an isolated cache directory at install time.

| Allowed | Example |
| ------- | ------- |
| Paths within the same plugin | `../../references/conventions.md` |
| Artefact paths in the user's repo | `{work-dir}/design.md`, `.claude/loop/active.md` |

| Forbidden in skill markdown | Why |
| --------------------------- | --- |
| `../other-plugin/references/…` | Sibling may not exist in cache |
| Repo-monorepo paths assuming checkout layout | Install is not monorepo |

Repo-root `scripts/` (validate) may reference any path — they
run in the monorepo, not in the plugin cache.

---

## MCP bundles (Phase 3 verification)

| Plugin | Bundled MCP | Notes |
| ------ | ----------- | ----- |
| product-management | atlassian, amplitude | Unchanged after delivery-practice merge — tracker + analytics |
| design | figma, playwright | Playwright required for ux-design-review/fix browser work |
| engineering | github, playwright, context7 | Engineering tool surface |
| brand-creative | fireflies | |
| content-marketing | canva | |
| search-optimisation | ahrefs | |
| ralph-loop | — | Hooks only |
| skills-index | — | Router only |
| plugin-management | — | Meta-plugin + skill QA tooling |
| document-management | — | Utility; no bundled MCP |

Skills degrade when a connector is absent — see each plugin's `CONNECTORS.md`.
