# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~project tracker` might mean Linear, Asana, or any other tracker with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (project tracker, product analytics, user feedback, etc.) rather than specific products. The `.mcp.json` pre-configures a minimal default; add any MCP server in that category to `.mcp.json`.

## Bundled in `.mcp.json`

| Category | Placeholder | Server |
| -------- | ----------- | ------ |
| Project tracker / wiki | `~~project tracker` | Atlassian (Jira / Confluence) |
| Product analytics | `~~product analytics` | Amplitude |

## Common additions

| Category | Placeholder | Examples |
| -------- | ----------- | -------- |
| Chat | `~~chat` | Slack (`https://mcp.slack.com/mcp`) |
| Knowledge base | `~~knowledge base` | Notion (`https://mcp.notion.com/mcp`) |
| Design | `~~design` | Figma (`https://mcp.figma.com/mcp`) — see **ux-design** |
| User feedback | `~~user feedback` | Intercom (`https://mcp.intercom.com/mcp`), Pendo |
| Meeting transcription | `~~meeting transcription` | Fireflies (`https://api.fireflies.ai/mcp`) — see **brand-creative** |
| Competitive intelligence | `~~competitive intelligence` | Similarweb (`https://mcp.similarweb.com/mcp`) |

Other options: Linear, Asana, monday.com, ClickUp (project tracker); Mixpanel, Heap (analytics); Gong (meeting transcription); Crayon, Klue (competitive intelligence).

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | `--check-integrations` | Atlassian, Amplitude (+ any additions) |
| **product** | — | Knowledge base, project tracker (optional) |
| **roadmap** | — | Project tracker (optional) |
| **write-spec** | — | Knowledge base, project tracker (optional) |
| **synthesize-research** | — | Meeting transcription, user feedback, knowledge base (optional) |
| **competitive-brief** | — | Competitive intelligence (optional) |
| **metrics-review** | — | Product analytics |
| **stakeholder-update** | — | Chat, project tracker (optional) |
| **product-brainstorming** | — | None required |
