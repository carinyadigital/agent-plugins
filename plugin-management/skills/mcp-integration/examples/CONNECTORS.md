# Connectors

> Worked example. A `CONNECTORS.md` is only worth writing when a plugin bundles
> **multiple swappable providers across categories**, or has companion plugins whose
> connectors it must not duplicate. A plugin that declares one or two concrete servers
> should document its env vars in `README.md` and skip this file. See the
> `mcp-integration` skill for when this file earns its keep.

## How tool references work

Skills describe workflows in terms of **categories**, not specific products, using a
`~~category` placeholder (e.g. `~~source control`). Whichever provider the user connects
in that category fills the placeholder — the skill body never names a product, so it
keeps working when the provider is swapped.

The concrete servers are declared in `.mcp.json` at the plugin root. Edit that file to
swap providers or add stack-specific servers; this document just explains the mapping.

## Connectors for this plugin

| Category | Placeholder | Bundled in `.mcp.json` | Other options |
| :------- | :---------- | :--------------------- | :------------ |
| Source control | `~~source control` | GitLab | GitHub |
| Knowledge base | `~~knowledge base` | Confluence | Notion, Google Drive |
| Chat | `~~chat` | Slack | Microsoft Teams |
| Observability | `~~observability` | Datadog | — |

Servers behind per-user OAuth (rather than a shared token) only work once the individual
user has connected them; skills must degrade to their CLI-fallback path when a connector
is absent (see `mcp-integration`'s prefer-MCP-for-reads / CLI-for-writes convention).

## Used by skill

| Skill | Mode | Connectors |
| :---- | :--- | :--------- |
| **setup** | `--check-integrations` | Source control, Chat |
| **triage** | run | Source control (read), Observability (read) |
| **report** | run | Knowledge base (write) |
| **status** | run | None required — reads local artifacts |

## Companion plugins (avoid duplicating connectors)

| Plugin | Relationship | Invoke |
| :----- | :----------- | :----- |
| **delivery-practice** | Companion | `/delivery-practice:backlog` |

Install a companion alongside this plugin when its connectors are needed; do **not**
bundle duplicate copies of the same servers in both plugins' `.mcp.json`. Keep each
server declared once, in the plugin that owns it.
