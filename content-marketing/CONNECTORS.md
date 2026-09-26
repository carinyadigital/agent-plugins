# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

`.mcp.json` ships empty. Add servers for your stack; skills fall back when a connector is not configured.

## Companion practice (recommended co-install)

| Practice | Relationship | Invoke |
| -------- | ------------ | ------ |
| **product-management** | Companion practice | `/product-management:tasks --product`, `/product-management:synthesize-research` |

Install `product-management` alongside this plugin when content planning needs
backlog alignment or research synthesis. Do not bundle duplicate copies of those
skills here.

## In `.mcp.json`

None shipped.

## Suggested additions

| Category | Placeholder | Examples |
| -------- | ----------- | -------- |
| Creative / design | `~~design` | Canva (`https://mcp.canva.com/mcp`) — per-user OAuth; social graphics and template autofill |
| Source control | `~~source control` | GitHub — see **engineering** |
| Knowledge base | `~~knowledge base` | Notion — see **product-management** |
| Chat | `~~chat` | Slack |
| Design reference | `~~design` | Figma — see **design** |
| CMS | `~~CMS` | Contentful, Sanity, WordPress |
| Social scheduling | `~~social scheduling` | Buffer, Later |

Skills still work from briefs and brand voice alone.

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | `--check-integrations` | Whatever is declared in `.mcp.json` |
| **content-calendar** | write, review | Knowledge base (optional seed material) |
| **draft-post**, **draft-recipe** | — | Source control (optional seed PRs) |
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
