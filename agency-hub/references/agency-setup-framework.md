# Agency setup framework — digital-agency

Every `agency-hub` bootstrap follows this framework. The `agency-setup` skill implements it; practice plugins read the output — they do not re-ask org-wide facts captured here.

## Invocation

| Command | Behaviour |
|---|---|
| `/agency-hub:agency-setup` | Detect existing setup; offer quick vs full if mode not specified |
| `/agency-hub:agency-setup --quick` | Business name, primary practice, one target; sensible defaults elsewhere |
| `/agency-hub:agency-setup --full` | Full interview; review seed documents when provided |
| `/agency-hub:agency-setup --redo` | Ignore existing profile; re-interview and overwrite on confirmation |
| `/agency-hub:agency-setup --resume` | Continue a paused interview from the saved session file |
| `/agency-hub:agency-setup --check-integrations` | Report MCP connector status; no interview unless user asks to continue |

Combine flags when useful (e.g. `--redo --full`). If `--resume` is present, load the session first; other flags adjust what happens after resume.

## Config paths

| Tier | File | Purpose |
|---|---|---|
| 0 — Personal | `~/.claude/plugins/config/digital-agency/agency-hub/CLAUDE.md` | Hub marketplace profile — watched registries, installed community skills, update prefs |
| 0 — Personal | `~/.claude/plugins/config/digital-agency/agency-hub/allowlist.yaml` | Install allowlist — copy from `references/allowlist-default.yaml` if missing |
| 0 — Personal | `~/.claude/plugins/config/digital-agency/agency-hub/install-log.yaml` | SHA-pinned install audit log |
| 0 — Personal | `~/.claude/plugins/config/digital-agency/agency-hub/agency-setup-resume.json` | Paused interview before instance repo exists |
| 1 — Instance | `<instance-repo>/config/instance.json` | Shared org/brand/config facts |
| 1 — Instance | `<instance-repo>/config/plugins.json` | Installed catalogue plugins |
| 1 — Instance | `<instance-repo>/config/.agency-setup-resume.json` | Paused interview after instance repo is bound |
| 2 — Target | `<instance-repo>/config/targets/<name>.json` | Per-target binding skeletons |
| 2 — Target | `<target-repo>/.digital-agency/target.json` | Pointer from target repo to instance |

**In-repo templates (read-only):** `${CLAUDE_PLUGIN_ROOT}/references/instance-profile-template.md` and `${CLAUDE_PLUGIN_ROOT}/references/agency-setup-framework.md`. Never modify installed plugin templates.

**Install scope:** User-scoped install (recommended) lets skills read seed material anywhere on disk. Project-scoped install limits reads to the project folder — note this if the user reports "can't read [file]" during seed-document review.

## Startup — detect existing state

Before asking questions:

1. **Is the working directory an instance repo?** Look for `config/instance.json`.
   - **`status: complete`** — summarize what's on file; offer refresh, `--redo`, or `--check-integrations` only. Do not re-interview unless the user chooses refresh or passed `--redo`.
   - **`status: template` or partial** — offer to resume or start fresh.
2. **If not an instance repo** — check for `~/.claude/plugins/config/digital-agency/agency-hub/agency-setup-resume.json` (paused session) or proceed to repo creation (link-first, § Repo creation).
3. **Legacy hand-edited config** — if non-standard paths are found, offer to normalize into `config/instance.json` without deleting legacy files without confirmation.

## Repo creation (v1 — link-first)

When no instance repo exists yet:

1. Explain the instance repo model: private, git-versioned workspace holding `config/`, `brand/`, `squads/`.
2. Provide the template link (when published):
   > Create a private repo from the **digital-agency-instance** template: `https://github.com/<your-org>/digital-agency-instance/generate`
3. If the template is not yet published, provide the minimum skeleton:
   ```
   config/
   config/targets/
   config/deployments/
   config/cadence/
   brand/
   squads/
   README.md
   ```
4. Wait for the user to confirm the repo exists and provide the local path or clone URL.
5. Open that repo as the working directory for all subsequent writes.

**Do not** call GitHub APIs to create repos autonomously in v1. The human executes the irreversible step.

## Interview pacing

- **Assume the answer exists somewhere.** Prompt for a link or paste before asking the user to type from memory.
- **Ask and wait** for questions needing typed answers.
- **Skip handling:** "Skip for now — I'll flag it; fill in later with `--redo`." Track skips.
- **Before writing:** list skipped fields; ask whether to fill now or leave as placeholders.
- **Never** write with silent gaps.
- **Batch size:** 2–3 answerable prompts per turn maximum.
- **Pause:** write resume file; tell user to run `--resume`.

### Preamble

