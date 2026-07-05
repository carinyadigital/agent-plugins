---
name: practice-setup
description: >
  Web development practice setup interview — detects or creates .digital-agency/target.json
  binding, reads instance profile from agency-setup, interviews tech stack, deployment
  platform, connectors, and persona preference (six engineering personas vs merged),
  writes practice profile. Use on first install after agency-setup, when the user says
  "set up web development" or "bind target repo", or to redo engineering defaults only.
argument-hint: "[--quick|--full] [--redo] [--resume] [--check-integrations]"
allowed-tools: Read, Grep, Glob, Write
disable-model-invocation: true
metadata:
  version: "0.1.0"
  owner: "web-development"
  review_cadence: "quarterly"
  work_shape: "orchestrate-delivery"
  permission_tier: artefact-writer
  output_class: "structured-data"
  sourcing_policy: "volatile-facts-must-be-sourced"
---

# /web-development:practice-setup

## When to use

First web development setup after instance bootstrap; standalone Try-tier setup; re-run
after stack or deployment platform changes. Explicit invocation only.

## What this skill does not do

- **Does not re-interview business identity** when `config/instance.json` is complete — references instance profile for target hints.
- **Does not write `config/instance.json`** — owned by `agency-hub:agency-setup`.
- **Does not install other plugins** — user installs `delivery-practice` from marketplace when planning companion skills are needed.
- **Does not write without explicit yes** after showing the plain-language summary.
- **Does not produce solution, design, or code artefacts** — those are separate skills after setup.
- **Does not write brand-guide.md** — owned by `brand-creative`; engineering reads it via artifact consumption.

## Preconditions

Read before proceeding:

- `${CLAUDE_PLUGIN_ROOT}/references/practice-setup-framework.md`
- `${CLAUDE_PLUGIN_ROOT}/references/web-development-conventions.md`
- `${CLAUDE_PLUGIN_ROOT}/references/instance-profile-template.md` (when instance profile may exist)

Honour flags: `--quick`, `--full`, `--redo`, `--resume`, `--check-integrations`.

## Provisional mode

Partial interview → write resume JSON per framework. Offer `--resume` on next run.

## Trust spine

Structured-aggregation; integration table reports ✓ only on successful MCP probe. Practice profile is user-local config — show full summary before write.

## Workflow

### Step 0 — Detect existing state

1. **Read** `.digital-agency/target.json` at working root if present — note target slug, instance pointer, binding status.
2. **Read** `config/instance.json` if present — note `status`, target definitions under `config/targets/`, squad structure.
3. **Resolve brand path** per `web-development-conventions.md` — check whether `brand-guide.md` exists (informational only; do not create it here).
4. **Inspect target repo** when bound — read `package.json`, `AGENTS.md` / `CLAUDE.md`, CI config for stack hints.
5. **Read** `~/.claude/plugins/config/digital-agency/web-development/CLAUDE.md` unless `--redo`.
6. If **complete** and not `--redo`: summarize on-file engineering defaults; offer refresh, `--redo`, or `--check-integrations`. Stop unless user chooses refresh.
7. If **paused resume file** exists: greet, summarize progress, continue or start over.

### Step 0b — Install scope check

If working directory looks project-scoped and engineering context may span repos, warn once per framework. Wait for confirmation.

### Step 1 — Mode and preamble

If neither `--quick` nor `--full` was passed, offer quick vs full.

**Quick path:** detect stack from repo files, deployment platform default, persona default (merged for solo).

**Full path:** all plugin-specific questions below.

Tell user: "Say **pause** anytime — I'll save progress for `--resume`."

### Step 2 — Integrations (`--check-integrations`)

Before interview (or as sole action when flag set):

> Engineering workflows can use source control, hosting, observability, chat, and project trackers when connected. Let me check what's available.

For each server in `${CLAUDE_PLUGIN_ROOT}/.mcp.json`:

- Probe if possible → ✓ connected
- Configured but not probeable → ⚪ configured but not verified
- Missing → ✗ not found + manual fallback

Note Neon and other stack-specific MCP categories even when not bundled — report manual fallback.

If `--check-integrations` only, stop here unless user asks to continue setup.

