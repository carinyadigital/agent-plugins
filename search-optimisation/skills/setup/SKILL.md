---
name: setup
description: >
  Search optimisation practice setup interview — reads instance business identity from
  instance bootstrap (this setup writes `config/instance.json` if absent), interviews target site(s), search visibility baseline, priority keyword
  themes, competitor set, and technical audit cadence, writes practice profile. Use on
  first install on first install, when the user says "set up SEO" or "configure search
  optimisation", or to redo SEO defaults only.
argument-hint: "[--quick|--full] [--redo] [--resume] [--check-integrations]"
allowed-tools: Read, Grep, Glob, Write
disable-model-invocation: true
metadata:
  version: "0.1.0"
  owner: "search-optimisation"
  review_cadence: "quarterly"
  work_shape: "orchestrate-delivery"
  permission_tier: artefact-writer
  output_class: "structured-data"
  sourcing_policy: "volatile-facts-must-be-sourced"
---

# /search-optimisation:setup

## When to use

First SEO setup after instance bootstrap; standalone Try-tier setup; re-run after target
site, keyword priorities, or audit cadence changes. Explicit invocation only.

## What this skill does not do

- **Does not re-interview business identity** when `config/instance.json` is complete — references instance profile for business name and context.
- **Writes `config/instance.json` if absent** — idempotent instance bootstrap, then this practice interview.
- **Does not install other plugins** — user installs `product-management` from marketplace when competitive brief companion skill is needed.
- **Does not write without explicit yes** after showing the plain-language summary.
- **Does not produce keyword research or audit artefacts** — those are separate skills after setup.

## Preconditions

Read before proceeding:

- `${CLAUDE_PLUGIN_ROOT}/references/search-optimisation-conventions.md`

Honour flags: `--quick`, `--full`, `--redo`, `--resume`, `--check-integrations`.

## Provisional mode

Partial interview → write resume JSON (see Pause and resume). Offer `--resume` on next run.

## Trust spine

Structured-aggregation; integration table reports ✓ only on successful MCP probe. Practice profile is user-local config — show full summary before write.

## Workflow

### Step 0 — Detect existing state

1. **Read** `config/instance.json` if present — note `status`, business identity, target definitions.
2. **Resolve target** per `search-optimisation-conventions.md` — note production URL if known.
3. **Read** `~/.claude/plugins/config/digital-agency/search-optimisation/CLAUDE.md` unless `--redo`.
4. If **complete** and not `--redo`: summarize on-file SEO defaults; offer refresh, `--redo`, or `--check-integrations`. Stop unless user chooses refresh.
5. If **paused resume file** exists: greet, summarize progress, continue or start over.

### Step 0a — Instance bootstrap

If `config/instance.json` is **absent**:

1. Interview minimal org facts: business name / prose name, single-business vs agency-serving-clients, primary practice, planning cadence, risk posture.
2. Show a plain-language summary of `config/instance.json` (and an optional target skeleton). **Wait for yes.**
3. Write `config/instance.json` with `status: complete`, `setup.completedAt` (ISO 8601), and `setup.mode`. Include `instance` slug, `business`, `services.enabled`, `cadence`, `riskPosture`, `governance` (`agentsNeverPushMain: true`), and `seedMaterial` as captured. Do not create GitHub repos autonomously.
4. Continue into the plugin-specific interview.

If present and complete, reference it — do not re-ask business identity.

### Step 0b — Install scope check

If working directory looks project-scoped and SEO context may span repos, warn once that a project-scoped install cannot read files outside the project folder. Wait for confirmation.

### Step 1 — Mode and preamble

If neither `--quick` nor `--full` was passed, offer quick vs full.

**Quick path:** primary target site from instance or user input; one-off audit cadence default.

**Full path:** all plugin-specific questions below.

Tell user: "Say **pause** anytime — I'll save progress for `--resume`."

### Step 2 — Integrations (`--check-integrations`)

Before interview (or as sole action when flag set):

> SEO workflows use source control for recommendations, browser automation for live site
> checks, and SEO intelligence (Ahrefs) for keyword and backlink data when connected.
> Let me check what's available.

For each server in `${CLAUDE_PLUGIN_ROOT}/.mcp.json`:

- Probe if possible → ✓ connected
- Configured but not probeable → ⚪ configured but not verified
- Missing → ✗ not found + manual fallback

Note Google Search Console and Semrush are not bundled — report as optional add-ons
when the user asks about live search data beyond Ahrefs.

If `--check-integrations` only, stop here unless user asks to continue setup.

### Step 3 — Interview (skip answered instance facts)

**2–3 prompts per turn.** Do not re-ask business name if `config/instance.json` has it — say "see instance profile".

#### 3a — Target site(s) (full mode; abbreviated in quick)

Production URL(s) and any staging URLs to include or exclude from audits. Read from
target config when present.

#### 3b — Search visibility baseline

Current indexed state, known ranking themes, or prior audit notes — optional.

#### 3c — Priority keyword themes

Topic clusters or keyword themes to prioritise in research — optional if unknown.

#### 3d — Competitor set

Domains or brands to watch — brief list only; full competitive analysis is
`/product-management:competitive-brief` (companion practice).

#### 3e — Technical audit cadence

One-off vs recurring (monthly, quarterly, ad hoc) and focus areas for recurring audits.

#### 3f — Companion practice

If competitive landscape analysis is needed, recommend installing `product-management` and
invoking `/product-management:competitive-brief` — do not bundle that skill here.

### Step 4 — Summarize before write

List every file to create/update:

- `~/.claude/plugins/config/digital-agency/search-optimisation/CLAUDE.md` — practice profile with target sites, baseline, keyword themes, competitor set, audit cadence, integration table

List deliberate skips. Ask: **"Write these files? (yes/no)"** — wait.

### Step 5 — Write practice profile (on yes)

Write `~/.claude/plugins/config/digital-agency/search-optimisation/CLAUDE.md` from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` template with interview answers filled. Set `Status: complete`.

Delete resume file if present.

### Step 6 — Next steps

Close with SEO Specialist handoff:

1. **Keyword research** — `/search-optimisation:keyword-research <topic-slug>`
2. **Technical audit** — `/search-optimisation:technical-seo-audit`
3. **Content review** — `/search-optimisation:content-seo-review <pr-url or seed path>`
4. **Competitive brief** — `/product-management:competitive-brief` (companion; requires product-management install)
5. **Refresh** — `/search-optimisation:setup --redo` to redo SEO defaults only.

## Pause and resume

On pause, write JSON:

```json
{
  "plugin": "search-optimisation",
  "skill": "setup",
  "mode": "quick|full",
  "startedAt": "ISO-8601",
  "instanceRoot": "<path or null>",
  "answers": {},
  "remainingSteps": [],
  "lastStepCompleted": ""
}
```

Location: `<instance-root>/config/.search-optimisation-setup-resume.json` if instance exists; else `~/.claude/plugins/config/digital-agency/search-optimisation/setup-resume.json`.

## Worked example

**Input:** Instance profile complete; `--quick`; one production URL; one-off audit cadence; two keyword themes noted.

**Expected output:** Practice profile at personal config path with target site and cadence recorded; handoff to `/search-optimisation:keyword-research`.

## Outputs

| Artefact | Path |
| -------- | ---- |
| Practice profile | `~/.claude/plugins/config/digital-agency/search-optimisation/CLAUDE.md` |

Next: invoke SEO skills, install `product-management` for companion skills, or `--check-integrations`.
