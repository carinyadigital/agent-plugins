---
name: wireframe
description: >
  Use when producing a low-fidelity layout and interaction spec from a brief.
  Output at `<design-dir>/{page-or-flow}.md`. Resolve `<design-dir>` per
  ux-design-conventions.md. Reads brand-guide.md when present. Do NOT use for
  epic technical design (web-development:design), visual brand tokens
  (brand-creative:brand-guide), or code implementation (web-development:implement).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<page-or-flow> [--brief <notes>] [--from figma]"
metadata:
  version: "0.1.0"
  owner: ux-design
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Wireframe

## When to use

Produce a low-fidelity layout and interaction spec when the user names a page or
flow and wants a wireframe document before implementation.

## What this skill does not do

- Does not write epic `design.md` (`/web-development:design`)
- Does not define brand tokens (`/brand-creative:brand-guide`)
- Does not implement UI (`/web-development:implement`)
- Does not run usability reviews or research synthesis (deferred in v1)

## Preconditions

- Read [../../references/ux-design-conventions.md](../../references/ux-design-conventions.md)
- Read `<resolved-brand-path>/brand-guide.md` when present for layout tokens
- Read practice profile at `~/.claude/plugins/config/digital-agency/ux-design/CLAUDE.md`
  when present for in-scope pages and design references
- When `--from figma` or Figma link in brief: extract layout structure via Figma MCP;
  do not invent dimensions without evidence

## Trust spine

| Failure mode | Mitigation |
| ------------ | ---------- |
| Over-specification | Low fidelity only — no component names, file paths, or API contracts |
| Brand safety | Reads brand-guide.md when present; structure-only when absent |
| Blast radius | Writes only under resolved design directory |
| DoD bypass | Show full draft; confirm before write when user has not pre-approved |

## Workflow

Follow [prompts/write.prompt.md](prompts/write.prompt.md).

## Outputs

`<design-dir>/{page-or-flow}.md` — kebab-case slug matching the argument.

## Related skills

- `/web-development:implement` — builds UI from approved wireframes
- `/brand-creative:brand-guide` — visual identity tokens wireframes may reference
