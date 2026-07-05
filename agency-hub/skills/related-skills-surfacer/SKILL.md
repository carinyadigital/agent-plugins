---
name: related-skills-surfacer
description: >
  Suggest community skills based on recent activity in other plugins. Checks
  whether the community has built something relevant to a task and mentions it
  once, non-intrusively. Use when the user says "is there a community skill for
  this", "what else is out there", or asks for skill recommendations; also runs
  passively as part of other plugins' workflows.
argument-hint: ""
allowed-tools: Read, Grep, Glob
metadata:
  version: "0.1.0"
  owner: "agency-hub"
  review_cadence: "quarterly"
  work_shape: "orchestrate-delivery"
  permission_tier: advisory
  output_class: "draft-for-review"
  sourcing_policy: "volatile-facts-must-be-sourced"
---
# /agency-hub:related-skills-surfacer

## When to use

Suggest community skills matching recent task — once, non-intrusively; strong matches only.

## Preconditions

| Input | If missing |
|---|---|
| Hub engagement profile | Offer agency-setup |
| Task context or user query | Ask what they were doing |

## Provisional mode

Notifications set to none in profile — skill off.

## Trust spine

Structured-aggregation; frequency limit via surfaced.json; no nag on weak matches.

## Workflow

The community might have built the thing you're about to build. This skill notices and mentions it — once, briefly, non-annoyingly.

## How it runs

This skill surfaces related community skills after a task. It can be invoked directly by the user ("what else is out there for X?") or wired into other plugins via a Stop hook — the hook-based pattern requires each sibling plugin to declare a Stop hook that calls this skill, which is not wired by default. Without the hook wiring, invoke it directly.

Other plugins can include a light check at the end of a task:
> "The agency-hub found a community skill that might help with this kind of thing: [name] — [one-line]. Want to take a look?"

## Load context

`~/.claude/plugins/config/digital-agency/agency-hub/CLAUDE.md` → engagement profile, installed skills (don't suggest what's already installed).
Registry cache from registry-browser.

## The match

Given a task description (what the user was just doing), find registry skills that match:

- Keyword overlap between the task and skill descriptions
- Engagement profile fit (don't suggest PMO skills to a corporate strategist who didn't ask)
- Not already installed

**Threshold:** Only surface if the match is strong. Weak matches are noise. Better to surface nothing than to annoy.

## Output

If strong match:
> The community has a skill for this: **[name]** from [registry] — "[description]". `/agency-hub:skill-installer [name]` to try it.

If no strong match: silent. No output. Don't announce "I found nothing."

## Frequency limit

Don't surface the same skill twice. If the user didn't install it the first time, they saw it and decided no. Track dismissals in `references/surfaced.json`.

## User control

Per `~/.claude/plugins/config/digital-agency/agency-hub/CLAUDE.md` → new skill notifications:
- **All:** Surface any match
- **Matching engagement profile:** Filter by profile (default)
- **None:** This skill is off

## Worked example

**Input:** User finished competitive landscape work; strong registry match exists; not installed.

**Expected output:** One-line suggestion with `/agency-hub:skill-installer` handoff.

## Propose profile update

When a stable convention surfaces during this run (thresholds, naming, tone, output format, or recurring corrections), **propose a profile update**: show the exact diff against `~/.claude/plugins/config/digital-agency/agency-hub/CLAUDE.md` (instance-wide facts go to `<instance-repo>/config/instance.json`), ask for confirmation, and write only on yes. Only `/agency-hub:agency-setup` auto-applies a full profile write.

## Outputs

Follows plugin `CLAUDE.md` § Outputs. Silent if no strong match. Decision tree when match surfaced.

## What this skill does not do

- Install anything.
- Interrupt a task in progress. Surfacing happens at the *end* of a task, not in the middle.
- Nag. One mention per skill, ever.
