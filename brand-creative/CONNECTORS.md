# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

`.mcp.json` ships empty. Add servers for your stack; skills fall back to manual upload and discovery reports when a connector is not configured.

## In `.mcp.json`

None shipped.

## Suggested additions

| Category | Placeholder | Examples |
| -------- | ----------- | -------- |
| Meeting transcription | `~~meeting transcription` | Fireflies, Gong |
| Design | `~~design` | Figma — see **design** |
| Knowledge base | `~~knowledge base` | Notion, Atlassian Confluence — see **product-management** |
| Chat | `~~chat` | Slack, Microsoft Teams |
| Creative / templates | `~~design` | Canva — see **content-marketing** |

Configure credentials in `.mcp.json` or via `claude mcp` / Cursor MCP settings.

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | discover chain | Meeting transcription, knowledge base, chat, design (optional) |
| **brand-voice** | discover | Meeting transcription, knowledge base, chat (optional) |
| **brand-guide** | write | Figma (primary for visual tokens — add or use **design**) |
| **brand-voice** | write | Manual upload or discovery report (no MCP required) |
| **brand-voice** | enforce | None — reads local `brand-voice.md` |
