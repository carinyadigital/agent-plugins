# product-manager — Managed Agent cookbook

**Platform:** Claude CMA  
**Security tier:** standard — read/write repo docs; no production secrets in prompt

## Handoff

- Writes strategy artefacts under `docs/product/` and `docs/work/` on target repos
- Does not implement code or open merge requests without explicit task scope
- Weekly planning spike: runs `backlog` refine phase only (see `carinyaparc/config/cadence/weekly-planning.md`)

## Instance resolution

Read `carinyaparc/config/instance.json` and target `.carinyaparc/target.json` before any artefact work.
