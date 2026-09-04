# architecture

Root-level **practice plugin** — setup interview, system architecture
(arc42), and architecture decision records. Self-contained under the MECE
practice model: edit skills here only; nothing is vendored from elsewhere.

Install standalone or after practice `setup` (writes `config/instance.json` if
absent) recommends it. Declare `engineering` as a **companion practice**
for work-item `design.md`, docs review, and implementation — invoke
`/engineering:design` and related skills directly rather than bundling
duplicates.

## Persona

| Persona | Primary skills | Focus |
| ------- | -------------- | ----- |
| **Principal Architect** | `solution`, `adr` | Architecture — `ARCHITECTURE.md` and ADRs |

Work-item technical design stays in `engineering` (`design`). Document-set
quality review stays in `engineering` (`docs-review`).

```
/architecture:solution
/architecture:solution --state target
/architecture:adr plan
/architecture:adr write
```

For work-item design and delivery:

```
/engineering:design checkout-foundation
/engineering:implement CHK01-01
/engineering:docs-review ARCHITECTURE.md
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
| **solution** | write — `ARCHITECTURE.md` at the repo root (current or target); review via `/engineering:docs-review` |
| **adr** | plan, write, review — `docs/decisions/` |

Path and boundary rules: `references/architecture-conventions.md`.

## Prerequisites

- **Instance profile** (optional) — practice `setup` writes `config/instance.json`
  if absent; setup reads cadence and target hints without re-asking.
- **engineering** (recommended companion) — `design`, `docs-review`,
  `implement`, and related delivery skills; see CONNECTORS.md.
- **product-management** (optional companion) — product.md / roadmap upstream of
  architecture.
- **Connectors** (optional) — source-control MCP supercharges ADR harvest when a
  work-id is named.

## After setup

1. Run `/architecture:solution` for as-is architecture, or
   `/architecture:solution --state target` at project start.
2. Run `/architecture:adr plan` then `adr write` for consequential decisions.
3. Hand off work-item design to `/engineering:design`.
4. Re-run `/architecture:setup --redo` to refresh architecture defaults.

## References

- `references/architecture-conventions.md` — path resolution, artefact boundaries
- `references/work-items.md` — work-id resolution and schema for `adr plan <work-id>`
