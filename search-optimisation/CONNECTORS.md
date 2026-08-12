# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

Each practice bundles a **minimal default** in `.mcp.json`. Add more entries for your stack.

## Companion practice (recommended co-install)

| Practice | Relationship | Invoke |
| -------- | ------------ | ------ |
| **product-management** | Companion practice | `/product-management:competitive-brief` |
| **product-engineering** | Companion practice | Playwright for live technical audits |

Install `product-management` when SEO work needs competitive landscape input.
Co-install **product-engineering** (or add Playwright to `.mcp.json`) for live browser checks in **technical-seo-audit**.

## Bundled in `.mcp.json`

| Category | Placeholder | Server |
| -------- | ----------- | ------ |
| SEO intelligence | `~~SEO intelligence` | Ahrefs |

Ahrefs requires a paid subscription and user authentication (MCP key or OAuth).
Configure credentials in `.mcp.json` or via `claude mcp` / Cursor MCP settings
before live queries.

## Common additions

| Category | Placeholder | Examples |
| -------- | ----------- | -------- |
| Browser automation | `~~browser automation` | Playwright — bundled in **product-engineering** |
| Source control | `~~source control` | GitHub — see **product-engineering** |
| SEO intelligence | `~~SEO intelligence` | Semrush (`https://mcp.semrush.com/v2/mcp`) |
| Search performance | — | Google Search Console (when supported) |

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | `--check-integrations` | Ahrefs (+ any additions) |
| **keyword-research** | — | SEO intelligence |
| **technical-seo-audit** | — | Browser automation (live checks), source control (issues) |
| **content-seo-review** | — | Source control (PR review); none required for local seed paths |

Competitive landscape: invoke `/product-management:competitive-brief` — requires
`product-management` install, not a connector category here.
