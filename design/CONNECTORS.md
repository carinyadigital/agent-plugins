# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

`.mcp.json` ships empty. Add servers for your stack; skills fall back when a connector is not configured.

## Companion practice (recommended co-install)

| Practice | Relationship | Consumption |
| -------- | ------------ | ----------- |
| **engineering** | Companion practice | Reads `<design-dir>/*.md` before UI implementation |

Install `engineering` alongside this plugin when wireframes feed frontend
implementation. No bundled duplicate skills and no hard install dependency — either
practice works standalone.

## In `.mcp.json`

None shipped.

## Suggested additions

| Category | Placeholder | Examples |
| -------- | ----------- | -------- |
| Design | `~~design` | Figma (`https://mcp.figma.com/mcp`) |
| Browser automation | `~~browser automation` | Playwright (`npx @playwright/mcp@latest`) |
| Creative / design | `~~design` | Canva (`https://mcp.canva.com/mcp`) — quick visual reference for social-sized layouts |

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | `--check-integrations` | Whatever is declared in `.mcp.json` |
| **wireframe** | write | Figma (optional — extract layout reference) |
| **wireframe** | write | None required — brief and brand-guide.md suffice |
| **ux-design-review** | — | Playwright (live browser) |
| **ux-design-fix** | — | None required — edits code from review findings |

Brand guide is **artifact consumption** — read `<resolved-brand-path>/brand-guide.md`
when present; no dependency on `brand-creative` being installed.
