---
name: disable
description: >
  Disable a community skill installed through the hub without removing its
  files. Use when the user wants to temporarily quiet a community skill
  ("disable [skill]"), stop its hooks from firing while keeping its config,
  or re-enable a previously disabled skill.
disable-model-invocation: true
argument-hint: "[skill name]"
allowed-tools: Read, Grep, Glob, Write
metadata:
  version: "0.1.0"
  owner: "agency-hub"
  review_cadence: "quarterly"
  work_shape: "orchestrate-delivery"
  permission_tier: elevated
  output_class: "tracking-update"
  sourcing_policy: "volatile-facts-must-be-sourced"
---
# /agency-hub:disable

## Status

**v2 — designed, deferred.** Marketplace management ships in Phase 3; v1 ships `agency-setup` only.

## When to use

Temporarily disable community skill — rename SKILL.md and hooks so discovery/triggers stop; files remain for re-enable.

## What this skill does not do

- **Does not touch first-party plugin skills.**
- **Does not delete files** — use `/agency-hub:uninstall` for removal.
- **Does not act without explicit yes.**

## Preconditions

| Input | If missing |
|---|---|
| Skill name | Ask |
| Install log entry (community, installed) | Refuse if not hub-installed |
| Load `skill-manager` reference | Required before substantive work |

## Provisional mode

N/A — confirm-before-rename always.

## Trust spine

Governance-tracking; install-log.yaml audit trail; built-in plugin refusal.

## Workflow

Run the `disable` workflow from the skill-manager reference skill against the named skill.

What disable does:

- Renames the skill's `SKILL.md` to `SKILL.md.disabled` so Claude no longer discovers it as an active skill. Files, references, templates, and config stay in place.
- If the skill ships hooks in `hooks/hooks.json`, also rename that file to `hooks.json.disabled` so no automatic triggers fire while the skill is disabled.
- Logs the action to `~/.claude/plugins/config/digital-agency/agency-hub/install-log.yaml`.

Safety rules:

1. **Only disable community skills installed through this hub.**
2. **Never disable a first-party plugin's skill.**
3. **Confirm before renaming.** Show the paths, get explicit `yes`.

Re-enable by running the command again with the same skill name.

> Detailed workflows live in the `skill-manager` reference skill — load it before doing substantive work.

## Worked example

**Input:** `disable competitor-scan` — community skill in install log.

**Expected output:** Paths shown; user confirms yes; SKILL.md → SKILL.md.disabled; log appended.

## Propose profile update

When a stable convention surfaces during this run (thresholds, naming, tone, output format, or recurring corrections), **propose a profile update**: show the exact diff against `~/.claude/plugins/config/digital-agency/agency-hub/CLAUDE.md` (instance-wide facts go to `<instance-repo>/config/instance.json`), ask for confirmation, and write only on yes. Only `/agency-hub:agency-setup` auto-applies a full profile write.

## Outputs

Follows plugin `CLAUDE.md` § Outputs. Next: re-enable same command, or `uninstall` if permanent removal needed.
