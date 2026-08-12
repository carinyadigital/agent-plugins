---
name: setup
description: >
  Instance bootstrap interview — detects existing instance state, guides repo
  creation (link-first), interviews business identity/services/cadence/targets,
  writes config/instance.json and target skeletons, then hands off to
  brand-creative setup. Use on first install, when the user says "set up
  my instance" or "bootstrap my agency workspace", or to re-check target bindings
  after config changes.
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

# /agency-hub:setup

## When to use

First install of digital-agency for real work; cold-start instance bootstrap; re-check target bindings after config changes. Explicit invocation only.

## What this skill does not do

- **Does not create GitHub repos autonomously** — v1 is link-first; the human creates the repo.
- **Does not install practice plugins** — recommends them; user installs from marketplace.
- **Does not duplicate brand interview** — recommends `brand-creative` and hands off to `/brand-creative:setup`.
- **Does not block on email/ads/analytics targets** — writes `not-yet-designed` skeletons and continues.
- **Does not write without explicit yes** after showing the plain-language diff.

## Preconditions

Read `${CLAUDE_PLUGIN_ROOT}/references/agency-setup-framework.md` and `${CLAUDE_PLUGIN_ROOT}/references/instance-profile-template.md` before proceeding.

Detect existing state per framework § Startup. Honour flags: `--quick`, `--full`, `--redo`, `--resume`, `--check-integrations`.

## Provisional mode

Partial interview → write resume JSON (`config/.setup-resume.json` in instance repo, or `~/.claude/plugins/config/digital-agency/agency-hub/setup-resume.json` before repo exists). Offer `--resume` on next run.

## Trust spine

Structured-aggregation; instance config is team-shared git artefacts — show full diff before write. Target pointer files in external repos require separate confirmation per repo. MCP connectors are configured in practice plugins, not agency-hub.

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

### Step 3 — Target bindings (Part 0)

Before business questions (skip if `--check-integrations` only):

> I'll verify target bindings for any repos already configured.

For each bound target repo, verify `.agency/target.json` exists and includes `name`, `instance`, and `target`.

Report: **valid**, **missing fields**, or **not found**. Name manual next steps. MCP connectors are not part of agency-hub — run `/<practice>:setup --check-integrations` on installed practice plugins to probe GitHub, Figma, etc.

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

| Practice area | Practice plugin | Companion practice | Notes |
|---|---|---|---|
| `brand-creative` | `brand-creative` | none | Shipped — no companion install |
| `web-development` | `web-development` | `product-management` | Practice plugin pending — interim catalogue: `engineering`, `frontend-engineer`, `qa-engineer`, `webops-engineer`, `principal-architect` |
| `content-marketing` | `content-marketing` | `product-management` | Shipped — run `/content-marketing:setup` after bootstrap; invoke `/product-management:tasks --product`, `/product-management:synthesize-research` for companion skills |
| `social-media` | `social-media` | TBD | Practice plugin pending — interim: `content-marketing` skills for captions and curation |
| `seo` | `search-optimisation` | `product-management` | Practice plugin shipped — run `/search-optimisation:setup` after bootstrap; invoke `/product-management:competitive-brief` for companion skill |

When recommending a companion practice, name the skills it needs (e.g. `web-development` → `/product-management:tasks --product`, `/product-management:sprint-planning`; `content-marketing` → `/product-management:tasks --product`, `/product-management:synthesize-research`; `search-optimisation` → `/product-management:competitive-brief`). `brand-creative` never needs a companion.

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
| website | Skeleton in `config/targets/website.json`; if repo path known, **propose** `.agency/` scaffold (`.gitignore`, `README.md`, `target.json`, stubs) + `target.json` separately |
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
- Any `.agency/` scaffold in external target repos — `.gitignore` and `README.md` from `${CLAUDE_PLUGIN_ROOT}/references/dot-agency/`, plus `target.json` and artefact stubs (separate confirmation per repo)

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
6. For website target binding (after separate yes for that repo): scaffold `.agency/` per framework § Target repo `.agency/` scaffold — copy `.gitignore` and `README.md` from `${CLAUDE_PLUGIN_ROOT}/references/dot-agency/`; write `target.json` with `name`, `instance`, and `target`; add stub files for `product.md`, `roadmap.md`, `backlog.md`; create empty `work/`, `architecture/`, and `reviews/` directories.
7. **Initialize Tier 0 hub state** — if `~/.claude/plugins/config/digital-agency/agency-hub/` is missing or empty, create `CLAUDE.md` (from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` template), `allowlist.yaml` (from `references/allowlist-default.yaml`), and `install-log.yaml` (`[]`). Populate hub profile fields from interview answers where available.

### Step 7 — Hand off to brand-creative

Do not run the brand interview here — plugins are self-contained and `agency-hub` cannot invoke another plugin's skill directly. User-mediated hand-off within the same conversation:

> **Brand setup next.** If `brand-creative` is not installed, install it from the marketplace. Then run `/brand-creative:setup` in this conversation — it reads seed material from instance setup and writes to `<instance-root>/brand/`.

If deferred, set `seedMaterial.notes` accordingly.

### Step 8 — Next steps

Close with a concrete path — not a pile of config files:

1. **Install** the first recommended **practice plugin** from the marketplace.
2. **`product-management` companion** — if that practice needs planning and cadence skills it does not own (e.g. `web-development` → install `product-management`, then use `/product-management:tasks --product` and `/product-management:sprint-planning`; `brand-creative` needs no companion).
3. **Practice setup** — run that practice's `setup` skill (e.g. `/brand-creative:setup` for brand; `/product-management:setup` for delivery).
4. **Bind targets** — complete `.agency/` scaffold and `target.json` in each target repo, social credentials when available.
5. **Deploy** — launch the first scheduled agent (dry-run first):
   `python3 digital-agency/scripts/deploy-squad-agents.py --dry-run --instance <path>`
6. **Edit anytime** — change `config/instance.json` directly or `/agency-hub:setup --redo`.

## Pause and resume

On pause, write JSON:

```json
{
  "plugin": "agency-hub",
  "skill": "setup",
  "mode": "quick|full",
  "startedAt": "ISO-8601",
  "instanceRoot": "<path or null>",
  "answers": {},
  "remainingSteps": [],
  "lastStepCompleted": ""
}
```

Location: instance repo `config/.setup-resume.json` if instance exists; else personal hub path above.

## Worked example

**Input:** Acme Co, single business, web-development + content, website target, quick mode.

**Expected output:** `config/instance.json` complete; `targets/website.json` skeleton; `plugins.json` lists `agency-hub` + recommended practice plugins; squad charters for site/content; handoff to `/brand-creative:setup` and next-steps naming `core` if web-development was chosen.

## Outputs

| Artefact | Path |
|---|---|
| Instance profile | `config/instance.json` |
| Plugin manifest | `config/plugins.json` |
| Target skeletons | `config/targets/<name>.json` |
| Deployment scaffolds | `config/deployments/*.json` |
| Squad charters | `squads/<squad>/charter.md` |
| Target pointer (on confirm) | `<target-repo>/.agency/` scaffold (`.gitignore`, `README.md`, `target.json`, stubs, dirs) |

Next: `/brand-creative:setup`, install first practice plugin, or `--check-integrations`.
