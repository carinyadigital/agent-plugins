# agency-hub

The first plugin to install from `digital-agency`. It bootstraps a **team-shared, git-versioned instance workspace** — org profile, target bindings, squad charters — that every practice plugin's setup reads from.

**v1 ships `agency-setup`.** Marketplace management skills are ported from `strategy-builder-hub` and may be refined in a later pass.

## Who this is for

Anyone adopting the digital-agency catalogue for real work — any business, agency, or in-house team. Install `agency-hub` before any practice plugin.

## First run: agency-setup

Interviews the business, creates or binds an instance repo, writes `config/` and target skeletons, then hands off to brand voice setup.

```
/agency-hub:agency-setup
```

| Flag | Behaviour |
|---|---|
| `--quick` | Business name, one practice, one target; sensible defaults elsewhere |
| `--full` | Full interview including seed material review |
| `--redo` | Ignore existing profile; re-interview and overwrite on confirmation |
| `--resume` | Continue a paused interview |
| `--check-integrations` | Report MCP connector status only; no interview |

## Config tiers

| Tier | Scope | Location |
|---|---|---|
| **0 — Personal hub state** | Marketplace preferences on this machine | `~/.claude/plugins/config/digital-agency/agency-hub/` (`CLAUDE.md`, `allowlist.yaml`, `install-log.yaml`) |
| **1 — Instance profile** | Shared org/brand/config facts, versioned in git | `<instance-repo>/config/instance.json`, `<instance-repo>/brand/` |
| **2 — Target bindings** | Per-target connection details | `<instance-repo>/config/targets/<name>.json` + `.digital-agency/target.json` in target repos |

Unlike personal dotfile config, Tier 1 lives in a **private instance repo** — multiple agents and humans read it over months.

## Repo creation (v1)

Link-first: `agency-setup` provides a template URL; the human creates the private repo and confirms the path. The agent then writes config into the existing repo. API-driven repo creation is deferred.

## Prerequisites

- **GitHub connector** — optional for `--check-integrations`; required when binding target repos hosted on GitHub.
- **Instance template** — `digital-agency-instance` template repo (when published). Until then, create an empty private repo with the directory skeleton described in `references/agency-setup-framework.md`.

## Commands

| Command | Does |
|---|---|
| `/agency-hub:agency-setup` | Detect state → interview → bind instance repo → write config → hand off to brand-setup |
| `/agency-hub:registry-browser [query]` | Search watched registries for community skills |
| `/agency-hub:skill-installer [skill]` | Install a community skill (allowlist + QA gate) |
| `/agency-hub:skills-qa [skill]` | Evaluate a skill against the Agency Skill Design Framework |
| `/agency-hub:auto-updater` | Check for updates; apply only on explicit approval |
| `/agency-hub:disable [skill]` | Disable an installed community skill |
| `/agency-hub:uninstall [skill]` | Uninstall a community skill |
| `/agency-hub:related-skills-surfacer` | Suggest relevant community skills after a task |

## Skills

| Skill | Status | Purpose |
|---|---|---|
| **agency-setup** | Shipped | Instance bootstrap interview |
| **registry-browser** | Shipped (port) | Search watched registries |
| **skill-installer** | Shipped (port) | Allowlist-gate, fetch, QA, install |
| **skills-qa** | Shipped (port) | Evaluate third-party candidates — refine against agency framework later |
| **auto-updater** | Shipped (port) | Check updates; apply on approval |
| **disable / uninstall** | Shipped (port) | Manage installed community skills |
| **related-skills-surfacer** | Shipped (port) | Suggest community skills after tasks |
| **skill-manager** | Reference | Workflows used by disable/uninstall |

## Security posture

Same defense-in-depth as strategy-builder-hub: watched registries ≠ trust, restrictive allowlist defaults fail-closed, raw `SKILL.md` before install, skills-qa + injection scan, human approval + SHA pinning in `install-log.yaml`. See `skills/skill-installer/references/allowlist.md`.

## Scheduled agents

| Agent | Cadence | Purpose |
|---|---|---|
| **registry-sync** | Weekly | Poll watched registries; post digest per update preferences |

## After setup

1. Install the first practice plugin recommended during setup (e.g. `brand`, `engineering`, `content`).
2. Run that practice's setup skill when available.
3. Deploy the first scheduled agent — see `digital-agency/scripts/deploy-squad-agents.sh`.

## References

- `references/agency-setup-framework.md` — invocation, config paths, interview structure
- `references/instance-profile-template.md` — Tier 1 schema for `config/instance.json`
