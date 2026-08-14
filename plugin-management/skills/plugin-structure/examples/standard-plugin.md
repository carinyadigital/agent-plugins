# Worked example: a standard, multi-skill plugin

Most plugins that outgrow a single skill land here: a few related skills, one
sub-agent, a real README, no hooks or MCP because nothing yet needs them. If you were
adding this, it would live at `plugins/pr-review-helper/`.

```
plugins/pr-review-helper/
├── .claude-plugin/
│   └── plugin.json
├── .cursor-plugin/
│   └── plugin.json
├── LICENSE
├── README.md
├── skills/
│   ├── review-checklist/
│   │   └── SKILL.md
│   ├── review-comment-style/
│   │   └── SKILL.md
│   └── flaky-test-triage/
│       └── SKILL.md
└── agents/
    └── pr-reviewer.md
```

## Why three skills instead of one big one

Each skill covers a distinct triggering scenario with its own description, so the
agent loads only the one that matches — a reviewer asking about comment tone doesn't
need the flaky-test triage logic pulled in too. See the `skill-development` skill for
how to decide where one skill's scope ends and another's begins: if two topics are
never relevant to the same task, they're two skills, not one with a long body.

## Why one agent, not zero and not three

`agents/pr-reviewer.md` exists because this plugin benefits from a persona distinct
from the general agent — an adversarial reviewer that reads a diff and nothing else,
scoped to read-only tools. It's the only agent because nothing else in this plugin
yet needs a dedicated persona; see `agent-development`'s read-only-vs-writer guidance
for when a second agent (typically the one writer) becomes justified — not needed
here since this plugin never writes anything, only reviews.

## Why still no hooks, MCP, or `docs/design.md`

- **No hooks** — nothing in this plugin needs to run automatically on a lifecycle
  event; every skill here is invoked by the agent choosing to use it.
- **No MCP** — the review skills work from files already in the working tree
  (the diff, the repo) with no external system to connect to.
- **No `docs/design.md`** — three skills and one agent is not enough architectural
  complexity to justify a standalone design doc; the `README.md` below is enough
  context for a future maintainer.

## `README.md` (excerpt)

```markdown
# PR Review Helper

Three skills for reviewing pull requests plus a dedicated review agent:

- `review-checklist` — the checklist to run before approving.
- `review-comment-style` — how to phrase review comments (blocking vs. nit).
- `flaky-test-triage` — deciding whether a failing test is flaky or a real regression.
- `agents/pr-reviewer.md` — a read-only agent that runs all three against a diff.
```

Compare with [`minimal-plugin.md`](minimal-plugin.md) for when a plugin doesn't need
this much structure, and [`advanced-plugin.md`](advanced-plugin.md) for the point at
which hooks, MCP, and a design doc do earn their place.
