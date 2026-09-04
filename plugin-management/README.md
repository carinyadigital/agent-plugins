# plugin-management

Create, customize, and manage plugins for the `agent-plugins` marketplace — end to end, with manifests, skills, agents, hooks, MCP connectors, marketplace registration, release, and skill quality gates. Built for Claude Cowork and Cursor.

## Overview

`plugin-management` is a meta-plugin: it turns the agent into a specialist at building and adapting plugins. It ships two guided workflow skills, nine component-authoring skills, two skill-quality skills (from the former `skill-authoring` plugin), and five sub-agents.

**Workflow skills** — the two entry points most people start from:

1. **`create-plugin`** — guided multi-phase workflow to build a whole new plugin from an idea.
2. **`customize-plugin`** — adapt an existing plugin to an organization's tools, terminology, and ways of working.

**Component-authoring skills:**

3. **`plugin-structure`** — dual Claude/Cursor manifest pair and plugin-root layout.
4. **`skill-development`** — portable `SKILL.md` authoring.
5. **`command-development`** — legacy `commands/*.md` layout when still needed.
6. **`agent-development`** — sub-agent frontmatter and read-only-vs-writer split.
7. **`hook-development`** — `hooks/hooks.json` event types and never-echo-secrets.
8. **`mcp-integration`** — `.mcp.json` server types and least-privilege scoping.
9. **`plugin-settings`** — per-project `.local.md` configuration.
10. **`plugin-portability`** — host-neutral content across Cowork, Cursor, and Agent Skills runtimes.
11. **`marketplace-and-release`** — catalogue registration and release.

**Skill quality gates** (former `skill-authoring`):

12. **`skills-qa`** — evaluate a skill against the Agency Skill Design Framework.
13. **`skill-review`** — research, review, and enhance skills on a cadence.

```
/plugin-management:create-plugin
/plugin-management:customize-plugin
/plugin-management:skills-qa path/to/SKILL.md
/plugin-management:skill-review implement
```

## Agents

| Agent | Read/write | Purpose |
| ----- | ---------- | ------- |
| `component-recommender` | Read-only | Scan a target codebase; recommend which components to ship |
| `plugin-validator` | Read-only | Audit a plugin directory against structure rules |
| `skill-reviewer` | Read-only | Review a `SKILL.md` for trigger quality and structure |
| `plugin-scaffolder` | Read + write | Create plugin files from a confirmed component plan |
| `eval-grader` | Read-only | Grade skill eval runs against `evals/evals.json` assertions |

## Tooling

| Script | Purpose |
| ------ | ------- |
| `scripts/validate_ralph.py` | Ralph hooks, preset graphs, epic-path script |
| `scripts/mutation-test.py` | Mutation tests for Ralph hook suites (`ralph-loop/`) |

Run from repo root:

```bash
python3 plugin-management/scripts/validate_ralph.py
python3 plugin-management/scripts/mutation-test.py
python3 scripts/validate_plugins.py plugin-management
python3 scripts/validate.py
```

## References and templates

- `references/agency-skill-design-framework.md` — design parameters and verdict bands
- `spec/agent-skills-spec.md` — local Agent Skills spec notes
- `template/SKILL.md` — starter template for new skills

## Install

```bash
/plugin marketplace add carinyadigital/agent-plugins
/plugin install plugin-management@agent-plugins
```

**Migration from `skill-authoring`:** uninstall `skill-authoring@agent-plugins` and install `plugin-management@agent-plugins`. Slash namespace changed from `/skill-authoring:` to `/plugin-management:`.

## License

[Apache License 2.0](./LICENSE)
