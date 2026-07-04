# Eval baselines — Sprint 4

Sprint 4 adds `evals/evals.json` and `trigger-queries.json` for content, SEO, and
top-used engineering skills. Run **plugin-eval** (`.agents/skills/plugin-eval/SKILL.md`)
against each path before merging skill changes.

## Coverage matrix

| Skill | Path | Evals | Strict frontmatter | Baseline status |
| ----- | ---- | ----- | ------------------ | --------------- |
| content-calendar | `skills/content/skills/content-calendar` | 2 | yes | schema only — live run pending |
| draft-post | `skills/content/skills/draft-post` | 1 | yes | schema only |
| draft-recipe | `skills/content/skills/draft-recipe` | 1 | yes | schema only |
| analyse-media | `skills/content/skills/analyse-media` | 1 | yes | schema only |
| write-captions | `skills/content/skills/write-captions` | 1 | yes | schema only |
| edit-content | `skills/content/skills/edit-content` | 1 | yes | schema only |
| curate-content | `skills/content/skills/curate-content` | 1 | yes | schema only |
| keyword-research | `skills/seo/skills/keyword-research` | 1 | yes | schema only |
| technical-seo-audit | `skills/seo/skills/technical-seo-audit` | 1 | yes | schema only |
| content-seo-review | `skills/seo/skills/content-seo-review` | 1 | yes | schema only |
| implement | `skills/engineering/skills/implement` | 1 | yes | schema only |
| code-review | `skills/engineering/skills/code-review` | 2 | yes | schema only |
| create-mr | `skills/engineering/skills/create-mr` | 1 | yes | schema only |

## Prior baselines (Sprints 1–3)

| Skill | Path | Baseline status |
| ----- | ---- | --------------- |
| design | `skills/engineering/skills/design` | schema only |
| backlog | `skills/product-management/skills/backlog` | schema only |
| tasks | `skills/product-management/skills/tasks` | schema only |
| validate | `skills/product-management/skills/validate` | schema only |

## Assertion sources

Content skill assertions incorporate steward quality checklists from
`skills/content/references/prompt-refinement.md` (ported from steward SW-06-07).

## Running evals

```bash
cd "$(git rev-parse --show-toplevel)"
python3 scripts/validate.py          # structural + evals schema
python3 scripts/validate.py --strict # Sprint 4 skills pass; legacy skills warn until phased
```

Invoke plugin-eval per skill path. Write results to `.notes/COVERAGE.md` after live runs.

## CI note

CI runs `validate.py` without `--strict`. Enable `--strict` repo-wide once all skills
ship agency-framework frontmatter (17/29 at Sprint 4 exit).
