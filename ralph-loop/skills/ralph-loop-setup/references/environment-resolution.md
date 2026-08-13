# Environment resolution

How `/ralph-loop-setup` resolves the repo-specific values substituted into the
loop templates. Resolve everything ONCE at setup; the loop never re-detects.

## Branch (`{{BRANCH}}`)

1. A `Branch:` (or equivalent) declaration in the work item's TASKS.local.md.
2. The current branch, if its name references the work item's slug or ID.
3. Otherwise propose `feat/{work-id}` and confirm with the user.

Never create or switch branches during setup — report the expectation only.

## Validation commands

Discover, in order, stopping at the first source that documents commands:

1. **AGENTS.md / CLAUDE.md** — many repos declare canonical check commands.
2. **CI config** (`.github/workflows/`, `.gitlab-ci.yml`, etc.) — mirror
   the pipeline's check steps.
3. **Project manifest** — `package.json` scripts (respect the detected
   package manager from the lockfile), `Makefile` targets, `pyproject.toml`
   / `tox.ini`, `go.mod` conventions, `Cargo.toml`.

Split into:

- `{{FAST_VALIDATION_COMMANDS}}` — lint + typecheck only; runs on every
  task at `validate_and_commit`. Must complete in a couple of minutes.
- `{{VALIDATION_COMMANDS}}` — the full ordered list for `final_validation`:
  install, format, lint, typecheck, build, test. Include only steps the
  repo actually has; keep the repo's own invocations (workspace filters,
  monorepo scoping) intact.

If nothing is discoverable, ask the user rather than guessing.

## Tracker (`{{TRACKER_SECTION}}`)

Reuse the source system already resolved for `{work-id}` per
engineering `references/work-item-resolution.md` (companion) —
including the `TASKS.local.md` pointer, when present. Do not re-run
detection here; this section only maps the *already-resolved* system to
concrete per-task actions:

- **Resolved to Linear:**
  - start: move the issue to In Progress (or the workspace's equivalent state)
  - progress: move to In Review, and add a 1-3 sentence comment summarising
    what shipped
- **Resolved to Jira:**
  - start: transition the issue to In Progress
  - progress: transition to In Review (or the project's equivalent), and
    add a 1-3 sentence comment summarising what shipped
- **Resolved to GitHub / GitLab issues:**
  - start: assign / label in-progress
  - progress: comment with the commit summary
- **Resolved to filesystem only** — write exactly:
  `No tracker configured — skip tracker actions in task-start and task-progress.`

Write the resolved actions as concrete instructions (tool names, target
states) into the context file so loop iterations never re-negotiate them.

## UI signals (`{{UI_SIGNALS}}`)

Repo-specific indicators that a task's diff touches rendered UI and should
get a `ux_review` step. Derive from the repo layout, e.g.:

- component/page directories (`src/components/`, `app/`, `pages/`, `views/`)
- style files (`*.css`, `*.scss`, tokens files, `tailwind.config.*`)
- template files (`*.tsx`, `*.vue`, `*.svelte`, `*.html` templates)

For a backend-only repo write: `No UI in this repo — skip ux_review.`

## Ambiguity rule

Setup is the one interactive moment of a Ralph run. If any of the above is
ambiguous, ask the user during setup — a wrong value here is repeated by
every iteration of the loop.
