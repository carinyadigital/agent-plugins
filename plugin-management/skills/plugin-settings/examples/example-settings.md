# Worked example: a `.local.md` settings file

Three variations on the same plugin's settings file, showing the range from minimal
to fuller use of the pattern. If you were adding this, it would live at
`<project-root>/.claude/code-review-helper.local.md`.

## Minimal — a couple of scalar toggles

```markdown
---
enabled: true
strictness: standard
---
```

No body needed if there's no freeform context to carry — frontmatter alone is a
valid, complete settings file.

## Typical — scalars plus a notes body

```markdown
---
enabled: true
strictness: strict
max_files_per_review: 20
---

# Notes

This team treats missing test coverage on new files as a blocking comment, not a
suggestion — stricter than this plugin's own default. Reviewers should also flag any
new dependency added without a corresponding note in the PR description.
```

The body here is read back verbatim and folded into the skill's own review criteria —
see [`reading-settings-in-a-skill.md`](reading-settings-in-a-skill.md) for how a skill
does that.

## Fuller — a list-shaped field via repeated keys

YAML frontmatter parsed with the lightweight, dependency-free technique this pattern
assumes (see the main skill body) handles flat scalars cleanly but not nested
lists/maps reliably — so prefer a delimited scalar over a real YAML list when the
plugin's own reader is a shell script, not a full YAML parser:

```markdown
---
enabled: true
excluded_paths: "vendor/,generated/,*.snap"
notify_channel: "#code-review-alerts"
---

# Notes

excluded_paths is comma-separated on purpose — a hook script parses this with plain
string splitting, not a YAML list parser.
```

If the only reader is a skill (which has a real YAML-aware `Read` tool available, not
a shell script), a proper nested YAML list is fine — the comma-separated convention
above is specifically for the hook-script-reader case where the parser is intentionally
minimal. State which case applies in your plugin's own README so contributors don't
guess wrong.
