# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

MCP servers for this practice are bundled in `.mcp.json` at the plugin root. Edit that file to swap providers or add stack-specific servers.

## Companion practice (recommended co-install)

| Practice | Relationship | Invoke |
| -------- | ------------ | ------ |
| **delivery-practice** | Companion practice | `/delivery-practice:tasks --product`, `/delivery-practice:synthesize-research` |

Install `delivery-practice` alongside this plugin when content planning needs backlog
alignment or research synthesis. Do not bundle duplicate copies of those skills here.

## Connectors for this plugin

| Category | Placeholder | Bundled in `.mcp.json` |
| -------- | ----------- | ---------------------- |
| Source control | `~~source control` | GitHub, GitLab |
| Knowledge base | `~~knowledge base` | Notion |
| Chat | `~~chat` | Slack |
| Creative / design | `~~design` | Canva |
| CMS | `~~CMS` | — |
| Social scheduling | `~~social scheduling` | — |

Canva requires per-user OAuth. Use for social graphics and template autofill when
connected; skills still work from briefs and brand voice alone.

Other options in each category: Figma (`https://mcp.figma.com/mcp` — design reference),
Confluence or Google Drive (knowledge base), Microsoft Teams (chat),
Contentful/Sanity/WordPress (CMS), Buffer or Later (social scheduling).

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | `--check-integrations` | GitHub, Notion, Slack, Canva |
| **content-calendar** | write, review | Knowledge base (optional seed material) |
| **draft-post**, **draft-recipe** | — | Source control (seed PRs) |
| **curate-content** | — | None required — inventory JSON input |
| **analyse-media** | — | None required — local media path |
| **write-captions**, **edit-content** | — | None — reads brand-voice.md locally |

Brand voice is **artifact consumption** — read `<resolved-brand-path>/brand-voice.md`;
no dependency on `brand-creative` being installed.

## Optional companion (search-optimisation)

| Practice | Relationship | Invoke |
| -------- | ------------ | ------ |
| **search-optimisation** | Optional pairing | `/search-optimisation:content-seo-review` |

Neither practice requires the other. Install `search-optimisation` when content
production and SEO review run as a paired workflow.
