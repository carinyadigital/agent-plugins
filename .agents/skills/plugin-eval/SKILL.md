---
name: plugin-eval
description: >
  Run live eval sessions against digital-agency skills — launch real Claude Code
  sessions, execute prompts from evals/evals.json, grade assertions with evidence,
  and write a coverage report. Use when shipping or tuning skills under skills/.
argument-hint: "[skill-path]"
allowed-tools: Read, Grep, Glob, Bash
disable-model-invocation: true
metadata:
  version: "0.1.0"
  owner: "digital-agency"
  work_shape: "monitor-and-report"
  output_class: "evidence-package"
---

# Plugin Eval

Launch real Claude Code sessions against a target skill, monitor debug logs and
written artefacts, grade every assertion in `evals/evals.json`, and write
`.notes/COVERAGE.md`.

## DO NOT (Hard Rules)

- **DO NOT** use `claude --print` or `-p` — skills do not run in print mode
- **DO NOT** use `--dangerously-skip-permissions`
- **DO NOT** create workspaces in `/tmp/` — use this repo root or `~/dev/digital-agency-testing/`
- **DO NOT** write eval shell scripts — do everything as Bash tool calls in the conversation
- **DO NOT** grade bundled copies under `agents/` — eval skill **sources** under `skills/`
- **DO NOT** pass on filename-only compliance — read file contents for evidence

**Copy the exact commands below. Do not improvise.**

## Quick Start (in-repo — preferred)

This catalogue **is** the workspace. `.agents/` and `skills/` are already on disk.

```bash
# 0. Set target skill (example)
SKILL=skills/engineering/skills/design
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# 1. Read eval prompts
cat "$SKILL/evals/evals.json"

# 2. Timestamp for this run (correlate log + report)
TS=$(date +%Y%m%d-%H%M)
SLUG="plugin-eval-$TS"

# 3. Launch live session via WezTerm — paste prompt from evals.json id 1
wezterm cli spawn --cwd "$REPO_ROOT" -- /bin/zsh -ic \
  "unset CLAUDECODE; x '/design Write walking-skeleton design for sample-epic' --allowedTools Read,Write,Edit,Grep,Glob,Bash; exec zsh"

# 4. Find debug log (~25s after session start)
find ~/.claude/debug -name "*.txt" -mmin -2 -exec grep -l "$REPO_ROOT" {} +
```

Repeat step 3 for each entry in `evals.json`. Use the exact `prompt` field — do
not paraphrase.

### Isolated clone (optional)

When you need a clean tree without local edits:

```bash
TS=$(date +%Y%m%d-%H%M)
SLUG="agency-eval-$TS"
mkdir -p ~/dev/digital-agency-testing/$SLUG
git clone --depth 1 git@github.com:carinyaparc/digital-agency.git ~/dev/digital-agency-testing/$SLUG
cd ~/dev/digital-agency-testing/$SLUG
# then same WezTerm spawn pattern with --cwd set to the clone path
```

Always append `$TS` to slugs so reruns do not overwrite prior workspaces.

## What to Monitor

### Session and tool activity

```bash
LOG=~/.claude/debug/<session-id>.txt

# Session lifecycle
grep -E "SessionStart|SessionEnd" "$LOG"

# Tool use (skill ran if Write/Edit fired on expected paths)
grep -E "Write|Edit|Read" "$LOG" | head -20
```

### Output artefacts

Skills write under repo conventions — check the paths relevant to the target skill:

```bash
# Design / tasks / validate (portable docs path)
find docs/work -name "*.md" -mmin -30 2>/dev/null

# Maintainer work path (this repo)
find .agents/work -name "*.md" -mmin -30 2>/dev/null
```

### Trigger routing (best-effort)

If `evals/trigger-queries.json` exists, note whether the host surfaced the
target skill for each query. When the host provides no routing signal, mark
checks `skipped` in the coverage report — do not invent pass/fail.

## Grading

1. Read `{skill-path}/evals/evals.json`.
2. For each eval `id`, confirm the session ran with that eval's `prompt`.
3. For each `assertion`: **PASS** or **FAIL** with quoted evidence (path + excerpt).
4. Critique eval quality: trivial assertions, missing outcomes, unverifiable claims.

```markdown
## Eval grade — {skill_name}

| Assertion | Verdict | Evidence |
| --------- | ------- | -------- |
| ... | PASS/FAIL | `path/to/file.md` L12: "excerpt..." |

### Eval quality notes
- ...
```

Do not mark PASS without reading the implementing content.

## Skills with evals

| Skill | Path |
| ----- | ---- |
| design | `skills/engineering/skills/design` |
| tasks | `delivery-practice/skills/tasks` |
| backlog | `delivery-practice/skills/backlog` |
| validate | `delivery-practice/skills/validate` |
| implement | `skills/engineering/skills/implement` |
| code-review | `skills/engineering/skills/code-review` |
| create-mr | `skills/engineering/skills/create-mr` |
| content-calendar | `skills/content/skills/content-calendar` |
| draft-post | `skills/content/skills/draft-post` |
| draft-recipe | `skills/content/skills/draft-recipe` |
| analyse-media | `skills/content/skills/analyse-media` |
| write-captions | `skills/content/skills/write-captions` |
| edit-content | `skills/content/skills/edit-content` |
| curate-content | `skills/content/skills/curate-content` |
| keyword-research | `skills/seo/skills/keyword-research` |
| technical-seo-audit | `skills/seo/skills/technical-seo-audit` |
| content-seo-review | `skills/seo/skills/content-seo-review` |

See `.notes/eval-baselines.md` for Sprint 4 coverage matrix and baseline status.

Run plugin-eval against each path before shipping changes to that skill.

## Coverage Report

Write results to `.notes/COVERAGE.md` (repo root or test workspace):

1. **Session index** — slug, session ID, target skill, eval ids run
2. **Assertion matrix** — all assertions with PASS/FAIL and quoted evidence
3. **Trigger routing** — pass/fail/skipped per `trigger-queries.json` entry
4. **Artefacts produced** — paths and one-line summary each
5. **Eval quality notes** — weak assertions, gaps, suggestions
6. **Issues found** — bugs, routing gaps, host setup problems

## Workflow with skills-qa

1. **plugin-eval** — runtime behaviour against `evals/` (this skill)
2. **skills-qa** — static design review against the Agency Skill Design Framework
3. **`validate.py`** — structural checks (manifests, cross-refs, drift, evals schema)

Run all three before merging skill changes. plugin-eval first, then `python3 scripts/validate.py`.

## Cleanup

When using isolated clones only:

```bash
rm -rf ~/dev/digital-agency-testing/agency-eval-*
```

Do not delete in-repo artefacts under `docs/work/` or `.agents/work/` — those may
be intentional eval outputs to review before revert.