### Step 3 — Interview (skip answered instance facts)

**2–3 prompts per turn.** Do not re-ask facts already in `config/instance.json` or detectable from the repo — say "see instance profile" or "detected from repo".

#### 3a — Target binding (full mode; abbreviated in quick)

If `.digital-agency/target.json` is missing and the user is in a target repo:

- Confirm this repo should be bound to an instance target.
- Resolve instance root (from user path or `config/targets/`).
- On confirmation, create `.digital-agency/target.json` with instance pointer and target slug.

If already bound, confirm binding is correct.

#### 3b — Tech stack (full mode; auto-detect in quick)

Framework, language, styling approach, CMS/backend, database, test runner. Prefer detection from repo files; ask only for gaps.

#### 3c — Deployment platform

Hosting provider, CI/CD pipeline, observability/error tracking when configured.

#### 3d — Persona preference (real branch — not cosmetic)

Does the customer want the six engineering personas as genuinely distinct surfaces, or merged into one working style?

- **One-person shop** → default merged; greet as single engineering partner.
- **Larger team** → default distinct; route to persona-appropriate skills.

Record which persona greets the user by default.

#### 3e — Companion practice

If backlog, task AC, sprint, or epic validation is needed during implementation, recommend installing `delivery-practice` and invoking `/delivery-practice:backlog`, `/delivery-practice:tasks`, `/delivery-practice:sprint`, and `/delivery-practice:validate` — do not bundle those skills here.

### Step 4 — Summarize before write

List every file to create/update:

- `~/.claude/plugins/config/digital-agency/web-development/CLAUDE.md` — practice profile with target binding, stack, deployment, persona preference, integration table
- `.digital-agency/target.json` — only when user confirmed first-time binding in Step 3a

List deliberate skips. Ask: **"Write these files? (yes/no)"** — wait.

### Step 5 — Write practice profile (on yes)

Write `~/.claude/plugins/config/digital-agency/web-development/CLAUDE.md` from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` template with interview answers filled. Set `Status: complete`.

Write `.digital-agency/target.json` when confirmed in Step 3a.

Delete resume file if present.

### Step 6 — Next steps

Close with persona-appropriate handoff:

**Frontend Engineer path:**

1. **Implement** — `/web-development:implement <task-id>`
2. **Review** — `/web-development:code-review <branch>`
3. **MR** — `/web-development:create-mr`

**Principal Architect path:**

1. **Solution** — `/web-development:solution write`
2. **Design** — `/web-development:design write <epic>`
3. **ADR** — `/web-development:adr write`

**QA Engineer path:**

1. **Deploy QA** — `/web-development:deploy-qa <branch>`
2. **Automated** — `/web-development:run-automated-suite`
3. **Exploratory** — `/web-development:exploratory-pass`

**Either:**

4. **Backlog** — `/delivery-practice:backlog` (companion; requires delivery-practice install)
5. **Refresh** — `/web-development:practice-setup --redo` to redo engineering defaults only.

## Pause and resume

On pause, write JSON:

```json
{
  "plugin": "web-development",
  "skill": "practice-setup",
  "mode": "quick|full",
  "startedAt": "ISO-8601",
  "instanceRoot": "<path or null>",
  "answers": {},
  "remainingSteps": [],
  "lastStepCompleted": ""
}
```

Location: `<instance-root>/config/.web-development-practice-setup-resume.json` if instance exists; else personal hub path per framework.

## Worked example

**Input:** Target repo with Next.js + TypeScript detected; `--quick`; solo operator; merged persona; Vercel hosting; `.digital-agency/target.json` created on confirmation.

**Expected output:** Practice profile at personal config path with stack, deployment, and merged persona recorded; target binding file written; handoff to `/web-development:implement` or `/web-development:solution write`.

## Outputs

| Artefact | Path |
| -------- | ---- |
| Practice profile | `~/.claude/plugins/config/digital-agency/web-development/CLAUDE.md` |
| Target binding (when confirmed) | `.digital-agency/target.json` at target repo root |

Next: invoke persona-appropriate skills, install `delivery-practice` for companion skills, or `--check-integrations`.
