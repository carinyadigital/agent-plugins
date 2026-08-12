# UX design conventions

Canonical rules for paths, artefact boundaries, and skill routing. All `product-design`
skills read this file when resolving paths or routing near-miss requests.

## Design directory (wireframe output)

Default path for wireframe specs: `<design-dir>/{page-or-flow}.md`.

Resolve `<design-dir>` in this order — first match wins:

1. **Explicit path named by the user** in the request.
2. **Inside an instance repo** — `config/instance.json` at working root →
   `<instance-root>/design/`.
3. **Inside a target repo** — `.agency/target.json` at working root →
   resolve instance root, then `<instance-root>/design/`.
4. **Standalone** — no instance or target pointer → `docs/design/` in the current
   project.

When `config/instance.json` defines a design path, treat it as relative to the
instance root unless the user overrides.

Create the design directory on first write when the user confirms.

## Brand guide (artifact consumption)

Before wireframing UI-heavy pages, read `<resolved-brand-path>/brand-guide.md` for
layout tokens, typography, and visual patterns when present. Resolve the brand
directory using the same order as `brand-creative` conventions:

1. **Explicit path named by the user** in the request.
2. **Inside an instance repo** — `config/instance.json` at working root →
   `<instance-root>/brand/`.
3. **Inside a target repo** — `.agency/target.json` at working root →
   resolve instance root, then `<instance-root>/brand/`.
4. **Standalone** — no instance or target pointer → `docs/brand/` in the current
   project.

If `brand-guide.md` does not exist, proceed with layout structure only — do not
require `brand-creative` to be installed. Do not bundle or invoke the brand-guide
skill; read the artefact directly when present.

## Downstream consumption (engineering)

`engineering` reads `<design-dir>/*.md` before implementing UI — the same
artifact-consumption pattern as `brand-guide.md`. No install dependency in either
direction.

Epic-level technical design (`docs/work/{work-id}/tdd.md`) remains owned by
`/engineering:tdd` — wireframes here are UX layout specs, not implementation
design docs.

## Companion practice (engineering)

For implementation after wireframes are approved, recommend `engineering` as a
co-install. Document in CONNECTORS.md.

## Skill routing (near-misses)

| User intent | Skill | Notes |
| ----------- | ----- | ----- |
| Low-fidelity page or flow layout | **wireframe** | Writes to `<design-dir>/` |
| Epic implementation spec | `/engineering:tdd` | Technical design — not this practice |
| System architecture / ADRs | `/architecture:solution`, `/architecture:adr` | Architecture practice |
| Visual brand tokens, colour, type | `/brand-creative:brand-guide` | Brand practice |
| Usability review, research synthesis | — | Deferred in v1 — not shipped |

## Artefact boundaries

| Content | Belongs in | Not in |
| ------- | ---------- | ------ |
| Page/flow layout, interaction notes | `<design-dir>/{page-or-flow}.md` | brand-guide, epic tdd.md |
| Visual tokens, colour, typography | `brand/brand-guide.md` | wireframe specs |
| Epic implementation spec, file list | `docs/work/{work-id}/tdd.md` | wireframe specs |
| Business strategy, personas | `docs/product/product.md` | wireframe specs |
| Task Gherkin AC | `docs/work/{work-id}/tasks.md` | wireframe specs |

Wireframe specs describe **what the user sees and does** at low fidelity. They do
not prescribe component names, file paths, or API contracts — those belong in
`/engineering:tdd`.
