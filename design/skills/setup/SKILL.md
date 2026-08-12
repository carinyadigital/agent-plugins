---
name: setup
description: >
  UX design practice setup interview — reads instance business identity from
  instance bootstrap (this setup writes `config/instance.json` if absent), interviews which pages/flows are in scope for wireframing and any
  existing design references to seed from, writes practice profile. Use on first
  install on first install, when the user says "set up UX" or "configure
  wireframes", or to redo UX defaults only.
argument-hint: "[--quick|--full] [--redo] [--resume] [--check-integrations]"
allowed-tools: Read, Grep, Glob, Write
disable-model-invocation: true
metadata:
  version: "0.1.0"
  owner: "design"
  review_cadence: "quarterly"
  work_shape: "orchestrate-delivery"
  permission_tier: artefact-writer
  output_class: "structured-data"
  sourcing_policy: "volatile-facts-must-be-sourced"
---

# /design:setup

## When to use

First UX setup after instance bootstrap; standalone Try-tier setup; re-run after scope
or reference material changes. Explicit invocation only.

## What this skill does not do

- **Does not re-interview business identity** when `config/instance.json` is complete — references instance profile.
- **Writes `config/instance.json` if absent** — idempotent instance bootstrap, then this practice interview.
- **Does not install other plugins** — user installs `engineering` from marketplace when implementation companion is needed.
- **Does not write without explicit yes** after showing the plain-language summary.
- **Does not produce wireframe artefacts** — those are separate skill invocations after setup.
- **Does not write `brand-guide.md`** — owned by `brand-creative`; wireframe reads it via artifact consumption when present.

## Preconditions

Read before proceeding:

- `${CLAUDE_PLUGIN_ROOT}/references/practice-setup-framework.md`
- `${CLAUDE_PLUGIN_ROOT}/references/design-conventions.md`
- `${CLAUDE_PLUGIN_ROOT}/references/instance-profile-template.md` (when instance profile may exist)

Honour flags: `--quick`, `--full`, `--redo`, `--resume`, `--check-integrations`.

## Provisional mode

Partial interview → write resume JSON per framework. Offer `--resume` on next run.

## Trust spine

Structured-aggregation; integration table reports ✓ only on successful MCP probe. Practice profile is user-local config — show full summary before write.

## Workflow

### Step 0 — Detect existing state

1. **Read** `config/instance.json` if present — note `status`, business identity, seed material.
2. **Resolve design directory** per `design-conventions.md` — note whether any wireframes already exist.
3. **Read** `~/.claude/plugins/config/digital-agency/ux-design/CLAUDE.md` unless `--redo`.
4. If **complete** and not `--redo`: summarize on-file UX defaults; offer refresh, `--redo`, or `--check-integrations`. Stop unless user chooses refresh.
5. If **paused resume file** exists: greet, summarize progress, continue or start over.

### Step 0a — Instance bootstrap

If `config/instance.json` is **absent**, follow `${CLAUDE_PLUGIN_ROOT}/references/practice-setup-framework.md` → **Instance bootstrap**: interview minimal org facts, show the summary, write `config/instance.json` on yes, then continue.

If present and complete, reference it — do not re-ask business identity.

### Step 0b — Install scope check

If working directory looks project-scoped and design context may span repos, warn once per framework. Wait for confirmation.

### Step 1 — Mode and preamble

If neither `--quick` nor `--full` was passed, offer quick vs full.

**Quick path:** default in-scope pages (home + primary conversion flow if inferable from instance profile), one design reference if available.

**Full path:** all plugin-specific questions below.

Tell user: "Say **pause** anytime — I'll save progress for `--resume`."

### Step 2 — Integrations (`--check-integrations`)

Before interview (or as sole action when flag set):

> Wireframe workflows can read Figma when connected. Let me check what's available.

For each server in `${CLAUDE_PLUGIN_ROOT}/.mcp.json`:

- Probe if possible → ✓ connected
- Configured but not probeable → ⚪ configured but not verified
- Missing → ✗ not found + manual fallback

If `--check-integrations` only, stop here unless user asks to continue setup.

### Step 3 — Interview (skip answered instance facts)

**2–3 prompts per turn.** Do not re-ask business name if `config/instance.json` has it — say "see instance profile".

#### 3a — Pages and flows in scope

Which pages or user flows should wireframing cover right now? List concrete names
(e.g. `home-page`, `contact-form`, `checkout-flow`). Quick mode: infer a minimal
set from instance profile product context when user defers.

#### 3b — Design references

Existing Figma files, prior wireframes, competitor references, or screenshots to
seed from. Read if accessible via Figma MCP; summarize findings — do not copy
proprietary content verbatim. Quick mode: one reference source minimum if none in
instance profile.

#### 3c — Brand context (informational)

Check whether `<resolved-brand-path>/brand-guide.md` exists. If yes, note that
wireframe will read it. If no, note that wireframes will be structure-only until
brand guide exists — do not create brand artefacts here.

### Step 4 — Summarize before write

List every file to create/update:

- `~/.claude/plugins/config/digital-agency/ux-design/CLAUDE.md` — practice profile with scope and references filled

List deliberate skips. Ask: **"Write these files? (yes/no)"** — wait.

### Step 5 — Write practice profile (on yes)

Write `~/.claude/plugins/config/digital-agency/ux-design/CLAUDE.md` from
`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` template with interview answers filled. Set
`Status: complete`.

Delete resume file if present.

### Step 6 — Next steps

Close with:

1. **Wireframe a page** — `/design:wireframe {page-or-flow}` for each item in scope.
2. **Refresh scope** — `/design:setup --redo` when pages or references change.
3. **Implement** — install `engineering` and invoke `/engineering:implement` when wireframes are approved.

## Pause and resume

On pause, write JSON:

```json
{
  "plugin": "design",
  "skill": "setup",
  "mode": "quick|full",
  "startedAt": "ISO-8601",
  "instanceRoot": "<path or null>",
  "designDir": "<resolved path>",
  "answers": {},
  "remainingSteps": [],
  "lastStepCompleted": ""
}
```

Location: `<instance-root>/config/.design-setup-resume.json` if instance exists; else personal hub path per framework.

## Worked example

**Input:** Instance profile complete; `--quick`; scope `home-page`, `contact-form`; one Figma link; brand-guide absent.

**Expected output:** Practice profile at personal config path with scope and references; handoff to `/design:wireframe home-page`.

## Outputs

| Artefact | Path |
| -------- | ---- |
| Practice profile | `~/.claude/plugins/config/digital-agency/ux-design/CLAUDE.md` |

Next: `/design:wireframe` for each page or flow in scope.
