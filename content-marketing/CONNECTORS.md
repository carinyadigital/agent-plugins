# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

Standalone connector plugins in this repo live under `connectors/<slug>/.mcp.json`.

## Companion practice (recommended co-install)

| Practice | Relationship | Invoke |
| -------- | ------------ | ------ |
| **delivery-practice** | Companion practice | `/delivery-practice:backlog`, `/delivery-practice:synthesize-research` |

Install `delivery-practice` alongside this plugin when content planning needs backlog
alignment or research synthesis. Do not bundle duplicate copies of those skills here.

## Connectors for this plugin

| Category | Placeholder | Bundled in `.mcp.json` | Also in `connectors/` |
| -------- | ----------- | ---------------------- | ------------------------------ |
| Source control | `~~source control` | GitHub | GitHub, GitLab |
| Knowledge base | `~~knowledge base` | Notion | — |
| Chat | `~~chat` | Slack | — |
| CMS | `~~CMS` | — | — |
| Social scheduling | `~~social scheduling` | — | — |

Other options in each category: GitLab (source control), Confluence or Google Drive
(knowledge base), Microsoft Teams (chat), Contentful/Sanity/WordPress (CMS), Buffer or
Later (social scheduling).

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **practice-setup** | `--check-integrations` | GitHub, Notion, Slack |
| **content-calendar** | write, review | Knowledge base (optional seed material) |
| **draft-post**, **draft-recipe** | run | Source control (seed PRs) |
| **curate-content** | run | None required — inventory JSON input |
| **analyse-media** | run | None required — local media path |
| **write-captions**, **edit-content** | run | None — reads brand-voice.md locally |

Brand voice is **artifact consumption** — read `<resolved-brand-path>/brand-voice.md`;
no dependency on `brand-creative` being installed.
