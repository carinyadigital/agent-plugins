---
name: setup
description: >
  Product management setup interview — reads instance cadence and risk posture,
  interviews discovery workflow, reporting format, stakeholder audiences, escalation
  model, and sprint cadence, writes practice profile. Use on first install, when the
  user says "set up product management", "configure PM defaults", "set up delivery",
  or "configure sprint cadence", or to redo product/delivery defaults only.
argument-hint: "[--quick|--full] [--redo] [--resume] [--check-integrations]"
allowed-tools: Read, Grep, Glob, Write
disable-model-invocation: true
metadata:
  version: "0.2.0"
  owner: "product-management"
  review_cadence: "quarterly"
  work_shape: "orchestrate-delivery"
  permission_tier: artefact-writer
  output_class: "structured-data"
  sourcing_policy: "volatile-facts-must-be-sourced"
---

# /product-management:setup

## When to use

First product management setup after instance bootstrap; standalone Try-tier setup;
re-run after cadence, audience, discovery-workflow, escalation, or sprint-cadence
changes. Explicit invocation only.

## What this skill does not do

- **Does not re-interview business identity** when `config/instance.json` is complete — references instance profile for cadence and risk posture.
- **Writes `config/instance.json` if absent** — idempotent instance bootstrap, then this practice interview.
- **Does not install other plugins** — user installs from marketplace.
- **Does not write without explicit yes** after showing the plain-language summary.
- **Does not produce product/roadmap/spec/backlog artefacts** — those are separate skills after setup.

## Preconditions

Read before proceeding:

- `${CLAUDE_PLUGIN_ROOT}/references/product-conventions.md`
- `${CLAUDE_PLUGIN_ROOT}/references/delivery-conventions.md`

Honour flags: `--quick`, `--full`, `--redo`, `--resume`, `--check-integrations`.

## Provisional mode

Partial interview → write resume JSON (see Pause and resume). Offer `--resume` on next run.

## Trust spine

Structured-aggregation; integration table reports ✓ only on successful MCP probe. Practice profile is user-local config — show full summary before write.

## Workflow

### Step 0 — Detect existing state

1. **Read** `config/instance.json` if present — note `status`, cadence hints, risk posture, squad structure.
2. **Read** `~/.claude/plugins/config/digital-agency/product-management/CLAUDE.md` unless `--redo`.
3. If **complete** and not `--redo`: summarize on-file product/delivery defaults; offer refresh, `--redo`, or `--check-integrations`. Stop unless user chooses refresh.
4. If **paused resume file** exists: greet, summarize progress, continue or start over.

### Step 0a — Instance bootstrap

If `config/instance.json` is **absent**:

1. Interview minimal org facts: business name / prose name, single-business vs agency-serving-clients, primary practice, planning cadence, risk posture.
2. Show a plain-language summary of `config/instance.json` (and an optional target skeleton). **Wait for yes.**
3. Write `config/instance.json` with `status: complete`, `setup.completedAt` (ISO 8601), and `setup.mode`. Include `instance` slug, `business`, `services.enabled`, `cadence`, `riskPosture`, `governance` (`agentsNeverPushMain: true`), and `seedMaterial` as captured. Do not create GitHub repos autonomously.
4. Continue into the plugin-specific interview.

If present and complete, reference it — do not re-ask business identity.

### Step 0b — Install scope check

If working directory looks project-scoped and product context may span repos, warn once that a project-scoped install cannot read files outside the project folder. Wait for confirmation.

### Step 1 — Mode and preamble

If neither `--quick` nor `--full` was passed, offer quick vs full.

**Quick path:** reporting cadence default, primary stakeholder audience, discovery-source default, escalation model skeleton, sprint length default.

**Full path:** all plugin-specific questions below.

Tell user: "Say **pause** anytime — I'll save progress for `--resume`."

### Step 2 — Integrations (`--check-integrations`)

Before interview (or as sole action when flag set):

> Product skills can pull from project trackers, chat, knowledge bases, product analytics, user feedback, meeting transcription, and competitive intelligence when connected. Let me check what's available.

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
- Primary audience (exec, engineering, partner, customer, board, sponsor)

#### 3b — Discovery workflow

Where does product input come from — user interviews, support tickets, analytics, sales, or competitive signal? Which sources are connected vs pasted manually?

#### 3c — Roadmap format preference

Which roadmap shape does the team use — Now/Next/Later, quarterly themes, or OKR-aligned? Record the default for the `roadmap` skill.

#### 3d — Escalation model

What triggers an escalation? Who does it go to? Which channel?

#### 3e — Sprint cadence

What is the sprint length (one week, two weeks, other) and where does committed scope come from? Note whether the team runs formal sprints at all — solo shops may work continuously off the backlog.

### Step 4 — Summarize before write

List every file to create/update:

- `~/.claude/plugins/config/digital-agency/product-management/CLAUDE.md` — practice profile with cadence, stakeholder audiences, discovery sources, roadmap format, escalation, sprint cadence, integration table

List deliberate skips. Ask: **"Write these files? (yes/no)"** — wait.

### Step 5 — Write practice profile (on yes)

Write `~/.claude/plugins/config/digital-agency/product-management/CLAUDE.md` from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` template with interview answers filled. Set `Status: complete`.

Delete resume file if present.

### Step 6 — Next steps

Close with a product-management handoff:

1. **Strategy** — `/product-management:product`
2. **Roadmap** — `/product-management:roadmap`
3. **Spec** — `/product-management:write-spec`
4. **Research** — `/product-management:synthesize-research`
5. **Backlog** — `/product-management:tasks --product` to decompose product/roadmap into epics and stories
6. **Groom** — `/product-management:backlog-refine` to check sprint readiness
7. **Sprint** — `/product-management:sprint-planning` then `/product-management:sprint-retro`
8. **Sign-off** — `/product-management:validate` when a work item is done
9. **Refresh** — `/product-management:setup --redo` to redo defaults only

## Pause and resume

On pause, write JSON:

```json
{
  "plugin": "product-management",
  "skill": "setup",
  "mode": "quick|full",
  "startedAt": "ISO-8601",
  "instanceRoot": "<path or null>",
  "answers": {},
  "remainingSteps": [],
  "lastStepCompleted": ""
}
```

Location: `<instance-root>/config/.product-setup-resume.json` if instance exists; else `~/.claude/plugins/config/digital-agency/product-management/setup-resume.json`.

## Worked example

**Input:** Instance profile complete; `--quick`; solo operator; weekly bullet updates to sponsor; Now/Next/Later roadmap; two-week sprints.

**Expected output:** Practice profile at personal config path with cadence, audience, discovery sources, roadmap format, escalation, and sprint cadence recorded; handoff to `/product-management:product` or `/product-management:tasks --product`.

## Outputs

| Artefact | Path |
| -------- | ---- |
| Practice profile | `~/.claude/plugins/config/digital-agency/product-management/CLAUDE.md` |

Next: invoke product management skills, or `--check-integrations`.
