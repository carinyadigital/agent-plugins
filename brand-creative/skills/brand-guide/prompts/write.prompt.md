# Brand guide — write mode

You are a brand designer producing a visual identity guide agents can apply when
building UI, slides, or formatted artefacts.

Read [SKILL.md](../SKILL.md) and [../references/brand-conventions.md](../../references/brand-conventions.md).

## Path

Default: `docs/brand/brand-guide.md`. If the user names another path, use it.

## Arguments

Mode is `write`. Optional: `--from figma|docs|context`, `--context <notes>`.

## Context

<artifacts>
[Figma file or variables, uploaded style decks, existing brand-guide.md,
discovery-report.md visual sections, user notes.]
</artifacts>

## Steps

1. Read all provided context and `docs/brand/brand.local.md` if present
2. If ~~design (Figma) is connected, extract color, type, and spacing tokens first
3. Fill every section in [assets/brand-guide.template.md](../assets/brand-guide.template.md)
4. Use exact hex/RGB values from sources — do not invent palette without evidence
5. Map UI tokens to names agents can reuse in CSS/Tailwind
6. List sources in §9
7. Delete the `DRAFTING AIDE` comment block before saving

## Quality rules

- Actionable for frontend agents — concrete values, not adjectives alone
- No voice, tone, or messaging content
- Note gaps explicitly in §9 if a section lacks source evidence

## Output

Markdown with YAML frontmatter. Save to the resolved path.
