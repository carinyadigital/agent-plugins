---
name: setup
description: >
  Brand practice setup interview — detects instance profile and existing brand
  artefacts, interviews enforcement strictness and discovery platforms, runs
  brand-voice discover → write → review and brand-guide write, saves to the
  resolved brand path. Use on first install on first install, when the user
  says "set up brand" or "configure brand voice", or to redo brand only.
argument-hint: "[--quick|--full] [--redo] [--resume] [--check-integrations]"
allowed-tools: Read, Grep, Glob, Write
disable-model-invocation: true
metadata:
  version: "0.1.0"
  owner: "brand-creative"
  review_cadence: "quarterly"
  work_shape: "orchestrate-delivery"
  permission_tier: artefact-writer
  output_class: "structured-data"
  sourcing_policy: "volatile-facts-must-be-sourced"
---

# /brand-creative:setup

## When to use

First brand setup after instance bootstrap; standalone Try-tier brand setup; re-run after material brand change. Explicit invocation only.

## What this skill does not do

- **Does not re-interview business identity** when `config/instance.json` is complete — references instance profile.
- **Writes `config/instance.json` if absent** — idempotent instance bootstrap, then this practice interview.
- **Does not install other plugins** — user installs from marketplace.
- **Does not write without explicit yes** after showing the plain-language diff.
- **Does not use `docs/brand/`** when an instance or target pointer exists — resolves per `brand-conventions.md`.

## Preconditions

Read before proceeding:

- `${CLAUDE_PLUGIN_ROOT}/references/brand-conventions.md`

Honour flags: `--quick`, `--full`, `--redo`, `--resume`, `--check-integrations`.

## Provisional mode

Partial interview → write resume JSON (see Pause and resume). Offer `--resume` on next run.

## Trust spine

Structured-aggregation; integration table reports ✓ only on successful MCP probe. Brand artefacts are team-shared git files when in an instance — show full diff before write.

## Workflow

### Step 0 — Detect existing state

1. **Resolve brand directory** per `brand-conventions.md` (explicit path → instance `brand/` → target pointer → `docs/brand/`).
2. **Read** `config/instance.json` if present — note `status`, `business`, `seedMaterial`.
3. **Read** `~/.claude/plugins/config/digital-agency/brand-creative/CLAUDE.md` unless `--redo`.
4. **Inspect brand artefacts** at resolved path — `brand-voice.md`, `brand-guide.md`, `brand.local.md`.
5. If **complete** and not `--redo`: summarize on-file brand; offer refresh, `--redo`, or `--check-integrations`. Stop unless user chooses refresh.
6. If **paused resume file** exists: greet, summarize progress, continue or start over.

### Step 0a — Instance bootstrap

If `config/instance.json` is **absent**:

1. Interview minimal org facts: business name / prose name, single-business vs agency-serving-clients, primary practice, planning cadence, risk posture.
2. Show a plain-language summary of `config/instance.json` (and an optional target skeleton). **Wait for yes.**
3. Write `config/instance.json` with `status: complete`, `setup.completedAt` (ISO 8601), and `setup.mode`. Include `instance` slug, `business`, `services.enabled`, `cadence`, `riskPosture`, `governance` (`agentsNeverPushMain: true`), and `seedMaterial` as captured. Do not create GitHub repos autonomously.
4. Continue into the plugin-specific interview.

If present and complete, reference it — do not re-ask business identity.

### Step 0b — Install scope check

If working directory looks project-scoped and seed material may be outside the folder, warn once that a project-scoped install cannot read files outside the project folder. Wait for confirmation.

### Step 1 — Mode and preamble

If neither `--quick` nor `--full` was passed, offer quick vs full.

**Quick path:** enforcement strictness default, one seed doc, skip discovery unless user asks.

**Full path:** all plugin-specific questions below plus seed material review.

Tell user: "Say **pause** anytime — I'll save progress for `--resume`."

### Step 2 — Integrations (`--check-integrations`)

Before interview (or as sole action when flag set):

> Brand discovery can search Notion, Confluence, Slack, Figma, and Fireflies when connected. Let me check what's available.

For each server in `${CLAUDE_PLUGIN_ROOT}/.mcp.json`:

