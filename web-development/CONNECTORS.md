# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Skills are **tool-agnostic** — they describe workflows in terms of categories rather than specific products.

Standalone connector plugins in this repo live under `connectors/<slug>/.mcp.json`.

## Companion practice (recommended co-install)

| Practice | Relationship | Invoke |
| -------- | ------------ | ------ |
| **delivery-practice** | Companion practice | `/delivery-practice:backlog`, `/delivery-practice:tasks`, `/delivery-practice:sprint`, `/delivery-practice:validate` |

Install `delivery-practice` alongside this plugin when implementation needs backlog
alignment, task AC, sprint cadence, or epic sign-off. Do not bundle duplicate copies
of those skills here.

## Connectors for this plugin

| Category | Placeholder | Bundled in `.mcp.json` | Also in `connectors/` |
| -------- | ----------- | ---------------------- | ------------------------------ |
| Source control | `~~source control` | GitHub | GitHub, GitLab |
| Hosting / deploy | `~~hosting` | Vercel | Vercel |
| Chat | `~~chat` | Slack | — |
| Project tracker | `~~project tracker` | Linear | Linear |
| Observability | `~~observability` | Datadog | — |
| Error tracking | `~~error tracking` | — | — |
| Database | `~~database` | — | — |
| Browser automation | — | — | Playwright |
| Framework docs | — | — | Context7, Next.js DevTools |

Sentry, Neon Postgres, and other stack-specific MCP servers are not bundled — install
connector plugins or configure user MCP when the target repo uses them.
`practice-setup --check-integrations` reports what is connected.

Other options in each category: GitLab (source control), PagerDuty (incidents),
Mixpanel (analytics), Figma (design handoff).

## Used by skill

| Skill | Mode | Connectors |
| ----- | ---- | ---------- |
| **practice-setup** | `--check-integrations` | GitHub, Vercel, Slack, Linear, Datadog |
| **create-mr** | run | Source control |
| **deploy-qa** | run | Source control, hosting |
| **run-automated-suite** | run | Source control (CI status) |
| **platform-health** | run | Hosting, observability, error tracking |
| **debug** | run | Source control, observability (optional) |
| **implement** | run | Source control (branch context) |

Brand guide is **artifact consumption** — read `<resolved-brand-path>/brand-guide.md`;
no dependency on `brand-creative` being installed.
