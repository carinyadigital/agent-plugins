---
name: release
description: >
  Cut a release of one or more digital-agency plugins — run plugin-check,
  validate, and test gates, bump per-plugin version(s), update CHANGELOG.md,
  and tag. Use when shipping a new or changed practice plugin, connector, or
  skill to the marketplace, or when the user asks to "cut a release", "ship
  this plugin", or "tag a version".
argument-hint: "[plugin-path ...] [--dry-run]"
allowed-tools: Read, Grep, Glob, Bash
disable-model-invocation: true
metadata:
  version: "0.1.0"
  owner: "digital-agency"
  work_shape: "orchestrate-delivery"
  output_class: "applied-change"
---

# Release

Cuts a release of one or more plugins in this monorepo: gates, version bump,
changelog, commit, tag, push. Adapted from the `vercel/vercel-plugin` release
skill shape — same staged-gate structure, but this repo has no build step
(pure Python/JSON/Markdown) and ships **many independently versioned plugins**
from one repo, not one plugin with one version. Read both differences below
before running this on autopilot.

## When to use

- A practice plugin, connector, or skill in the catalogue has changed and is ready to ship.
- The user asks to "release", "cut a version", "tag", or "ship" a plugin.

## What this skill does not do

- **Does not** decide semver bump type for you. Propose one from the commit
  messages touching the plugin (`fix:` → patch, `feat:` → minor, anything
  with `BREAKING CHANGE` → major) but confirm with the user before writing it.
- **Does not** run `scripts/deploy-squad-agents.py` or touch Managed Agent
  deployment — that's a separate, later concern from `managed-agents/`.
- **Does not** invent a single repo-wide version. Each plugin's
  `.claude-plugin/plugin.json` / `.cursor-plugin/plugin.json` is versioned
  independently; this skill bumps only the plugin(s) that changed.
- **Does not** push if any gate fails. Stop and report; do not skip a gate to
  "get it green."

## Preconditions

- Clean working tree (`git status --short` empty) on `main` or a release
  branch.
- `python3 scripts/validate.py` currently fails on `main` with 22 errors —
  stale references to the retired `agents/<slug>` layout in
  `check_managed_agent_cookbooks` (and possibly `check_agent_prompts`) from
  before the practice-plugin migration. **Fix that first.** Running this
  skill's validate gate against a repo that's already red makes the gate
  meaningless — you can't tell your change from the pre-existing breakage.
  `scripts/plugin-check.py` (new) is unaffected — it's scoped to individual
  plugin directories and passes clean today.

## Workflow

### 1. Identify target plugin(s)

If the user gave explicit plugin paths, use those. Otherwise, detect what
changed since the last tag:

```bash
git fetch --tags
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -n "$LAST_TAG" ]; then
  git diff --name-only "$LAST_TAG"..HEAD
else
  git diff --name-only HEAD~10..HEAD   # fallback for a repo with no tags yet
fi
```

Map changed file paths to their top-level plugin directory (the first path
segment for practice plugins/`practice setup`). Present the list of affected plugins to the user and confirm
before proceeding — a release should never silently include a plugin the
user didn't mean to ship.

If shared meta-framework reference files changed (`instance-profile-template.md`,
`setup-framework.md`), run `python3 scripts/sync-references.py` before
the gates below.

### 2. Fast gate — plugin-check

```bash
python3 scripts/plugin-check.py <plugin-dir-1> [<plugin-dir-2> ...]
```

Scoped to just the plugin(s) being released: manifest completeness, MCP
definitions, SKILL.md frontmatter, JSON sanity. Fix and re-run until clean —
do not proceed on a failure here.

### 3. Confirm and write the version bump

For each target plugin, read the current `version` from
`<plugin>/.claude-plugin/plugin.json`, propose a bump (see "does not do"
above), and confirm with the user. Then write the **same** new version into
both `<plugin>/.claude-plugin/plugin.json` and
`<plugin>/.cursor-plugin/plugin.json` — `check_marketplace_plugin_sync` in
`validate.py` will fail the release if these two drift, and marketplace
entries must match `name`/`description` against both.

### 4. Update CHANGELOG.md

Move the relevant `[Unreleased]` bullets for each released plugin into a new
dated section. If releasing multiple plugins in one pass, group bullets under
per-plugin sub-headings so the entry is unambiguous about which plugin got
which version.

### 5. Full gate — validate

```bash
python3 scripts/validate.py
```

Must exit 0. This is the repo-wide check — marketplace parity, marketplace↔
plugin.json sync, cross-references, bundled-skill drift, evals schema,
managed-agent cookbooks. See Preconditions if this is currently red for
reasons unrelated to your change.

### 6. Test gate

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

Must pass. (`test_repo_validation_passes` and
`test_json_format_emits_parseable_report` both call into `validate.py` and
will fail alongside it — see Preconditions.)

### 7. Commit

```bash
git add -A
git commit -m "release: <plugin-slug>@<version>[, <plugin-slug-2>@<version-2>]"
```

### 8. Tag — one tag per plugin, not one repo-wide tag

Independent plugin versions mean a single `v1.2.0`-style repo tag is
ambiguous about which plugin it refers to. Tag per plugin instead:

```bash
git tag <plugin-slug>-v<version>
```

Repeat for each plugin released in this pass.

### 9. Push

```bash
git push
git push --tags
```

## Outputs

- Updated `plugin.json` (both manifests) per released plugin.
- Updated `CHANGELOG.md`.
- One commit, one git tag per released plugin, pushed to `main`.
- A short summary to the user: plugin(s) released, old → new version(s), tag
  name(s), and links to the gate output for each of the three checks.

## Dry run

Pass `--dry-run` (or if the user just wants a preview): run steps 1–2, 5, and
6 only. Report what *would* change — target plugins, proposed version bumps,
changelog draft — without writing files, committing, or tagging.