---
name: mcp-integration
description: Explains how to declare a `.mcp.json` in a plugin — server types (stdio/SSE/HTTP), the prefer-connected-server-for-reads/CLI-fallback-for-writes convention, least-privilege server scoping, and environment-variable credential handling. Use when the user asks to "add an MCP server", "integrate MCP", "connect an external service", or mentions `.mcp.json`.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
metadata:
  version: "0.2.0"
  owner: "plugin-management"
  review_cadence: "quarterly"
  work_shape: "generate-draft"
  output_class: "draft-for-review"
---

# MCP integration

MCP (Model Context Protocol) lets a plugin connect the agent to an external system —
an API, a database, a ticketing tool. For the protocol's full transport and auth
reference, see [modelcontextprotocol.io](https://modelcontextprotocol.io); this skill
covers what a plugin author needs to declare one correctly and safely.

## Where it lives

```
plugins/<plugin>/
└── .mcp.json
```

At the plugin root, same rule as everything else (see `plugin-structure`).

## Server types

| Type | Transport | Typical use |
| :--- | :-------- | :----------- |
| `stdio` | Local subprocess over stdin/stdout | A CLI-wrapping server installed via `npx`/`uvx`/similar, running on the same machine as the agent. |
| `sse` | Server-sent events over HTTP | A hosted server, often behind OAuth, that streams responses. |
| `http` | Plain HTTP request/response | A REST-style hosted server with no streaming need. |

[`examples/stdio-server.json`](examples/stdio-server.json),
[`examples/sse-server.json`](examples/sse-server.json), and
[`examples/http-server.json`](examples/http-server.json) show a minimal, complete
declaration of each.

Two caveats on the `stdio` example specifically:

- It passes `${DATABASE_URL}` as both a CLI argument and an environment variable,
  mirroring that server's own documented usage — but a credential passed as a CLI
  argument can leak into `ps`/process-listing output on a shared machine, which an
  environment variable does not. Prefer env-only where the server supports reading its
  connection string from the environment instead of an argument.
- `@modelcontextprotocol/server-postgres` was archived by its maintainers in 2025 and
  has a known SQL-injection bypass of its read-only guarantee — it's a reference
  implementation, not something to run against a real database. Treat the name in the
  example as illustrative of the `stdio` shape only; point at an actively maintained
  Postgres MCP server for real use, and re-check any other reference-server name you
  copy from an example for the same reason before shipping it.

A minimal `stdio` declaration:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@some-org/mcp-server"],
      "env": { "API_TOKEN": "${API_TOKEN}" }
    }
  }
}
```

Scope every server to the narrowest set of tools/permissions the plugin actually
needs — don't wire up a general-purpose server when the plugin only ever calls two of
its tools.

## The convention: prefer a connected server for reads, CLI for writes

- **Prefer a connected MCP server for reads.** If an MCP server is available and
  covers the data the plugin needs, use it over shelling out to a CLI — it's
  typically faster, structured, and doesn't require the CLI to be installed.
- **Fall back to CLI for writes, or when MCP lacks coverage.** State-changing
  operations, and anything the connected server doesn't expose, go through the
  equivalent CLI (`git`, the service's own tool) instead.
- **This is a fallback chain, not a choice per plugin.** A single skill or command
  can legitimately use MCP for the read half of its work and CLI for the write half
  in the same invocation. State which path was chosen and why when it isn't obvious.

## Least privilege and no secrets in output

- Credentials/tokens the server needs go through **environment variable
  substitution** (`${API_TOKEN}`) in `.mcp.json`, never hardcoded values.
- Document every required environment variable in the plugin's `README.md` — name
  and purpose only, never an example real value.
- If a skill or command pre-allows specific MCP tools, name them individually rather
  than wildcarding a whole server's tool surface — the same least-privilege principle
  the `agent-development` skill applies to `tools:` scoping.
- Never echo a token, connection string, or credential value in skill/command output
  that uses an MCP tool — the same secret-handling rule the `hook-development` skill
  states for hooks applies identically here.

## Out of scope: authoring your own MCP server

Everything above is about **declaring/consuming** a server someone else wrote. This
skill doesn't cover **authoring** one — building the server binary itself — but two
things are worth knowing if a plugin ever does:

- **Tool annotations.** A well-authored server tags each tool with
  `readOnlyHint`/`destructiveHint`/`idempotentHint`/`openWorldHint`. Claude Code uses
  `readOnlyHint` to decide it can parallelise calls to that tool safely — a server that
  omits annotations forces more conservative, serial calling behaviour on every client,
  not just this one.
- **`sse`/`http` servers are a bigger attack surface than `stdio`.** They're often
  behind OAuth, and a malicious or compromised `authorization_endpoint` is a real,
  exploited vector — CVE-2025-6514 in `mcp-remote` was a remote-code-execution bug
  reachable exactly this way. If you're authoring (not just declaring) a remote server,
  follow OAuth 2.1 with PKCE, require HTTPS, and validate the token audience — don't
  trust an `authorization_endpoint` value without verifying it points where you expect.

This skill's own checklist stops at the declaring/consuming boundary; treat
server-authoring guidance above as a pointer, not full coverage.

## Documenting connectors: `README.md` vs a `CONNECTORS.md`

- **The common case — document env vars in `README.md`.** A plugin that declares one or
  two concrete servers needs nothing more than the required-environment-variable note
  above. Don't manufacture a separate catalogue file for it; an almost-empty
  `CONNECTORS.md` just drifts from `.mcp.json`.
- **The catalogue case — add a `CONNECTORS.md`.** When a plugin bundles **multiple
  swappable providers across categories** (a source-control server *and* a chat server
  *and* a knowledge-base server, any of which the user might swap), or has companion
  plugins whose connectors it must not duplicate, a `CONNECTORS.md` at the plugin root
  earns its place. It documents category → placeholder → bundled-provider mapping, a
  "used by skill" matrix, and companion-plugin relationships — the human-facing map that
  `.mcp.json` (the machine contract) doesn't carry.
- **Tool-agnostic placeholders.** In that pattern, skills refer to a `~~category`
  placeholder (`~~source control`) rather than naming a product, so the skill body keeps
  working when the provider is swapped in `.mcp.json`. See
  [`examples/CONNECTORS.md`](examples/CONNECTORS.md) for the full shape.
- **Declare each server once.** Whether or not a `CONNECTORS.md` exists, a given server
  belongs in exactly one plugin's `.mcp.json`. If a companion plugin already declares it,
  depend on that plugin rather than bundling a duplicate copy.

The `create-plugin` skill offers to scaffold a `CONNECTORS.md` only when the plan shows
this catalogue shape — it doesn't prompt for a single-server plugin.

## Portability note

`.mcp.json` and its transport types are a cross-host standard maintained outside any
single agent vendor, so an MCP server declared here is inherently more portable than a
host-specific hook — but host support for *which* transport types and auth flows are
wired up still varies. Treat MCP integration the same way as a hook: real
functionality, but isolate it so the plugin's skills/commands degrade to their
CLI-fallback path rather than breaking outright on a host that doesn't connect the
server. See the `plugin-portability` skill.

## Validation checklist

- [ ] `.mcp.json` at the plugin root
- [ ] Every credential in `env` uses `${VAR}` substitution, never a literal value
- [ ] Required environment variables documented in the plugin's `README.md`
- [ ] Skills/commands using this server state the prefer-MCP/CLI-fallback choice
      explicitly when it isn't the obvious default
- [ ] Pre-allowed MCP tools (if any) are named individually, not wildcarded
- [ ] Multi-provider/swappable-category plugins document the mapping in a
      `CONNECTORS.md`; single-server plugins do **not** add one

## Related skills

- **`plugin-structure`** — where `.mcp.json` sits relative to the rest of the plugin.
- **`hook-development`** — the other opt-in, host-adjacent component type, and the
  shared secret-handling rule.
- **`plugin-portability`** — isolating MCP as opt-in rather than load-bearing functionality.
