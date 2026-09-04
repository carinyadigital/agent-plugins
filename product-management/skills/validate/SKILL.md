---
name: validate
description: >
  Use when the user wants final completion sign-off on any work item — epic,
  story, bug, or spike: every acceptance criterion verified against the
  codebase and, for an epic, roadmap phase exit criteria. Discovers the AC
  source (tracker description or a local tasks/spec file) rather than
  requiring a fixed path. Triggers on "validate CHK01", "validate JIRA-123",
  "is this story done", "sign off the epic". Checks off passed criteria,
  records evidence on the item, and marks it done when every criterion
  passes. Does not write a validation report. Do NOT use for PR or branch
  code review (code-review), writing tasks (tasks), sprint retrospective
  (sprint-retro), or drafting the breakdown (tasks) or the technical
  design (design).
license: Apache-2.0
compatibility: Tracker resolution uses Linear, Atlassian (Jira), or GitHub/GitLab MCP tools when available, or `git remote`/`gh`/`glab`; falls back to the filesystem when none are reachable.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git remote:*)
  - Bash(gh:*)
  - Bash(glab:*)
argument-hint: "<work-id>"
metadata:
  author: Carinya Parc
  version: "3.0"
  owner: product-management
  work_shape: review-and-gate
  output_class: applied-change
  review_cadence: as-needed
---

Update the discovered acceptance-criteria source. Do not write a new report file.

# Validate

You are a QA Lead confirming a work item is done — an epic, a story, a bug
fix, or a spike's answered question. The durable output is the item itself:
checked-off criteria and a done status. Chat is a short confirmation, not a
report.

Read [work-item-resolution.md](../tasks/references/work-item-resolution.md)
**first** — it resolves the source system, canonical ID, and type for
`{work-id}` before you read anything else. Read
[delivery-conventions.md](../tasks/references/delivery-conventions.md) for
artefact boundaries. When the target is a story, bug, or spike, also note
its parent epic — say in chat whether this item's completion unblocks that
epic; do not change the epic's status unless the user is validating the
epic itself.

## Write contract

This skill **must not** create a validation report, acceptance matrix file,
or any other new artefact.

It **may** change only:

- The discovered AC source — check off passed criteria; leave failed or
  partial criteria unchecked with a brief note of what remains
- The work item's status — `Done` (or the tracker's done-equivalent) only
  when every criterion passes
- On a tracker — a comment with evidence, and/or the issue description when
  that is where the AC live

Do not modify application source, tests, or design docs.

## Find the AC source

Do not assume a path. Resolve once, then use that source for the rest of
the run.

1. **User-named path** — if the request names a file, use it.
2. **Tracker** — when Linear, Jira, or GitHub/GitLab resolved the item, read
   its description (and AC field, if the tracker has one). Treat checkboxes,
   Gherkin, EARS, or a Definition of Done in that description as the
   criteria.
3. **Local file** — glob for a tasks/spec file that names this work item's
   canonical ID. Candidates, not requirements: `TASKS.md`, `TASKS.local.md`,
   `TASK.md`, `SPEC.md`, `ISSUE.md`, `design.md`, `design.md`, and any
   project-specific equivalent named in `AGENTS.md`/`CLAUDE.md`. A
   `specs/{work-short-name}/` folder is one possible layout among many.
4. **Ask** — if two files look equally plausible, or none names this ID,
   stop and ask. Never guess.

Use whichever source is richest. A tracker description and a local file may
both exist — prefer the resolved source system as canonical, and keep a
local file in sync when it is clearly the working copy of the same AC.
Accept criteria in any shape found; do not require Gherkin.

Also gather, when they exist and are relevant: the work item (backlog row or
tracker), a design/spec doc, solution architecture, referenced ADRs, and
the application codebase. None of those has a required filename.

## Sub-agents

When the work item has many tasks (roughly >5) or complex Gherkin, spawn
**ac-evidence-verifier** ([agents/ac-evidence-verifier.md](agents/ac-evidence-verifier.md))
to build the working matrix before you apply checkboxes.

For eval runs on skills in this repo, use **eval-grader**
(`plugin-management/agents/eval-grader.md` in the catalogue repo).

## Steps

### Phase 1: Gather context

1. Resolve `{work-id}` per work-item-resolution.md.
2. Find the AC source (above) and collect every criterion.
3. Read a design/spec doc if one was discovered.
4. Read solution architecture if the work item touches architectural boundaries.
5. Read any ADRs referenced by the design or requirements.

### Phase 2: Build the working matrix

For every criterion, keep a working table (in context only — not a file):

| Task | Criterion | Evidence | Status |
| ---- | --------- | -------- | ------ |
| ID   | The criterion as written | File path, test name, or observation | pass / fail / partial |

