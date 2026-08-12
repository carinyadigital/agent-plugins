# Worked example: the smallest valid plugin

The minimum that satisfies every rule in this skill: one manifest pair, one skill,
one README. If you were adding this, it would live at `plugins/changelog-helper/`.

```
plugins/changelog-helper/
├── .claude-plugin/
│   └── plugin.json
├── .cursor-plugin/
│   └── plugin.json
├── README.md
└── skills/
    └── changelog-entry/
        └── SKILL.md
```

## `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`

Byte-identical on `name`/`description`/`version`, per the manifest-pair rule:

```json
{
  "name": "changelog-helper",
  "displayName": "Changelog Helper",
  "description": "Write changelog entries in this project's style.",
  "version": "0.1.0",
  "license": "Apache-2.0",
  "keywords": ["changelog-helper", "changelog", "release-notes"],
  "author": { "name": "Your Team" }
}
```

## `README.md`

```markdown
# Changelog Helper

Adds a `changelog-entry` skill that writes entries in this project's style.

## Install

/plugin install changelog-helper@your-marketplace
```

## `skills/changelog-entry/SKILL.md`

See the `skill-development` skill's own
[`examples/thin-skill-example.md`](../../skill-development/examples/thin-skill-example.md)
for the full body — this plugin exists to show that a single thin skill is a
complete, shippable plugin on its own. No agents, no hooks, no MCP, no legacy
commands — none of those are required just because they exist as component types.

## Why this is the right shape for a small plugin

Resist the urge to add a `commands/` directory, an `agents/` directory, or a
`docs/design.md` "just in case" — every one of those is opt-in, and an empty or
token-effort one is worse than not having it. Compare with
[`standard-plugin.md`](standard-plugin.md) for the point at which those become worth
adding, and [`advanced-plugin.md`](advanced-plugin.md) for a plugin that genuinely
needs all of them.
