---
name: practice-setup
description: >
  Delivery practice setup interview — reads instance cadence and risk posture from
  agency-setup, interviews reporting format, escalation model, and persona preference
  (Product Manager vs Delivery Lead vs merged), writes practice profile. Use on first
  install after agency-setup, when the user says "set up delivery" or "configure sprint
  cadence", or to redo delivery defaults only.
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

# /delivery-practice:practice-setup

## When to use

First delivery setup after instance bootstrap; standalone Try-tier setup; re-run after
cadence or escalation model changes. Explicit invocation only.

## What this skill does not do

- **Does not re-interview business identity** when `config/instance.json` is complete — references instance profile for cadence and risk posture.
- **Does not write `config/instance.json`** — owned by `agency-hub:agency-setup`.
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

#### 3c — Persona preference (real branch — not cosmetic)

Does the customer want **Product Manager** and **Delivery Lead** as genuinely distinct personas, or merged into one working style?

- **One-person shop** → default merged; greet as single delivery partner.
- **Larger team** → default distinct; Product Manager for strategy skills, Delivery Lead for cadence skills.

Record which persona greets the user by default.

### Step 4 — Summarize before write

List every file to create/update:

- `~/.claude/plugins/config/digital-agency/delivery-practice/CLAUDE.md` — practice profile with cadence, escalation, persona preference, integration table

List deliberate skips. Ask: **"Write these files? (yes/no)"** — wait.

### Step 5 — Write practice profile (on yes)

Write `~/.claude/plugins/config/digital-agency/delivery-practice/CLAUDE.md` from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` template with interview answers filled. Set `Status: complete`.

Delete resume file if present.

### Step 6 — Next steps

Close with persona-appropriate handoff:

**Product Manager path:**

1. **Strategy** — `/delivery-practice:product write`
2. **Roadmap** — `/delivery-practice:roadmap write`
3. **Backlog** — `/delivery-practice:backlog write`

**Delivery Lead path:**

1. **Sprint** — `/delivery-practice:sprint plan`
2. **Status** — `/delivery-practice:stakeholder-update`
3. **Metrics** — `/delivery-practice:metrics-review`

**Either:**

4. **Route** — `/delivery-practice:skills-index` when unsure which skill to use.
5. **Refresh** — `/delivery-practice:practice-setup --redo` to redo delivery defaults only.

## Pause and resume

On pause, write JSON:

```json
{
  "plugin": "delivery-practice",
  "skill": "practice-setup",
  "mode": "quick|full",
  "startedAt": "ISO-8601",
  "instanceRoot": "<path or null>",
  "answers": {},
  "remainingSteps": [],
  "lastStepCompleted": ""
}
```

Location: `<instance-root>/config/.delivery-practice-practice-setup-resume.json` if instance exists; else personal hub path per framework.

## Worked example

**Input:** Instance profile complete; `--quick`; solo operator; merged persona; weekly bullet updates to sponsor.

**Expected output:** Practice profile at personal config path with cadence, escalation, and merged persona recorded; handoff to `/delivery-practice:product write` or `/delivery-practice:sprint plan`.

## Outputs

| Artefact | Path |
| -------- | ---- |
| Practice profile | `~/.claude/plugins/config/digital-agency/delivery-practice/CLAUDE.md` |

Next: invoke Product Manager or Delivery Lead skills per persona preference, or `--check-integrations`.
