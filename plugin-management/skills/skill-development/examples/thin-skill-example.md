# Worked example: a thin, single-file skill

This is the common case: a complete, useful skill with nothing else beside it. If you
were adding this to a real plugin, it would live at
`skills/changelog-entry/SKILL.md`.

```markdown
---
name: changelog-entry
description: Explains how to write a changelog entry for this project — one line per change, imperative mood, grouped under Added/Changed/Fixed/Removed. Use when the user asks to "add a changelog entry", "update CHANGELOG.md", or has just finished a change worth recording.
---

# Changelog entry

Keep `CHANGELOG.md` at the repo root under a single `## Unreleased` heading until the
next release renames it to a version number. Add new entries under the matching
category, creating the category heading if it doesn't exist yet for this unreleased
block:

## Unreleased

### Added
- Support for exporting reports as CSV.

### Fixed
- Timezone offset was applied twice on the dashboard.

## Writing style

- One line per change, imperative mood ("Add …", "Fix …", not "Added …" or "Fixes …").
- State the user-visible effect, not the implementation.
- No trailing period; entries read like a list of headlines, not sentences.

## Categories, in order

Added, Changed, Deprecated, Removed, Fixed, Security. Omit categories with nothing in
them for the current unreleased block.
```

Notice what makes this "thin": every fact needed to apply the skill is in the body
itself, with no `references/`, `prompts/`, or `agents/` subdirectory. That's the right
shape whenever a skill's whole content fits comfortably in one read. Compare with
[`router-skill-example.md`](router-skill-example.md) for when it doesn't.
