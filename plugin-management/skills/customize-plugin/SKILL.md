---
name: customize-plugin
description: Adapt an existing plugin to a specific organization's tools, terminology, and ways of working — replacing tool-agnostic placeholders, updating skill/command content, wiring up the right MCP connectors, and repackaging it. Use when the user asks to "customize a plugin", "set up a plugin", "configure a plugin", "tailor a plugin", "adjust plugin settings", "customize plugin connectors", "swap the tool a plugin uses", or "tweak a plugin".
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
metadata:
  version: "0.2.0"
  owner: "plugin-management"
  review_cadence: "quarterly"
  work_shape: "implement-and-ship"
  output_class: "applied-change"
---

# Customize a plugin

Adapt a plugin someone else built to how *this* organization actually works — either by
setting up a tool-agnostic template for the first time, or by refining a plugin that's
already configured. This is the counterpart to `create-plugin`: it changes an existing
plugin rather than building a new one.

> **Keep it plain.** All user-facing output — questions, todo items, summaries — must
> be in plain, nontechnical language. Never mention placeholders, `~~` prefixes, file
> paths, or manifest fields to the user. Frame everything in terms of the plugin's
> capabilities and the organization's tools.

> **Never rename anything.** Do not change the plugin's or any skill's `name`, or
> rename directories or files. Customization only replaces placeholder values and
> updates content — the identity of the plugin stays fixed.

## Finding the plugin

Locate the plugin's source directory before changing anything, then read its files to
understand its structure. Where the plugin lives depends on the host:

- **Claude Cowork (desktop):** search the mounted plugin directories, e.g.
  `find mnt/.local-plugins mnt/.plugins -type d -name "*<plugin-name>*"`. If nothing is
  found, the user is likely in a remote container — stop and tell them customizing
  plugins is currently only available in the desktop app's Cowork mode.
- **This marketplace repo / Cursor:** the plugin is a top-level directory `<name>/`.
  Work on it in place.

Whichever host, read the plugin's manifest(s) first. This marketplace pairs a
`.claude-plugin/plugin.json` with a `.cursor-plugin/plugin.json` — any change to
`name`/`description`/`version` (you won't be changing `name`) must stay identical
across both, or the repo's validator fails.

## Determining the customization mode

After locating the plugin, check for tool-agnostic placeholders (the `~~category`
pattern the `mcp-integration` skill describes):
`grep -rn '~~\w' /path/to/plugin --include='*.md' --include='*.json'`.

| Mode | When | What to do |
| :--- | :--- | :--------- |
| **Generic setup** | Placeholders exist | Default here unless the user asked for something specific. Replace each placeholder with the org's real value. |
| **Scoped** | No placeholders; user named a specific part ("update the standup skill", "change the ticket tool") | Read only the relevant section(s); don't scan the whole plugin or surface unrelated items. |
| **General** | No placeholders; user wants broad changes | Read the plugin's files, understand the current config, then ask what they'd like to change. |

> **Legacy `commands/`.** Some plugins have a `commands/` directory. Cowork presents
> these alongside skills as one "Skills" concept — treat `commands/*.md` the same as
> `skills/*/SKILL.md` when customizing.

## Workflow

### Phase 0: Gather intent (scoped and general modes only)

If the user already gave free-form context ("we do async standups in #eng-updates"),
record it and use it to pre-fill later answers. Otherwise ask one short, specific
open-ended question tailored to what they want to change.

### Phase 1: Gather context from knowledge sources

Use company-internal knowledge connectors (chat, documents, email) to collect what's
relevant to the customization scope — tool names, workflows, team conventions, and
config values (workspace IDs, project names, channel names). See
[`references/search-strategies.md`](references/search-strategies.md) for query patterns
by category. Record all findings for Phase 3. If no knowledge connectors are available,
skip this and ask the user directly.

### Phase 2: Build a todo list

List the changes to make, scoped to the mode:

- **Generic setup:** re-run the placeholder grep and group the results by theme.
- **Scoped:** only items for the section the user named.
- **General:** the changes implied by the user's request.

Use user-friendly descriptions — "Learn how standup prep works here", not "Replace
placeholders in skills/standup-prep/SKILL.md".

### Phase 3: Apply the changes

Work through each item using context from Phases 0 and 1. If that context already gives
a clear answer, apply it directly. Otherwise ask the user (with a structured question
prompt where supported) — don't assume "industry standard" defaults. If the user
doesn't know or skips, leave the value unchanged (or the placeholder, in generic
setup). Typical change types: placeholder replacement, content/workflow updates, URL
pattern updates, and configuration values.

### Phase 4: Wire up connectors

After the content changes are resolved, connect MCP servers for any tools that were
identified or changed. See [`references/mcp-servers.md`](references/mcp-servers.md) for
the discovery-and-connect workflow, the category-to-keywords map, and where the config
file lives. Update the plugin's MCP config (check `plugin.json` for a custom
`mcpServers` path, otherwise `.mcp.json` at the plugin root — see
[`examples/customized-mcp.json`](examples/customized-mcp.json)). Collect all connector
results and present them together in the summary, not one at a time.

## Packaging

Once every change is applied, hand the plugin back:

- **Cowork:** package as a `.plugin` file. Zip to a temp location first, then copy to
  outputs (writing directly may fail on permissions), excluding any `setup/` directory:
  ```bash
  cd /path/to/plugin && zip -r /tmp/<name>.plugin . -x "setup/*" -x "*.DS_Store" && cp /tmp/<name>.plugin /path/to/outputs/<name>.plugin
  ```
  Name the file after the original plugin directory. It appears as a rich preview the
  user can browse and accept.
- **This marketplace repo:** re-run the validator (`python3 scripts/validate.py`),
  then let the user review the diff and use the `marketplace-and-release` skill to ship
  it. Bump the plugin's `version` in **both** manifest flavors if the change ships.

## Summary output

Present what was learned, grouped by source, then which connectors were wired up and
which the user should still connect:

```markdown
## From searching chat
- You use Asana for project management
- Sprint cycles are 2 weeks

## From your answers
- Ticket statuses are: Backlog, In Progress, In Review, Done
```

If no knowledge connectors were available and the user answered at least one question
manually, add: "Connecting sources like Slack or your docs would let me find answers
automatically next time you customize a plugin."

## Related skills

- **`create-plugin`** — the counterpart for building a new plugin from scratch.
- **`mcp-integration`** — the `.mcp.json` shape and the `~~category` placeholder
  convention this skill fills in.
- **`plugin-settings`** — per-project, user-editable configuration, a lighter-weight
  alternative to editing a plugin's files for values that vary by project.
- **`marketplace-and-release`** — shipping a customized plugin that lives in a
  marketplace repo.
