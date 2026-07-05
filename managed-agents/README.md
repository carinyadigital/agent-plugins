# Managed Agents — deployment cookbooks

Cookbooks wire **catalogue plugins** to cloud platforms. Each cookbook points at the canonical
agent prompt in `agents/<slug>/` — it does not fork or vendor prompts in `carinyaparc`.

Instance binding (which agent, which repos, which schedule) lives in
`carinyaparc/config/deployments/` and is applied by `scripts/deploy-squad-agents.sh`.

## Placement matrix

| Platform | Agents | Notes |
| -------- | ------ | ----- |
| **Claude Managed Agents (CMA)** | `content-marketing` (personas) | Content personas; Anthropic admin API |
| **Cursor Cloud Agents** | `frontend-engineer`, `senior-frontend-engineer`, `principal-frontend-engineer`, `qa-engineer`, `webops-engineer` | Code, review, QA, platform; Cursor Automations API |
| **Either** | `principal-architect` | Architecture; resolve at deploy time |

Product Manager and Delivery Lead personas live in the **`delivery-practice`** plugin — invoke skills directly (`/delivery-practice:product`, `/delivery-practice:sprint`); no standalone agent plugin or CMA cookbook. SEO Specialist persona lives in **`search-optimisation`** — invoke skills directly (`/search-optimisation:keyword-research`, etc.); no standalone agent plugin or CMA cookbook.

Spike scope (Sprint 3): `frontend-engineer` only (product-manager and delivery-lead cookbooks retired with agent plugins).

## Cookbook layout

```
managed-agents/<slug>/
├── agent.yaml           # platform, prompt path, skills, connectors
├── README.md            # security tier + handoff notes
└── steering-examples.json   # optional CMA steering samples
```

## Deploy

```bash
# Plan changes (no side effects)
./scripts/deploy-squad-agents.sh --dry-run --instance ../carinyaparc

# Apply schedules (API or dashboard-import JSON)
./scripts/deploy-squad-agents.sh apply --instance ../carinyaparc

# Spike: weekly planning only
./scripts/deploy-squad-agents.sh apply --ritual weekly-planning --dry-run-first --instance ../carinyaparc

# Manual trigger (when platform supports run-now)
./scripts/deploy-squad-agents.sh apply --run-now --ritual weekly-planning --instance ../carinyaparc
```

Thin instance wrapper: `carinyaparc/scripts/deploy-agents.sh`.

## Required secrets (never commit)

Configure in Cursor dashboard or Claude CMA console — reference by name in deployment manifests only.

| Secret | Platform | Purpose |
| ------ | -------- | ------- |
| `CURSOR_API_TOKEN` | Cursor | Create/update Cloud Agent automations |
| `ANTHROPIC_ADMIN_KEY` | Claude CMA | Schedule Managed Agents |
| `GITHUB_TOKEN` | Both | Issues, PRs (via MCP or platform integration) |

Optional MCP secrets (per connector docs): `VERCEL_TOKEN`, `SENTRY_AUTH_TOKEN`, etc.

## API gap

Until Cursor/Anthropic schedule APIs are available in your workspace tier, `apply` writes
idempotent **dashboard-import JSON** to `{instance}/.deploy-artifacts/` for manual import.
`--dry-run` always works and is enforced in CI on deployment/cookbook changes.

## Validation

```bash
python3 scripts/validate.py                    # cookbook path + plugin slug checks
python3 ../carinyaparc/scripts/validate-deployments.py   # charter + target cross-check
```
