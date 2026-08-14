# Worked example: a full-featured plugin

The point at which every component type earns its place: several skills, more than
one agent (still only one writer), a hook, an MCP server, a design doc, and — because
it's maintaining an older integration that predates this marketplace's skills-first
guidance — one legacy command it hasn't migrated yet. If you were adding this, it
would live at `plugins/incident-response/`.

```
plugins/incident-response/
├── .claude-plugin/
│   └── plugin.json
├── .cursor-plugin/
│   └── plugin.json
├── LICENSE
├── README.md
├── docs/
│   └── design.md
├── .mcp.json
├── skills/
│   ├── incident-triage/
│   │   └── SKILL.md
│   ├── runbook-lookup/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── runbook-index.md
│   └── postmortem-writing/
│       └── SKILL.md
├── agents/
│   ├── incident-investigator.md
│   └── postmortem-drafter.md
├── hooks/
│   ├── hooks.json
│   └── scripts/
│       └── log-incident-actions.sh
└── commands/
    └── legacy-page-oncall.md
```

## Why a design doc here but not in the standard example

Multiple skills interact with each other's output (triage feeds the investigator,
which feeds the postmortem drafter), there's a real external integration (MCP) with a
credential-handling story, and a hook that logs every action taken during an incident
for audit purposes. That's enough architectural surface — what talks to what, what's
deliberately out of scope (this plugin pages on-call, it doesn't resolve incidents
itself) — to be worth writing down once rather than re-deriving from the code on every
future change.

## Why two agents, still only one writer

- `agents/incident-investigator.md` — **read-only.** Gathers context (logs, recent
  deploys, related past incidents) and reports findings; never changes anything.
- `agents/postmortem-drafter.md` — **the one writer.** Creates the postmortem document
  from the investigator's findings, once a human has confirmed the incident is
  resolved. Every other agent in this plugin stays read-only specifically so this is
  the only place a file gets created.

## Why a hook here but not in the standard example

`hooks/hooks.json` registers a `PostToolUse` hook that appends every tool call made
during an active incident to an audit log — a genuine automatic, lifecycle-driven
need that no skill invoked by choice can satisfy, since the point is that it can't be
skipped. See `hook-development` for the secret-handling rules this hook's script
still has to follow (it logs *that* a command ran, never a credential the command
might have touched).

## Why MCP here but not in the standard example

`.mcp.json` connects to this org's paging/incident-management system so
`incident-triage` can read current on-call status without a human copy-pasting it in.
See `mcp-integration` for why this is a read path only — paging a human is still a
CLI/API call gated by explicit confirmation in the `incident-triage` skill's own body,
not something an MCP tool call does silently.

## Why one legacy command still exists here

`commands/legacy-page-oncall.md` predates this plugin's adoption of the skills-first
convention and a handful of on-call runbooks still reference it by its exact slash
command name. Per `command-development`, this is exactly the legitimate reason to keep
the legacy layout for one specific file rather than migrating it: an external
dependency on the old invocation, not a preference for the old shape.

Compare with [`minimal-plugin.md`](minimal-plugin.md) and
[`standard-plugin.md`](standard-plugin.md) — most plugins should look like one of
those two, not this one. Reach for this shape only when the roster above is
genuinely justified by real, current needs, not speculatively.
