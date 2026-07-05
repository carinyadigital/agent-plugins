# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

MCP servers for this practice are bundled in `.mcp.json` at the plugin root. Edit that file to swap providers or add stack-specific servers.

## Connectors for this plugin

| Category | Placeholder | Bundled in `.mcp.json` |
| -------- | ----------- | ---------------------- |
| Chat | `~~chat` | Slack |
| Knowledge base | `~~knowledge base` | Notion |
| Wiki / docs | `~~knowledge base` | Atlassian (Confluence) |
| Design | `~~design` | Figma |
| Meeting transcription | `~~meeting transcription` | Fireflies |

Other options in each category: Canva (`https://mcp.canva.com/mcp` — design and
template generation; OAuth per user), Google Drive or SharePoint (file storage).

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **practice-setup** | discover chain | Notion, Confluence, Slack, Figma, Fireflies |
| **brand-voice** | discover | Notion, Confluence, Slack, Figma, Fireflies |
| **brand-guide** | write | Figma (primary for visual tokens) |
| **brand-voice** | write | Manual upload or discovery report (no MCP required) |
| **brand-voice** | enforce | None — reads local `brand-voice.md` |

Gong (meeting transcription) and Microsoft Teams (chat) are also supported when
configured in `.mcp.json`.
