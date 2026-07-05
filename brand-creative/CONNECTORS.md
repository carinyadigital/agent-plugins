# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

Standalone connector plugins in this repo live under `connectors/<slug>/.mcp.json`.

## Connectors for this plugin

| Category | Placeholder | Bundled in `.mcp.json` | Also in `connectors/` |
| -------- | ----------- | ---------------------- | ------------------------------ |
| Chat | `~~chat` | Slack | — |
| Knowledge base | `~~knowledge base` | Notion | — |
| Wiki / docs | `~~knowledge base` | Atlassian (Confluence) | — |
| Design | `~~design` | Figma | Figma |
| Meeting transcription | `~~meeting transcription` | Fireflies | — |

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **practice-setup** | discover chain | Notion, Confluence, Slack, Figma, Fireflies |
| **brand-voice** | discover | Notion, Confluence, Slack, Figma, Fireflies |
| **brand-guide** | write | Figma (primary for visual tokens) |
| **brand-voice** | write | Manual upload or discovery report (no MCP required) |
| **brand-voice** | enforce | None — reads local `brand-voice.md` |

Other options in each category: Google Drive or SharePoint (file storage — connect when available), Gong (meeting transcription), Microsoft Teams (chat).
