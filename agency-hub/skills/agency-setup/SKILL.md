---
name: agency-setup
description: >
  Instance bootstrap interview — detects existing instance state, guides repo
  creation (link-first), interviews business identity/services/cadence/targets,
  writes config/instance.json and target skeletons, then hands off to
  brand-creative practice-setup. Use on first install, when the user says "set up
  my instance" or "bootstrap my agency workspace", or to re-run integration checks
  after adding MCP connectors.
argument-hint: "[--quick|--full] [--redo] [--resume] [--check-integrations]"
allowed-tools: Read, Grep, Glob, Write
disable-model-invocation: true
metadata:
  version: "0.1.0"
  owner: "agency-hub"
  review_cadence: "quarterly"
  work_shape: "orchestrate-delivery"
  permission_tier: artefact-writer
  output_class: "structured-data"
  sourcing_policy: "volatile-facts-must-be-sourced"
---

# /agency-hub:agency-setup

## When to use

First install of digital-agency for real work; cold-start instance bootstrap; re-check integrations after connector changes. Explicit invocation only.

## What this skill does not do

- **Does not create GitHub repos autonomously** — v1 is link-first; the human creates the repo.
- **Does not install practice plugins** — recommends them; user installs from marketplace.
- **Does not duplicate brand interview** — recommends `brand-creative` and hands off to `/brand-creative:practice-setup`.
- **Does not block on email/ads/analytics targets** — writes `not-yet-designed` skeletons and continues.
- **Does not write without explicit yes** after showing the plain-language diff.

## Preconditions

Read `${CLAUDE_PLUGIN_ROOT}/references/agency-setup-framework.md` and `${CLAUDE_PLUGIN_ROOT}/references/instance-profile-template.md` before proceeding.

Detect existing state per framework § Startup. Honour flags: `--quick`, `--full`, `--redo`, `--resume`, `--check-integrations`.

## Provisional mode

Partial interview → write resume JSON (`config/.agency-setup-resume.json` in instance repo, or `~/.claude/plugins/config/digital-agency/agency-hub/agency-setup-resume.json` before repo exists). Offer `--resume` on next run.

## Trust spine

Structured-aggregation; integration table reports ✓ only on successful MCP probe. Instance config is team-shared git artefacts — show full diff before write. Target pointer files in external repos require separate confirmation per repo.

## Workflow

### Step 0 — Detect existing state

1. Look for `config/instance.json` in the working directory.
2. If **`status: complete`** and not `--redo`: summarize on-file config; offer refresh, `--redo`, or `--check-integrations`. Stop unless user chooses refresh.
3. If **paused resume file** exists: greet, summarize progress, continue or start over.
4. If **no instance repo**: proceed to repo creation (Step 1).

### Step 0b — Install scope check

If the working directory looks project-scoped (not user home, limited to one repo that is not an instance repo), say once:

> **Heads up — project-scoped install limits file reads to this folder.** Seed material in Downloads, Documents, or sibling repos may be unreadable. Continue here, move files in, or reinstall user-scoped.

Wait for confirmation before proceeding.

### Step 1 — Repo creation (link-first, when needed)

When not already inside an instance repo:

1. Explain the instance model (private git repo: `config/`, `brand/`, `squads/`).
2. Offer template URL when published:
   `https://github.com/<your-org>/digital-agency-instance/generate`
3. If template unavailable, list minimum skeleton directories (see framework).
4. **Wait** for user to confirm repo exists and provide local path.
5. Verify path is readable; treat it as the instance root for all writes.

**Do not** call GitHub API to create repos in v1.

### Step 2 — Mode and preamble

If neither `--quick` nor `--full` was passed, show preamble (framework § Preamble) and ask quick or full.

**Quick path:** business name + prose name, one primary practice, one target, defaults elsewhere (`[DEFAULT]` in JSON where applicable).

**Full path:** all interview sections below.

Tell user: "Say **pause** anytime — I'll save progress for `--resume`."

### Step 3 — Integrations (Part 0)

Before business questions (skip if `--check-integrations` only):

> This setup can use GitHub to validate target repos and read seed material. Let me check what's connected.

For each server in `${CLAUDE_PLUGIN_ROOT}/.mcp.json`:

- Probe if possible → ✓ connected
- Configured but not probeable → ⚪ configured but not verified
- Missing → ✗ not found + manual fallback

Write findings. Also scan bound target repos for legacy business-named pointer files (non-`.digital-agency/target.json`); if found, propose rename to `.digital-agency/target.json` per framework § Target pointers.

If `--check-integrations` only, stop here unless user asks to continue setup.

### Step 4 — Interview

Follow framework sections. **2–3 prompts per turn.** Wait for typed answers when needed.

#### 4a — Business identity

- Name and prose name
- `single-business` vs `agency-serving-clients`
- Industry / geography (brief)
- **Catalogue source** — where this team installs the digital-agency marketplace (GitHub `org/repo` slug or equivalent); written to `config/plugins.json` → `catalogue`

#### 4b — Services wanted

Map to **practice plugins** (MECE — one install per practice). Recommend; do not install autonomously. See `instance-profile-template.md` service table for full mapping.

| Practice area | Practice plugin | `core` companion | Notes |
|---|---|---|---|
| `brand-creative` | `brand-creative` | none | Shipped — no companion install |
| `web-development` | `web-development` | `core` | Practice plugin pending — interim catalogue: `engineering`, `frontend-engineer`, `qa-engineer`, `webops-engineer`, `principal-architect` |
| `content-marketing` | `content-marketing` | `core` | Practice plugin pending — interim: `content`, `content-strategist`, `content-writer` |
| `social-media` | `social-media` | TBD | Practice plugin pending — interim: `content`, `content-strategist`, `content-writer` |
| `seo` | `seo` | TBD | Practice plugin pending — interim: `seo`, `seo-specialist` |

