<!--
TEMPLATE — do not write user data here.

This file ships with the plugin and shows the structure the hub config should have.
It is replaced on every plugin update. Never write user data here.

The `setup` skill (and marketplace skills) copy or update the user config at:
  ~/.claude/plugins/config/digital-agency/agency-hub/CLAUDE.md

Instance-wide org facts live in the instance repo at:
  <instance-repo>/config/instance.json
-->

# Agency Hub — Personal Marketplace Profile

*Written by `/agency-hub:setup` or initialized on first marketplace use.*

---

## Who's using this

**Role:** [PLACEHOLDER — Agency practitioner / technical lead | Non-practitioner with practitioner access | Non-practitioner working independently]
**Practitioner contact:** [PLACEHOLDER — Name / team / outside firm / N/A]

---

## Connectors

Agency-hub does not bundle MCP servers. Install practice plugins and configure connectors in their `.mcp.json` files — see each practice's `CONNECTORS.md`.

*Re-check target bindings: `/agency-hub:setup --check-integrations`*

---

## Deployment context

**Context:** [PLACEHOLDER — personal | firm-internal | product-embedding]

Drives license defaults in `allowlist.yaml`. See `skills/skill-installer/references/allowlist.md`.

---

## Watched registries

| Registry | URL | Last synced | Update preference |
|---|---|---|---|
| [PLACEHOLDER — add via /agency-hub:registry-browser] | | | |

---

## Installed community skills

| Skill | Source | Installed | Pinned SHA |
|---|---|---|---|
| [PLACEHOLDER] | | | |

Authoritative audit trail: `install-log.yaml` in this directory.

---

## Update preferences

**Update preference:** [PLACEHOLDER — notify (default) / manual]
**New skill notifications:** [PLACEHOLDER — all / matching profile / none]

---

## Freshness reminders

| Content category | Max age before reminder | Rationale |
|---|---|---|
| market-data | 6 months | Markets shift quickly |
| methodology | 12 months | Frameworks evolve slower |
| benchmarks | 6 months | Benchmarks update annually at most |
| unknown | 3 months | Undeclared freshness treated cautiously |

---

## Built-in plugins

First-party plugins from the digital-agency catalogue — installed via marketplace, **not** via v2 `skill-installer`. `uninstall` and `disable` (when shipped) refuse to touch them.

**Hub:** `agency-hub`

**Practice plugins:** `brand-creative`, `product-management`, `content-marketing`, `ux-design`, `search-optimisation` (shipped); `web-development`, `social-media` (pending)

**Interim catalogue (until practice plugins ship):** `engineering` skill plugin; named agents under `agents/`

MCP servers are bundled in each practice plugin's `.mcp.json` — see `CONNECTORS.md` in the practice you install.

---

*Re-run: `/agency-hub:setup --redo`*
