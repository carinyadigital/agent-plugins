# Migration: `carinyaparc/skills` → `carinyaparc/carinya-plugins`

The flat [carinyaparc/skills](https://github.com/carinyaparc/skills) repo is **archived** (read-only). All skills now live in practice plugins under [carinyaparc/carinya-plugins](https://github.com/carinyaparc/carinya-plugins).

## Install the new marketplace

```bash
/plugin marketplace add carinyaparc/carinya-plugins
/plugin install product-management@carinya-plugins
/plugin install product-engineering@carinya-plugins
# … install other practice plugins as needed
```

Marketplace name: **`carinya-plugins`** (formerly `carinya-digital` — no redirect; remove the old marketplace first).

## Skill address map

Every skill from the flat repo, mapped to its new home.

| Old skill (flat repo) | New slash command | New plugin | skills.sh subpath |
|---|---|---|---|
| `product` | `/product-management:product` | product-management | `product-management/skills/product` |
| `roadmap` | `/product-management:roadmap` | product-management | `product-management/skills/roadmap` |
| `tasks` | `/product-management:tasks` | product-management | `product-management/skills/tasks` |
| `backlog-refine` | `/product-management:backlog-refine` | product-management | `product-management/skills/backlog-refine` |
| `sprint-planning` | `/product-management:sprint-planning` | product-management | `product-management/skills/sprint-planning` |
| `sprint-retro` | `/product-management:sprint-retro` | product-management | `product-management/skills/sprint-retro` |
| `validate` | `/product-management:validate` | product-management | `product-management/skills/validate` |
| `solution` | `/product-engineering:solution` | product-engineering | `product-engineering/skills/solution` |
| `adr` | `/product-engineering:adr` | product-engineering | `product-engineering/skills/adr` |
| `tdd` | `/product-engineering:design` | product-engineering | `product-engineering/skills/design` |
| `implement` | `/product-engineering:implement` | product-engineering | `product-engineering/skills/implement` |
| `code-review` | `/product-engineering:code-review` | product-engineering | `product-engineering/skills/code-review` |
| `code-review-fix` | `/product-engineering:code-review-fix` | product-engineering | `product-engineering/skills/code-review-fix` |
| `merge-request` | `/product-engineering:merge-request` | product-engineering | `product-engineering/skills/merge-request` |
| `merge-request-babysit` | `/product-engineering:merge-request-babysit` | product-engineering | `product-engineering/skills/merge-request-babysit` |
| `merge-request-review` | `/product-engineering:merge-request-review` | product-engineering | `product-engineering/skills/merge-request-review` |
| `docs-review` | `/product-engineering:docs-review` | product-engineering | `product-engineering/skills/docs-review` |
| `ux-design-review` | `/product-design:ux-design-review` | product-design | `product-design/skills/ux-design-review` |
| `ux-design-fix` | `/product-design:ux-design-fix` | product-design | `product-design/skills/ux-design-fix` |
| `ralph-loop` | `/ralph-loop:ralph-loop` | ralph-loop | `ralph-loop/skills/ralph-loop` |
| `ralph-loop-setup` | `/ralph-loop:ralph-loop-setup` | ralph-loop | `ralph-loop/skills/ralph-loop-setup` |
| `skills-index` | `/skills-index:find` | skills-index | `skills-index/skills/find` |

### Renames and moves

| Change | Detail |
|---|---|
| `tdd` → `design` | Same skill, new name; lives in `product-engineering` |
| `skills-index` → `find` | Router skill renamed; install-aware routing |
| Delivery skills merged | `tasks`, `sprint-*`, `validate`, `backlog-refine` moved from delivery-practice into `product-management` |
| UX skills split out | `ux-design-review`, `ux-design-fix` moved to `product-design` |
| Ralph extracted | `ralph-loop` + hooks in dedicated `ralph-loop` plugin |

### New skills (not in flat repo)

These ship only in `carinya-plugins`:

| Plugin | Skills |
|---|---|
| product-management | `write-spec`, `product-brainstorming`, `synthesize-research`, `competitive-brief`, `metrics-review`, `stakeholder-update` |
| product-engineering | `final-code-review`, `debug`, `tech-debt`, `deploy-qa`, `run-automated-suite`, `exploratory-pass`, `document-defects`, `platform-health` |
| product-design | `wireframe` |
| brand-creative | `setup`, `brand-voice`, `brand-guide` |
| content-marketing | 8 content skills |
| search-optimisation | 4 SEO skills |
| skill-authoring | `skills-qa` |
| skills-index | `related-skills-surfacer` (absorbed into `find`) |

## skills.sh install (skill files only)

```bash
# Replaces: npx skills add carinyaparc/skills/code-review
npx skills add carinyaparc/carinya-plugins/product-engineering/skills/code-review

# Replaces: npx skills add carinyaparc/skills
npx skills add carinyaparc/carinya-plugins
```

See [SKILLS-SH.md](./SKILLS-SH.md) for the full distribution decision.

## Archive checklist (maintainer)

Apply on `carinyaparc/skills` before or when archiving:

1. Replace `README.md` with [archive README template](./archive/carinyaparc-skills-README.md).
2. Add a one-line freeze notice at the top of the old README commit message.
3. GitHub → Settings → Archive this repository (read-only; preserves clone URLs).
4. Do **not** delete — install URLs are in the wild.
