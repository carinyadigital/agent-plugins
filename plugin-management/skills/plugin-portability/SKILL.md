---
name: plugin-portability
description: Explains how to keep a skill, agent, or command host-neutral so it works on Cursor, Copilot, Codex, Gemini CLI, and other Agent Skills-compatible runtimes, not just Claude Code. Use when the user asks "will this work in Cursor", "make this portable", "does this only work in Claude Code", or is authoring a skill/agent/command intended to ship across multiple agent hosts.
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

# Plugin portability

A plugin that ships to more than one host — Claude Code and Cursor today, others
tomorrow — solves portability at two layers. The **manifest** layer (which manifest
file each host reads, covered in `plugin-structure`) is usually solved once, at the
marketplace level. This skill is about the layer underneath it: making sure the
*content* — the prose in a `SKILL.md`, an agent's system prompt, a command's body —
doesn't quietly assume it's only ever read by one vendor's runtime.

## Why this is tractable, not a rewrite

Skills are written to the open [Agent Skills](https://agentskills.io/) standard — a
`SKILL.md` contract adopted by roughly 40 agent runtimes, including Claude Code,
Cursor, Gemini CLI, GitHub Copilot, and OpenAI Codex. A skill written to that contract
does not need to know in advance which of those hosts will read it — portability is
the default, not something bolted on afterwards. This skill turns that standard into
concrete authoring rules for the parts of a skill/agent/command that are easy to get
wrong.

Two worked examples live alongside this skill:

- [`examples/host-coupled-vs-portable.md`](examples/host-coupled-vs-portable.md) —
  four before/after rewrites across skill prose, command steps, agent `tools:`, and
  MCP-dependent logic.
- [`examples/graceful-degradation-examples.md`](examples/graceful-degradation-examples.md)
  — the "name it, then state the fallback, same breath" pattern applied to hooks,
  MCP, environment variables, sub-agent dispatch, and settings surfaces.

## Three concrete rules

### 1. Describe outcomes, not host primitives

Write prompt bodies (skill instructions, agent system prompts, command steps) around
*what* must happen — read this file, write that artifact, ask for approval here —
never a mechanism that only exists on one host (a specific slash-command
orchestration feature, a host-specific sub-agent dispatch primitive, a vendor's own
workflow-engine API). If a step genuinely needs a host-specific capability, name the
capability and say what to do when it's absent, rather than assuming it's always
there.

```markdown
# Host-coupled — assumes a specific runtime feature exists
Use the Workflow tool to fan out five parallel research agents.

# Portable — states the outcome; the how is left to whatever's available
Research five topics in parallel where the host supports concurrent sub-agent
dispatch; otherwise run them sequentially. Either way, synthesise one findings doc.
```

### 2. Use generic capability names for tools, where you can

When a skill, agent, or command references what it needs to *do* — read a file, run a
shell command, fetch a URL — prefer the generic capability name (`Read`, `Write`,
`Glob`, `Grep`, `WebFetch`) over a host-specific tool identifier, when the field you're
writing doesn't require an exact host tool ID to function.

There's a real tension here worth knowing about rather than glossing over: an agent's
`tools:` frontmatter (see `agent-development`) is typically read literally by the host
that loads it — Claude Code expects its own tool name `Bash` for shell access, for
example, not a generic `Shell`. Writing the generic name in a field the host matches
exactly can mean the capability silently doesn't work, which is worse than the
non-portability it was meant to avoid. The practical rule: use generic names in prose
and in any field that's advisory rather than mechanically parsed; use the real host
tool name in a field a specific host's runtime parses literally, and note in a comment
or nearby sentence that another host's equivalent may need a different name.

### 3. Resolve context without assuming one repo/tracker/host shape

Don't hardcode assumptions like "this always runs inside a single git repo with one
specific remote host" or "there is always an issue tracker reachable via this one MCP
server" into a skill's core logic. Where a skill needs external context (a ticket, a
docs page, a CI status), state what it's looking for and how it degrades when that
source isn't configured — the same "prefer a connected server, fall back to CLI, then
explain what's missing" chain the `mcp-integration` skill documents for a different
reason. A skill that hard-fails when a specific integration isn't installed, instead
of explaining what's missing and continuing with what it has, isn't portable even if
its `SKILL.md` syntax is.

## What "genuinely host-specific" looks like, and how to isolate it

Some functionality really is one host's alone — a hook (`hooks/hooks.json`, see
`hook-development`), an environment variable like Claude Code's
`${CLAUDE_PLUGIN_ROOT}`, a host-only setting. That's fine to ship. The rule is
**isolation**: make it obviously opt-in, never load-bearing for the skill's core
behaviour. State the fallback inline, in the same sentence that introduces the
host-specific mechanism:

```markdown
Read ${CLAUDE_PLUGIN_ROOT}/data/reference.md, or the `data/reference.md` file at this
plugin's own root if that variable isn't set on the current host.
```

That one-line pattern — name the host-specific mechanism, then state the fallback in
the same breath — is the whole technique. Apply it anywhere a skill, agent, or command
would otherwise silently assume one host's environment.

## Where this sits next to `AGENTS.md`

`AGENTS.md` is a different, complementary layer, not a competing one: it's a
repo-level file of plain-prose instructions that most agent hosts read regardless of
whether any plugin is installed, while this skill is about making *plugin* content
(skills, agents, commands) portable across whichever hosts read `SKILL.md`. A plugin
doesn't need to duplicate its skill content into `AGENTS.md`, but if the host repo a
plugin installs into doesn't have one yet, or its own `AGENTS.md` is stale, that's a
gap this skill doesn't close — reach for the `agents-md-management` plugin for that,
rather than trying to fold repo-wide instructions into a plugin's skills.

## What this skill does not ask for

Don't pre-build adapters for hosts nobody has a real plugin on yet. Portability here
means *the content doesn't lock you out later*, not that every skill ships parallel
implementations for hosts nobody uses yet. When a third host becomes real, the fix
belongs in that plugin's own adapter surface (its manifest, any host-specific
settings) — not in a rewrite of content this discipline already kept host-neutral.

## Checklist

- [ ] Prompt bodies describe outcomes; any host-specific mechanism named explicitly
      names its host and states the non-host fallback in the same breath
- [ ] Fields that are advisory (prose, descriptions) use generic capability names;
      fields a specific host parses literally (like an agent's `tools:`) use that
      host's real tool name, with a note about the naming gap for other hosts
- [ ] External-context lookups (tickets, docs, CI) degrade gracefully when the
      expected integration isn't configured, rather than hard-failing
- [ ] Anything genuinely host-specific states its fallback inline, in the same
      sentence, not in a separate caveat far from where it's used

## Related skills

- **`plugin-structure`** — the manifest-layer portability a dual-manifest (or
  single-manifest) marketplace convention already solves; this skill is the content
  layer on top of it.
- **`skill-development`** — where trigger-description quality and progressive
  disclosure meet the same host-neutral writing discipline.
- **`agent-development`** — tool-name genericity applied to `tools:` frontmatter
  specifically, including the Bash/Shell naming tension above.
- **`plugin-settings`** — plain markdown + YAML is host-neutral by construction;
  keep any reader logic that way too.
