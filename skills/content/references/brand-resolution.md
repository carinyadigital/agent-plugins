# Brand and instance resolution

Content skills read Carinya Parc brand from the **carinyaparc instance repo**, not from
target repo `docs/brand/` or a separate plugin.

## Steps

1. If working in a target repo, read `.carinyaparc/target.json` → `{ instance, target }`.
2. Open the carinyaparc instance repo (sibling checkout or multi-root workspace).
3. Read `config/instance.json` for brand path keys (relative to carinyaparc root).
4. Optionally read `config/targets/{target}.json` for artefact paths and squad charters.
5. Load brand files, e.g. `brand/brand-voice.md`, `brand/taxonomy.md`.

If the carinyaparc repo is not available, ask the user for brand context — do not
fall back to `docs/brand/` on the target repo.

## Path map (Carinya Parc)

| Key in `config/instance.json` | File |
| ----------------------------- | ---- |
| `brand.voice` | `brand/brand-voice.md` |
| `brand.taxonomy` | `brand/taxonomy.md` |
| `brand.hashtags` | `brand/hashtags.md` |
| `brand.seasonalCalendar` | `brand/seasonal-calendar.md` |

All paths relative to the **carinyaparc** repository root.
