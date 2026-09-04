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
ARCHITECTURE.md               system architecture (arc42)
docs/product/                 product.md, roadmap.md, backlog.md
docs/decisions/               register.md, ADR-NNNN-*.md
specs/{work-short-name}/      design.md; TASKS.local.md when required  (owned by engineering / product-management)
```

Write the architecture narrative at repo-root `ARCHITECTURE.md`. Write ADRs
under `docs/decisions/`. Leftover `docs/architecture/decisions/` is a read
fallback only; the `adr` skill migrates it into `docs/decisions/`.

Override paths when the user names them explicitly in the request.

## Architecture file — read / write

**Write** (`/architecture:solution`):

1. Path the user named.
2. `ARCHITECTURE.md` at the target repo root.

**Read** (any skill consuming architecture):

1. Path the user named.
2. `artefactPaths.architecture` from bound target config, if present.
3. `ARCHITECTURE.md` at the target repo root.
4. Legacy `docs/architecture/solution.md` — treat as superseded; the
   `solution` skill migrates it into `ARCHITECTURE.md`.

## Artefact boundaries

| Content | Belongs in | Not in |
| ------- | ---------- | ------ |
| Architecture, NFRs, cross-epic patterns | `ARCHITECTURE.md` | design.md (cite only) |
| ADR decisions | `docs/decisions/` | `ARCHITECTURE.md` |
| Work-item implementation spec | `{work-dir}/design.md` | architecture, backlog |
| Business strategy, personas, outcomes | `docs/product/product.md` | architecture |
| Task Gherkin AC | `specs/{work-short-name}/TASKS.local.md` | architecture |

## Companion practices

| Need | Invoke |
| ---- | ------ |
| Work-item technical design (`design.md`) | `/engineering:design` |
| Document-set quality review | `/engineering:docs-review` |
| Implementation | `/engineering:implement` |
| Product strategy / roadmap | `/product-management:product`, `/product-management:roadmap` |
| Epics / tasks / AC | `/product-management:tasks` |

When a companion plugin is **not installed**, do not emit a bare slash command.
State what you can do without it, then:

```text
Install: /plugin install <plugin>@agent-plugins
Then run: /<plugin>:<skill> …
```

See `docs/CROSS-PLUGIN-CONTRACTS.md` (monorepo) for the full edge list.

## Skill routing (near-misses)

| User intent | Skill | Notes |
| ----------- | ----- | ----- |
| System architecture / arc42 | **solution** | Writes `ARCHITECTURE.md` |
| ADR plan / write / review | **adr** | Register + `ADR-NNNN-*.md` |
| Work-item `design.md` | `/engineering:design` | Companion — not this practice |
| Docs quality / consistency | `/engineering:docs-review` | Companion |
| Tech debt audit | `/engineering:tech-debt` | Companion |
| Implement code | `/engineering:implement` | Companion |

## Work-item resolution

When `adr plan <work-id>` harvests from a work item, resolve the ID per
[work-items.md](work-items.md) before reading `design.md`.
