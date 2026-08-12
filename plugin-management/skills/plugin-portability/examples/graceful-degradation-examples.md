# Worked examples: naming a host-specific mechanism and its fallback together

Five short patterns, one per component type this kit covers, all following the same
"name it, then state the fallback, same breath" rule.

## Hook-backed behaviour

```markdown
This plugin normally re-lints a file automatically after every edit via a PostToolUse
hook. On a host that doesn't support hooks, this doesn't happen automatically — run
the lint skill manually after editing instead; nothing else about this plugin depends
on the hook having fired.
```

## MCP-backed data

```markdown
Read the current sprint's ticket list from the connected project-tracker MCP server,
or ask the user to paste the ticket list if no such server is configured — either way,
proceed with the same triage logic once you have the list.
```

## Host-specific environment variable

```markdown
Read `${CLAUDE_PLUGIN_ROOT}/data/checklist.md`, or `data/checklist.md` relative to
this plugin's own root on a host that doesn't set that variable.
```

## Sub-agent dispatch

```markdown
Where the host supports dispatching a dedicated sub-agent, use the skill-reviewer
agent for this review; on a host without sub-agent dispatch, apply the same review
checklist directly in this conversation instead of skipping the review.
```

## Host-specific settings surface

```markdown
If this host exposes a settings UI for plugin configuration, mention that the same
values can be set there; otherwise, guide the user to the plain `.local.md` file this
plugin also reads (see the plugin-settings skill) — both are read the same way once
written, only how a user gets there differs.
```

Every one of these keeps a single logical behaviour working across hosts by stating
both paths up front, rather than writing the ideal-host version and hoping nobody
notices it's silent on every other host.