- Probe if possible → ✓ connected
- Configured but not probeable → ⚪ configured but not verified
- Missing → ✗ not found + manual fallback

If `--check-integrations` only, stop here unless user asks to continue setup.

### Step 3 — Interview (skip answered instance facts)

**2–3 prompts per turn.** Do not re-ask business name or house tone if `config/instance.json` has them — say "see instance profile".

#### 3a — Discovery platforms (full mode; skip in quick unless user opts in)

Which connected platforms to search during discover? Default: all connected platforms from Step 2.

#### 3b — Enforcement defaults

- **Strictness:** `strict` | `balanced` | `flexible` (default `balanced`)
- **Always explain:** when enforcing voice, explain rewrites? (default `true`)

#### 3c — Primary channels

Which channels should tone flex across? (web copy, social, email, ads, support — informs tone-flex guidance in voice doc, not separate artefacts)

#### 3d — Seed material

Ask for existing site copy, past posts, prior brand docs, Figma file links. Read if accessible; summarize findings — do not copy proprietary content verbatim. Quick mode: one seed source minimum if none in instance profile.

### Step 4 — Summarize before write

List every file to create/update:

- `<brand-dir>/brand-voice.md`
- `<brand-dir>/brand-guide.md` (when visual sources exist)
- `<brand-dir>/brand.local.md` — platforms, strictness, `always_explain`, `known_materials`
- `<brand-dir>/discovery-report.md` (if discover ran)
- `~/.claude/plugins/config/digital-agency/brand-creative/CLAUDE.md` — practice profile

List deliberate skips. Ask: **"Write these files? (yes/no)"** — wait.

### Step 5 — Delivery chain (on yes)

Orchestrate in this conversation using bundled skills:

1. **`/brand-creative:brand-voice discover`** — skip when `--quick` and no platforms connected unless user requested discovery.
2. **`/brand-creative:brand-voice write`** — use discovery report, seed material, and instance profile context.
3. **`/brand-creative:brand-guide write`** — parallel when Figma connected or visual seed exists; otherwise note deferred with placeholder section.
4. **`/brand-creative:brand-voice review`** — surface open questions with agent recommendations.

Use resolved paths from Step 0 for all reads and writes.

### Step 6 — Write practice profile

On successful chain, write `~/.claude/plugins/config/digital-agency/brand-creative/CLAUDE.md` from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` template with interview answers filled. Set `Status: complete`.

Delete resume file if present.

### Step 7 — Next steps

Close with:

1. **Enforce voice** — `/brand-creative:brand-voice enforce` for on-brand copy.
2. **Refine** — `/brand-creative:brand-voice refine` after team resolves open questions.
3. **Visual updates** — `/brand-creative:brand-guide write --from figma` when design source changes.
4. **Refresh** — `/brand-creative:setup --redo` to redo brand only.

## Pause and resume

On pause, write JSON:

```json
{
  "plugin": "brand-creative",
  "skill": "setup",
  "mode": "quick|full",
  "startedAt": "ISO-8601",
  "instanceRoot": "<path or null>",
  "brandDir": "<resolved path>",
  "answers": {},
  "remainingSteps": [],
  "lastStepCompleted": ""
}
```

Location: `<instance-root>/config/.brand-creative-setup-resume.json` if instance exists; else `~/.claude/plugins/config/digital-agency/brand-creative/setup-resume.json`.

## Worked example

**Input:** Instance profile complete; `--quick`; strictness `balanced`; one seed URL; no platforms connected.

**Expected output:** `brand/brand-voice.md` and `brand/brand.local.md` at instance root; practice profile at personal config path; handoff to enforce/refine commands.

## Outputs

| Artefact | Path |
|---|---|
| Brand voice | `<brand-dir>/brand-voice.md` |
| Brand guide | `<brand-dir>/brand-guide.md` |
| Settings | `<brand-dir>/brand.local.md` |
| Discovery report | `<brand-dir>/discovery-report.md` (optional) |
| Practice profile | `~/.claude/plugins/config/digital-agency/brand-creative/CLAUDE.md` |

Next: `/brand-creative:brand-voice enforce`, install content plugins, or `--check-integrations`.
