# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool you connect in that category.

`agency-hub` bootstraps instance configuration — it does not produce client deliverables. Connectors support repo binding, integration checks, and (v2) registry browsing.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|---|---|---|---|
| Source control | `~~source control` | GitHub | GitLab |
| Chat | `~~chat` | — | Slack (v2 registry-sync notifications) |
| Documents | `~~documents` | — | Google Drive |

## Notes

- **GitHub** enables `--check-integrations` to verify repository access when binding website or other code targets. v1 uses link-first repo creation — the human creates the repo; GitHub connector helps validate the path and read seed material from existing repos.
- **Chat** is optional and only meaningful once v2 marketplace management ships (`registry-sync` agent).
- Practice plugins carry their own connector manifests. `setup` reports what's available here; it does not replace per-practice integration checks.
