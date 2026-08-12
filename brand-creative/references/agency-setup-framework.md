# Agency setup framework — digital-agency

Instance bootstrap follows this framework. Any practice `setup` may run it when `config/instance.json` is absent; practice plugins then read the output and do not re-ask org-wide facts.

## Invocation

| Command | Behaviour |
|---|---|
| `/<practice>:setup` | Detect existing setup; offer quick vs full if mode not specified |
| `/<practice>:setup --quick` | Business name, primary practice, one target; sensible defaults elsewhere |
| `/<practice>:setup --full` | Full interview; review seed documents when provided |
| `/<practice>:setup --redo` | Ignore existing profile; re-interview and overwrite on confirmation |
| `/<practice>:setup --resume` | Continue a paused interview from the saved session file |
| `/<practice>:setup --check-integrations` | Report target binding status; no interview unless user asks to continue |

Combine flags when useful (e.g. `--redo --full`). If `--resume` is present, load the session first; other flags adjust what happens after resume.

## Config paths

| Tier | File | Purpose |
|---|---|---|
| 0 — Personal | `~/.claude/plugins/config/digital-agency/brand-creative/CLAUDE.md` | Hub marketplace profile — watched registries, installed community skills, update prefs |
| 0 — Personal | `~/.claude/plugins/config/digital-agency/brand-creative/allowlist.yaml` | Install allowlist — copy from `references/allowlist-default.yaml` if missing |
| 0 — Personal | `~/.claude/plugins/config/digital-agency/brand-creative/install-log.yaml` | SHA-pinned install audit log |
| 0 — Personal | `~/.claude/plugins/config/digital-agency/brand-creative/setup-resume.json` | Paused interview before instance repo exists |
| 1 — Instance | `<instance-repo>/config/instance.json` | Shared org/brand/config facts |
| 1 — Instance | `<instance-repo>/config/plugins.json` | Installed catalogue plugins |
| 1 — Instance | `<instance-repo>/config/.setup-resume.json` | Paused interview after instance repo is bound |
| 2 — Target | `<instance-repo>/config/targets/<name>.json` | Per-target binding skeletons |
| 2 — Target | `<target-repo>/config/target.json` | Pointer from target repo to instance |

**In-repo templates (read-only):** `${CLAUDE_PLUGIN_ROOT}/references/instance-profile-template.md` and `${CLAUDE_PLUGIN_ROOT}/references/agency-setup-framework.md`. Never modify installed plugin templates.

**Install scope:** User-scoped install (recommended) lets skills read seed material anywhere on disk. Project-scoped install limits reads to the project folder — note this if the user reports "can't read [file]" during seed-document review.

## Startup — detect existing state

Before asking questions:

1. **Is the working directory an instance repo?** Look for `config/instance.json`.
   - **`status: complete`** — summarize what's on file; offer refresh, `--redo`, or `--check-integrations` only. Do not re-interview unless the user chooses refresh or passed `--redo`.
   - **`status: template` or partial** — offer to resume or start fresh.
2. **If not an instance repo** — check for `~/.claude/plugins/config/digital-agency/brand-creative/setup-resume.json` (paused session) or proceed to repo creation (link-first, § Repo creation).
3. **Non-standard config** — if config lives outside `config/instance.json`, offer to normalize into that path without deleting the existing files without confirmation.

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

> **Practice setup bootstraps your instance** when `config/instance.json` is absent — the shared config every practice plugin reads.
>
> **Quick (~5 min):** business name, one practice, one target. **Full (~20 min):** services, cadence, risk posture, seed material, all target skeletons.
>
> Quick or full? (Upgrade anytime with `/<practice>:setup --full`.)

## Interview sections

### 1. Business identity

- Legal / trading name and how the business refers to itself in prose
- Single business vs agency serving multiple clients
- Industry / market and geography (brief)
- **Catalogue source** — GitHub org/repo slug (or equivalent) where this team installs the digital-agency marketplace; written to `config/plugins.json` → `catalogue`

### 2. Services wanted

Map to **practice plugins** (MECE — self-contained install units). See `instance-profile-template.md` § Service → plugin mapping:

- `brand-creative` — shipped; no `core` companion
- `engineering`, `content-marketing`, `social-media`, `seo` — practice plugins pending; recommend interim catalogue entries and `core` where noted

Quick mode: one primary practice. Full mode: all that apply now vs later.

### 3. Cadence and risk posture

