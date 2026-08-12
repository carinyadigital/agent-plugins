---
name: hook-development
description: Explains how to add a `hooks/hooks.json` to a plugin — event types, the rule that hooks must never echo secrets, keeping hook scripts inside the plugin directory, and the portability trade-off of shipping host-specific automation. Use when the user asks to "add a hook", "create a PreToolUse hook", "run something automatically on an event", or mentions `hooks.json`.
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

# Hook development

Hooks run a command automatically on a lifecycle event — before/after a tool call,
session start, and so on. This is opt-in, host-specific infrastructure: treat it as
real functionality that's never load-bearing for the plugin's core behaviour on a host
that doesn't support it (see the `plugin-portability` skill).

## Where it lives

```
plugins/<plugin>/
└── hooks/
    ├── hooks.json
    └── scripts/
        └── validate.sh
```

`hooks/hooks.json` sits at the plugin root, same rule as every other component (see
`plugin-structure`). Keep any hook scripts **inside the plugin** — `hooks/scripts/`, not
a path outside `plugins/<plugin>/` — so the plugin remains self-contained and portable
when installed elsewhere.

```json
{
  "description": "Brief explanation of what these hooks do",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh" }
        ]
      }
    ]
  }
}
```

The `hooks` wrapper key is required in a plugin's `hooks/hooks.json` — this is the
plugin-specific format; a user-level settings file for the same host may use event
names directly at the top level, with no wrapper, which is a different file this skill
doesn't cover.

[`examples/hooks.json`](examples/hooks.json) wires up three complete, working
scripts:

- [`examples/scripts/validate-write.sh`](examples/scripts/validate-write.sh) — a
  `PreToolUse` hook blocking writes to common secret-file paths.
- [`examples/scripts/validate-bash.sh`](examples/scripts/validate-bash.sh) — a
  `PreToolUse` hook denylisting a small set of unambiguously dangerous shell command
  shapes.
- [`examples/scripts/load-context.sh`](examples/scripts/load-context.sh) — a
  `SessionStart` hook surfacing a project's own settings file (see the
  `plugin-settings` skill) at the start of every session.

## Event types available

| Event | Fires | Typical use |
| :---- | :---- | :----------- |
| `PreToolUse` | Before any tool runs | Approve/deny/modify a tool call |
| `PostToolUse` | After a tool completes | React to results, log, lint-after-write |
| `Stop` / `SubagentStop` | Agent considers stopping | Enforce completion standards |
| `SessionStart` | Session begins | Load project context |
| `SessionEnd` | Session ends | Cleanup, logging |
| `UserPromptSubmit` | User submits a prompt | Add context, block/validate |
| `PreCompact` | Before context compaction | Preserve critical info |
| `Notification` | Agent sends a notification | React to it |

Both **command** hooks (`"type": "command"`, a deterministic script) and **prompt**
hooks (`"type": "prompt"`, an LLM-evaluated instruction, typically supported on `Stop`,
`SubagentStop`, `UserPromptSubmit`, `PreToolUse`) are valid — prefer command hooks for
fast deterministic checks, prompt hooks for context-dependent judgement calls.

## The allow/block contract — get this wrong and nothing is actually blocked

This is the single most important thing to get right in a command hook, and the
easiest to get wrong by intuition: **`exit 1` does not block anything.**

| Exit code | Effect |
| :-------- | :----- |
| `0` | Allow. Claude Code parses **stdout** for optional JSON (see below). |
| `2` | **Block** — but only on blocking-capable events (`PreToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`, and a few others). Claude Code **ignores stdout entirely** on exit 2; the block reason must be written to **stderr**. |
| Anything else (including `1`) | A **non-blocking** error. The message surfaces to the user/model, but the tool call, prompt, or stop **proceeds anyway**. |

A hook meant to enforce policy that does `echo "Blocked: ..."` (to stdout) followed by
`exit 1` — the shape that looks most natural to write — allows the very thing it meant
to block. The two scripts this skill ships
([`examples/scripts/validate-write.sh`](examples/scripts/validate-write.sh),
[`examples/scripts/validate-bash.sh`](examples/scripts/validate-bash.sh)) write their
block reason to stderr and `exit 2`, and are the reference to copy.

There is a second, more reliable mechanism worth knowing: exit `0` and print a
structured decision to **stdout** instead of relying on the exit code at all:

```json
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "Writes to .env files are not allowed via this tool."}}
```

For `PreToolUse` specifically, `permissionDecision` (`allow`/`deny`/`ask`/`defer`) on
stdout with exit `0` is the canonical form — some Claude Code versions have shipped
with `exit 2` not reliably blocking every tool type (`Task`, some MCP tools), while the
stdout-JSON path did. A belt-and-suspenders hook emits both: the JSON decision on
stdout, `exit 2` as backup, and a human-readable reason on stderr.

