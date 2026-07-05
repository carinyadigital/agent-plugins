# Brand voice — discover mode

Search connected platforms and provided materials for existing brand voice,
messaging, and style guidance. Produce a triaged discovery report.

Read [SKILL.md](../SKILL.md) and [brand-conventions.md](../../references/brand-conventions.md).

## Path

Resolve `<brand-dir>` per [brand-conventions.md](../../references/brand-conventions.md).
Optional save: `<brand-dir>/discovery-report.md`.

## Arguments

Mode is `discover`. Optional platform filters or `--depth standard|deep`.

## Settings

Read `<brand-dir>/brand.local.md` if present: company name, enabled platforms,
search depth, known_materials list.

## Search strategy

1. Check known_materials and user-provided URLs first
2. Search enabled platforms (~~knowledge base, ~~chat, ~~design, ~~meeting transcription)
3. Triage findings: authoritative vs draft vs contradictory
4. Score confidence per finding ([confidence-scoring.md](../references/confidence-scoring.md))
5. Flag gaps for write mode

## Output

Discovery report in chat. Save to `<brand-dir>/discovery-report.md` unless user asks for session-only output.
