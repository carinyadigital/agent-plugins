# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

Each practice bundles a **minimal default** in `.mcp.json` — one or two servers most relevant to that practice. Add more entries for your stack; skills fall back gracefully when a category is not connected.

## Companion practice (recommended co-install)

| Practice | Relationship | Invoke |
| -------- | ------------ | ------ |
| **product-management** | Companion practice | `/product-management:tasks --product`, `/product-management:tasks`, `/product-management:backlog-refine`, `/product-management:sprint-planning`, `/product-management:sprint-retro`, `/product-management:validate` |

Install `product-management` alongside this plugin when implementation needs backlog
alignment, task AC, sprint cadence, or epic sign-off. Do not bundle duplicate copies
of those skills here.

## Bundled in `.mcp.json`

| Category | Placeholder | Server |
| -------- | ----------- | ------ |
| Source control | `~~source control` | GitHub |
| Browser automation | `~~browser automation` | Playwright |
| Framework docs | `~~framework docs` | Context7 |

## Common additions

Add these to `.mcp.json` (or connect via Cursor / Claude MCP settings) when your stack uses them:

| Category | Placeholder | Examples |
| -------- | ----------- | -------- |
| Source control | `~~source control` | GitLab |
| Hosting / deploy | `~~hosting` | Vercel (`https://mcp.vercel.com`) |
| Chat | `~~chat` | Slack (`https://mcp.slack.com/mcp`) |
| Project tracker | `~~project tracker` | Linear, Asana — see **product-management** |
| Observability | `~~observability` | Datadog |
| Error tracking | `~~error tracking` | Sentry (`https://mcp.sentry.dev/mcp`) |
| Design | `~~design` | Figma — see **ux-design** |
| Database | `~~database` | Neon Postgres, etc. |

Neon Postgres and other stack-specific MCP servers are not bundled — add entries to
`.mcp.json` when the target repo uses them. `setup --check-integrations`
reports what is connected.

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **setup** | `--check-integrations` | GitHub, Playwright, Context7 (+ any additions) |
| **merge-request** | create, babysit | Source control |
| **merge-request-review** | run | Source control |
| **ux-design-review** | review, fix | Figma (optional), Playwright |
| **deploy-qa** | — | Source control, hosting |
| **run-automated-suite** | — | Source control (CI status) |
| **platform-health** | — | Hosting, observability, error tracking |
| **debug** | — | Source control, observability (optional) |
| **implement** | — | Source control (branch context), framework docs |

Brand guide is **artifact consumption** — read `<resolved-brand-path>/brand-guide.md`;
no dependency on `brand-creative` being installed.
