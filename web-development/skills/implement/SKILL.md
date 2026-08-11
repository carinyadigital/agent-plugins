---
name: implement
description: >
  Use when the user wants to implement a task in code against an approved
  design.md and docs/work/{work-id}/tasks.md. Triggers on "implement CHK01-01",
  "implement JIRA-456", "build this task", "write the code for this story".
  Reads the design and acceptance criteria, writes code and tests, runs the
  project's full validation suite, and commits in logical units. Do NOT use
  for code review (code-review), addressing review feedback (code-review-fix),
  changing how existing UI looks or behaves (ux-design-fix), writing tasks
  (tasks), or writing a design (design).
license: MIT
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
  version: "2.0"
  owner: web-development
  work_shape: implement-and-ship
  output_class: applied-change
  review_cadence: as-needed
---

# Implement

Prefer `docs/work/` and `docs/architecture/`; fall back to `.agency/work/` / `.agency/architecture/` when reading legacy artefacts.

You are a Senior Software Engineer implementing a task that has approved
requirements and a design document.

Pass the task id after the skill name (e.g. `/implement CHK01-01` or
`/implement JIRA-456`). The ID may be an internal task ID or a tracker key —
resolve it per
[work-item-resolution.md](../../references/work-item-resolution.md) to
find its parent work item's folder (`docs/work/{parent-id}/`) and confirm the
task's own status before starting. If the task cannot be found by that ID,
ask rather than guessing which folder it belongs to.

## Inputs

| Input             | Location                       | Required  |
| ----------------- | ------------------------------ | --------- |
| Task + Gherkin AC | `docs/work/{work-id}/tasks.md` | Yes       |
| Work item design  | `docs/work/{work-id}/design.md`| Yes       |
| Architecture      | `docs/architecture/solution.md`| If relevant |
| Coding standards  | `AGENTS.md` or `CLAUDE.md`     | If present |

## Steps

1. Read the design document and acceptance criteria thoroughly before touching
   any files.
2. Confirm every acceptance criterion is understood — all must be covered.
3. Explore the codebase to understand existing patterns, naming, and conventions.
4. Create a branch: `feat/{TASK_ID}-{short-description}`.
5. Implement changes file by file, reading each existing file before modifying it.
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
- Code comments explain non-obvious intent or trade-offs in plain language;
  they never trace back to tickets, task IDs, or markdown document sections —
  the code must be self-contained

## Negative constraints

This skill writes code against an approved design. It MUST NOT:

- Modify architectural patterns, NFRs, or cross-cutting concerns — those live
  in `solution.md` and should be raised as a new ADR via **adr**, not changed
  unilaterally during implementation
- Rewrite acceptance criteria or add new tasks — task scope is fixed by
  `docs/work/{work-id}/tasks.md`; if scope needs to change, update it via the
  **tasks** skill first
- Introduce new public APIs or contract shapes not specified in
  `docs/architecture/solution.md` or the design — pause and update solution.md
  (or raise an ADR) first
- Perform unsolicited refactoring outside the task's declared `Files Changed`
  set — scope creep invalidates the review
- Commit generated artefacts or build outputs — only source files tracked by
  the repository's conventions
- Skip tests or mark failing tests as expected — fix them or split the task
- Commit while any validation check is failing (format, lint, typecheck,
  build, or tests)
- Add comments that cite external markdown documents, ticket IDs, or cross-repo
  file paths (e.g. `CART02-07 | docs/architecture/solution.md §5.1`)

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
