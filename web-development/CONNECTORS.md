# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

MCP servers for this practice are bundled in `.mcp.json` at the plugin root. Edit that file to swap providers or add stack-specific servers.

## Companion practice (recommended co-install)

| Practice | Relationship | Invoke |
| -------- | ------------ | ------ |
| **delivery-practice** | Companion practice | `/delivery-practice:backlog`, `/delivery-practice:tasks`, `/delivery-practice:sprint`, `/delivery-practice:validate` |

Install `delivery-practice` alongside this plugin when implementation needs backlog
alignment, task AC, sprint cadence, or epic sign-off. Do not bundle duplicate copies
of those skills here.

## Connectors for this plugin

| Category | Placeholder | Bundled in `.mcp.json` |
| -------- | ----------- | ---------------------- |
| Source control | `~~source control` | GitHub, GitLab |
| Hosting / deploy | `~~hosting` | Vercel |
| Chat | `~~chat` | Slack |
| Project tracker | `~~project tracker` | Linear |
| Observability | `~~observability` | Datadog |
| Error tracking | `~~error tracking` | Sentry |
| Database | `~~database` | — |
| Browser automation | `~~browser automation` | Playwright |
| Framework docs | `~~framework docs` | Context7, Next.js DevTools |

Neon Postgres and other stack-specific MCP servers are not bundled — add entries to
`.mcp.json` when the target repo uses them. `practice-setup --check-integrations`
reports what is connected.

Other options in each category: PagerDuty (incidents), Mixpanel (analytics).

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **practice-setup** | `--check-integrations` | GitHub, Vercel, Slack, Linear, Datadog, Sentry |
| **create-mr** | run | Source control |
| **deploy-qa** | run | Source control, hosting |
| **run-automated-suite** | run | Source control (CI status) |
| **platform-health** | run | Hosting, observability, error tracking |
| **debug** | run | Source control, observability (optional) |
| **implement** | run | Source control (branch context) |

Brand guide is **artifact consumption** — read `<resolved-brand-path>/brand-guide.md`;
no dependency on `brand-creative` being installed.
