# architecture

Root-level **practice plugin** — setup interview, system solution design
(arc42-lite), and architecture decision records. Self-contained under the MECE
practice model: edit skills here only; nothing is vendored from elsewhere.

Install standalone or after practice `setup` (writes `config/instance.json` if
absent) recommends it. Declare `engineering` as a **companion practice**
for work-item `tdd.md`, docs review, and implementation — invoke
`/engineering:tdd` and related skills directly rather than bundling
duplicates.

## Persona

| Persona | Primary skills | Focus |
| ------- | -------------- | ----- |
| **Principal Architect** | `solution`, `adr` | Architecture — solution.md and ADRs |

Work-item technical design stays in `engineering` (`tdd`). Document-set
quality review stays in `engineering` (`docs-review`).

```
/architecture:solution
/architecture:adr plan
/architecture:adr write
```

For work-item design and delivery:

```
/engineering:tdd checkout-foundation
/engineering:implement CHK01-01
/engineering:docs-review docs/architecture/
```

## First run: setup

After instance bootstrap (or standalone):

```
/architecture:setup
```

| Flag | Behaviour |
| ---- | --------- |
| `--quick` | Defaults for target binding and companion install notes |
| `--full` | Full interview including architecture scope and connector audit |
| `--redo` | Re-run architecture setup only; overwrite on confirmation |
| `--resume` | Continue a paused interview |
| `--check-integrations` | Report MCP connector status only; no interview |

## Skills

| Skill | Purpose |
| ----- | ------- |
| **setup** | Interview → write practice profile and target hints |
| **solution** | write — `docs/architecture/solution.md`; review via `/engineering:docs-review` |
| **adr** | plan, write, review — `docs/architecture/decisions/` |

Path and boundary rules: `references/architecture-conventions.md`.

## Prerequisites

- **Instance profile** (optional) — practice `setup` writes `config/instance.json`
  if absent; setup reads cadence and target hints without re-asking.
- **engineering** (recommended companion) — `tdd`, `docs-review`,
  `implement`, and related delivery skills; see CONNECTORS.md.
- **product-management** (optional companion) — product.md / roadmap upstream of
  solution.
- **Connectors** (optional) — source-control MCP supercharges ADR harvest when a
  work-id is named.

## After setup

1. Run `/architecture:solution` (stub or full) for system architecture.
2. Run `/architecture:adr plan` then `adr write` for consequential decisions.
3. Hand off work-item design to `/engineering:tdd`.
4. Re-run `/architecture:setup --redo` to refresh architecture defaults.

## References

- `references/practice-setup-framework.md` — invocation, config paths, interview structure
- `references/architecture-conventions.md` — path resolution, artefact boundaries
- `references/work-item-resolution.md` — work-id resolution for `adr plan <work-id>`
- `references/instance-profile-template.md` — Tier 1 schema (canonical in brand-creative; synced copy)

Meta-framework files (`instance-profile-template.md`, `practice-setup-framework.md`)
are kept in sync across practice plugins via `python3 scripts/sync-references.py`.
