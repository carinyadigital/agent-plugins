# brand-creative

Root-level **practice plugin** — one install delivers the complete brand service:
setup interview, voice lifecycle, and visual identity guide. Self-contained under
the MECE practice model: edit skills here only; nothing is vendored from elsewhere.

Install standalone or after `agency-hub:setup` recommends it.

## Who this is for

Teams that want brand voice and visual identity in one plugin. Works with or
without an instance repo:

| Context | Brand artefacts land at |
|---|---|
| Instance repo (`config/instance.json` present) | `<instance-root>/brand/` |
| Target repo (`.agency/target.json` pointer) | Instance `brand/` via pointer |
| Standalone (no instance) | `docs/brand/` in the current project |

## First run: setup

Golden path 3 — brand voice setup after instance bootstrap:

```
/brand-creative:setup
```

| Flag | Behaviour |
|---|---|
| `--quick` | Strictness default + one seed doc; skip discovery |
| `--full` | Full interview + discovery when platforms connected |
| `--redo` | Re-run brand setup only; overwrite on confirmation |
| `--resume` | Continue a paused interview |
| `--check-integrations` | Report MCP connector status only; no interview |

## Skills

| Skill | Purpose |
|---|---|
| **setup** | Interview → discover → write → review → save to resolved brand path |
| **brand-voice** | discover, write, review, refine, enforce |
| **brand-guide** | write, review, refine (visual identity, UI tokens) |

Direct invocation works post-setup:

```
/brand-creative:brand-voice write
/brand-creative:brand-guide write --from figma
```

Path resolution for all skills: `references/brand-conventions.md`.

## Prerequisites

- **Instance profile** (optional) — `agency-hub:setup` writes
  `config/instance.json`; setup reads business identity and seed material
  without re-asking.
- **Connectors** (optional) — Notion, Atlassian, Slack, Figma, Fireflies enable
  `brand-voice discover`. Visual guide generation benefits from Figma.

## After setup

1. Content and engineering roles read brand from the resolved path automatically.
2. Re-run `/brand-creative:setup --redo` to refresh voice or guide.
3. Use `brand-voice enforce` for on-brand copy; `brand-guide review` after design
   changes.

## References

- `references/practice-setup-framework.md` — invocation, config paths, interview structure
- `references/brand-conventions.md` — path resolution and artefact boundaries
- `references/instance-profile-template.md` — Tier 1 schema (owned by agency-hub; synced copy)

Meta-framework files (`instance-profile-template.md`, `setup-framework.md`)
are kept in sync across practice plugins via `python3 scripts/sync-references.py`.
