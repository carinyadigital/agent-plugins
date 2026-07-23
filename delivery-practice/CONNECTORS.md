# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~project tracker` might mean Linear, Asana, or any other tracker with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (project tracker, design, product analytics, etc.) rather than specific products. The `.mcp.json` pre-configures a minimal default; add any MCP server in that category to `.mcp.json`.

## Bundled in `.mcp.json`

| Category | Placeholder | Server |
| -------- | ----------- | ------ |
| Project tracker / wiki | `~~project tracker` | Atlassian (Jira / Confluence) |

## Common additions

| Category | Placeholder | Examples |
| -------- | ----------- | -------- |
| Chat | `~~chat` | Slack (`https://mcp.slack.com/mcp`) |
| Knowledge base | `~~knowledge base` | Notion (`https://mcp.notion.com/mcp`) |
| Design | `~~design` | Figma — see **ux-design** |
| User feedback | `~~user feedback` | Intercom, Pendo |
| Meeting transcription | `~~meeting transcription` | Fireflies — see **brand-creative** |
| Competitive intelligence | `~~competitive intelligence` | Similarweb |
| Source control | `~~source control` | GitHub — see **web-development** |
| Hosting / deploy | `~~hosting` | Vercel — add to **web-development** |
| Browser automation | `~~browser automation` | Playwright — bundled in **web-development** |

Other options: Linear, Asana, monday.com (project tracker); Mixpanel, Heap (analytics); Gong (meeting transcription); Crayon, Klue (competitive intelligence).

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | `--check-integrations` | Atlassian (+ any additions) |
| **tasks** | — | Project tracker (optional) |
| **backlog-refine** | — | Project tracker (optional) |
| **sprint-planning** | — | Project tracker (optional) |
| **sprint-retro** | — | Project tracker (optional) |
| **validate** | — | Project tracker (optional) |

Strategy, research, metrics, and competitive-intelligence connectors are used by
the companion **product-management** plugin — see its `CONNECTORS.md`.
