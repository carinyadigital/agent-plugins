# Architecture conventions

Canonical rules for paths, artefact boundaries, and skill routing. All
`architecture` skills read this file when resolving paths or routing near-miss
requests.

## Target binding

Resolve the working target before writing architecture artefacts. Apply this
order — first match wins:

1. **Explicit path named by the user** in the request.
2. **Inside a target repo** — `config/target.json` exists at the working
   root → read the pointer, resolve instance root and target metadata.
3. **Inside an instance repo** — `config/instance.json` at working root → use
   `config/targets/{target}.json` when the user names a target slug.
4. **Standalone** — no instance or target pointer → treat the current project as
   the target; read `AGENTS.md` / `CLAUDE.md` for local conventions.

## Document layout

```text
docs/product/                 product.md, roadmap.md, backlog.md
docs/architecture/            solution.md, decisions/register.md, ADR-NNNN-*.md
specs/{work-short-name}/          tdd.md; TASKS.local.md when required  (owned by engineering / product-management)
```

Write architecture artefacts under `docs/architecture/`.

Override paths when the user names them explicitly in the request.

## Artefact boundaries

| Content | Belongs in | Not in |
| ------- | ---------- | ------ |
| Architecture, NFRs, cross-epic patterns | `docs/architecture/solution.md` | tdd.md (cite only) |
| ADR decisions | `docs/architecture/decisions/` | solution narrative |
| Work-item implementation spec | `specs/{work-short-name}/tdd.md` | solution, backlog |
| Business strategy, personas, outcomes | `docs/product/product.md` | solution |
| Task Gherkin AC | `specs/{work-short-name}/TASKS.local.md` | solution |

## Companion practices

| Need | Invoke |
| ---- | ------ |
| Work-item technical design (`tdd.md`) | `/engineering:tdd` |
| Document-set quality review | `/engineering:docs-review` |
| Implementation | `/engineering:implement` |
| Product strategy / roadmap | `/product-management:product`, `/product-management:roadmap` |
| Epics / tasks / AC | `/product-management:tasks` |

When a companion plugin is **not installed**, do not emit a bare slash command.
State what you can do without it, then:

```text
Install: /plugin install <plugin>@carinya-plugins
Then run: /<plugin>:<skill> …
```

See `docs/CROSS-PLUGIN-CONTRACTS.md` (monorepo) for the full edge list.

## Skill routing (near-misses)

| User intent | Skill | Notes |
| ----------- | ----- | ----- |
| System architecture / arc42 | **solution** | Writes `docs/architecture/solution.md` |
| ADR plan / write / review | **adr** | Register + `ADR-NNNN-*.md` |
| Work-item `tdd.md` | `/engineering:tdd` | Companion — not this practice |
| Docs quality / consistency | `/engineering:docs-review` | Companion |
| Tech debt audit | `/engineering:tech-debt` | Companion |
| Implement code | `/engineering:implement` | Companion |

## Work-item resolution

When `adr plan <work-id>` harvests from a work item, resolve the ID per
[work-item-resolution.md](work-item-resolution.md) before reading `tdd.md`.