When recommending `core`, name the roles the practice needs (e.g. `web-development` → `/core:product-manager`, `/core:delivery-lead`). `brand-creative` never needs `core`.

Quick: one primary. Full: now vs later for each.

#### 4c — Cadence and risk posture

- Planning rhythm
- Approval-gate strictness: relaxed / standard / strict
- Escalation — PR merge, content publish, social publish approvers
- Risk posture: conservative / balanced / aggressive + hard constraints

Populate `governance` fields: agents never push main; artefacts are drafts until human gate.

#### 4d — Seed material (full mode)

Ask for site URL, brand docs path, sample content. Read if accessible; summarize findings in `seedMaterial`; do not copy proprietary content verbatim.

#### 4e — Targets

For each channel discussed:

| Target | Action |
|---|---|
| website | Skeleton in `config/targets/website.json`; if repo path known, **propose** `.digital-agency/target.json` content separately |
| social | Skeleton; `enabled: false` until social publishing connector credentials |
| email, ads, analytics | Skeleton with `status: not-yet-designed` — note "coming soon", continue |

Quick mode: one target skeleton minimum.

### Step 5 — Summarize before write

List every file to create/update in plain language:

- `config/instance.json` — key fields
- `config/plugins.json`
- `config/targets/*.json`
- `config/deployments/*.json` (all `enabled: false`)
- `squads/*/charter.md` skeletons
- Any `.digital-agency/target.json` in external repos (separate confirmation)

List deliberate skips/placeholders. Ask: **"Write these files? (yes/no)"** — wait.

### Step 6 — Write Tier 1 and Tier 2

On **yes**:

1. Write files per `instance-profile-template.md`.
2. Set `status: complete`, `setup.completedAt` (ISO 8601), `setup.mode` (`quick`/`full`).
3. Include `agency-hub` in `config/plugins.json` plus recommended practice plugins; set `catalogue` from the user's catalogue source answer (not a hard-coded publisher).
4. Deployment scaffolds example (adjust to services):

```json
{
  "agent": "product-manager",
  "ritual": "weekly-planning",
  "squad": "site",
  "enabled": false,
  "platform": null,
  "schedule": null,
  "repos": []
}
```

5. Delete resume file if present.
6. For website pointer binding: write `.digital-agency/target.json` only after separate yes for that repo.
7. **Initialize Tier 0 hub state** — if `~/.claude/plugins/config/digital-agency/agency-hub/` is missing or empty, create `CLAUDE.md` (from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` template), `allowlist.yaml` (from `references/allowlist-default.yaml`), and `install-log.yaml` (`[]`). Populate hub profile fields from interview answers where available.

### Step 7 — Hand off to brand-creative

Do not run the brand interview here — plugins are self-contained and `agency-hub` cannot invoke another plugin's skill directly. User-mediated hand-off within the same conversation:

> **Brand setup next.** If `brand-creative` is not installed, install it from the marketplace. Then run `/brand-creative:practice-setup` in this conversation — it reads seed material from instance setup and writes to `<instance-root>/brand/`.

If deferred, set `seedMaterial.notes` accordingly.

### Step 8 — Next steps

Close with a concrete path — not a pile of config files:

1. **Install** the first recommended **practice plugin** from the marketplace.
2. **`core` companion** — if that practice needs shared roles it does not own (e.g. `web-development` → install `core`, then use `/core:product-manager` and `/core:delivery-lead`; `brand-creative` needs no companion).
3. **Practice setup** — run that practice's `practice-setup` skill (e.g. `/brand-creative:practice-setup` for brand).
4. **Bind targets** — complete website `.digital-agency/target.json` pointer, social credentials when available.
5. **Deploy** — launch the first scheduled agent (dry-run first):
   `./digital-agency/scripts/deploy-squad-agents.sh --dry-run --instance <path>`
6. **Edit anytime** — change `config/instance.json` directly or `/agency-hub:agency-setup --redo`.

## Pause and resume

On pause, write JSON:

```json
{
  "plugin": "agency-hub",
  "skill": "agency-setup",
  "mode": "quick|full",
  "startedAt": "ISO-8601",
  "instanceRoot": "<path or null>",
  "answers": {},
  "remainingSteps": [],
  "lastStepCompleted": ""
}
```

Location: instance repo `config/.agency-setup-resume.json` if instance exists; else personal hub path above.

## Worked example

**Input:** Acme Co, single business, web-development + content, website target, quick mode.

**Expected output:** `config/instance.json` complete; `targets/website.json` skeleton; `plugins.json` lists `agency-hub` + recommended practice plugins; squad charters for site/content; handoff to `/brand-creative:practice-setup` and next-steps naming `core` if web-development was chosen.

## Outputs

| Artefact | Path |
|---|---|
| Instance profile | `config/instance.json` |
| Plugin manifest | `config/plugins.json` |
| Target skeletons | `config/targets/<name>.json` |
| Deployment scaffolds | `config/deployments/*.json` |
| Squad charters | `squads/<squad>/charter.md` |
| Target pointer (on confirm) | `<target-repo>/.digital-agency/target.json` |

Next: `/brand-creative:practice-setup`, install first practice plugin, or `--check-integrations`.
