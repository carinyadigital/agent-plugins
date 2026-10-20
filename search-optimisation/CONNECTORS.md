# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

`.mcp.json` ships empty. Add servers for your stack; skills fall back when a connector is not configured.

## Companion practice (recommended co-install)

| Practice | Relationship | Invoke |
| -------- | ------------ | ------ |
| **product-management** | Companion practice | `/product-management:competitive-brief` |
| **engineering** | Companion practice | Playwright for live technical audits |

Install `product-management` when SEO work needs competitive landscape input.
Co-install **engineering** (or add Playwright to `.mcp.json`) for live browser checks in **technical-seo-audit**.

## In `.mcp.json`

None shipped.

## Suggested additions

| Category | Placeholder | Examples |
| -------- | ----------- | -------- |
| SEO intelligence | `~~SEO intelligence` | Ahrefs (`https://api.ahrefs.com/mcp/mcp`) — paid subscription + MCP key or OAuth; Semrush (`https://mcp.semrush.com/v2/mcp`) |
| Browser automation | `~~browser automation` | Playwright — add to **engineering** |
| Source control | `~~source control` | GitHub — see **engineering** |
| Search performance | `~~search performance` | Google Search Console — via SEO-tool connector (Ahrefs GSC endpoints) or signed-in browser |
| Web analytics | `~~web analytics` | Google Analytics 4 (Supermetrics connector or signed-in browser); hosting analytics as fallback |
| Signed-in browser | `~~browser` | Claude in Chrome — read-only use per `references/search-data-sources.md` |
| Project tracker | `~~project tracker` | Linear, GitHub Issues |
| Email marketing | `~~email marketing` | MailerLite, Mailchimp — sign-ups by source |
| Notifications | `~~chat` | Slack — run summaries |

Configure credentials in `.mcp.json` or via `claude mcp` / Cursor MCP settings
before live queries.

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | `--check-integrations` | Whatever is declared in `.mcp.json` |
| **keyword-research** | — | SEO intelligence |
| **technical-seo-audit** | — | Browser automation (live checks), source control (issues) |
| **content-seo-review** | — | Source control (PR review); none required for local seed paths |
| **local-authority** | — | Web search; SEO intelligence (backlinks) optional; project tracker for site fixes |
| **search-metrics** | — | Search performance, web analytics, SEO intelligence — connector or browser |
| **seo-agency** (agent) | scheduled | All of the above; browser and tracker connectors require running as the main session of a scheduled task on a device with the browser |

Competitive landscape: invoke `/product-management:competitive-brief` — requires
`product-management` install, not a connector category here.
