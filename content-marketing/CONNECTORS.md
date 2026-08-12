# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

Each practice bundles a **minimal default** in `.mcp.json`. Add more entries for your stack.

## Companion practice (recommended co-install)

| Practice | Relationship | Invoke |
| -------- | ------------ | ------ |
| **product-management** | Companion practice | `/product-management:tasks --product`, `/product-management:synthesize-research` |

Install `product-management` alongside this plugin when content planning needs
backlog alignment or research synthesis. Do not bundle duplicate copies of those
skills here.

## Bundled in `.mcp.json`

| Category | Placeholder | Server |
| -------- | ----------- | ------ |
| Creative / design | `~~design` | Canva |

Canva requires per-user OAuth. Use for social graphics and template autofill when
connected; skills still work from briefs and brand voice alone.

## Common additions

| Category | Placeholder | Examples |
| -------- | ----------- | -------- |
| Source control | `~~source control` | GitHub — see **product-engineering** |
| Knowledge base | `~~knowledge base` | Notion — see **product-management** |
| Chat | `~~chat` | Slack |
| Design reference | `~~design` | Figma — see **product-design** |
| CMS | `~~CMS` | Contentful, Sanity, WordPress |
| Social scheduling | `~~social scheduling` | Buffer, Later |

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | `--check-integrations` | Canva (+ any additions) |
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
