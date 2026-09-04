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

## Issue and task sources (`{{TRACKER_SECTION}}`)

Discover existing sources; never create a source during Ralph setup. In
particular, do not create a repo-root `TASKS.local.md` tracker pointer.

Possible sources include Jira, Linear, GitHub/GitLab issues, `TASKS.md`, an
existing `TASKS.local.md`, or a user-named system. Record every source that is
authoritative for the current task. If Jira and a local task document both
carry status, both are configured sources.

For each source, resolve concrete actions for all lifecycle phases:

- **start:** In Progress, or the source's exact equivalent (during `implement`);
- **review:** In Review, or the source's exact equivalent (during `review`);
- **complete:** Done, or the source's exact equivalent, plus a short shipped
  summary when the source supports comments (during `validate_and_commit`).

Filesystem actions must name the existing path, task identifier, status field,
and checkbox convention. Tracker actions must name the integration, issue key,
target status, and how to discover a valid transition. Do not leave generic
"update tracker" instructions.

Write all sources and actions into the context file. The loop must update
every source in the same lifecycle step and must not advance when one update
fails. Completion re-reads every source and confirms Done.

Reuse the source system already resolved for `{work-id}` per engineering
`references/work-items.md` (companion) — including an existing
`TASKS.local.md` pointer, when present. Do not re-run detection here.

## UI signals (`{{UI_SIGNALS}}`)

UX review is **not** a default engineering-delivery stage. Resolve UI signals
only when the user asked to add UX review. Then derive repo-specific
indicators that a task's diff touches rendered UI, e.g.:

- component/page directories (`src/components/`, `app/`, `pages/`, `views/`)
- style files (`*.css`, `*.scss`, tokens files, `tailwind.config.*`)
- template files (`*.tsx`, `*.vue`, `*.svelte`, `*.html` templates)

For a backend-only repo, or when UX review was not requested, write:
`No UX review in this run — skip ux_review.`

## Ambiguity rule

Setup is the one interactive moment of a Ralph run. If any of the above is
ambiguous, ask the user during setup — a wrong value here is repeated by
every iteration of the loop.
