---
name: related-skills-surfacer
description: >
  Suggest uninstalled catalogue plugins or community skills based on recent
  activity. Mentions a strong match once, non-intrusively, with an install
  command. Use when the user says "is there a skill for this", "what else is
  out there", or asks for skill recommendations after a task.
argument-hint: ""
allowed-tools: Read, Grep, Glob
metadata:
  version: "0.2.0"
  owner: "skills-index"
  review_cadence: "quarterly"
  work_shape: "orchestrate-delivery"
  permission_tier: advisory
  output_class: "decision-support"
  sourcing_policy: "volatile-facts-must-be-sourced"
---

# /skills-index:related-skills-surfacer

## When to use

After a task, or when the user asks what else exists for the work they just did.
Strong matches only — better to stay silent than nag.

## What this skill does not do

- **Does not install plugins** — only offers `/plugin install …@carinya-plugins`
- **Does not re-route vague "which skill?" questions** — that is `/skills-index:find`
- **Does not promote deleted hub package-manager skills**

## Workflow

1. Infer the task just completed (or ask once).
2. Match against the `/skills-index:find` catalogue — prefer **uninstalled**
   plugins that clearly own the next step.
3. If a strong match exists and was not already suggested this session, output
   one short line with the install command and the skill to run after.
4. Track suggestions in `references/surfaced.json` so the same skill is not
   surfaced twice without the user asking again.

## Output

If strong match:

> Related: install **`product-design`** for live UX review —
> `/plugin install product-design@carinya-plugins` then `/product-design:ux-design-review`.

If no strong match: silent.

## Frequency limit

Do not surface the same plugin twice in a session unless the user asks again.
Append dismissed suggestions to `references/surfaced.json`.