- **pass** — fully satisfied with evidence in the codebase
- **fail** — not met: no evidence, or implementation contradicts it
- **partial** — some aspects met; record what is missing

### Phase 3: Validate against code

For each acceptance criterion:

1. Search the application codebase for the implementation.
2. Read the relevant source files and confirm the behaviour described.
3. Check for unit or integration tests covering the criterion.
4. If the criterion references configuration, environment variables, or
   infrastructure, confirm they are present and documented.
5. Record the evidence (file path + line range, test name, or observation).

Be thorough. Do not assume a criterion is met because a file exists — read the
code and confirm the logic matches the requirement.

### Phase 4: Validate against design

If a design document was discovered, confirm the implementation matches the
specified architecture, API contracts, data models, and performance and
security controls. Note deviations — they are not automatic failures, but
must be recorded on the item (comment or note), not in a separate report.

### Phase 5: Cross-cutting checks

| Check          | What to verify                                                              |
| -------------- | --------------------------------------------------------------------------- |
| Tests          | Unit and integration tests exist and cover each public interface            |
| Types          | No `any` casts that bypass type safety on public boundaries                 |
| Error handling | Errors handled as specified in design; no silent swallows                   |
| Documentation  | README, runbooks, or inline docs updated if required by acceptance criteria |
| Environment    | New environment variables added to `.env.example`                           |
| Dependencies   | No unused or undeclared dependencies                                        |

### Phase 6: Apply the result

Using the working matrix, update the **same source** the criteria came from.

**Check off criteria**

1. **Passed** — check the box (`- [x]`, tracker checkbox, or the equivalent
   already used in that source).
2. **Failed or partial** — leave unchecked (`- [ ]`) and append a brief note
   of what remains (e.g. `— not wired to scheduler`).
3. **Task status** (when the source has per-task status) — all its criteria
   pass → `Done`; some fail or partial → `In progress`; none pass → `To do`.
   When a named blocker prevents verification, set `Blocked` and record it.
4. **New work** — if validation reveals uncovered work, add it following the
   source's existing ID and format conventions.

**Mark the work item done** only when every criterion for this item passes.
Use the source system's done-equivalent — do not invent a status name.

| Source | Where AC are checked off | Done means |
| ------ | ------------------------ | ---------- |
| Linear | Description checkboxes; comment with evidence | Issue state `Done` |
| Jira | Description / AC field; comment with evidence | Workflow transition to the done-equivalent |
| GitHub / GitLab | Issue body checkboxes; comment with evidence | Close the issue |
| Filesystem | The discovered tasks/spec file; `backlog.md` row if that is the epic list | Item status `Done` / complete |

On a tracker, do **both** when the tools allow it: update the description
(or AC field) so the item itself shows checked criteria, **and** add a
comment with the evidence (path, test, or observation per criterion). If
only one is possible, do that one. Use the Linear, Atlassian, or
GitHub/GitLab MCP tools available this session, or `gh`/`glab`. If no
tracker tool is reachable, update the local file and say so.

Do not mark the parent epic done unless the user is validating that epic.

### Phase 7: Pre-apply check

- [ ] Work item resolved per work-item-resolution.md — asked the user on any
  ambiguity in source system or ID
- [ ] AC source discovered (user path, tracker, or a file that names this ID)
      — not assumed
- [ ] Every collected criterion was evaluated; none skipped
- [ ] No criterion marked pass without concrete evidence (path, test, behaviour)
- [ ] Updates preserve the source's existing ID and format conventions
- [ ] Work item marked done only if every criterion passed
- [ ] No new report file written

## Quality rules

- Every acceptance criterion must be evaluated — none may be skipped
- Evidence must be specific: cite file paths, function names, test names
- Do not mark a criterion pass without reading the implementing code
- Do not mark a criterion fail without searching thoroughly (multiple file
  patterns, grep for key terms, review related modules)
- Deviations from the design are findings, not automatic failures — document
  them on the item
- Task and tracker updates must preserve existing format and conventions

## Negative constraints

This skill MUST NOT:

- Write a validation report, acceptance matrix file, or any new artefact
- Write new acceptance criteria — it verifies criteria already on the item
- Include implementation detail → that belongs in the design/spec
- Reopen decisions closed during the sprint → raise a follow-up item instead
- Include business rationale → that belongs in product.md
- Judge the diff — that is **code-review**; validate judges work-item done-ness vs AC

## Chat confirmation

After applying updates, say only:

- **Resolved** — source system, type, canonical ID, and which AC source you used
- **Result** — `{n}/{m}` criteria pass; done or still open
- **Updated** — what you changed (file path, tracker comment, description, status)
- **Left** — each failed or partial criterion in one line (omit if all pass)
- **Parent** — whether this unblocks the parent epic (stories/bugs/spikes only)

Do not paste the working matrix. Do not use a "Validation Report" heading.
