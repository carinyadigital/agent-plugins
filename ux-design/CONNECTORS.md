# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

MCP servers for this practice are bundled in `.mcp.json` at the plugin root. Edit that file to swap providers or add stack-specific servers.

## Companion practice (recommended co-install)

| Practice | Relationship | Consumption |
| -------- | ------------ | ----------- |
| **web-development** | Companion practice | Reads `<design-dir>/*.md` before UI implementation |

Install `web-development` alongside this plugin when wireframes feed frontend
implementation. No bundled duplicate skills and no hard install dependency — either
practice works standalone.

## Connectors for this plugin

| Category | Placeholder | Bundled in `.mcp.json` |
| -------- | ----------- | ---------------------- |
| Design | `~~design` | Figma |

Other options in each category: Canva (`https://mcp.canva.com/mcp` — quick visual
reference for social-sized layouts).

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **practice-setup** | `--check-integrations` | Figma |
| **wireframe** | write | Figma (optional — extract layout reference) |
| **wireframe** | write | None required — brief and brand-guide.md suffice |

Brand guide is **artifact consumption** — read `<resolved-brand-path>/brand-guide.md`
when present; no dependency on `brand-creative` being installed.
