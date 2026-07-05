<!--
TEMPLATE — do not write user data here.

This file ships with the plugin and shows the structure the hub config should have.
It is replaced on every plugin update. Never write user data here.

The `agency-setup` skill (and marketplace skills) copy or update the user config at:
  ~/.claude/plugins/config/digital-agency/agency-hub/CLAUDE.md

Instance-wide org facts live in the instance repo at:
  <instance-repo>/config/instance.json
-->

# Agency Hub — Personal Marketplace Profile

*Written by `/agency-hub:agency-setup` or initialized on first marketplace use.*

---

## Who's using this

**Role:** [PLACEHOLDER — Agency practitioner / technical lead | Non-practitioner with practitioner access | Non-practitioner working independently]
**Practitioner contact:** [PLACEHOLDER — Name / team / outside firm / N/A]

---

## Available integrations

| Integration | Status | Fallback if unavailable |
|---|---|---|
| GitHub | [✓ / ✗] | Registry browse and install fall back to manual URL paste |
| Slack | [✓ / ✗] | Registry-sync digest written to file instead of chat |

*Re-check: `/agency-hub:agency-setup --check-integrations`*

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

**Practice plugins:** `brand-creative`, `delivery-practice` (shipped); `web-development`, `content-marketing`, `social-media`, `seo` (pending)

**Interim catalogue (until practice plugins ship):** `engineering`, `content`, `seo` skill plugins; named agents under `agents/`

**Connectors:** `github`, `gitlab`, `vercel`, `figma`, `linear`, `playwright`, `context7`, `next-devtools`

---

*Re-run: `/agency-hub:agency-setup --redo`*
