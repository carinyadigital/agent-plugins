# Contributing to Digital Agency

Everything in this repo is markdown and JSON — no build step. Fork, edit, open a PR.

## Layout

```text
<practice>/                   # practice plugins — self-contained skill libraries
  skills/<name>/
    SKILL.md
    prompts/
    agents/                   # sub-agents scoped to this skill
    evals/                    # evals.json + trigger-queries.json
    scripts/                  # optional helper scripts
  references/                 # practice conventions + synced meta-framework files
  .claude-plugin/plugin.json
  .cursor-plugin/plugin.json
  .mcp.json

brand-creative/                   # instance bootstrap + marketplace management (install first)

scripts/
  sync-references.py          # propagate shared meta-framework files across practice plugins
  validate.py                 # orchestrator — runs plugins + skills validators (before PR)
  validate_plugins.py         # marketplace, manifests, MCP, cookbooks; scoped mode for one plugin
  validate_skills.py          # frontmatter budgets, agents/*.md contracts, orphans, drift, evals
  validate_lib.py             # shared reporting + YAML frontmatter helpers

.cursor-plugin/marketplace.json
.claude-plugin/marketplace.json
```

**Source of truth:** edit skills in the owning practice plugin's `skills/` directory. Practice plugins own their skills outright — there is no separate sync step after skill edits.

## Changing a skill

1. Edit `<practice>/skills/<name>/`.
2. Update the skill `description` in frontmatter when routing or scope changes.
3. Test in Cowork or Cursor — install the practice plugin and invoke the skill directly.

## Adding a skill

1. Create `<practice>/skills/<name>/SKILL.md` (and optional `prompts/`, `agents/`, `evals/`, `scripts/`).
2. Add `evals/evals.json` and `evals/trigger-queries.json` to define test cases and routing expectations.
3. Follow [skill-authoring/references/agency-skill-design-framework.md](./skill-authoring/references/agency-skill-design-framework.md) for skill design conventions.
4. Register it in the practice plugin's `plugin.json` if needed.
5. Run `python3 scripts/validate.py` and fix errors.

## Adding or changing a practice plugin

1. Add `<practice>/` with `skills/`, `references/`, `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and `.mcp.json`.
2. Register the plugin in `.cursor-plugin/marketplace.json` and `.claude-plugin/marketplace.json` (keep `name` and `description` in sync with each plugin's `plugin.json`).
3. Run `python3 scripts/validate.py`.

Follow existing practice plugins (e.g. `product-management/`, `product-engineering/`, `brand-creative/`) for structure and naming.

## Adding or changing MCP servers

1. Edit `<practice>/.mcp.json` — add or update entries under `mcpServers`.
2. Update `<practice>/CONNECTORS.md` so category placeholders and bundled providers stay in sync.
3. Do not commit secrets or API keys — use env var placeholders where providers require auth.
4. Run `python3 scripts/validate.py`.

Follow existing practice plugins (e.g. `product-engineering/.mcp.json`) for structure and naming.

## Syncing shared references

After editing shared meta-framework files in `references/` (`instance-profile-template.md`, `practice-setup-framework.md`):

```bash
python3 scripts/sync-references.py        # propagate to practice plugin copies
python3 scripts/sync-references.py --check  # verify copies are in sync (CI-friendly)
```

## Validation

Run structural checks locally before opening a PR:

```bash
python3 scripts/validate.py                    # full repo validation (plugins + skills)
python3 scripts/validate_plugins.py <dir>      # scoped check for one practice plugin
python3 scripts/validate_skills.py             # skill/agent contracts only
python3 skill-authoring/scripts/validate_ralph.py  # Ralph hooks + presets
```

`validate.py` orchestrates plugin-domain and skill-domain checks:

| Check | What it catches |
| ----- | ---------------- |
| Marketplace manifests | Invalid JSON, duplicate plugin names, slug format, description length, missing source dirs |
| Marketplace parity | Claude ↔ Cursor marketplace lists out of sync |
| Marketplace ↔ plugin.json | `name` / `description` drift between marketplace and per-plugin manifests |
| Plugin manifests | Missing `name`, `version`, or `description` |
| MCP connectors | Missing or invalid practice `.mcp.json`; empty `mcpServers` |
| SKILL.md frontmatter | Missing `name`/`description`/`allowed-tools`; name/description budgets; agency metadata (warnings by default) |
| Agent contracts | Every `**/agents/*.md`: `model: inherit`, constrained tools, `model_tier`, numeric `budget` |
| Orphan SKILL.md | `SKILL.md` outside `skills/<name>/` (excl. `skill-authoring/template/`) |
| Markdown cross-refs | Broken relative links in skill files |
| Evals schema | Malformed `evals/evals.json` or `evals/trigger-queries.json` |
| JSON sanity | Any `*.json` in the repo that fails to parse |
| Cross-plugin paths | Sibling-plugin `../` references inside plugin trees (cache-unsafe) |
| Legacy artefact paths | References to the retired digital-agency dotted path prefix |

Options:

```bash
python3 scripts/validate.py --format json   # machine-readable report for CI
python3 scripts/validate.py --strict        # agency-framework frontmatter gaps → errors
python3 scripts/validate.py --skip-drift    # skip bundled-skill drift (faster local pass)
```

Fix marketplace ↔ plugin.json description drift by updating both manifests together
when you change a plugin description.

### CI

- **CI** — `.github/workflows/ci.yml` runs `python3 scripts/validate.py --format json`,
  `python3 skill-authoring/scripts/validate_ralph.py --quiet`, mutation tests, and
  the unit tests in `tests/` on every push to `main` and on pull requests.

## Pull requests

- Run `python3 scripts/sync-references.py` after editing shared meta-framework reference files.
- Run `python3 scripts/validate.py` and fix all errors before pushing.
- Register new plugins in both marketplace manifests.
- Add or update `evals/evals.json` and `evals/trigger-queries.json` for any new or changed skill; run `python3 scripts/validate.py`.
- Describe what workflow or skill behaviour changed and how you tested it (Cowork, Cursor, or local install).
- Keep changes focused — one skill or practice plugin per PR when possible.

## Local config

User-specific overrides belong in `*.local.md` files (gitignored). Do not commit credentials or client data.
