---
name: setup
description: >
  Architecture practice setup interview — reads instance business identity from
  instance bootstrap (this setup writes `config/instance.json` if absent),
  interviews target binding and architecture scope defaults, writes practice
  profile. Use on first install, when the user says "set up architecture" or
  "configure solution/ADRs", or to redo architecture defaults only.
argument-hint: "[--quick|--full] [--redo] [--resume] [--check-integrations]"
allowed-tools: Read, Grep, Glob, Write
disable-model-invocation: true
metadata:
  version: "0.1.0"
  owner: "architecture"
  review_cadence: "quarterly"
  work_shape: "orchestrate-delivery"
  permission_tier: artefact-writer
  output_class: "structured-data"
  sourcing_policy: "volatile-facts-must-be-sourced"
---

# /architecture:setup

## When to use

First architecture setup after instance bootstrap; standalone Try-tier setup;
re-run after scope or binding changes. Explicit invocation only.

## What this skill does not do

- **Does not re-interview business identity** when `config/instance.json` is complete — references instance profile.
- **Writes `config/instance.json` if absent** — idempotent instance bootstrap, then this practice interview.
- **Does not install other plugins** — user installs `engineering` / `product-management` from marketplace when companions are needed.
- **Does not write without explicit yes** after showing the plain-language summary.
- **Does not produce solution.md or ADRs** — those are separate skill invocations after setup.

## Preconditions

Read before proceeding:

- `${CLAUDE_PLUGIN_ROOT}/references/practice-setup-framework.md`
- `${CLAUDE_PLUGIN_ROOT}/references/architecture-conventions.md`
- `${CLAUDE_PLUGIN_ROOT}/references/instance-profile-template.md` (when instance profile may exist)

Honour flags: `--quick`, `--full`, `--redo`, `--resume`, `--check-integrations`.

## Provisional mode

Partial interview → write resume JSON per framework. Offer `--resume` on next run.

## Trust spine

Structured-aggregation; integration table reports ✓ only on successful MCP probe. Practice profile is user-local config — show full summary before write.

## Workflow

### Step 0 — Detect existing state

1. **Read** `config/instance.json` if present — note `status`, business identity, seed material.
2. **Resolve target** per `architecture-conventions.md` — note whether `docs/architecture/` already exists.
3. **Read** `~/.claude/plugins/config/digital-agency/architecture/CLAUDE.md` unless `--redo`.
4. If **complete** and not `--redo`: summarize on-file architecture defaults; offer refresh, `--redo`, or `--check-integrations`. Stop unless user chooses refresh.
5. If **paused resume file** exists: greet, summarize progress, continue or start over.

### Step 0a — Instance bootstrap

If `config/instance.json` is **absent**, follow `${CLAUDE_PLUGIN_ROOT}/references/practice-setup-framework.md` → **Instance bootstrap**: interview minimal org facts, show the summary, write `config/instance.json` on yes, then continue.

If present and complete, reference it — do not re-ask business identity.

### Step 0b — Install scope check

If working directory looks project-scoped and architecture may span repos, warn once per framework. Wait for confirmation.

### Step 1 — Mode and preamble

If neither `--quick` nor `--full` was passed, offer quick vs full.

**Quick path:** infer target binding when possible; default solution stage `stub` if no solution.md exists else `full`; note companion install for `engineering`.

**Full path:** all plugin-specific questions below.

Tell user: "Say **pause** anytime — I'll save progress for `--resume`."

### Step 2 — Integrations (`--check-integrations`)

Before interview (or as sole action when flag set):

> ADR harvest can use source control / trackers when connected. Let me check what's available.

For each server in `${CLAUDE_PLUGIN_ROOT}/.mcp.json`:

- Probe if possible → ✓ connected
- Configured but not probeable → ⚪ configured but not verified
- Missing → ✗ not found + manual fallback

If `--check-integrations` only, stop here unless user asks to continue setup.

### Step 3 — Interview (skip answered instance facts)

Ask only what is still needed:

1. **Target binding** — confirm target repo / standalone; create `config/target.json` when confirmed.
2. **Architecture scope** — systems in scope; default solution stage (`stub` vs `full`).
3. **ADR habit** — when to harvest (after epic / sprint end / ad hoc).
4. **Companions** — whether `engineering` and `product-management` are installed or should be recommended (do not install them).

### Step 3a — Target binding confirmation

When the user confirms target association, write `config/target.json` with `name`, `instance`, and `target` per framework.

### Step 4 — Summary and write

Show a plain-language summary of the practice profile. On explicit yes, write
`~/.claude/plugins/config/digital-agency/architecture/CLAUDE.md` from
`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` with answers filled. Set `Status: complete`.

Delete resume file if present.

### Step 5 — Next steps

1. **Solution** — `/architecture:solution` (use `--stage stub` or `full`)
2. **ADR** — `/architecture:adr plan` then `/architecture:adr write`
3. **Work-item design** — `/engineering:design <work-id>` (companion)
4. **Docs review** — `/engineering:docs-review docs/architecture/` (companion)
5. **Refresh** — `/architecture:setup --redo`

## Pause and resume

On pause, write JSON:

```json
{
  "plugin": "architecture",
  "skill": "setup",
  "mode": "quick|full",
  "startedAt": "ISO-8601",
  "instanceRoot": "<path or null>",
  "answers": {},
  "remainingSteps": [],
  "lastStepCompleted": ""
}
```

Location: `<instance-root>/config/.architecture-setup-resume.json` if instance exists; else personal hub path per framework.

## Outputs

| Artefact | Path |
| -------- | ---- |
| Practice profile | `~/.claude/plugins/config/digital-agency/architecture/CLAUDE.md` |
| Target binding (when confirmed) | `config/target.json` at target repo root |

Next: invoke `/architecture:solution` or `/architecture:adr`, or install companions for design / delivery.
