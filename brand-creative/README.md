# brand-creative

Root-level **practice plugin** — one install delivers the complete brand service: setup interview, voice lifecycle, and visual identity guide. Pilot for the practice-packaging pattern used by future practice plugins.

Install standalone (Try tier) or after `agency-hub:agency-setup` recommends it.

## Who this is for

Teams that want brand voice and visual identity in one plugin rather than assembling discipline skills separately. Works with or without an instance repo:

| Context | Brand artefacts land at |
|---|---|
| Instance repo (`config/instance.json` present) | `<instance-root>/brand/` |
| Target repo (`.digital-agency/target.json` pointer) | Instance `brand/` via pointer |
| Standalone / Try tier | `docs/brand/` in the current project |

## First run: practice-setup

Golden path 3 — brand voice setup after instance bootstrap:

```
/brand-creative:practice-setup
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
| **practice-setup** | Interview → discover → write → review → save to resolved brand path |
| **brand-voice** | discover, write, review, refine, enforce |
| **brand-guide** | write, review, refine (visual identity, UI tokens) |

Direct invocation works post-setup:

```
/brand-creative:brand-voice write
/brand-creative:brand-guide write --from figma
```

## Relationship to `skills/brand`

The `brand` discipline plugin remains available for fine-grained Try-tier installs. `brand-creative` vendors copies of `brand-guide` and `brand-voice` from `skills/brand/` — edit the canonical skills there, then run `python3 scripts/sync-agent-skills.py`.

## Prerequisites

- **Instance profile** (optional) — `agency-hub:agency-setup` writes `config/instance.json`; practice-setup reads business identity and seed material without re-asking.
- **Connectors** (optional) — Notion, Atlassian, Slack, Figma, Fireflies enable `brand-voice discover`. Visual guide generation benefits from Figma.

## After setup

1. Content and engineering skills read brand from the resolved path automatically.
2. Re-run `/brand-creative:practice-setup --redo` to refresh voice or guide.
3. Use `brand-voice enforce` for on-brand copy; `brand-guide review` after design changes.

## References

- `references/practice-setup-framework.md` — invocation, config paths, interview structure
- `references/brand-conventions.md` — path resolution and artefact boundaries
- `references/instance-profile-template.md` — Tier 1 schema (owned by agency-hub; read-only copy)
