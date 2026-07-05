# agency-hub

The first plugin to install from `digital-agency`. It bootstraps a **team-shared, git-versioned instance workspace** — org profile, target bindings, squad charters — that every practice plugin's setup reads from.

**v1 ships `agency-setup` only.** Marketplace management skills are designed (see `references/agency-skill-design-framework.md`) but deferred until Phase 3 — ported stubs exist in `skills/` for shape validation, not as v1 deliverables.

## Who this is for

Anyone adopting the digital-agency catalogue for real work — any business, agency, or in-house team. Install `agency-hub` before any practice plugin.

## First run: agency-setup

Interviews the business, creates or binds an instance repo, writes `config/` and target skeletons, then hands off to brand setup and the first practice plugin.

```
/agency-hub:agency-setup
```

| Flag | Behaviour |
|---|---|
| `--quick` | Business name, one practice, one target; sensible defaults elsewhere |
| `--full` | Full interview including seed material review |
| `--redo` | Ignore existing profile; re-interview and overwrite on confirmation |
| `--resume` | Continue a paused interview |
| `--check-integrations` | Report MCP connector status and legacy target-pointer paths; no interview |

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

## Commands (v1)

| Command | Does |
|---|---|
| `/agency-hub:agency-setup` | Detect state → interview → bind instance repo → write config → hand off to brand-creative |
| `/agency-hub:agency-setup --quick` | Minimal path: business name, one practice, one target |
| `/agency-hub:agency-setup --redo` | Ignore existing profile, re-interview, overwrite on confirmation |
| `/agency-hub:agency-setup --resume` | Continue a paused interview |
| `/agency-hub:agency-setup --check-integrations` | Report connector status only, no interview |

## Commands (v2 — deferred)

Marketplace management — designed, not built for v1:

| Command | Purpose |
|---|---|
| `/agency-hub:registry-browser [query]` | Search watched registries for community skills |
| `/agency-hub:skill-installer [skill]` | Allowlist-gate, fetch, QA, install |
| `/agency-hub:skills-qa [skill]` | Evaluate a third-party candidate |
| `/agency-hub:auto-updater` | Check updates; apply on explicit approval |
| `/agency-hub:disable [skill]` | Disable an installed community skill |
| `/agency-hub:uninstall [skill]` | Uninstall a community skill |
| `/agency-hub:related-skills-surfacer` | Suggest relevant community skills after a task |

## Skills

| Skill | Status | Purpose |
|---|---|---|
| **agency-setup** | **v1 — shipped** | Instance bootstrap interview |
| **registry-browser** | v2 — deferred | Search watched registries |
| **skill-installer** | v2 — deferred | Allowlist-gate, fetch, QA, install |
| **skills-qa** | v2 — deferred | Evaluate third-party candidates before install |
| **auto-updater** | v2 — deferred | Check updates; apply on approval |
| **disable / uninstall** | v2 — deferred | Manage installed community skills |
| **related-skills-surfacer** | v2 — deferred | Suggest community skills after tasks |
| **skill-manager** | v2 — reference | Workflows used by disable/uninstall |

## Security posture (v2)

When marketplace management ships: watched registries ≠ trust, restrictive allowlist defaults fail-closed, raw `SKILL.md` before install, skills-qa + injection scan, human approval + SHA pinning in `install-log.yaml`. See `skills/skill-installer/references/allowlist.md`.

## Scheduled agents (v2)

| Agent | Cadence | Purpose |
|---|---|---|
| **registry-sync** | Weekly | Poll watched registries; post digest per update preferences |

## After setup

1. Install the first **practice plugin** recommended during setup (e.g. `brand-creative`).
2. Install **`core`** if that practice needs shared roles (`web-development` → `core`; `brand-creative` → none).
3. Run that practice's **`practice-setup`** (e.g. `/brand-creative:practice-setup`).
4. Bind targets — website pointer (`.digital-agency/target.json`), social credentials when ready.
5. Deploy the first scheduled agent — see `digital-agency/scripts/deploy-squad-agents.sh`.

## References

- `references/agency-setup-framework.md` — invocation, config paths, interview structure
- `references/instance-profile-template.md` — Tier 1 schema for `config/instance.json`
