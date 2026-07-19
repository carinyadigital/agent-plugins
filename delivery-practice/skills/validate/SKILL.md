---
name: validate
description: >
  Use when the user wants final epic completion sign-off: every task in
  .agency/work/{epic}/tasks.md verified against Gherkin AC and roadmap phase exit
  criteria. Triggers on "validate CHK01", "is this epic done", "sign off the
  epic". Builds an acceptance matrix with evidence, updates task and epic
  status, and produces a validation report. Do NOT use for PR or branch code
  review (code-review), writing tasks (tasks), sprint retrospective (sprint-retro),
  or drafting the breakdown (tasks) or design.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
argument-hint: "<epic-slug|epic-id>"
metadata:
  author: Carinya Parc
  version: "1.0"
  owner: delivery
  work_shape: review-and-gate
  output_class: decision-support
  review_cadence: as-needed
---

# Validate

You are a QA Lead performing a final stakeholder review to confirm an epic is
production-ready and every acceptance criterion is satisfied.

Read [delivery-conventions.md](../tasks/references/delivery-conventions.md)
when resolving `{epic}`. Resolve the slug from `.agency/backlog.md` when
the user passes only an Epic ID.

## Inputs

| Input                 | Location                        | Required    |
| --------------------- | ------------------------------- | ----------- |
| Product backlog       | `.agency/backlog.md`       | Yes         |
| Tasks                 | `.agency/work/{epic}/tasks.md`     | Yes         |
| Design                | `.agency/work/{epic}/design.md`    | If exists   |
| Application code      | `src/` (or repo equivalent)     | Yes         |
| Solution architecture | `.agency/architecture/solution.md` | If relevant |
| ADRs                  | `.agency/architecture/decisions/`  | If relevant |

## Sub-agents

When the epic has many tasks (roughly >5) or complex Gherkin, spawn
**ac-evidence-verifier** ([agents/ac-evidence-verifier.md](agents/ac-evidence-verifier.md))
to build the acceptance matrix before writing the report and updating tasks.md.

For eval runs on skills in this repo, use root **eval-grader** (`agents/eval-grader.md`).

## Steps

### Phase 1: Gather context

1. Read `.agency/backlog.md` — locate the epic row (Epic ID, Title, work
   path `.agency/work/{epic}/`).
2. Read `.agency/work/{epic}/tasks.md` and collect all tasks.
3. Read `.agency/work/{epic}/design.md` if it exists.
4. Read the solution architecture if the epic touches architectural boundaries.
5. Read any ADRs referenced by the design or requirements.

### Phase 2: Build the acceptance matrix

For every task in `.agency/work/{epic}/tasks.md`, build a table:

| Task     | Criterion                    | Evidence                             | Status                |
| -------- | ---------------------------- | ------------------------------------ | --------------------- |
| CF-XX-YY | Description of the criterion | File path, test name, or observation | pass / fail / partial |

- **pass** — criterion fully satisfied with evidence in the codebase
- **fail** — criterion not met: no evidence found, or implementation contradicts it
- **partial** — some aspects met but gaps remain; describe what is missing

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

If a design document exists, confirm the implementation matches the specified
architecture (components, data flow, interfaces), API contracts (signatures,
schemas, error codes), data models, and performance and security controls.
Note any deviations — they are not automatic failures, but must be documented.

### Phase 5: Cross-cutting checks

| Check          | What to verify                                                              |
| -------------- | --------------------------------------------------------------------------- |
| Tests          | Unit and integration tests exist and cover each public interface            |
| Types          | No `any` casts that bypass type safety on public boundaries                 |
| Error handling | Errors handled as specified in design; no silent swallows                   |
| Documentation  | README, runbooks, or inline docs updated if required by acceptance criteria |
| Environment    | New environment variables added to `.env.example`                           |
| Dependencies   | No unused or undeclared dependencies                                        |

### Phase 6: Update tasks and backlog

Based on the acceptance matrix, update `.agency/work/{epic}/tasks.md`:

1. **Completed criteria** — check the box `- [x]`.
2. **Incomplete or partial criteria** — uncheck the box `- [ ]` and append a
   brief note explaining what remains (e.g. `— not wired to scheduler`).
3. **Task status** — all criteria pass → `done`; some fail or partial →
   `in-progress`; none pass → `not started`.
4. **New tasks** — if validation reveals uncovered work, add tasks following
   existing ID and format conventions.
5. **Epic status** — update in `.agency/backlog.md` only when every task
   for the epic is verified done.

### Phase 7: Pre-report validation

- [ ] Every task in `.agency/work/{epic}/tasks.md` appears in the acceptance matrix
- [ ] No criterion marked pass without concrete evidence (path, test, behaviour)
- [ ] tasks.md and backlog.md updates preserve existing ID and format conventions
- [ ] Epic status set to complete only if all tasks are verified done

### Phase 8: Produce the validation report

Use the output format below.

## Quality rules

- Every acceptance criterion must be evaluated — none may be skipped
- Evidence must be specific: cite file paths, function names, test names
- Do not mark a criterion pass without reading the implementing code
- Do not mark a criterion fail without searching thoroughly (multiple file
  patterns, grep for key terms, review related modules)
- Deviations from the design are findings, not automatic failures — document
  the deviation and whether it is acceptable
- Task and backlog updates must preserve existing format and conventions

## Negative constraints

A validation report MUST NOT:

- Write new acceptance criteria — it verifies criteria already in tasks.md
- Include implementation detail → that belongs in solution.md or design.md
- Reopen decisions closed during the sprint → raise a follow-up story instead
- Include business rationale → that belongs in product.md
- Judge the diff — that is **code-review**; validate judges epic done-ness vs AC

## Output format

<example>

## Validation Report — CF-XX: Epic Title

**Date:** YYYY-MM-DD
**Validator:** AI QA Review
**Epic status:** complete | incomplete

### Summary

{1-2 sentence summary: how many stories, how many criteria, overall result}

### Acceptance Matrix

| Story    | Criterion   | Evidence                                       | Status  |
| -------- | ----------- | ---------------------------------------------- | ------- |
| CF-XX-01 | Description | `path/to/file.ts` L12-45                       | pass    |
| CF-XX-01 | Description | `path/to/test.ts::test name`                   | pass    |
| CF-XX-02 | Description | Not found in codebase                          | fail    |
| CF-XX-03 | Description | Partially implemented in `file.ts` — missing X | partial |

### Design Deviations

| Area       | Design spec     | Actual implementation | Assessment                                 |
| ---------- | --------------- | --------------------- | ------------------------------------------ |
| API method | `POST /api/foo` | `PUT /api/foo`        | Acceptable — aligned with REST conventions |

(Omit this section if no deviations found.)

### Findings

- **[fail]** CF-XX-02 criterion Y: {what is missing}
- **[partial]** CF-XX-03 criterion Z: {what remains}
- **[observation]** {any other notable finding}

(Omit this section if all criteria pass.)

### Backlog Changes

- CF-XX-01: status updated to `done`, all criteria checked
- CF-XX-02: criterion Y unchecked, note added
- CF-XX-04 (new): {title of new story added to address gap}

### Conclusion

{Is the epic ready for stakeholder sign-off? If not, what must be resolved first?}

</example>
