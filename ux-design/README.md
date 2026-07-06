# ux-design

Root-level **practice plugin** — minimal v1 delivers setup interview and one
wireframe skill. Self-contained under the MECE practice model: edit skills here
only; nothing is vendored from elsewhere.

Install standalone or after `agency-hub:setup` recommends it. Recommend
`web-development` as a **companion practice** for implementation — it reads
`<design-dir>/*.md` via artifact consumption; no install dependency in either
direction.

## First run: setup

After instance bootstrap (or standalone):

```
/ux-design:setup
```

| Flag | Behaviour |
| ---- | --------- |
| `--quick` | Default in-scope pages; one design reference if available |
| `--full` | Full interview including all pages/flows and reference sources |
| `--redo` | Re-run UX setup only; overwrite on confirmation |
| `--resume` | Continue a paused interview |
| `--check-integrations` | Report MCP connector status only; no interview |

## Skills

| Skill | Purpose |
| ----- | ------- |
| **setup** | Interview → write practice profile and wireframe scope defaults |
| **wireframe** | Produce low-fidelity layout/interaction spec from a brief |

Direct invocation works post-setup:

```
/ux-design:wireframe home-page
/ux-design:wireframe checkout-flow --brief "guest checkout, 3 steps"
```

Path resolution for all skills: `references/ux-design-conventions.md`.

## Where wireframes land

| Context | Design artefacts land at |
| ------- | ------------------------ |
| Instance repo (`config/instance.json` present) | `<instance-root>/design/` |
| Target repo (`.agency/target.json` pointer) | Instance `design/` via pointer |
| Standalone (no instance) | `docs/design/` in the current project |

## Brand guide (artifact consumption)

Wireframe reads `<resolved-brand-path>/brand-guide.md` when present for layout
tokens and visual patterns — no bundled skill and no install dependency on
`brand-creative`. If the file does not exist, proceed with structure-only wireframes.

## Prerequisites

- **Instance profile** (optional) — `agency-hub:setup` writes
  `config/instance.json`; setup reads business identity without re-asking.
- **Figma** (optional) — connected Figma enables reference extraction during setup
  and wireframe write.
- **web-development** (recommended companion) — reads wireframes before UI
  implementation; see CONNECTORS.md.

## After setup

1. Run `/ux-design:wireframe` for each page or flow in scope.
2. Hand off to `/web-development:implement` when wireframes are approved.
3. Re-run `/ux-design:setup --redo` to refresh scope or references.

## References

- `references/practice-setup-framework.md` — invocation, config paths, interview structure
- `references/ux-design-conventions.md` — path resolution and artefact boundaries
- `references/instance-profile-template.md` — Tier 1 schema (owned by agency-hub; synced copy)

Meta-framework files (`instance-profile-template.md`, `setup-framework.md`)
are kept in sync across practice plugins via `python3 scripts/sync-references.py`.
