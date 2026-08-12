# skills.sh distribution decision

**Decision (Phase 4):** Keep the [vercel-labs/skills](https://github.com/vercel-labs/skills) channel. Do **not** maintain a flattened mirror branch.

## Verification

Tested 12 Aug 2026 with `npx skills@latest`:

| Command | Result |
|---|---|
| `npx skills add carinyaparc/carinya-plugins --list` | Found **53 skills** across all practice plugins |
| `npx skills add carinyaparc/carinya-plugins/product-engineering/skills/code-review --list` | Found **1 skill** (`code-review`) |
| `npx skills add carinyaparc/skills/code-review --list` | Still resolves the **legacy flat repo** (deprecated) |

The CLI clones the GitHub repo and discovers `SKILL.md` files. Subpath syntax (`owner/repo/path/to/skill-dir`) works for monorepo installs — no flattening required.

## Install commands (canonical)

```bash
# All skills from the monorepo
npx skills add carinyaparc/carinya-plugins

# One skill
npx skills add carinyaparc/carinya-plugins/product-engineering/skills/code-review

# One plugin's skills
npx skills add carinyaparc/carinya-plugins/product-management/skills/tasks
```

Prefer **marketplace plugins** (`/plugin install product-engineering@carinya-plugins`) when you want hooks, MCP connectors, and practice profiles — skills.sh installs skill files only.

## Legacy flat repo

`carinyaparc/skills` used flat paths like `npx skills add carinyaparc/skills/code-review`. That repo is archived; see [SKILLS-MIGRATION.md](./SKILLS-MIGRATION.md) for the skill → plugin address map.

## Rejected alternatives

| Alternative | Why not |
|---|---|
| Flattened mirror branch | Hand-maintained second library; CLI already supports subpaths |
| Drop skills.sh entirely | Low cost to keep; useful for skill-only installs without full plugin surface |
