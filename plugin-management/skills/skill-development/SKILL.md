---
name: skill-development
description: Explains how to author a portable `SKILL.md` — required frontmatter, progressive disclosure (when to keep everything in one file vs split into `references/`/`prompts/`/`agents/`/`examples/`), user-invoked vs agent-invoked skills, trigger-description quality, and writing style. Use when the user asks to "create a skill", "write a SKILL.md", "add a skill to this plugin", "improve a skill description", "should this be a skill or a command", or a skill isn't triggering when expected.
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

# Skill development

Skills are the **default, primary component** in this marketplace — a `SKILL.md` the
agent loads when a task matches its `description`, or that a user runs explicitly by
name. Prefer a skill over the legacy `commands/*.md` layout (see
`command-development`) for anything new: the same file shape covers both the
"agent decides to use this" case and the "user explicitly invokes this" case, so there
is no need to maintain two component types for two triggering styles.

## Required shape

Every skill needs `SKILL.md` at `skills/<name>/SKILL.md`, with YAML frontmatter
carrying at minimum `name` and `description` — this repo's validator fails the build
if either is missing:

```markdown
---
name: skill-name
description: One or two sentences stating what the skill covers and when to use it.
---

Skill body …
```

`name` should match the directory name.

## Agent-invoked vs user-invoked skills

Both are the same component type; the difference is in frontmatter and framing, not
file layout:

| | Agent-invoked | User-invoked |
| :--- | :--- | :--- |
| Triggered by | The agent matching `description` against the current task | A person naming the skill explicitly, the way they'd run a slash command |
| Extra frontmatter | None required | `argument-hint` describing expected arguments; a tool-scoping field if the host supports one |
| Body voice | Guidance/knowledge for the agent to apply | Directives for the agent to execute, in order — see this plugin's own
  [`create-plugin`](../create-plugin/SKILL.md) skill for the directive voice a
  user-invoked, multi-phase procedure uses |

See the `plugin-portability` skill before adding any host-specific frontmatter field (a tool
ID that only exists on one host) — most skills need only `name` and `description`
because they're advisory rather than tool-scoped.

## Write the description so the agent picks it correctly

The `description` is the only thing loaded into every session up front — it is how the
agent decides whether this skill matches the current task, before anything else in the
file is read. Two things make a description work:

1. **Say what it covers.** Not "helps with hooks" — "hook event types, the rule that
   hooks must never echo secrets, keeping hook scripts inside the plugin."
2. **Say when to use it.** Include the concrete phrases a user or agent would naturally
   produce that should trigger this skill — "create a hook", "add a PreToolUse hook" —
   not just an abstract topic name.

Compare:

```yaml
# Weak — topic only, no trigger signal
description: Guidance for hooks.

# Strong — states coverage and concrete triggers
description: Explains hooks.json event types, the rule that hooks must never echo
  secrets, and keeping hook scripts inside the plugin. Use when the user asks to
  "create a hook", "add a PostToolUse hook", or mentions hooks.json.
```

Third person ("Explains…", "Use when…") is the convention used throughout this plugin
— follow it for consistency with sibling skills in whatever plugin you're adding to.

For a skill with more than one plausible triggering scenario, consider adding a short
worked example the way a sub-agent's frontmatter does — see `agent-development` for
the `<example>` block pattern, which also improves trigger reliability for skills with
ambiguous framing.

## Progressive disclosure: one file, or a directory of resources?

Start with a single `SKILL.md`. Most skills never need more. Split into bundled
resources only when a concrete need shows up:

| Resource | Add it when |
| :------- | :----------- |
| `references/` | Detailed knowledge that would bloat `SKILL.md` every time it triggers, or that several examples/prompts in the same skill share. |
| `prompts/` | The skill has more than one mode/stage and the procedure itself (not just background knowledge) differs per mode. |
| `agents/` | The skill needs a sub-agent specific to it that no other skill shares. Shared agents belong at the plugin root (`agents/`), cited by relative path, never copied. |
| `examples/` | Concrete worked input/output that's clearer as a standalone file than inline prose. |

Two worked examples live inside this plugin, showing both ends of that spectrum:

- [`examples/thin-skill-example.md`](examples/thin-skill-example.md) — a complete,
  useful skill with nothing else beside it. This is the common case.
- [`examples/router-skill-example.md`](examples/router-skill-example.md) — the same
  skill grown a `references/` directory once its detail got too large to inline every
  time it triggers. Read [`references/progressive-disclosure.md`](references/progressive-disclosure.md)
  alongside it for the full router-pattern rationale.

(These are illustration files, not real skills of this plugin — see the note in
`plugin-structure` on why example component files should never use the literal
`SKILL.md`/`agents/*.md`/`commands/*.md` filenames a host auto-discovers.)

When a skill does grow resources, keep `SKILL.md` itself a thin router: frontmatter,
one or two sentences on when to use / not use it, and a pointer into the resource
files — not a restatement of their content.

## Keep it lean; cite your own repo's spec, don't restate it

If a `SKILL.md` is describing something your own repo's docs already say — a manifest
schema, a command convention, a safety rule — state the substance inline (so the skill
works standalone, without depending on that other file existing) but keep the skill
itself the single place that substance lives for *this plugin's* purposes. Don't split
one fact across three skills that each restate it slightly differently — pick the one
skill that owns it and have the others link to that skill, not to an external doc that
might move or not exist wherever this plugin is installed.

There's no hard word limit, but if a `SKILL.md` body is growing past a few hundred
lines of prose that isn't decision-relevant, that's the signal to move detail into
`references/` rather than trim content that's actually needed.

## Validation checklist

- [ ] `name` + `description` present in frontmatter
- [ ] `name` matches the directory name
- [ ] `description` states both what the skill covers and when to use it, with
      concrete trigger phrases
- [ ] If user-invoked, frontmatter includes `argument-hint` and states expected
      arguments in the body
- [ ] No content duplicated between `SKILL.md` and another skill in the same plugin —
      link to the owning skill instead
- [ ] If bundled resources exist, `SKILL.md` points at every one of them
- [ ] This repo's structural validator, if present, passes

## Related skills

- **`plugin-structure`** — where a skill directory sits relative to the rest of the
  plugin, and when a skill needs no directory at all.
- **`plugin-portability`** — keeping the skill's tool references and prompt bodies
  host-neutral so it works outside Claude Code too.
- **`command-development`** — the legacy shape this skill's user-invoked mode
  replaces for new work.
- **`agent-development`** — a skill can invoke a sub-agent; the `<example>` block
  pattern for trigger reliability applies to both.
