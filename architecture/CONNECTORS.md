# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user
connects in that category. Skills are **tool-agnostic** — they describe
workflows in terms of categories rather than specific products.

`.mcp.json` ships empty. Add servers for your stack; skills fall back when a
connector is not configured.

## Companion practices (recommended co-install)

| Practice | Relationship | Consumption |
| -------- | ------------ | ----------- |
| **engineering** | Companion | `design`, `docs-review`, `implement`, `tech-debt` |
| **product-management** | Companion | `product`, `roadmap`, `tasks` upstream of solution |

Install companions alongside this plugin when architecture feeds delivery. No
bundled duplicate skills and no hard install dependency — this practice works
standalone when `ARCHITECTURE.md` / ADRs are the only artefacts needed.

## In `.mcp.json`

None shipped.

## Suggested additions

| Category | Placeholder | Examples |
| -------- | ----------- | -------- |
| Source control | `~~source control` | GitHub, GitLab, Bitbucket |
| Project tracker | `~~project tracker` | Linear, Atlassian (Jira) for work-id resolution during `adr plan <work-id>` |

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | `--check-integrations` | Whatever is declared in `.mcp.json` |
| **solution** | write | None required — product.md, the repo, and user context suffice |
| **adr** | plan / write / review | Source control / tracker optional for work-id harvest |
