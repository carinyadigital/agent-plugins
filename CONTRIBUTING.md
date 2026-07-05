# Contributing to Digital Agency

Everything in this repo is markdown and JSON — no build step. Fork, edit, open a PR.

## Layout

```text
agents/<slug>/                # named agents — self-contained plugins
  agents/<slug>.md            # system prompt (canonical)
  skills/                     # bundled copies — do not edit directly
  .claude-plugin/plugin.json
  .cursor-plugin/plugin.json

skills/<discipline>/        # skill and command sources
  skills/<name>/
    SKILL.md
    prompts/
    agents/                 # sub-agents scoped to this skill
    evals/                  # evals.json + trigger-queries.json
    scripts/                # optional helper scripts
  commands/

managed-agents/<slug>/        # Managed Agent cookbooks (agent.yaml, subagents, …)

scripts/
  sync-agent-skills.py        # propagate skills/ → agents/*/skills/
  validate.py                 # structural repo validation (run before PR)

.cursor-plugin/marketplace.json
.claude-plugin/marketplace.json
```

**Source of truth:** edit skills under `skills/`, not under `agents/`. Agent plugins bundle synced copies so they stay installable on their own. Edit MCP connectors under `connectors/`, not in agent bundles.

## Changing a skill

1. Edit `skills/<discipline>/skills/<name>/`.
2. Update the skill `description` in frontmatter when routing or scope changes.
3. Run sync to propagate into every agent that bundles it:

   ```bash
   python3 scripts/sync-agent-skills.py
   ```

4. Test in Cowork or Cursor — install the skill plugin or an agent that bundles the skill.

## Adding a skill

1. Create `skills/<discipline>/skills/<name>/SKILL.md` (and optional `prompts/`, `agents/`, `evals/`, `scripts/`).
2. Add `evals/evals.json` and `evals/trigger-queries.json` to define test cases and routing expectations.
3. Follow [agency-hub/references/agency-skill-design-framework.md](./agency-hub/references/agency-skill-design-framework.md) for skill design conventions.
4. Register it in the discipline plugin’s `plugin.json` if needed.
5. Add a bundled copy to any agent that should use it under `agents/<slug>/skills/<name>/`.
6. Run `python3 scripts/sync-agent-skills.py`.
7. Run `python3 scripts/validate.py` and fix errors.

## Adding or changing an agent

1. Add `agents/<slug>/` with:
   - `agents/<slug>.md` — system prompt
   - `skills/` — bundled skills (synced from discipline plugins under `skills/<discipline>/`)
   - `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`
2. Register the plugin in `.cursor-plugin/marketplace.json` and `.claude-plugin/marketplace.json` (keep `name` and `description` in sync with each plugin's `plugin.json`).
3. Add a matching `managed-agents/<slug>/` when Managed Agent deployment is in scope.
4. Run `python3 scripts/validate.py`.

Follow existing agents (e.g. `agents/frontend-engineer/`, `agents/principal-architect/`, `agents/delivery-lead/`) for structure and naming. See the [Agents roster](../../AGENTS.md#agents-current-roster) in `AGENTS.md`.

## Adding or changing a connector

1. Add `connectors/<slug>/` with:
   - `.mcp.json` — one MCP server definition
   - `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json` with `"mcpServers": "./.mcp.json"`
2. Register the plugin in both marketplace manifests (keep fields in sync with `plugin.json`).
3. Do not commit secrets or API keys — use env var placeholders where providers require auth.
4. Run `python3 scripts/validate.py`.

Follow existing connectors (e.g. `connectors/github/`) for structure and naming.

## Commands and connectors

- **Commands** — slash actions live in `skills/<discipline>/commands/`. Invoked as `/plugin:command-name` in Cowork.
- **MCP connectors** — one provider per plugin under `connectors/<slug>/.mcp.json`. Point entries at your providers; do not commit secrets or API keys.

## Validation

Run structural checks locally before opening a PR:

```bash
python3 scripts/sync-agent-skills.py   # after any skill edit under skills/
python3 scripts/validate.py            # full repo validation
```

`validate.py` checks:

| Check | What it catches |
| ----- | ---------------- |
| Marketplace manifests | Invalid JSON, duplicate plugin names, slug format, description length, missing source dirs |
| Marketplace parity | Claude ↔ Cursor marketplace lists out of sync |
| Marketplace ↔ plugin.json | `name` / `description` drift between marketplace and per-plugin manifests |
| Plugin manifests | Missing `name`, `version`, or `description` |
| MCP connectors | Missing or invalid `.mcp.json`; connector manifests without `mcpServers` |
| SKILL.md frontmatter | Missing `name`, `description`, or `allowed-tools`; invalid agency-framework metadata (warnings by default) |
| Markdown cross-refs | Broken relative links in skill and agent prompt files |
| Agent prompts | Missing `agents/<slug>/agents/<slug>.md` |
| Bundled skill drift | `agents/*/skills/*` differs from `skills/*/skills/*` source |
| Evals schema | Malformed `evals/evals.json` or `evals/trigger-queries.json` |
| JSON sanity | Any `*.json` in the repo that fails to parse |

Options:

```bash
python3 scripts/validate.py --format json   # machine-readable report for CI
python3 scripts/validate.py --strict        # agency-framework frontmatter gaps → errors
python3 scripts/validate.py --skip-drift    # skip bundled-skill drift (faster local pass)
```

Fix marketplace ↔ plugin.json description drift by updating both manifests together
when you change a plugin description.

### CI and local hooks

- **CI** — `.github/workflows/validate.yml` runs `python3 scripts/validate.py --format json`
  and the unit tests in `tests/` on every push to `main` and on pull requests.
- **Pre-commit** — install a git hook that runs the same validation before each commit:

  ```bash
  scripts/install-git-hooks.sh
  ```

  The hook lives at `scripts/git-hooks/pre-commit` and is copied into `.git/hooks/`.

## Pull requests

- Run `python3 scripts/sync-agent-skills.py` after any skill change under `skills/`.
- Run `python3 scripts/validate.py` and fix all errors before pushing.
- Register new plugins in both marketplace manifests.
- Add or update `evals/evals.json` and `evals/trigger-queries.json` for any new or changed skill; run `python3 scripts/validate.py`.
- Describe what workflow or agent behaviour changed and how you tested it (Cowork, Cursor, or local install).
- Keep changes focused — one skill, agent, discipline, or connector per PR when possible.

## Local config

User-specific overrides belong in `*.local.md` files (gitignored). Do not commit credentials or client data.
