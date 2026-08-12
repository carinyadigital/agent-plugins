# ⚠️ Archived — moved to carinya-plugins

**This repository is archived and read-only.**

All skills have moved to [carinyaparc/carinya-plugins](https://github.com/carinyaparc/carinya-plugins) as practice plugins on the **`carinya-plugins`** marketplace.

## Install the new marketplace

```bash
/plugin marketplace add carinyaparc/carinya-plugins
/plugin install product-management@carinya-plugins
/plugin install product-engineering@carinya-plugins
```

Full migration guide: [docs/SKILLS-MIGRATION.md](https://github.com/carinyaparc/carinya-plugins/blob/main/docs/SKILLS-MIGRATION.md)

## Skill address map

| Old skill | New command |
|---|---|
| `product` | `/product-management:product` |
| `roadmap` | `/product-management:roadmap` |
| `tasks` | `/product-management:tasks` |
| `backlog-refine` | `/product-management:backlog-refine` |
| `sprint-planning` | `/product-management:sprint-planning` |
| `sprint-retro` | `/product-management:sprint-retro` |
| `validate` | `/product-management:validate` |
| `solution` | `/product-engineering:solution` |
| `adr` | `/product-engineering:adr` |
| `tdd` | `/product-engineering:design` |
| `implement` | `/product-engineering:implement` |
| `code-review` | `/product-engineering:code-review` |
| `code-review-fix` | `/product-engineering:code-review-fix` |
| `merge-request` | `/product-engineering:merge-request` |
| `merge-request-babysit` | `/product-engineering:merge-request-babysit` |
| `merge-request-review` | `/product-engineering:merge-request-review` |
| `docs-review` | `/product-engineering:docs-review` |
| `ux-design-review` | `/product-design:ux-design-review` |
| `ux-design-fix` | `/product-design:ux-design-fix` |
| `ralph-loop` | `/ralph-loop:ralph-loop` |
| `ralph-loop-setup` | `/ralph-loop:ralph-loop-setup` |
| `skills-index` | `/skills-index:find` |

## skills.sh (skill files only)

```bash
# Replaces: npx skills add carinyaparc/skills/code-review
npx skills add carinyaparc/carinya-plugins/product-engineering/skills/code-review
```

Do not install from this archived repo.
