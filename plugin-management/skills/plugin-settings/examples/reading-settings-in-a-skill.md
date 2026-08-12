# Worked example: creating and reading `.local.md` from a skill

A skill excerpt showing both directions — offering to create the file when it's
missing, and reading it back on every later invocation. This is prose you'd put in a
real `SKILL.md` body, not a standalone file.

## Offering to create it

```markdown
## First-time setup

If `.claude/code-review-helper.local.md` doesn't exist in the project root, this is
the first time this plugin has run here. Ask the user:

1. "What strictness level? (standard / strict)" — write the answer to `strictness`.
2. "Any paths to exclude from review? (comma-separated, or none)" — write to
   `excluded_paths`, comma-separated, or omit the field entirely if none.

Write the file with those fields as YAML frontmatter and no body, then proceed with
the review using the values just captured. Never write a default value the user
didn't confirm — if they skip a question, omit that field rather than guessing a
default into the file.
```

## Reading it back on every invocation

```markdown
## Before reviewing

1. Check whether `.claude/code-review-helper.local.md` exists in the project root.
2. If absent, use built-in defaults (`strictness: standard`, no excluded paths) and
   proceed — do not block the review on missing settings.
3. If present, read it and extract `strictness` and `excluded_paths` from the
   frontmatter. Skip any file matching an excluded path before applying review
   criteria to it.
4. If the body contains freeform notes (see
   [`example-settings.md`](example-settings.md)), fold them into the review criteria
   for this run — e.g. a note about a stricter test-coverage bar becomes an actual
   check applied below, not just background context.
```

The quick-exit-when-absent behaviour in step 2 is the one rule that matters most here
— a settings file is optional, per-project convenience, never a hard dependency the
skill breaks without.
