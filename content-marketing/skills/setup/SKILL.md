---
name: setup
description: >
  Content marketing practice setup interview — reads instance business identity and house
  tone hints from `config/instance.json` when present, interviews content cadence, primary channels, distribution
  connectors, and persona preference (Content Strategist vs Content Writer vs merged),
  writes practice profile. Use on first install on first install, when the user says
  "set up content" or "configure editorial calendar", or to redo content defaults only.
argument-hint: "[--quick|--full] [--redo] [--resume] [--check-integrations]"
allowed-tools: Read, Grep, Glob, Write
disable-model-invocation: true
metadata:
  version: "0.1.0"
  owner: "content-marketing"
  review_cadence: "quarterly"
  work_shape: "orchestrate-delivery"
  permission_tier: artefact-writer
  output_class: "structured-data"
  sourcing_policy: "volatile-facts-must-be-sourced"
---

# /content-marketing:setup

## When to use

First content setup after instance bootstrap; standalone Try-tier setup; re-run after
cadence or channel mix changes. Explicit invocation only.

## What this skill does not do

- **Does not re-interview business identity** when `config/instance.json` is complete — references instance profile for business name and house tone hints.
- **Writes `config/instance.json` if absent** — idempotent instance bootstrap, then this practice interview.
- **Does not install other plugins** — user installs `product-management` from marketplace when companion backlog or research skills are needed.
- **Does not write without explicit yes** after showing the plain-language summary.
- **Does not produce calendar or seed artefacts** — those are separate skills after setup.
- **Does not write brand-voice.md** — owned by `brand-creative`; content reads it via artifact consumption.

## Preconditions

Read before proceeding:

- `${CLAUDE_PLUGIN_ROOT}/references/content-conventions.md`

Honour flags: `--quick`, `--full`, `--redo`, `--resume`, `--check-integrations`.

## Provisional mode

Partial interview → write resume JSON (see Pause and resume). Offer `--resume` on next run.

## Trust spine

Structured-aggregation; integration table reports ✓ only on successful MCP probe. Practice profile is user-local config — show full summary before write.

## Workflow

### Step 0 — Detect existing state

1. **Read** `config/instance.json` if present — note `status`, business identity, house tone hints, seed material.
2. **Resolve brand path** per `content-conventions.md` — check whether `brand-voice.md` exists (informational only; do not create it here).
3. **Read** `~/.claude/plugins/config/digital-agency/content-marketing/CLAUDE.md` unless `--redo`.
4. If **complete** and not `--redo`: summarize on-file content defaults; offer refresh, `--redo`, or `--check-integrations`. Stop unless user chooses refresh.
5. If **paused resume file** exists: greet, summarize progress, continue or start over.

### Step 0a — Instance bootstrap

If `config/instance.json` is **absent**:

1. Interview minimal org facts: business name / prose name, single-business vs agency-serving-clients, primary practice, planning cadence, risk posture.
2. Show a plain-language summary of `config/instance.json` (and an optional target skeleton). **Wait for yes.**
3. Write `config/instance.json` with `status: complete`, `setup.completedAt` (ISO 8601), and `setup.mode`. Include `instance` slug, `business`, `services.enabled`, `cadence`, `riskPosture`, `governance` (`agentsNeverPushMain: true`), and `seedMaterial` as captured. Do not create GitHub repos autonomously.
4. Continue into the plugin-specific interview.

If present and complete, reference it — do not re-ask business identity.

### Step 0b — Install scope check

If working directory looks project-scoped and content context may span repos, warn once that a project-scoped install cannot read files outside the project folder. Wait for confirmation.

### Step 1 — Mode and preamble

If neither `--quick` nor `--full` was passed, offer quick vs full.

**Quick path:** primary channels default (web + social), calendar rhythm default, persona default (merged for solo).

**Full path:** all plugin-specific questions below.

Tell user: "Say **pause** anytime — I'll save progress for `--resume`."

### Step 2 — Integrations (`--check-integrations`)

Before interview (or as sole action when flag set):

