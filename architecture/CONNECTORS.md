# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user
connects in that category. Skills are **tool-agnostic** — they describe
workflows in terms of categories rather than specific products.

Each practice bundles a **minimal default** in `.mcp.json`. Add more entries for
your stack.

## Companion practices (recommended co-install)

| Practice | Relationship | Consumption |
| -------- | ------------ | ----------- |
| **engineering** | Companion | `design`, `docs-review`, `implement`, `tech-debt` |
| **product-management** | Companion | `product`, `roadmap`, `tasks` upstream of solution |

Install companions alongside this plugin when architecture feeds delivery. No
bundled duplicate skills and no hard install dependency — this practice works
standalone when `solution.md` / ADRs are the only artefacts needed.

## Bundled in `.mcp.json`

| Category | Placeholder | Server |
| -------- | ----------- | ------ |
| Source control | `~~source control` | GitHub |

Other options: GitLab, Bitbucket, Linear, Atlassian (Jira) for tracker resolution
during `adr plan <work-id>`.

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | `--check-integrations` | GitHub |
| **solution** | write | None required — product.md and user context suffice |
| **adr** | plan / write / review | Source control / tracker optional for work-id harvest |
