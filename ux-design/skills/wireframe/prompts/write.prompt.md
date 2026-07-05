# Wireframe write

## Before running

1. Resolve paths per [../../references/ux-design-conventions.md](../../references/ux-design-conventions.md).
2. Read `<resolved-brand-path>/brand-guide.md` when present — cite layout patterns; do not duplicate tokens.
3. Read practice profile when present for in-scope pages and design references.
4. Parse `{page-or-flow}` from the skill argument — kebab-case slug for the output filename.
5. If `--brief` provided, treat it as the primary requirements source.
6. If `--from figma` or Figma URL in brief: use Figma MCP to extract frame structure; map regions to wireframe sections.
7. Check for existing wireframe at `<design-dir>/{page-or-flow}.md` — offer update vs new version if present.

## Task

Write `<design-dir>/{page-or-flow}.md` using [../assets/wireframe.template.md](../assets/wireframe.template.md).

### Fidelity rules

- **Low fidelity** — layout regions, hierarchy, labels, interaction notes only.
- **No implementation detail** — no component names, file paths, TypeScript types, or API shapes.
- **No brand token invention** — when brand-guide exists, reference it; when absent, use generic region labels.
- **Accessible structure** — note heading order, form labels, focus order for interactive flows.

### Flow wireframes

When `{page-or-flow}` names a multi-step flow (e.g. `checkout-flow`):

- Add a **Flow overview** subsection before layout with numbered steps.
- One layout section per step, or a combined overview plus step detail — pick whichever is clearer.
- Document back/next/cancel on each step.

## Output

Single markdown file. Delete the DRAFTING AIDE block before saving.

## Review criteria

- User goal and entry/exit documented
- Desktop layout with named regions (ASCII or table)
- Mobile behaviour noted when layout differs
- Interactions table covers primary actions
- Key states listed (default, error at minimum for forms)
- Open questions surfaced with owners
- No implementation or brand-token prose that belongs elsewhere

## Handoff

After user approves, recommend `/web-development:implement` with reference to this wireframe path.
