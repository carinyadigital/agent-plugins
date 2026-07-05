---
name: uninstall
description: >
  Uninstall a community skill that was installed via the hub. Confirms before
  deleting files, refuses to touch first-party plugin skills, and logs every
  action. Use when the user wants to fully remove a community skill
  ("uninstall [skill]", "remove this skill") rather than just disable it.
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
# /agency-hub:uninstall

## Status

**v2 — designed, deferred.** Marketplace management ships in Phase 3; v1 ships `agency-setup` only.

## When to use

Fully remove hub-installed community skill — confirm paths, delete files, log uninstall.

## What this skill does not do

- **Does not touch first-party plugins.**
- **Does not delete without explicit yes.**
- **Does not disable-only** — suggest `/agency-hub:disable` to keep files.

## Preconditions

| Input | If missing |
|---|---|
| Skill name | Ask |
| Install log entry | Refuse if not recorded |
| Load `skill-manager` reference | Required before substantive work |

## Provisional mode

N/A — confirm-before-delete always.

## Trust spine

Governance-tracking; install-log audit; built-in plugin refusal.

## Workflow

Run the `uninstall` workflow from the skill-manager reference skill.

Safety rules:

1. **Only uninstall community skills installed through this hub.**
2. **Never uninstall first-party plugin skills.**
3. **Confirm before removing files** — show every path; proceed only on explicit `yes`.
4. **Log the uninstall** to `install-log.yaml`.

If the user wants to keep files, suggest `/agency-hub:disable` instead.

> Detailed workflows live in the `skill-manager` reference skill.

## Worked example

**Input:** `uninstall old-scan` — in install log, not first-party.

**Expected output:** Deletion paths listed; user types yes; files removed; log entry `uninstall`.

## Propose profile update

When a stable convention surfaces during this run (thresholds, naming, tone, output format, or recurring corrections), **propose a profile update**: show the exact diff against `~/.claude/plugins/config/digital-agency/agency-hub/CLAUDE.md` (instance-wide facts go to `<instance-repo>/config/instance.json`), ask for confirmation, and write only on yes. Only `/agency-hub:agency-setup` auto-applies a full profile write.

## Outputs

Follows plugin `CLAUDE.md` § Outputs. Next: `registry-browser` for replacement skill, or done.
