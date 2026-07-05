# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~project tracker` might mean Linear, Asana, or any other tracker with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (project tracker, design, product analytics, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

MCP servers for this practice are bundled in `.mcp.json` at the plugin root. Edit that file to swap providers or add stack-specific servers.

## Connectors for this plugin

| Category | Placeholder | Bundled in `.mcp.json` |
| -------- | ----------- | ---------------------- |
| Chat | `~~chat` | Slack |
| Project tracker | `~~project tracker` | Linear, Asana, Atlassian (Jira/Confluence) |
| Knowledge base | `~~knowledge base` | Notion |
| Design | `~~design` | Figma |
| Product analytics | `~~product analytics` | Amplitude, Pendo |
| User feedback | `~~user feedback` | Intercom |
| Meeting transcription | `~~meeting transcription` | Fireflies |
| Competitive intelligence | `~~competitive intelligence` | Similarweb |
| Source control | `~~source control` | GitHub, GitLab |
| CI/CD | `~~CI/CD` | — |
| Hosting / deploy | `~~hosting` | Vercel |
| Browser automation | `~~browser automation` | Playwright |
| Framework docs | `~~framework docs` | Context7, Next.js DevTools |

Other options in each category: Microsoft Teams (chat), monday.com or ClickUp (project tracker), Confluence or Guru (knowledge base), Mixpanel or Heap (product analytics), Productboard or Canny (user feedback), Gong or Dovetail (meeting transcription), Crayon or Klue (competitive intelligence).
