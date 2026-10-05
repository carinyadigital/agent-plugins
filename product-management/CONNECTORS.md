# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~project tracker` might mean Linear, Asana, or any other tracker with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (project tracker, product analytics, user feedback, etc.) rather than specific products. `.mcp.json` ships empty; add any MCP server in that category.

## In `.mcp.json`

None shipped.

## Suggested additions

| Category | Placeholder | Examples |
| -------- | ----------- | -------- |
| Project tracker / wiki | `~~project tracker` | Atlassian (Jira / Confluence), Linear, Asana, monday.com, ClickUp |
| Product analytics | `~~product analytics` | Amplitude, Mixpanel, Heap |
| Chat | `~~chat` | Slack (`https://mcp.slack.com/mcp`) |
| Knowledge base | `~~knowledge base` | Notion (`https://mcp.notion.com/mcp`) |
| Design | `~~design` | Figma (`https://mcp.figma.com/mcp`) — see **design** |
| User feedback | `~~user feedback` | Intercom (`https://mcp.intercom.com/mcp`), Pendo |
| Meeting transcription | `~~meeting transcription` | Fireflies (`https://api.fireflies.ai/mcp`), Gong — see **brand-creative** |
| Competitive intelligence | `~~competitive intelligence` | Similarweb (`https://mcp.similarweb.com/mcp`), Crayon, Klue |
| Source control | `~~source control` | GitHub — see **engineering** |
| Hosting / deploy | `~~hosting` | Vercel — add to **engineering** |
| Browser automation | `~~browser automation` | Playwright — add to **engineering** |

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | `--check-integrations` | Whatever is declared in `.mcp.json` |
| **product** | — | Knowledge base, project tracker (optional) |
| **roadmap** | — | Project tracker (optional) |
| **write-spec** | — | Knowledge base, project tracker (optional) |
| **write-initiative** | — | Project tracker (optional) |
| **write-epic** | — | Project tracker (optional) |
| **write-story** | — | Project tracker (optional) |
| **synthesize-research** | — | Meeting transcription, user feedback, knowledge base (optional) |
| **competitive-brief** | — | Competitive intelligence (optional) |
| **metrics-review** | — | Product analytics |
| **stakeholder-update** | — | Chat, project tracker (optional) |
| **product-brainstorming** | — | None required |
| **tasks** | — | Project tracker (optional) |
| **backlog-refine** | — | Project tracker (optional) |
| **sprint-planning** | — | Project tracker (optional) |
| **sprint-retro** | — | Project tracker (optional) |
| **validate** | — | Project tracker (optional) |
