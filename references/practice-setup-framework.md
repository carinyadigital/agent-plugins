# Practice setup framework — digital-agency

> Catalogue-only. Lives once at repo-root `references/`. Do not copy into practice plugins — each `/<practice>:setup` skill is self-contained and follows this contract.

Every root-level practice plugin's `setup` skill follows this framework. Plugin skills add only **plugin-specific** questions on top; org-wide facts live once in the instance profile (`config/instance.json`). **Whichever practice plugin you install first bootstraps** — if `config/instance.json` is absent, that practice's `setup` writes it, then runs its own interview.

## Invocation

| Command | Behaviour |
|---|---|
| `/<plugin>:setup` | Detect existing setup; offer quick vs full if mode not specified |
| `/<plugin>:setup --quick` | Short path: skip answered instance facts + minimal plugin questions |
| `/<plugin>:setup --full` | Full plugin interview; review seed documents when provided |
| `/<plugin>:setup --redo` | Ignore existing brand artefacts for this run; re-interview and overwrite on confirmation |
| `/<plugin>:setup --check-integrations` | Report MCP connector status for this plugin; no interview unless user asks to continue |
| `/<plugin>:setup --resume` | Continue a paused interview from the saved session file |

Combine flags when useful (e.g. `--redo --full`). If `--resume` is present, load the session first; other flags adjust what happens after resume.

## Config paths

| Tier | File | Purpose |
|---|---|---|
| 1 — Instance | `<instance-repo>/config/instance.json` | Shared org/brand/config facts — read, do not re-ask when complete |
| 1 — Instance | `<instance-repo>/brand/*` | Brand artefacts — voice, guide, discovery report, settings |
| 0 — Personal | `~/.claude/plugins/config/digital-agency/<plugin>/CLAUDE.md` | Plugin practice profile — plugin-specific conventions only |
| 0 — Personal | `~/.claude/plugins/config/digital-agency/<plugin>/setup-resume.json` | Paused interview before instance exists |
| 1 — Instance | `<instance-repo>/config/.<plugin>-setup-resume.json` | Paused interview after instance repo is bound |

**Brand path resolution:** When this plugin reads brand artefacts, resolve per `${CLAUDE_PLUGIN_ROOT}/references/brand-conventions.md` (brand-creative) or the equivalent conventions file in this plugin — instance `brand/`, target pointer, or standalone `docs/brand/`.

**In-repo templates (read-only):** `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` (practice profile template). Never modify installed plugin templates. Instance JSON schema lives at catalogue `references/instance-profile-template.md` — not shipped inside plugins.

**Install scope:** User-scoped install (recommended) lets skills read seed material anywhere on disk. Project-scoped install limits reads to the project folder — note this if the user reports "can't read [file]" during seed-document review.

## Startup — detect existing state

Before asking questions:

1. **Resolve brand directory** when this practice consumes brand artefacts (per conventions).
2. **Read** `config/instance.json` if present. Note `status`, `business`, `seedMaterial`, and any house tone hints. **Do not re-ask** facts already captured unless `--redo`.
3. **Read** `~/.claude/plugins/config/digital-agency/<plugin>/CLAUDE.md` unless `--redo`.
4. **Check brand artefacts** at resolved path when applicable — `brand-voice.md`, `brand-guide.md`, `brand.local.md`.
5. **If artefacts and practice profile are complete** and not `--redo`: summarize what's on file; offer refresh, `--redo`, or `--check-integrations` only. Do not re-interview unless the user chooses refresh or passed `--redo`.
6. **If instance profile exists but brand is empty:** say the instance layer is done; run plugin-specific interview only.
7. **If neither instance nor brand artefacts exist:** explain the model (instance profile optional; brand artefacts at resolved path) and proceed.

## Instance profile — read-only layer

When `config/instance.json` exists and `status: complete`:

- **Skip** business identity and house tone questions — reference the instance profile ("see instance profile").
- **Use** `seedMaterial.sources` and `seedMaterial.notes` as starting context.
- **If `config/instance.json` is absent:** run the **instance bootstrap** subsection below, write the profile, then continue with plugin-specific questions.
- **If present and complete:** do not rewrite it from setup — propose updates separately if new org facts emerge.

### Instance bootstrap (when `config/instance.json` is absent)

1. Interview minimal org facts: business name / prose name, single-business vs agency-serving-clients, primary practice, planning cadence, risk posture.
2. Show the plain-language summary of `config/instance.json` (and optional target skeleton). **Wait for yes.**
3. Write `config/instance.json` matching the catalogue schema (`references/instance-profile-template.md`) with `status: complete` (link-first — do not create GitHub repos autonomously).
4. Continue into the plugin-specific interview.


## Plugin-specific interview

After the instance layer is satisfied (or skipped):

1. **Mode** — `--quick` or `--full` if not already set.
2. Run the **plugin-specific** questions defined in the skill (`setup/SKILL.md` below the framework section).
3. **Quick mode:** skip answered sections; minimal plugin questions.
4. **Full mode:** request seed material; read for tone and vocabulary — not to copy proprietary content verbatim.
5. **Write practice profile** to personal config path and **practice artefacts** to their resolved paths on confirmation.

## Integrations — `--check-integrations`

Read the installed plugin's `.mcp.json` (in-repo: `${CLAUDE_PLUGIN_ROOT}/.mcp.json`) and `${CLAUDE_PLUGIN_ROOT}/CONNECTORS.md`. For each bundled server, report:

- **connected** (probe succeeded)
- **configured but not verified**
- **not in manifest**

Name which setup or skill steps are degraded without each connector. Stop after report unless user asks to continue setup.

## Delivery chain

After interview, run this plugin's skill chain as defined in `setup/SKILL.md` (orchestrated in conversation — no cross-plugin file reads). Companion skills in other plugins are **invoked by slash command**, not by reading sibling plugin directories.

When a companion plugin is required for the chain, state the install command:

```text
Install: /plugin install <plugin>@carinya-plugins
Then run: /<plugin>:<skill> …
```

See `docs/CROSS-PLUGIN-CONTRACTS.md` in the monorepo for the full edge list.

## Pause and resume

**Pause:** Write resume JSON with: `plugin`, `skill`, `mode`, `startedAt`, `instanceRoot`, `brandDir`, `answers`, `remainingSteps`, `lastStepCompleted`. Tell the user to run `/<plugin>:setup --resume`.

**Resume:** Load session, summarize progress, continue from `remainingSteps`. Delete session file after successful write.

## Confirm and summarize

1. Show **practice profile** changes and **artefact** paths in plain language.
2. List every file to create/update.
3. Wait for explicit **yes** before writing.
4. After write: remind user they can edit files directly, run `--redo`, or `--check-integrations`.

## Living profile rules

- **`setup`** is the only skill that may **auto-apply** a full profile write (after confirmation above).
- **Every other skill** uses **propose profile update** for stable conventions — show exact diff, ask, write only on yes.
- Org-level facts discovered later → propose update to `config/instance.json` (human edit or `setup --redo`). Plugin-specific facts → propose update to plugin `CLAUDE.md` or practice-local config files.
