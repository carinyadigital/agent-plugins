# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

Each practice bundles a **minimal default** in `.mcp.json`. Add more entries for your stack.

## Companion practice (recommended co-install)

| Practice | Relationship | Consumption |
| -------- | ------------ | ----------- |
| **web-development** | Companion practice | Reads `<design-dir>/*.md` before UI implementation |

Install `web-development` alongside this plugin when wireframes feed frontend
implementation. No bundled duplicate skills and no hard install dependency — either
practice works standalone.

## Bundled in `.mcp.json`

| Category | Placeholder | Server |
| -------- | ----------- | ------ |
| Design | `~~design` | Figma |
| Browser automation | `~~browser automation` | Playwright |

Other options in each category: Canva (`https://mcp.canva.com/mcp` — quick visual
reference for social-sized layouts).

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | `--check-integrations` | Figma, Playwright |
| **wireframe** | write | Figma (optional — extract layout reference) |
| **wireframe** | write | None required — brief and brand-guide.md suffice |
| **ux-design-review** | — | Playwright (live browser) |
| **ux-design-fix** | — | None required — edits code from review findings |

Brand guide is **artifact consumption** — read `<resolved-brand-path>/brand-guide.md`
when present; no dependency on `brand-creative` being installed.
