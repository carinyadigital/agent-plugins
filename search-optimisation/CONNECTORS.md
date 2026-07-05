# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

MCP servers for this practice are bundled in `.mcp.json` at the plugin root. Edit that file to swap providers or add stack-specific servers.

## Companion practice (recommended co-install)

| Practice | Relationship | Invoke |
| -------- | ------------ | ------ |
| **delivery-practice** | Companion practice | `/delivery-practice:competitive-brief` |

Install `delivery-practice` alongside this plugin when SEO work needs competitive
landscape input. Do not bundle a duplicate copy of `competitive-brief` here.

## Optional companion (content-marketing)

| Practice | Relationship | Invoke |
| -------- | ------------ | ------ |
| **content-marketing** | Optional pairing | `/content-marketing:draft-post`, `/content-marketing:draft-recipe` |

Neither practice requires the other. `content-seo-review` accepts pasted content or
seed paths directly. Install `content-marketing` when content production and SEO
review run as a paired workflow.

## Connectors for this plugin

| Category | Placeholder | Bundled in `.mcp.json` |
| -------- | ----------- | ---------------------- |
| Source control | `~~source control` | GitHub, GitLab |
| Browser automation | `~~browser automation` | Playwright |
| SEO intelligence | `~~SEO intelligence` | Ahrefs |

Google Search Console is not bundled — connect when your client supports it.
Ahrefs and Semrush require a paid subscription and user authentication (MCP key or
OAuth). Configure credentials in `.mcp.json` or via `claude mcp` / Cursor MCP
settings before live queries.

Other options in each category: Semrush (`https://mcp.semrush.com/v2/mcp` — SEO
intelligence), Google Search Console (search performance).

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **practice-setup** | `--check-integrations` | GitHub, Playwright, Ahrefs |
| **keyword-research** | run | SEO intelligence (optional — enriches volume and difficulty signals) |
| **technical-seo-audit** | run | Playwright (live checks), GitHub (issues) |
| **content-seo-review** | run | Source control (PR review); none required for local seed paths |

Competitive landscape: invoke `/delivery-practice:competitive-brief` — requires
`delivery-practice` install, not a connector category here.
