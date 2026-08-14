---
name: plugin-structure
description: Explains how a plugin directory is laid out for this marketplace — the dual Claude/Cursor manifest pair, the plugin-root rule for every component directory, the marketplace `category` field, and when a single bare `SKILL.md` is enough versus a full `skills/<name>/` directory. Use when the user asks to "create a plugin", "scaffold a plugin", "add a plugin to the marketplace", "where does plugin.json go", "what's the plugin directory structure", or is starting a new `<name>/` plugin directory from scratch.
allowed-tools:
  - Read
  - Glob
  - Grep
metadata:
  version: "0.2.0"
  owner: "plugin-management"
  review_cadence: "quarterly"
  work_shape: "generate-draft"
  output_class: "decision-support"
---

# Plugin structure

In this marketplace a plugin is a top-level directory `<name>/` (other host repos may
use `plugins/<name>/` — match the convention you find). This skill covers the shape of
that directory and its manifest in full — everything needed to scaffold a correct
plugin without leaving this file.

## The one rule that matters most: every manifest exists twice

This marketplace ships every plugin to two hosts, Claude Code and Cursor, each of
which reads its own manifest file. Both manifests must carry the same `name`,
`description`, and `version` — a structural validator fails the build the moment they
diverge. There is no single source manifest one generates the other from: edit both,
every time, in the same change.

```
<name>/   # or plugins/<name>/ in host repos that nest plugins
├── .claude-plugin/
│   └── plugin.json     # Claude Code / Cowork
└── .cursor-plugin/
    └── plugin.json     # Cursor
```

Minimum required fields (enforced by this repo's validator): `name`, `description`,
`version`, `author`. `name` must equal the plugin's folder name exactly.

```json
{
  "name": "my-plugin",
  "displayName": "My Plugin",
  "description": "One sentence a marketplace browser can act on.",
  "version": "0.1.0",
  "license": "Apache-2.0",
  "keywords": ["my-plugin", "topic-1", "topic-2"],
  "author": { "name": "Your Team" }
}
```

There is no repo-wide version — each plugin versions independently. See the
`marketplace-and-release` skill for the bump rule.

`author` and `license` don't strictly have to match between the two manifest flavors
but should, for consistency — only `name`/`description`/`version` are validator-checked
for drift.

## The plugin-root rule

Only `plugin.json` lives inside `.claude-plugin/`/`.cursor-plugin/`. Every other
component — `skills/`, `commands/`, `agents/`, `hooks/`, `.mcp.json`, `README.md`,
`LICENSE`, `docs/` — sits at the **plugin root**, sibling to those two manifest folders, never
nested inside them:

```
plugins/my-plugin/
├── .claude-plugin/plugin.json
├── .cursor-plugin/plugin.json
├── LICENSE               # Apache-2.0 text — required at plugin root
├── README.md
├── skills/
│   └── some-skill/SKILL.md
├── agents/
│   └── some-agent.md
├── hooks/                # Optional
├── commands/             # Optional, legacy — see command-development 
├── .mcp.json             # Optional
├── settings.json         # Optional: plugin-level settings
└── ...
```

Getting this backwards (e.g. `.claude-plugin/skills/...`) is the single most common
scaffolding mistake — the component simply won't be discovered by either host.

Copy the repo-root `LICENSE` into every new plugin. Claude Code's plugin layout
includes a license file at plugin root so the Apache-2.0 text travels with an
independently installed plugin; Cursor does not require the file, but the SPDX
`license` field in both manifests should still be `"Apache-2.0"`.

## Skills are the primary component

Default to `skills/` for everything a plugin does — both agent-invoked guidance
("teach me how to do X") and user-invoked procedures (a person explicitly runs it by
name, the way a slash command works). A skill can carry `argument-hint` and a
tool-scoping field in its frontmatter for the user-invoked case, same file, same
directory shape, no separate component type required.

`commands/*.md` is a **legacy** layout, covered fully in the `command-development`
skill — reach for it only when a host or an existing plugin already depends on that
file shape, not for new work.

## Bare `SKILL.md` vs a full `skills/<name>/` directory

Both are valid; the choice is about whether the skill needs bundled resources, not
about the skill's importance.

| Shape | When |
| :---- | :--- |
| `skills/<name>/SKILL.md` only | The skill is self-contained guidance or a short procedure. No bundled files. This is the common case. |
| `skills/<name>/SKILL.md` + `references/`, `prompts/`, `agents/`, `examples/` | The skill has enough depth that inlining everything would bloat the body every time it triggers, or it needs skill-specific sub-agents/knowledge that no other skill shares. |

See the `skill-development` skill — and this plugin's own `skills/skill-development/`
directory as a live example — for how to decide and how to keep `SKILL.md` a thin
router once it grows resources.

## Illustrating a component vs shipping one

When a skill bundles a worked example of *another* skill, agent, or command (for
teaching purposes, the way this plugin's own `skill-development` skill does), never
name that illustration file `SKILL.md`, put it directly under `agents/*.md`, or put it
directly under `commands/*.md`. Those are the exact filenames/locations hosts use for
auto-discovery — some scan recursively, so even nesting one inside a skill's own
`examples/` directory can cause it to be picked up as a real, installable component.
Show the illustration as a fenced code block inside an ordinary `.md` file instead
(e.g. `examples/worked-example.md` containing a ```` ```markdown ```` block), never as
a file a host would discover on its own.

## The `category` field

`category` lives on the **marketplace manifest entry** for this plugin, not on the
plugin's own `plugin.json`:

```json
{
  "name": "my-plugin",
  "description": "…",
  "source": "plugins/my-plugin",
  "category": "Knowledge Work",
  "homepage": "https://your-marketplace-host/plugins/my-plugin"
}
```

The validator requires `name`, `description`, `source`, and `category` on every
marketplace entry, in **both** `.claude-plugin/marketplace.json` and
`.cursor-plugin/marketplace.json`. Pick a `category` string that matches whichever
existing plugin in your marketplace is closest in ownership shape — don't invent a new
one for a single plugin. See the `marketplace-and-release` skill for the full
registration step.

## Optional: a plugin-level `settings.json`

A plugin can declare a default sub-agent or other plugin-wide configuration via a
`settings.json` at the plugin root. Add it only when a concrete need shows up (a
default agent, a plugin-scoped setting) — don't add it speculatively. Keep it at the
plugin root alongside `README.md`, following the same plugin-root rule as everything
else above.

Don't confuse this with **per-project, user-editable configuration** — a plugin that
needs a file a user fills in once installed, that hooks/skills read back at runtime.
That's a different, unrelated pattern; see the `plugin-settings` skill.

## Checklist for a new plugin directory

- [ ] `<name>/.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`,
      matching on `name`/`description`/`version`
- [ ] `name` matches the folder name exactly
- [ ] At least one component (`skills/` preferred, `agents/`, `commands/` if legacy)
      at the plugin root
- [ ] Non-empty `README.md` at the plugin root
- [ ] The marketplace's structural validator, if this repo has one, run and passing
      clean

## Related skills

- **`skill-development`** — authoring the `SKILL.md` files themselves; the default,
  primary component type.
- **`command-development`** — the legacy `commands/*.md` layout and its section
  conventions, for cases that still need it.
- **`agent-development`** — the `agents/*.md` format and tool scoping.
- **`plugin-settings`** — per-project, user-editable configuration, a different
  concept from this skill's plugin-root `settings.json`.
- **`marketplace-and-release`** — registering the finished plugin and shipping it.
