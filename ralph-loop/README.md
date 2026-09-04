# ralph-loop

Self-referential delivery loop plugin. Seed with `ralph-loop-setup`, run with
`ralph-loop`. Ships Claude Code and Cursor stop hooks plus `ad-hoc`, `custom`,
and `engineering-delivery` presets.

The `engineering-delivery` preset invokes companion skills (`/engineering:*`,
`/product-management:validate`) from the **seeded loop files** in the target
repo. Engineering does not ship a preset; after setup it reads
`.claude/loop/` or `.cursor/loop/`.

## Skills

| Skill | Purpose |
| ----- | ------- |
| **ralph-loop-setup** | Interview → seed loop files via `scripts/seed-ralph-loop.sh` |
| **ralph-loop** | Start, status, cancel an active loop |

```
/ralph-loop-setup --prompt "…"
/ralph-loop start
```

## Hooks

- Claude Code: `hooks/claude/hooks.json` → Stop → `stop-hook.sh`
- Cursor: `hooks/cursor/hooks.json` → afterAgentResponse + stop

Cursor hooks search `workspace_roots` for `.cursor/loop/active.md`. Seed the
loop in the checkout that should own it; a multi-root window is fine.

## Presets

| Preset | Where |
| ------ | ----- |
| `ad-hoc` | `skills/ralph-loop/assets/presets/ad-hoc.md` |
| `custom` | `skills/ralph-loop/assets/presets/custom.md` |
| `engineering-delivery` | `skills/ralph-loop/assets/presets/engineering-delivery.md` |