Show before the interview (adapt to context):

> **`agency-hub` bootstraps your digital-agency instance** — the shared config every practice plugin reads. Looking for a specific workflow? Install a practice plugin directly after setup.
>
> **Quick (~5 min):** business name, one practice, one target. **Full (~20 min):** services, cadence, risk posture, seed material, all target skeletons.
>
> Quick or full? (Upgrade anytime with `/agency-hub:agency-setup --full`.)

## Interview sections

### 1. Business identity

- Legal / trading name and how the business refers to itself in prose
- Single business vs agency serving multiple clients
- Industry / market and geography (brief)
- **Catalogue source** — GitHub org/repo slug (or equivalent) where this team installs the digital-agency marketplace; written to `config/plugins.json` → `catalogue`

### 2. Services wanted

Map to practice areas and recommended catalogue plugins (see `instance-profile-template.md` service table):

- Web development
- Content marketing
- Social media
- SEO
- Brand / creative

Quick mode: one primary practice. Full mode: all that apply now vs later.

### 3. Cadence and risk posture

- Planning rhythm (weekly sprints, monthly editorial, quarterly strategy)
- Approval-gate strictness (`relaxed` / `standard` / `strict`)
- Escalation model — who approves PRs, content, publishes
- Default risk posture and hard constraints

### 4. Seed material (full mode; optional in quick)

Existing site URL, past content, prior brand docs. **Read, don't copy verbatim.** Flag gaps for brand-setup handoff.

### 5. Targets

Which apply **now** vs **later**:

| Target | v1 status |
|---|---|
| `website` | Proven — write skeleton + document pointer binding step |
| `social` | Proven — write skeleton; social publishing connector binding deferred until credentials |
| `email`, `ads`, `analytics` | **Not yet designed** — write `status: not-yet-designed` skeleton; do not block |

For each active target: repository path/URL if known. Website binding requires writing `.digital-agency/target.json` in the target repo **after user confirms** — propose the diff first.

## Write Tier 1 and Tier 2 config

After interview, before any write:

1. Show plain-language summary of files to create/update.
2. Wait for explicit **yes**.
3. Write:
   - `config/instance.json` (set `status: complete`, `setup.completedAt`, `setup.mode`)
   - `config/plugins.json` with `agency-hub` and recommended practice plugins
   - `config/targets/<name>.json` per target discussed
   - `config/deployments/` — one scaffold per recommended scheduled agent, all `"enabled": false`
   - `squads/<squad>/charter.md` skeletons for enabled services
   - `brand/.gitkeep` or empty README if `brand/` is empty
4. Delete resume file on successful completion.

## Initialize Tier 0 hub state (personal)

After instance config write (or on `--full` setup completion), ensure personal marketplace files exist at `~/.claude/plugins/config/digital-agency/agency-hub/`:

1. **`CLAUDE.md`** — copy structure from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` template if missing; populate Role, deployment context, update preferences from interview answers.
2. **`allowlist.yaml`** — copy from `${CLAUDE_PLUGIN_ROOT}/references/allowlist-default.yaml` if missing; set `mode` per team size / deployment context (restrictive for firm-internal, confirm permissive explicitly for solo).
3. **`install-log.yaml`** — create as `[]` if missing (from `references/install-log-template.yaml`).

Tell the user where these live. Marketplace skills read them before install.

## Hand off to brand-setup

Do not duplicate brand interview logic. After config write:

> Next: brand voice. Run **`/brand:brand-voice discover`** then **`/brand:brand-voice write`** against seed material we noted. Content skills read from `brand/` via `config/instance.json`.

If the user declines now, note in `instance.json` `seedMaterial.notes` that brand-setup is pending.

## Integrations — `--check-integrations`

Read `${CLAUDE_PLUGIN_ROOT}/.mcp.json`. For each server:

| Server | Enables in agency-hub |
|---|---|
| github | Validate target repo access; read seed repos |

Report: **connected** (successful probe), **configured but not verified**, or **not found**. Name degraded steps. Offer to continue setup after the report.

## Confirm and summarize

1. Show instance profile and target skeleton changes in plain language.
2. Wait for explicit confirmation before writing.
3. After write: remind user they can edit files directly, run `--redo`, or `--check-integrations`.
4. Close with **next steps** — install first practice plugin, run brand-setup, deploy first scheduled agent (`deploy-squad-agents.sh --dry-run`).

## Living profile rules

- **`agency-setup`** is the only skill that may auto-apply a full instance profile write (after confirmation).
- Practice plugins use **propose profile update** for stable conventions discovered later — show diff, ask, write only on yes.
- Target binding completion (pointer files, connector credentials) may be done incrementally after bootstrap.
