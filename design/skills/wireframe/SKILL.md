---
name: wireframe
description: >
  Produce a low-fidelity layout and interaction spec from a brief. Use when the
  user names a page or flow and wants a wireframe before implementation. Writes
  `<design-dir>/{page-or-flow}.md` (resolve path per design-conventions.md).
  Reads brand-guide.md when present. Do NOT use for epic technical design
  (design), visual brand tokens (brand-guide), or code implementation (implement).
license: MIT
allowed-tools: Read Write Glob Grep
argument-hint: "<page-or-flow> [--brief <notes>] [--from figma]"
metadata:
  author: Carinya Parc
  version: "0.1.0"
  owner: design
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Wireframe

You produce a low-fidelity layout and interaction spec. Pass `{page-or-flow}`
(kebab-case slug) after the skill name; optional `--brief` and `--from figma`.

Read [design-conventions.md](../../references/design-conventions.md). Read
`<resolved-brand-path>/brand-guide.md` when present for layout patterns. Read the
practice profile when present for in-scope pages and design references.

## Inputs

| Input          | Location                                           | Required   |
| -------------- | -------------------------------------------------- | ---------- |
| Page or flow   | Argument (kebab-case slug)                         | Yes        |
| Brief          | `--brief` or conversation                          | If present |
| Brand guide    | `<resolved-brand-path>/brand-guide.md`             | If present |
| Figma          | `--from figma` or URL in brief                     | Optional   |
| Existing file  | `<design-dir>/{page-or-flow}.md`                   | Check      |

## Steps

1. Resolve design directory per design-conventions. Parse `{page-or-flow}` for
   the output filename.
2. If `--brief` provided, treat it as the primary requirements source.
3. If `--from figma` or Figma URL: extract frame structure via Figma MCP; map
   regions to wireframe sections. Do not invent dimensions without evidence.
4. If a wireframe already exists, offer update vs new version.
5. Write `<design-dir>/{page-or-flow}.md` using
   [wireframe.template.md](assets/wireframe.template.md). Delete the DRAFTING AIDE
   block before saving. Show full draft; confirm before write when the user has
   not pre-approved.
6. After approval, recommend `/engineering:implement` with this wireframe path.

### Fidelity rules

- Low fidelity — layout regions, hierarchy, labels, interaction notes only
- No implementation detail — no component names, file paths, types, or API shapes
- No brand token invention — reference brand-guide when present; else generic labels
- Accessible structure — heading order, form labels, focus order for interactive flows

### Flow wireframes

When the slug names a multi-step flow (e.g. `checkout-flow`):

- Add a **Flow overview** with numbered steps before layout
- One layout section per step, or combined overview + step detail
- Document back/next/cancel on each step

## Quality rules

- User goal and entry/exit documented
- Desktop layout with named regions (ASCII or table)
- Mobile behaviour noted when layout differs
- Interactions table covers primary actions
- Key states listed (default, error at minimum for forms)
- Open questions surfaced with owners
- No implementation or brand-token prose that belongs elsewhere
