---
name: command-development
description: Explains the legacy `commands/*.md` layout — its required sections, frontmatter, destructive-operation confirmation rule, and when to use it instead of a user-invoked skill. Use when the user asks to "add a slash command", "write a command file", is maintaining an existing plugin that already uses `commands/`, or a command is failing a section-conventions check.
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

# Command development (legacy layout)

`commands/*.md` is treated as a **legacy** component shape **in this marketplace's own
convention** — Claude Code itself does not officially deprecate slash commands, and
this is a house opinion about which shape to reach for by default, not a statement
about upstream support. For new work here, write a user-invoked skill instead — see
the "Agent-invoked vs user-invoked skills" section of `skill-development` — which
covers the same "a person explicitly runs this by name" use case with one component
type instead of two. Before steering a plugin away from `commands/*.md` on a host
you're less familiar with, double-check that a user-invoked skill is actually invoked
the same way a `/command` is on that specific host — the equivalence this skill relies
on is confirmed for Claude Code, but verify it for whichever host you're targeting
before treating it as a given.

Reach for this legacy layout only when:

- You're maintaining an existing plugin that already has a `commands/` directory and
  changing its shape isn't in scope for the current change, or
- Your specific host or marketplace enforces its own structural checks against
  `commands/*.md` files specifically (this marketplace's validator does — see below)
  and you need a file in exactly that shape for that reason.

## The six required sections

A command file here must contain all six of the following headings
(`##`/`###`, matched case-insensitively, anywhere in the section title):

| Section | Enforcement | Purpose |
| :------ | :----------- | :------ |
| **Preflight** | Hard failure if missing | Check prerequisites: service/repo state, tooling on `PATH`, monorepo scope. |
| **Plan** | Warning if missing | State what will happen before running it; flag destructive/production-impacting steps. |
| **Commands** | Warning if missing | The operational core — prefer a connected integration for reads, fall back to a CLI for writes; no secrets in output; confirmation for destructive ops. |
| **Verification** | Hard failure if missing | Confirm the outcome actually took effect — don't just assume success because nothing errored. |
| **Summary** | Warning if missing | A concise `## Result` block. |
| **Next Steps** | Warning if missing | Logical follow-ups. |

`Preflight` and `Verification` are hard failures in this marketplace's validator; the
other four are warnings — still fix them, they're not optional in practice, just not
build-breaking. Two worked examples show the range:

- [`examples/minimal-command-example.md`](examples/minimal-command-example.md)
  — the smallest command that still passes, no destructive operations.
- [`examples/command-example.md`](examples/command-example.md) — a
  fuller command with a destructive step and the confirmation language it requires.

## Frontmatter

Every command file needs a `description` in YAML frontmatter — this is the one hard
requirement:

```markdown
---
description: One-line summary of what the command does.
argument-hint: "[arg1] [arg2]"
---
```

`argument-hint` and any tool-scoping field are optional and host-dependent — see the
`plugin-portability` skill before adding a host-specific tools field, since it's the one part
of a command file that commonly isn't portable as-is.

## Destructive operations need confirmation language nearby

This marketplace is a PCI-regulated environment. Its validator scans every command
body for destructive patterns — `git push --force`, `DROP TABLE`, `DELETE FROM`,
`kubectl delete`, `rm -rf`, `--prod`/`--production` — and fails unless nearby text
contains a confirmation/safety signal: the word "confirm", "explicit", or a `⚠` marker.
If a command's `Commands` section touches any of these, say so explicitly and require
an approval step before running it — don't just mention the operation and move on.

```markdown
⚠ This step force-pushes to the release branch. **Require explicit user confirmation**
before running it.
```

## File naming: commands vs meta-docs

Command files live in `commands/*.md` (root-level or per-plugin) and are the only
files scanned for the six sections. Files prefixed with `_` are meta-documents,
excluded from validation and not presented as slash commands — if you're writing a
doc *about* commands rather than a command itself, prefix it with `_`.

## Writing for the agent, not the user

The body of a command file is read by the agent as its own instructions, not shown to
the user as a message. Write directives ("Check the working tree is clean before
proceeding"), not narration ("This command will check your working tree"). The full
[`examples/command-example.md`](examples/command-example.md) follows all six sections
plus this instruction-voice convention — study it as the worked example. This plugin
itself deliberately does **not** ship a `commands/` directory: its own guided,
multi-phase entry point is the user-invoked [`create-plugin`](../create-plugin/SKILL.md)
skill, which is the shape to prefer for new work per the guidance at the top of this
skill.

## Validation checklist

- [ ] Frontmatter has `description`
- [ ] All six sections present, `##`/`###` headed
- [ ] Any destructive pattern the body touches has confirmation language nearby
- [ ] Not accidentally prefixed with `_` (which would exclude it from discovery)
- [ ] This marketplace's structural validator passes with no command-section issues

## Related skills

- **`skill-development`** — the preferred alternative for new user-invoked
  procedures; covers the same use case without a second component type.
- **`plugin-portability`** — keeping any tool-scoping frontmatter host-neutral.
- **`marketplace-and-release`** — where the finished command's plugin gets registered.