> Content workflows can use source control, CMS, social scheduling, knowledge bases, and chat when connected. Let me check what's available.

For each server in `${CLAUDE_PLUGIN_ROOT}/.mcp.json`:

- Probe if possible → ✓ connected
- Configured but not probeable → ⚪ configured but not verified
- Missing → ✗ not found + manual fallback

Note CMS and social scheduling categories even when not bundled — report manual fallback.

If `--check-integrations` only, stop here unless user asks to continue setup.

### Step 3 — Interview (skip answered instance facts)

**2–3 prompts per turn.** Do not re-ask business name or house tone if `config/instance.json` has them — say "see instance profile".

#### 3a — Primary channels (full mode; abbreviated in quick)

Which channels does this practice actually produce for?

- Web copy (blog, landing pages, CMS seeds)
- Social (captions, curation, inventory)
- Email (excerpts, newsletters)

Record which artefact types are in scope.

#### 3b — Content cadence

Calendar rhythm (weekly, fortnightly, monthly, ad hoc) and primary content types (blog, recipes, social, mixed).

#### 3c — Seed material

Existing published content, prior calendars, style examples. Read if accessible; summarize findings — do not copy proprietary content verbatim. Quick mode: one seed source minimum if none in instance profile.

#### 3d — Persona preference (real branch — not cosmetic)

Does the customer want **Content Strategist** and **Content Writer** as genuinely distinct personas, or merged into one working style?

- **One-person shop** → default merged; greet as single content partner.
- **Larger team** → default distinct; Strategist for planning skills, Writer for draft skills.

Record which persona greets the user by default.

#### 3e — Companion practice

If backlog alignment or research synthesis is needed, recommend installing `product-management` and invoking `/product-management:tasks --product` and `/product-management:synthesize-research` — do not bundle those skills here.

### Step 4 — Summarize before write

List every file to create/update:

- `~/.claude/plugins/config/digital-agency/content-marketing/CLAUDE.md` — practice profile with channels, cadence, persona preference, integration table, seed material notes

List deliberate skips. Ask: **"Write these files? (yes/no)"** — wait.

### Step 5 — Write practice profile (on yes)

Write `~/.claude/plugins/config/digital-agency/content-marketing/CLAUDE.md` from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` template with interview answers filled. Set `Status: complete`.

Delete resume file if present.

### Step 6 — Next steps

Close with persona-appropriate handoff:

**Content Strategist path:**

1. **Calendar** — `/content-marketing:content-calendar write`
2. **Inventory** — `/content-marketing:curate-content`
3. **Backlog** — `/product-management:tasks --product` (companion; requires product-management install)

**Content Writer path:**

1. **Draft post** — `/content-marketing:draft-post <slug>`
2. **Draft recipe** — `/content-marketing:draft-recipe <slug>`
3. **Captions** — `/content-marketing:write-captions`

**Either:**

4. **Media analysis** — `/content-marketing:analyse-media <path>`
5. **Refresh** — `/content-marketing:setup --redo` to redo content defaults only.

## Pause and resume

On pause, write JSON:

```json
{
  "plugin": "content-marketing",
  "skill": "setup",
  "mode": "quick|full",
  "startedAt": "ISO-8601",
  "instanceRoot": "<path or null>",
  "answers": {},
  "remainingSteps": [],
  "lastStepCompleted": ""
}
```

Location: `<instance-root>/config/.content-marketing-setup-resume.json` if instance exists; else `~/.claude/plugins/config/digital-agency/content-marketing/setup-resume.json`.

## Worked example

**Input:** Instance profile complete; `--quick`; solo operator; merged persona; web + social channels; monthly calendar.

**Expected output:** Practice profile at personal config path with channels, cadence, and merged persona recorded; handoff to `/content-marketing:content-calendar write`.

## Outputs

| Artefact | Path |
| -------- | ---- |
| Practice profile | `~/.claude/plugins/config/digital-agency/content-marketing/CLAUDE.md` |

Next: invoke Content Strategist or Content Writer skills per persona preference, install `product-management` for companion skills, or `--check-integrations`.
