# Doc comments

Agent instructions for every comment written into a file. Skills that
author or patch source, tests, config, SQL, HTML, or any other repo file
MUST follow this. Skills that review those files MUST flag violations.

This rule is about **comments inside files**. It does not apply to merge-request
descriptions, commit messages, or working-document bodies (`design.md`,
`TASKS.local.md`, review reports) — those artefacts may name work items and other
docs. It **does** apply to comments embedded in those files (HTML comments,
code-fence comments, file banners).

## What a comment is for

A comment is for the next reader of this file, at this line. It MUST make
complete sense without opening another file, following a link, or knowing
the ticket that caused the change. Do not use comments as a paper trail.

## MUST

Doc comments MUST:

- Stand on their own so they can be read inline
- State the intent, constraint, or trade-off in full, in plain language
- Remain true if the surrounding work item, tracker, or design doc is renamed,
  archived, or deleted

## MUST NOT

Doc comments MUST NOT:

- Contain any external reference — no URLs, repo paths, section numbers,
  headings, or "see …" / "per …" / "as in …" pointers
- Reference any external source, including issue systems (Jira, Linear,
  GitHub Issues, GitLab issues, Azure Boards, Shortcut, Asana) and their
  keys, ticket numbers, story IDs, epic IDs, or task IDs (`JIRA-456`,
  `CHK01-01`, `#42`)
- Reference working documents — `design.md`, `tdd.md` (legacy), `TASKS.local.md`,
  `ARCHITECTURE.md`, ADRs, PRDs, specs, briefs, roadmaps, backlogs, review
  verdicts, or any other planning or delivery artefact
- Use JSDoc/docstring tags that exist only to point elsewhere (`@see`,
  `@link`, `@ticket`, `@jira`, `@issue`)

A protocol, status code, or language feature named as a fact is not a
reference (`HTTP 429`, `PostgreSQL advisory lock`). Pointing at a document
that explains it is (`see RFC 6585`, `per ARCHITECTURE.md §5`).

## Do not write

```text
// CART02-07 | ARCHITECTURE.md §5.1
// Implements CHK01-01 from TASKS.local.md
// See design.md §3 for the retry policy
// Fixes JIRA-456
// Per ADR-0012, keep this mapping stable
<!-- Linear ENG-89 -->
/**
 * @see specs/checkout-foundation/design.md
 * @ticket PROJ-001
 */
```

## Write instead

```text
// Cap retries at 3: the payment provider duplicates charges on a fourth attempt
// Keep this mapping in insertion order — downstream hashing depends on it
// Reject paths that escape the repository root; callers pass user-supplied names
```

If the only thing you would write is a pointer to a ticket or a design doc,
write nothing. The code and a self-contained comment (or a clear name) must
carry the meaning.

## Scope

Applies to every comment form: `//`, `/* */`, `#`, `--`, `<!-- -->`,
file-level banners, JSDoc, docstrings, and annotated config. License or
copyright headers that the file already uses as a project convention may
stay; do not add tracker keys or doc paths to them.
