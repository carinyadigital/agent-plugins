# Description guidelines

How to write the MR/PR title and description. The description's one job is
to manage the reviewer's attention: orient them in ~30 seconds — what
changed, why, and where to start reading — before they open the diff.

## Title

1. **Detect the repo's convention first**; impose nothing:
   - A commitlint / semantic-PR config (`commitlint.config.*`,
     `.commitlintrc*`, `semantic.yml`) → follow it.
   - Recent merged MR/PR titles and `git log --oneline -20` on the default
     branch → follow the dominant style.
   - No detectable convention → default to Conventional Commits:
     `type(scope): summary` with `feat|fix|docs|refactor|test|chore|build|ci|perf`.
2. Imperative mood ("add", not "added"/"adds"), ≤ 72 characters, no trailing
   period, specific enough to identify the change in a list of twenty.
3. Draft state is set via the provider's draft flag (or `Draft:` prefix on
   GitLab), only when requested.

## Summary first (the two-sentence rule)

Open the description with two sentences:

1. The problem — with a concrete number, error, or example where possible.
2. What this change does about it.

Everything else is supporting detail below the fold.

## Size-adaptive sections

Don't emit full ceremony for a ten-line fix. Judge by diff size *and* number
of concerns:

| Change | Include | Skip |
| ------ | ------- | ---- |
| Small (< ~50 lines, one concern) | Summary, why, linked work | files map, reviewer notes, test table |
| Medium (~50–200 lines) | Summary, what changed, why, how to verify, linked work | reviewer notes unless a trade-off is non-obvious |
| Large (200+ lines or several concerns) | Everything, **including** a key-files map and reviewer notes ("start here", known trade-offs) | nothing — reviewers need a map |

When the repo's own template mandates sections, the template wins — fill it,
dropping only sections irrelevant to the diff (see
[template-discovery.md](template-discovery.md)).

## Content rules

- **Why over what.** The diff shows what; the description must carry the why
  — the diff cannot.
- **How to verify** — concrete steps or the test command, not "tests added".
- Every claim must be true of the diff as pushed. No intended-but-unbuilt
  behaviour, no "TODO in a follow-up" for things the MR claims to do.
- Breaking changes, migrations, and rollout/rollback steps get their own
  clearly-marked section whenever they exist — never buried in prose.
- Screenshots/recordings for user-visible UI changes, when obtainable.

## Linked work

- Use the provider's auto-closing keyword when merging should close the item:
  `Closes #42` (GitHub/GitLab), `Closes PROJ-42` (Jira via integration).
- Use a plain reference (`Relates to #42`) when it should stay open.
- When no work item was resolved, say so ("No tracked work item — ad-hoc
  fix") rather than omitting the section or inventing a reference.

## Metadata

- **Labels** — apply what the work item or repo conventions imply (existing
  labels only; never create new ones).
- **Milestone** — only when the work item names one.
- **Reviewers** — suggest from CODEOWNERS / provider config (see
  [provider-resolution.md](provider-resolution.md)); confirm before
  assigning.

## Mechanics

- Always write the body to a temporary file and pass it by file
  (`--body-file`, `--description-file`) or read the file's content into the
  MCP call parameter. Never inline the body through a shell command —
  backticks, quotes, and `$` get double-interpreted.
- Markdown in the body: real headings, fenced code blocks for
  commands/errors, relative links only where the provider resolves them.