**Not every event can block at all.** `PostToolUse` fires after the tool already ran —
exit 2 there surfaces stderr to Claude but can't undo the call. `SessionStart`,
`Notification`, and several other purely-informational events ignore exit 2 for
blocking purposes too. If you need a hard stop, confirm the specific event you're
wiring up is in the blocking-capable set before relying on it — check this host's
current hooks reference, since which events block, and the exact JSON field names,
have both shifted across releases; don't rely on this section alone for a
compliance-critical control.

## The rule that matters most: hooks must never echo secrets

Every hook script must be written on the assumption its stdout/stderr may end up in a
transcript a human reads later:

- **Never print a credential, token, connection string, or environment variable
  value.** Reference the variable *name* only ("checked `$DATABASE_URL` is set", not
  its value).
- **Mask, don't redact silently.** If a hook must report that it found something
  sensitive (e.g. a validation hook flagging a hardcoded key), show a masked preview
  (`AKIA****`) rather than either the raw value or nothing at all — the finding is the
  practice, not the value.
- **Validate before acting.** If a hook shells out based on tool input (a file path, a
  command string), validate it first — reject path traversal (`..`), reject writes to
  sensitive paths (`.env`, credential files) — before running anything.
- **Quote every variable** in hook scripts (`"$file_path"`, not `$file_path`) to avoid
  injection via crafted tool input.

[`examples/scripts/validate-write.sh`](examples/scripts/validate-write.sh) applies all
four rules in a real, runnable script — read it alongside this list, not instead of it.

If this is a PCI- or otherwise regulated environment, treat this rule as a hard
requirement, not a style preference — a hook that leaks a secret into a transcript is
a compliance incident, not a bug report.

## Portability note

`${CLAUDE_PLUGIN_ROOT}` resolves the plugin's install path on Claude Code; other hosts
that support hooks may expose an equivalent under a different name, or none at all.
Because hooks are inherently host-specific infrastructure — there is no cross-host
hooks standard the way there is for `SKILL.md` — treat any hook as **opt-in, isolated
functionality**, never load-bearing for the plugin's core behaviour on a host that
doesn't support it. See the `plugin-portability` skill for how this fits the layered
authoring model.

**This skill's `hooks/hooks.json` shape is Claude-only — Cursor does not run it.**
Cursor has its own hooks system with a genuinely different shape, not just a renamed
one, so a Claude `hooks.json` silently does nothing on Cursor rather than partially
working:

| | Claude Code (`hooks/hooks.json`) | Cursor |
| :--- | :--- | :--- |
| Event naming | PascalCase (`PreToolUse`, `SessionStart`) | camelCase (`beforeShellExecution`, `afterFileEdit`, `beforeSubmitPrompt`, `stop`) |
| File wrapper | `{"hooks": {...}}`, no version field | `{"version": 1, "hooks": {...}}` — `version` is required |
| Path variable | `${CLAUDE_PLUGIN_ROOT}` resolves the plugin's install path | No equivalent; Cursor's own docs use paths relative to the `hooks.json` location |
| Turn-completion hook | `Stop` can **block** — exit 2 keeps Claude from stopping | `stop` **cannot** block turn completion at all — it can only inject a `followup_message`, a strictly weaker mechanism |

If a plugin needs hooks on both hosts, that's two separate, hand-written
configurations, not one translated automatically — a Cursor plugin can point its own
`.cursor-plugin/plugin.json` `hooks` field at a Cursor-shaped hooks file if this
ever becomes a real need. Until then, the default for this kit is: **hooks are
Claude-only; Cursor installs of a plugin using `hooks/hooks.json` simply don't get
that automation**, which is fine as long as the plugin's core behaviour (its skills)
doesn't depend on the hook firing — the same isolation rule the checklist below
already requires.

## Validation checklist

- [ ] `hooks/hooks.json` at the plugin root, wrapped in `{"hooks": {...}}`
- [ ] Any hook meant to enforce a policy writes its reason to **stderr** and
      `exit 2`s (or emits `permissionDecision`/`decision` JSON on stdout with `exit 0`)
      — never `exit 1` with a message on stdout, which allows the action through
- [ ] The event the hook is wired to is actually in that host's blocking-capable set
      (e.g. `PreToolUse`, not `PostToolUse` or `SessionStart`)
- [ ] Hook scripts live inside `hooks/` (or a subdirectory), never outside the plugin
- [ ] No hook script prints a credential, token, or connection-string value
- [ ] Path/command inputs validated before use in any command hook — parsed with `jq`
      where available, not a hand-rolled `grep`/regex that a quoted value inside the
      JSON payload (e.g. `\"`) can silently defeat
- [ ] Every variable reference in a hook script is quoted
- [ ] Plugin still functions with the hook absent, on a host that ignores `hooks.json`
      (Cursor does — see the portability note above)

## Related skills

- **`plugin-structure`** — where `hooks/` sits relative to the rest of the plugin.
- **`plugin-portability`** — isolating host-specific functionality like hooks.
- **`mcp-integration`** — the other opt-in, host-adjacent component type.
- **`plugin-settings`** — a hook is the most likely consumer of a `.local.md`
  settings file, e.g. to toggle itself off without editing `hooks.json`.