- Planning rhythm (weekly sprints, monthly editorial, quarterly strategy)
- Approval-gate strictness (`relaxed` / `standard` / `strict`)
- Escalation model — who approves PRs, content, publishes
- Default risk posture and hard constraints

### 4. Seed material (full mode; optional in quick)

Existing site URL, past content, prior brand docs. **Read, don't copy verbatim.** Flag gaps for `brand-creative:setup` handoff.

### 5. Targets

Which apply **now** vs **later**:

| Target | v1 status |
|---|---|
| `website` | Proven — write skeleton + document pointer binding step |
| `social` | Proven — write skeleton; social publishing connector binding deferred until credentials |
| `email`, `ads`, `analytics` | **Not yet designed** — write `status: not-yet-designed` skeleton; do not block |

For each active target: repository path/URL if known. Website binding requires writing `config/target.json` in the target repo **after user confirms** — propose the diff first.

### Target repo bind

On bind (after separate confirmation per target repo), write:

```text
config/target.json         ← binding pointer + repo identity (name, instance, target)
docs/product/              ← product.md, roadmap.md, backlog.md (created by product skills)
docs/architecture/         ← solution.md, decisions/ (created by architecture skills)
docs/work/                 ← work-item folders created by delivery skills
docs/reviews/              ← review state and agent byproducts
```

`config/target.json` must include a `name` field carrying the target repo identity (typically the git repo slug). Skills resolve the target by reading this file — they do not infer identity from the directory name.

## Write Tier 1 and Tier 2 config

After interview, before any write:

1. Show plain-language summary of files to create/update.
2. Wait for explicit **yes**.
3. Write:
   - `config/instance.json` (set `status: complete`, `setup.completedAt`, `setup.mode`)
   - `config/plugins.json` with recommended practice plugins
   - `config/targets/<name>.json` per target discussed
   - `config/deployments/` — one scaffold per recommended scheduled agent, all `"enabled": false`
   - `squads/<squad>/charter.md` skeletons for enabled services
   - `brand/.gitkeep` or empty README if `brand/` is empty
4. Delete resume file on successful completion.

## Initialize Tier 0 hub state (personal)

After instance config write (or on `--full` setup completion), ensure personal marketplace files exist at `~/.claude/plugins/config/digital-agency/brand-creative/`:

1. **`CLAUDE.md`** — copy structure from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` template if missing; populate Role, deployment context, update preferences from interview answers.
2. **`allowlist.yaml`** — copy from `${CLAUDE_PLUGIN_ROOT}/references/allowlist-default.yaml` if missing; set `mode` per team size / deployment context (restrictive for firm-internal, confirm permissive explicitly for solo).
3. **`install-log.yaml`** — create as `[]` if missing (from `references/install-log-template.yaml`).

Tell the user where these live. v2 marketplace skills read them before install.

## Hand off to brand-creative

Do not duplicate brand interview logic — plugins are self-contained. After config write, user-mediated hand-off within the same conversation:

> Next: brand setup. Install **`brand-creative`** from the marketplace if needed, then run **`/brand-creative:setup`** in this conversation. It reads seed material from setup and writes to `<instance-root>/brand/`.

If the user declines now, note in `instance.json` `seedMaterial.notes` that brand-creative setup is pending.

## Integrations — `--check-integrations`

Agency-hub does **not** bundle MCP servers. This flag verifies **target bindings** only.

For each bound target repo, verify:

- `config/target.json` exists at the target repo root
- `config/target.json` includes `name`, `instance`, and `target` fields

Report: **valid**, **missing fields**, or **not found**. Name manual next steps.

To probe MCP connectors (GitHub, Figma, etc.), run `/<practice>:setup --check-integrations` on installed practice plugins.

Offer to continue setup after the report.

## Confirm and summarize

1. Show instance profile and target skeleton changes in plain language.
2. Wait for explicit confirmation before writing.
3. After write: remind user they can edit files directly, run `--redo`, or `--check-integrations`.
4. Close with **next steps**:
   - Install the first recommended **practice plugin**
   - Install **`core`** if that practice needs shared roles (`engineering` → yes; `brand-creative` → no)
   - Run that practice's **`setup`**
   - Hand off to `/brand-creative:setup` when brand is in scope

## Living profile rules

- **`setup`** is the only skill that may auto-apply a full instance profile write (after confirmation).
- Practice plugins use **propose profile update** for stable conventions discovered later — show diff, ask, write only on yes.
- Target binding completion (pointer files, connector credentials) may be done incrementally after bootstrap.
