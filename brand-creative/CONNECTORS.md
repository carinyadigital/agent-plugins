# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

Each practice bundles a **minimal default** in `.mcp.json`. Add more entries for your stack; skills fall back to manual upload and discovery reports when a connector is not configured.

## Bundled in `.mcp.json`

| Category | Placeholder | Server |
| -------- | ----------- | ------ |
| Meeting transcription | `~~meeting transcription` | Fireflies |

## Common additions

| Category | Placeholder | Examples |
| -------- | ----------- | -------- |
| Design | `~~design` | Figma — see **design** |
| Knowledge base | `~~knowledge base` | Notion, Atlassian Confluence — see **product-management** |
| Chat | `~~chat` | Slack |
| Creative / templates | `~~design` | Canva — see **content-marketing** |

Gong (meeting transcription) and Microsoft Teams (chat) are also supported when
configured in `.mcp.json`.

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | discover chain | Fireflies (+ any additions) |
| **brand-voice** | discover | Meeting transcription, knowledge base, chat (optional) |
| **brand-guide** | write | Figma (primary for visual tokens — add or use **design**) |
| **brand-voice** | write | Manual upload or discovery report (no MCP required) |
| **brand-voice** | enforce | None — reads local `brand-voice.md` |
