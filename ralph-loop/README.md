# ralph-loop

Self-referential delivery loop plugin. Seed with `ralph-loop-setup`, run with
`ralph-loop`. Ships Claude Code and Cursor stop hooks plus `ad-hoc` and `custom`
presets.

The `engineering-delivery` preset lives in the companion **product-engineering**
plugin (`assets/ralph-presets/engineering-delivery.md`) so the loop stays
domain-agnostic while the preset ships with the skills it calls.

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

## Presets

| Preset | Where |
| ------ | ----- |
| `ad-hoc` | `skills/ralph-loop/assets/presets/ad-hoc.md` |
| `custom` | `skills/ralph-loop/assets/presets/custom.md` |
| `engineering-delivery` | `product-engineering/assets/ralph-presets/` (companion) |
