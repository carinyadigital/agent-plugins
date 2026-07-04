# Content Plugin

Content practice for media analysis, caption writing, editorial review, and content
curation. Generalized from steward Instagram pipeline; Carinya-specific brand values
read from **`carinyaparc/brand/`** via **`carinyaparc/config/instance.json`** — not
from target repo `docs/brand/`.

## Skills

| Skill | Mode | Description |
| ----- | ---- | ----------- |
| **analyse-media** | run | Vision analysis — subjects, season, mood, quality |
| **write-captions** | run | Instagram variants + channel copy |
| **edit-content** | run | Select or refine best caption variant |
| **curate-content** | run | Rank assets from inventory for posting |

## Brand resolution

Read [references/brand-resolution.md](references/brand-resolution.md) before running
any skill.

## Related plugins

- **brand** / **brand-voice** — enforce voice on generated copy
- **carinyaparc** instance — `brand/` and `config/` in the instance repo

## Maintainers

```bash
python3 scripts/validate.py
```

See [references/prompt-refinement.md](references/prompt-refinement.md) for prompt quality rationale.
