# Work item resolution

How any skill turns a bare argument — `JIRA-123`, `ENG-45`, `#812`,
`checkout-foundation`, `CHK01` — into a **source system**, a **canonical ID**,
and a **type**. Every skill that accepts a work item argument reads this file
before doing anything else. Resolve once per session and reuse the result;
do not re-detect per file read.

**Golden rule: never guess.** If the source system, the ID, or the type is
ambiguous in any way, stop and ask the user. A wrong guess here corrupts every
path this skill writes to and every ID it hands to `implement` or `validate`
downstream.

## Step 1 — Check the pointer file

Look for `TASKS.local.md` at the **repo root** before doing anything else.
That file is the Linear/Jira source-system pointer. It is not the work-item
task list — that lives at `specs/{work-short-name}/TASKS.local.md` when a
local breakdown is required.

- **Exists and names Linear or Jira** — trust it. Use the recorded site,
  workspace/team, and project key. Do not re-run detection or re-ask the user.
- **Exists and names filesystem** — trust it; skip to
  [ID and path resolution](#id-and-path-resolution).
- **Missing** — run [Step 2](#step-2--detect-the-source-system).
- **Exists but looks stale or contradicts what you find** (e.g. it names Jira
  but no Atlassian MCP tool is available this session) — say so and ask the
  user whether to keep it, update it, or use the filesystem.

## Step 2 — Detect the source system

Check what the current session can actually reach, then match it against the
argument's shape. Both checks matter — a tool being available does not mean
the ID belongs to it.

| System | Tool available when | ID shape |
| ------ | -------------------- | -------- |
| Linear | Linear MCP tools | `{TEAM}-{n}`, e.g. `ENG-45` |
| Jira | Atlassian MCP tools | `{PROJECT}-{n}`, e.g. `CHK-123` |
| GitHub / GitLab issues | GitHub/GitLab MCP, or `gh`/`glab` CLI, remote resolved from `git remote -v` | `#123`, or a bare number in context |
| Filesystem | Always available | kebab-case slug or internal `{PREFIX}{nn}` (`checkout-foundation`, `CHK01`) — matches a row in `docs/product/backlog.md` |

**Jira and Linear share the same `PREFIX-NUMBER` shape** — the ID alone cannot
disambiguate them. Resolve in this order and stop at the first that applies:

1. **User named the system explicitly** — "in Jira", "the Linear ticket" — use it.
2. **Only one of Linear/Jira has reachable MCP tools this session, and
   nothing already in view (an existing `TASKS.local.md`, a `backlog.md`
   row, prior conversation) names the other one** — use the reachable one.
   This is a convenience, not a certainty; say which system you resolved to
   and why, so the user can correct it before anything is written.
3. **Both are reachable, or neither is, or something in view names a system
   with no reachable tool** — ask the user which system it belongs to. Do
   not default to either.
4. **No external tracker is reachable and the ID does not match any external
   shape** — filesystem. Confirm a matching row exists in `backlog.md` (for a
   top-level ID) or a matching task in some `specs/*/TASKS.local.md` (for a
   child ID); if neither exists, ask whether this is new work or a typo.

If the repo has no `docs/product/backlog.md` and
no reachable tracker tool at all, ask the user which system they use before
writing anything — do not default to creating a filesystem backlog silently.

## Step 3 — Write or refresh the pointer

**Only when the resolved system is Linear or Jira**, and only after resolving
it fresh (not when Step 1 already trusted an existing pointer): write
`TASKS.local.md` at the repo root. The pointer template is owned by the
`tasks` skill (`product-management` companion —
`skills/tasks/assets/tasks-local.template.md`). If that companion is not
installed, write the same fields: **Source**, **Site / workspace**,
**Project / team key**, **Resolved**, **Resolved by**.

GitHub/GitLab and filesystem do not get a pointer — they are cheap to
re-derive (`git remote -v`, or the presence of `backlog.md`) every time, and
caching them risks staleness across repos that share a plugin cache.

Tell the user the pointer was written and that `TASKS.local.md` should be
added to `.gitignore` — it can name environment-specific sites and project
keys that do not belong in shared history. Do not edit `.gitignore` yourself
unless asked.

## Step 4 — Resolve the type

Read the work item's type from its source system:

- **Jira** — the issue type field, verbatim.
- **Linear** — the issue's team/label-based type if the workspace models one;
  otherwise ask — do not default to `task`.
- **GitHub/GitLab** — labels (`type:*`, `kind/*`, `bug`, `epic`) if present;
  otherwise ask, since bare issues carry no type field.
- **Filesystem** — inferred from structure, not a labelled field: a row in
  `backlog.md` is always `epic`; inside a `TASKS.local.md`, a `### S{n}` heading is
  `story` and a line under it is `task`, as is a line under `## Foundational`
  or `## Cross-cutting`. A filesystem-only `bug` or `spike` has no structural
  marker of its own — ask the user to confirm the type rather than inferring
  one from where it happens to sit.

**Known set:** `epic`, `story`, `task`, `bug`, `spike`. Treat this as a
starting vocabulary, not a whitelist — map whatever the source system reports
to the closest known type for the purpose of deciding skill behaviour (see
the type-to-behaviour table in
[work-item-schema.md](work-item-schema.md#type)), but keep the system's own
label in any artefact you write (do not silently relabel a Jira "Improvement"
as "story" in the artefact — cite it as reported).

**If the mapping is unclear** — a custom type you have not seen before, or a
type that plausibly decomposes two different ways — ask the user how to treat
it rather than picking the closest-sounding match.

## ID and path resolution

**Canonical ID.** When an external tracker resolved the item, its native key
**is** the canonical ID — `JIRA-123`, `ENG-45`. Never generate a parallel
internal ID for it, never re-slug it, and never invent a local numbering
scheme alongside it. Internal IDs (`{PREFIX}{nn}`, `{PREFIX}{nn}-{nn}`) exist
**only** for repos with no external tracker resolved.

**Work path.** `specs/{work-short-name}/` — one folder per resolved work item.
`{work-short-name}` is kebab-case, at most two words, derived from the title
(`cart`, `checkout-foundation`). When a short name is not known and cannot be
discovered, use `{work-id}` (`specs/JIRA-123/`, `specs/CHK01/`). See
[delivery-conventions.md](delivery-conventions.md#work-short-name-work-short-name)
for the discovery order.

An epic's design lives at `{work-dir}/design.md`; its local task
breakdown, when required, at `specs/{work-short-name}/TASKS.local.md`. A
story, bug, or spike that gets its own design or further breakdown lives in
its own `specs/{work-short-name}/` folder, alongside — not nested inside —
its parent epic's folder. Cross-reference the parent by ID in the artefact,
not by nesting.

The canonical ID still appears in every ID field inside the artefact (task
IDs, `Depends on`, the backlog row); only the directory name uses the short
name.

When the short name (or the fallback `{work-id}`) contains characters unsafe
for a path segment, ask the user how they want it represented on disk rather
than silently substituting.

**New work with no ID yet.**

- External tracker resolved: ask whether to create the item in the tracker
  (if the skill has write access via MCP) or ask the user for the ID once
  they create it. Never assign an internal ID as a placeholder for
  tracker-backed work.
- Filesystem only: assign the next internal ID in sequence, per
  [work-item-schema.md](work-item-schema.md). Never reuse or renumber once
  written.

## Ask-first checklist

Ask the user, in a single batch of clear questions, whenever any of the
following is true — do not proceed on an assumption:

- [ ] No pointer file exists and Step 2's ordering did not confidently
  resolve to a single system — it fell through to case 3 (both or neither
  reachable, or a name in view with no reachable tool)
- [ ] The pointer file's recorded system does not match what is reachable now
- [ ] The work item's type does not map cleanly to a known behaviour
- [ ] The requested action doesn't make sense for the resolved type (e.g.
  asking to decompose a `spike` or a `bug` — confirm intent rather than
  refusing or silently complying)
- [ ] The item does not exist yet and it is unclear whether to create it
- [ ] The canonical ID is unsafe to use as a path segment
