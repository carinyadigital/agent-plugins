# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool you connect in that category.

`agency-hub` bootstraps instance configuration — it does not produce client deliverables and **does not bundle MCP servers**. Connectors live in practice plugins; install the practices you need and edit their `.mcp.json` files (or connect via Cursor / Claude MCP settings).

## Practice plugin connectors

| Practice | Default bundled | See |
| -------- | ----------------- | --- |
| **web-development** | GitHub, Playwright, Context7 | [web-development/CONNECTORS.md](../web-development/CONNECTORS.md) |
| **product-management** | Atlassian, Amplitude | [product-management/CONNECTORS.md](../product-management/CONNECTORS.md) |
| **brand-creative** | Fireflies | [brand-creative/CONNECTORS.md](../brand-creative/CONNECTORS.md) |
| **content-marketing** | Canva | [content-marketing/CONNECTORS.md](../content-marketing/CONNECTORS.md) |
| **product-design** | Figma | [product-design/CONNECTORS.md](../product-design/CONNECTORS.md) |
| **search-optimisation** | Ahrefs | [search-optimisation/CONNECTORS.md](../search-optimisation/CONNECTORS.md) |

## Notes

- v1 instance bootstrap is **link-first** — the human creates target repos; GitHub MCP in **web-development** helps validate repo access when that plugin is installed.
- **Chat** connectors are optional and only meaningful once v2 marketplace management ships (`registry-sync` agent).
- `/agency-hub:setup --check-integrations` verifies target bindings (`.agency/target.json` in bound repos), not MCP connector status.
