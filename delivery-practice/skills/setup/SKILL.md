---
name: setup
description: >
  Delivery practice setup interview — reads instance cadence and risk posture from
  `/agency-hub:setup`, interviews reporting format, escalation model, and sprint cadence,
  writes practice profile. Use on first install after `/agency-hub:setup`, when the user
  says "set up delivery" or "configure sprint cadence", or to redo delivery defaults only.
argument-hint: "[--quick|--full] [--redo] [--resume] [--check-integrations]"
allowed-tools: Read, Grep, Glob, Write
disable-model-invocation: true
metadata:
  version: "0.1.0"
  owner: "delivery-practice"
  review_cadence: "quarterly"
  work_shape: "orchestrate-delivery"
  permission_tier: artefact-writer
  output_class: "structured-data"
  sourcing_policy: "volatile-facts-must-be-sourced"
---

# /delivery-practice:setup

## When to use

First delivery setup after instance bootstrap; standalone Try-tier setup; re-run after
cadence or escalation model changes. Explicit invocation only.

## What this skill does not do

- **Does not re-interview business identity** when `config/instance.json` is complete — references instance profile for cadence and risk posture.
- **Does not write `config/instance.json`** — owned by `agency-hub:setup`.
- **Does not install other plugins** — user installs from marketplace.
- **Does not write without explicit yes** after showing the plain-language summary.
- **Does not produce product/roadmap/backlog artefacts** — those are separate skills after setup.

## Preconditions

Read before proceeding:

- `${CLAUDE_PLUGIN_ROOT}/references/practice-setup-framework.md`
- `${CLAUDE_PLUGIN_ROOT}/references/delivery-conventions.md`
- `${CLAUDE_PLUGIN_ROOT}/references/instance-profile-template.md` (when instance profile may exist)

Honour flags: `--quick`, `--full`, `--redo`, `--resume`, `--check-integrations`.

## Provisional mode

Partial interview → write resume JSON per framework. Offer `--resume` on next run.

## Trust spine

Structured-aggregation; integration table reports ✓ only on successful MCP probe. Practice profile is user-local config — show full summary before write.

## Workflow

### Step 0 — Detect existing state

1. **Read** `config/instance.json` if present — note `status`, cadence hints, risk posture, squad structure.
2. **Read** `~/.claude/plugins/config/digital-agency/delivery-practice/CLAUDE.md` unless `--redo`.
3. If **complete** and not `--redo`: summarize on-file delivery defaults; offer refresh, `--redo`, or `--check-integrations`. Stop unless user chooses refresh.
4. If **paused resume file** exists: greet, summarize progress, continue or start over.

### Step 0b — Install scope check

If working directory looks project-scoped and delivery context may span repos, warn once per framework. Wait for confirmation.

### Step 1 — Mode and preamble

If neither `--quick` nor `--full` was passed, offer quick vs full.

**Quick path:** reporting cadence default, escalation model skeleton, persona default (merged for solo).

**Full path:** all plugin-specific questions below.

Tell user: "Say **pause** anytime — I'll save progress for `--resume`."

### Step 2 — Integrations (`--check-integrations`)

Before interview (or as sole action when flag set):

> Delivery skills can pull from project trackers, chat, knowledge bases, analytics, and competitive intelligence when connected. Let me check what's available.

For each server in `${CLAUDE_PLUGIN_ROOT}/.mcp.json`:

- Probe if possible → ✓ connected
- Configured but not probeable → ⚪ configured but not verified
- Missing → ✗ not found + manual fallback

If `--check-integrations` only, stop here unless user asks to continue setup.

### Step 3 — Interview (skip answered instance facts)

**2–3 prompts per turn.** Do not re-ask cadence or risk posture if `config/instance.json` has them — say "see instance profile".

#### 3a — Reporting cadence and format (full mode; abbreviated in quick)

What does a stakeholder update actually look like for this business?

- Frequency (weekly, fortnightly, monthly, ad hoc)
- Format (brief bullets, narrative, dashboard summary)
- Primary audience (sponsor, internal team, board)

#### 3b — Escalation model

What triggers an escalation? Who does it go to? Which channel?

#### 3c — Sprint cadence

What is the sprint length (one week, two weeks, other) and where does committed scope come from? Note whether the team runs formal sprints at all — solo shops may work continuously off the backlog.

Product strategy, roadmap, specs, research, and stakeholder communication live in the companion **product-management** plugin — recommend it if the user needs those and route there rather than re-scoping this practice.

### Step 4 — Summarize before write

List every file to create/update:

- `~/.claude/plugins/config/digital-agency/delivery-practice/CLAUDE.md` — practice profile with cadence, escalation, sprint cadence, integration table

List deliberate skips. Ask: **"Write these files? (yes/no)"** — wait.

### Step 5 — Write practice profile (on yes)

Write `~/.claude/plugins/config/digital-agency/delivery-practice/CLAUDE.md` from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` template with interview answers filled. Set `Status: complete`.

Delete resume file if present.

### Step 6 — Next steps

Close with a delivery handoff:

1. **Backlog** — `/delivery-practice:tasks --product` to decompose product/roadmap into epics and stories.
2. **Groom** — `/delivery-practice:backlog-refine` to check sprint readiness.
3. **Sprint** — `/delivery-practice:sprint-planning` then `/delivery-practice:sprint-retro`.
4. **Sign-off** — `/delivery-practice:validate` when an epic is done.
5. **Route** — `/delivery-practice:skills-index` when unsure which skill to use.
6. **Refresh** — `/delivery-practice:setup --redo` to redo delivery defaults only.

For product strategy, roadmap, specs, research, metrics, or stakeholder updates, install the companion **product-management** plugin (`/product-management:product`, `/product-management:roadmap`, `/product-management:write-spec`).

## Pause and resume

On pause, write JSON:

```json
{
  "plugin": "delivery-practice",
  "skill": "setup",
  "mode": "quick|full",
  "startedAt": "ISO-8601",
  "instanceRoot": "<path or null>",
  "answers": {},
  "remainingSteps": [],
  "lastStepCompleted": ""
}
```

Location: `<instance-root>/config/.delivery-setup-resume.json` if instance exists; else personal hub path per framework.

## Worked example

**Input:** Instance profile complete; `--quick`; solo operator; two-week sprints; weekly bullet updates to sponsor.

**Expected output:** Practice profile at personal config path with cadence, escalation, and sprint cadence recorded; handoff to `/delivery-practice:tasks --product` or `/delivery-practice:sprint-planning`.

## Outputs

| Artefact | Path |
| -------- | ---- |
| Practice profile | `~/.claude/plugins/config/digital-agency/delivery-practice/CLAUDE.md` |

Next: invoke delivery skills (`tasks`, `sprint-planning`, `validate`), or `--check-integrations`.
