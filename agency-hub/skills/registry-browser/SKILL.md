---
name: registry-browser
description: >
  Search watched registries for community agency skills, showing matches with
  descriptions and offering to show the full SKILL.md before install. Use when
  the user says "browse", "search skills", "find a skill for", "what's out
  there for", or wants to add a new registry to the watchlist.
argument-hint: "[search query]"
allowed-tools: Read, Grep, Glob, Write, WebFetch
metadata:
  version: "0.1.0"
  owner: "agency-hub"
  review_cadence: "quarterly"
  work_shape: "orchestrate-delivery"
  permission_tier: elevated
  output_class: "structured-data"
  sourcing_policy: "volatile-facts-must-be-sourced"
---
# /agency-hub:registry-browser

## Status

**v2 — designed, deferred.** Marketplace management ships in Phase 3; v1 ships `setup` only.

## When to use

Search watched registries; preview full SKILL.md; add registries to watchlist on confirmation.

## Preconditions

| Input | If missing |
|---|---|
| Hub profile with watched registries | Offer to add registry or setup |

## Provisional mode

Empty watchlist — guide user to add first trusted registry.

## Trust spine

Structured-aggregation; browse only — no install without skill-installer.

## Workflow

Find skills across the watched registries. Search, preview, decide.

## Load context

`~/.claude/plugins/config/digital-agency/agency-hub/CLAUDE.md` → watched registries list.

## Workflow

### Step 1: Fetch registry indexes

For each watched registry:

- GitHub repos: fetch `skills/` directory listing and each `SKILL.md` frontmatter (name + description).
- Marketplace-style registries: fetch the index.

Cache the index locally (`references/registry-cache.json`) so browsing is fast. Refresh cache if >7 days old or on request.

### Step 2: Search

Match query against skill names and descriptions. Simple keyword match is fine — these are small enough that fuzzy search is overkill.

Also: browse by category if the registry organizes skills that way.

### Step 3: Present matches

```markdown
## Search: "[query]"

**Found [N] skills across [M] registries:**

### [skill-name]
**From:** [registry name]
**Description:** [from frontmatter]
[View full SKILL.md] [Install]

### [skill-name]
[...]
```

### Step 4: Preview

On "view full SKILL.md": fetch and show the whole file. User reads it before deciding to install. No surprises.

### Step 5: Add a registry

If the user has a URL to a registry not in the watchlist:

1. Fetch it, validate it's a skills repo (has `skills/` or `.claude-plugin/`)
2. Show what's in it
3. Add to `~/.claude/plugins/config/digital-agency/agency-hub/CLAUDE.md` → watched registries on confirmation

## Default registries

No default registries are pre-configured. Add registries you trust via this command or by editing your engagement profile directly.

## What this skill does not do

- Install anything. It browses. skill-installer installs.
- Rate or review skills. It shows you the SKILL.md; you judge.
- Search the whole internet. Only watched registries.

## Worked example

**Input:** Search "competitive landscape" across two watched registries.

**Expected output:** Match list with descriptions; offer full SKILL.md preview per match.

## Propose profile update

When a stable convention surfaces during this run (thresholds, naming, tone, output format, or recurring corrections), **propose a profile update**: show the exact diff against `~/.claude/plugins/config/digital-agency/agency-hub/CLAUDE.md` (instance-wide facts go to `<instance-repo>/config/instance.json`), ask for confirmation, and write only on yes. Only `/agency-hub:setup` auto-applies a full profile write.

## Outputs

Follows plugin `CLAUDE.md` § Outputs. Next: `skill-installer` or add registry to watchlist.
