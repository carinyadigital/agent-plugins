---
name: plugin-settings
description: Explains the `.claude/<plugin-name>.local.md` pattern for per-project, user-editable plugin configuration — YAML frontmatter for structured settings plus a markdown body for prompts or notes, read back by skills or hooks. Use when the user asks about "plugin settings", "user-configurable plugin", "store plugin state", ".local.md files", "per-project plugin configuration", or wants to make a plugin's behaviour configurable without editing its manifest.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
metadata:
  version: "0.2.0"
  owner: "plugin-management"
  review_cadence: "quarterly"
  work_shape: "generate-draft"
  output_class: "draft-for-review"
---

# Plugin settings

Some plugins need configuration that varies **per project** and is owned by the
person who installed the plugin there — not by whoever wrote it. That's different
from the plugin's own manifest (`plugin.json`, committed, identical for every
installer) or the plugin-root `settings.json` the `plugin-structure` skill covers (a
default sub-agent, still authored by the plugin, still shipped with it). This pattern
is for state and preferences that belong to *this* project's installation.

## Where it lives

```
<project-root>/
└── .claude/
    └── <plugin-name>.local.md
```

This lives in the **installing project**, not inside the plugin's own directory — it's
data the installer owns, never checked into the repo the plugin ships from. If your
plugin's README tells users to create one in *their own* project, also tell them to
add `.claude/*.local.md` to that project's `.gitignore` — this file is local, per-
installation state, not something to commit.

**The location is Claude-namespaced even though the file format isn't.** `.claude/` is
a Claude Code-specific directory; a Cursor install of the same plugin has no reason to
look there, and would more naturally expect `.cursor/<plugin-name>.local.md` instead.
The YAML-frontmatter-plus-markdown-body *shape* this skill teaches is genuinely
host-neutral, but this skill's own examples hardcode the `.claude/` path. If a plugin
ships to both hosts and actually needs this pattern on both, document (and have every
reader check) both locations rather than assuming the Claude path covers Cursor too.

Three worked examples live alongside this skill:

- [`examples/example-settings.md`](examples/example-settings.md) — minimal, typical,
  and fuller `.local.md` content.
- [`examples/reading-settings-in-a-skill.md`](examples/reading-settings-in-a-skill.md)
  — a skill excerpt that offers to create the file and reads it back on every run.
- [`examples/read-settings-hook.sh`](examples/read-settings-hook.sh) — a working
  script showing the frontmatter-by-hand parsing technique a hook needs.

## File shape

YAML frontmatter for structured fields, a markdown body for prose the plugin should
read back verbatim (a prompt, a note, task context):

```markdown
---
enabled: true
mode: standard
max_retries: 3
---

# Notes

Freeform context the plugin should factor in — a task description, a reminder,
anything that doesn't fit a scalar field.
```

## Reading it back

From a skill, read with a quick-exit if the file is absent — never require it:

```markdown
1. Check whether `.claude/<plugin-name>.local.md` exists in the project root.
2. If absent, proceed with sensible defaults; do not treat this as an error.
3. If present, read it and parse the YAML frontmatter for the fields this plugin
   defines; treat the body as freeform context to fold into the task.
```

If a hook needs the same file (see the `hook-development` skill), it has to parse the
frontmatter itself since hooks run as plain scripts, not through the agent's own
YAML-aware tools — extract the block between the `---` markers and grep individual
`key: value` lines. Quote every variable and validate any path-shaped field, the same
way `hook-development`'s secret-handling rules already require for any script that
consumes untrusted input.

## Creating it

A skill can write the file after asking the user for values — but apply the same
secret-handling rule everywhere: never write a literal credential or token into it,
and sanitise user input before writing (escape quotes, reject path traversal in any
path-shaped field). Document the fields your plugin supports, and a template, in the
plugin's own `README.md` so a user can hand-edit the file directly instead of going
through a skill.

## What changes take effect when

Skills re-read the file fresh on every invocation, so edits apply immediately. Hooks
are wired up when a session starts, so a settings change that flips hook behaviour
(e.g. an `enabled: false` kill switch a hook checks) may need a session restart to
take effect — say so in the plugin's README if any hook consumes this file.

## Validation checklist

- [ ] Documented in the plugin's `README.md` with the exact filename and a template
- [ ] If this plugin ships to more than one host and needs this pattern on all of
      them, the README and every reader account for that host's own settings
      directory (`.claude/` vs `.cursor/`), not just `.claude/`
- [ ] Every reader (skill/hook) quick-exits cleanly when the file is absent, with
      sensible defaults
- [ ] No credential, token, or connection-string value is ever written to or read
      back verbatim from the file
- [ ] Any path-shaped field is validated (no `..` traversal) before use
- [ ] If a hook consumes the file, the README notes whether a restart is needed

## Related skills

- **`plugin-structure`** — the plugin's own, committed `settings.json` (a default
  sub-agent) — a different, plugin-authored concept from this one.
- **`hook-development`** — the most likely consumer of a settings file that needs to
  toggle hook behaviour without editing `hooks.json`.
- **`plugin-portability`** — this pattern is plain markdown + YAML, host-neutral by
  construction; keep any reader logic generic rather than assuming one host's parser.
