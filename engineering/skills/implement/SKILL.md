---
name: implement
description: >
  Use when the user wants to implement a task in code against an approved
  design.md and {work-dir}/TASKS.local.md. Triggers on "implement CHK01-01",
  "implement JIRA-456", "build this task",   "write the code for this story".
  Reads the design and acceptance criteria, writes code and tests, runs the
  project's full validation suite, and commits in logical units. This is also
  the skill for test-driven development — "use TDD for this", "write a failing
  test first", "red/green/refactor", "add tests for X" — because that is code
  authoring, not document authoring. Do NOT use for delivering a whole work
  item through review and an MR (deliver), code review (code-review),
  addressing review feedback (code-review-fix), changing how existing UI looks
  or behaves (ux-design-fix), writing tasks (tasks), or writing a Solution
  Design (design).
license: Apache-2.0
compatibility: Requires git and the project's own validation toolchain (formatter, linter, typechecker, test runner).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
argument-hint: "<task-id>"
metadata:
  author: Carinya Parc
  version: "2.1"
  owner: engineering
  work_shape: implement-and-ship
  output_class: applied-change
  review_cadence: as-needed
---

Work directory `{work-dir}/`; default (if not specified or unknown): `specs/{work-short-name}/`. Read artefacts from `{work-dir}/`, `ARCHITECTURE.md`, and `docs/architecture/decisions/`.

# Implement

You are a Senior Software Engineer implementing a task that has approved
requirements and a design document.

Pass the task id after the skill name (e.g. `/implement CHK01-01` or
`/implement JIRA-456`). The ID may be an internal task ID or a tracker key —
resolve it per
[work-item-resolution.md](../../references/work-item-resolution.md) to
find its parent work item's folder (`{work-dir}/`) and confirm the
task's own status before starting. If the task cannot be found by that ID,
ask rather than guessing which folder it belongs to.

## Inputs

| Input             | Location                       | Required  |
| ----------------- | ------------------------------ | --------- |
| Task + Gherkin AC | `{work-dir}/TASKS.local.md` | Yes       |
| Work item design  | `{work-dir}/design.md` | Yes       |
| Architecture      | `ARCHITECTURE.md`| If relevant |
| Coding standards  | `AGENTS.md` or `CLAUDE.md`     | If present |

## Steps

1. Read the design document and acceptance criteria thoroughly before touching
   any files.
2. Confirm every acceptance criterion is understood — all must be covered.
3. Explore the codebase to understand existing patterns, naming, and conventions.
4. Create a branch: `feat/{TASK_ID}-{short-description}`.
5. Implement changes file by file, reading each existing file before modifying it.
   Comments MUST stand on their own so they can be read inline — see
   **Doc comments** below.
6. Write tests that verify each acceptance criterion.
7. Discover and run the project's full validation suite before committing:
   check `AGENTS.md` (or `CLAUDE.md`) first; if the commands are not documented
   there, read the CI config or the project manifest. Run format check, lint,
   typecheck, build/compile (if the project has one), and tests. Every check
   must pass before step 8 — fix each failure.
8. Review the full diff with `git diff` before committing.
9. Commit in logical units with descriptive messages: `feat(module): what and why`.

## Quality rules

- Read before writing — never modify a file you have not read
- Follow the plan exactly — no scope creep or unsolicited refactoring
- Preserve existing code style, naming, and architectural patterns
- Commits must not contain secrets or credentials
- Every new public function or interface must have a test
- Do not create a single monolithic commit — group related changes
- Doc comments follow [doc-comments.md](../../references/doc-comments.md)

## Doc comments

Read [doc-comments.md](../../references/doc-comments.md) before writing any
comment in code or any other file.

A comment MUST stand on its own so it can be read inline. State the intent,
constraint, or trade-off in full, in plain language. A reader who never opens
another file MUST still understand it.

Doc comments MUST NOT:

- Contain any external reference (no URLs, file paths, section numbers, or
  "see …" pointers)
- Reference any external source — including issue systems (Jira, Linear,
  GitHub/GitLab issues) and their keys, ticket numbers, story IDs, or task IDs
- Reference working documents (`design.md`, `TASKS.local.md`, `ARCHITECTURE.md`, ADRs,
  specs, designs, briefs, or any other planning artefact)

If the only comment you would add is a pointer to a ticket or a design doc,
write nothing.

## Negative constraints

This skill writes code against an approved design. It MUST NOT:

- Modify architectural patterns, NFRs, or cross-cutting concerns — those live
  in `ARCHITECTURE.md` and should be raised as a new ADR via `/architecture:adr`, not changed
  unilaterally during implementation
- Rewrite acceptance criteria or add new tasks — task scope is fixed by
  `{work-dir}/TASKS.local.md`; if scope needs to change, update it via
  `/product-management:tasks` first
- Introduce new public APIs or contract shapes not specified in
  `ARCHITECTURE.md` or the design — pause and update ARCHITECTURE.md
  (or raise an ADR) first
- Perform unsolicited refactoring outside the task's declared `Files Changed`
  set — scope creep invalidates the review
- Commit generated artefacts or build outputs — only source files tracked by
  the repository's conventions
- Skip tests or mark failing tests as expected — fix them or split the task
- Commit while any validation check is failing (format, lint, typecheck,
  build, or tests)
- Add comments that cite issue systems, working documents, or any other
  external source (e.g. `CART02-07 | ARCHITECTURE.md §5.1`)

## Output format

After completing implementation, write a summary:

<example>

## Implementation Summary

**Branch:** feat/PROJ-001-context-assembler
**Commits:** 3

### Files Changed

- `src/context/assembler.ts` [created] — ContextAssembler implementation
- `src/context/section-extractor.ts` [created] — Section extraction logic
- `src/context/assembler.test.ts` [created] — Unit tests

### Commits

1. `a1b2c3d` — feat(context): add ContextAssembler with token budget enforcement
2. `d4e5f6g` — feat(context): add section extraction from markdown headings
3. `h7i8j9k` — test(context): add unit tests for assembler and section extractor

### Verification

- Format: pass
- Lint: pass (no new warnings)
- Typecheck: pass
- Build: pass (or n/a — no compile step)
- Tests: 12/12 pass

</example>

## Related workflow

- `design` — work-item Solution Design
- `/product-management:tasks` — Gherkin AC / local breakdown
- `discovery-review` — Ready for Development gate before this skill
- `discover` agent — write Solution Design + tasks until that gate passes
- `deliver` agent — whole work item through review, validate, and MR
- `/architecture:adr` — raise a new ADR rather than changing `ARCHITECTURE.md` unilaterally (if not installed: `Install: /plugin install architecture@carinya-plugins`)
- `code-review` — review the working diff after implementation
