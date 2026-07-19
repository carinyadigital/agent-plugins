# Design source resolution

Self-contained discovery rules for the **design source of truth** — what the
implemented UI is supposed to look like. This skill makes no assumption
about design tooling: it discovers whatever exists and degrades gracefully.
Resolve once, up front, and pass the result to every sub-agent.

## Resolution ladder

Stop at the first level that yields a usable source; combine levels when
they complement (a Figma node for layout + a tokens file for values):

1. **Explicit argument** — the user passed a Figma URL, mockup path, or
   spec link.
2. **Linked from the work item** — a Figma/design link in the PR or MR
   description, the linked issue/ticket, or a local spec file
   (`**/design.md`, `SPEC*.md`) associated with the change.
3. **Figma via MCP** — when a Figma MCP server is connected (official Dev
   Mode server, remote or desktop) and a node URL/ID is known:
   - screenshot of the node (`get_image` / `get_screenshot`) — visual truth;
   - variable definitions (`get_variable_defs`) — token truth (color,
     spacing, typography);
   - code/design context and the Code Connect map where available —
     intended component mapping.
   Tool names vary by server version — discover what the connected server
   exposes. The server needs a node reference; never guess node IDs. If a
   Figma link exists but no MCP server is connected, say so — do not
   scrape.
4. **Design artifacts in the repo** — exported mockups/screenshots
   (`design/`, `docs/design/`, `mockups/`, image files referenced by the
   work item), redlines, or spec documents.
5. **Tokens and style guide** — a design-tokens file (`tokens.*`,
   `theme.*`, CSS custom properties, Tailwind config), brand/style-guide
   docs, Storybook. No layout truth, but authoritative for values.
6. **Design principles doc** — `DESIGN_PRINCIPLES.md`, brand guidelines
   named in `AGENTS.md`/`CLAUDE.md`. Judgement criteria, not a comparison
   target.
7. **None found** — judge against the application's own internal
   consistency plus [ux-heuristics.md](ux-heuristics.md), and **say so
   explicitly** in the verdict ("no design source — reviewed for internal
   consistency and UX heuristics"). Never silently invent a standard.

## What each level supports

| Level | Fidelity comparison | Token audit | Heuristic bar |
| ----- | ------------------- | ----------- | ------------- |
| Figma via MCP | yes — pixel/screenshot + variables | yes | yes |
| Repo mockups/specs | yes — visual | only if values annotated | yes |
| Tokens/style guide | no layout truth | yes | yes |
| Principles doc | no | no | yes — sharpened |
| None | no | no | yes — heuristics only |

`conformance-reviewer` runs its fidelity pass only at levels 1–4; below that there is
nothing to be faithful to. Its design-system pass runs at any level, including none, so
long as the repo has tokens or a component library — which is why it is the one lens
that still returns a useful review when nothing renders.

## Recording the resolution

Produce a short bundle and reuse it verbatim across the review and every
sub-agent:

```text
Design source: <level & what> — <node URL / file paths, or "none">
Access: <Figma MCP tools available | files read | n/a>
Covers: <which changed components the source actually shows>
Source ref: <Figma node version / file hash, for drift detection>
Intentional deviations: <called out in work item/PR, or "none stated">
```

Deviations the work item or PR description explicitly calls out are not
findings — record them here so no lens re-flags them.

## Design-side drift

The design is not fixed. On an incremental review, compare `Source ref` against the one
recorded in the review state (see
[environment-resolution.md](environment-resolution.md) — Review state).

If the design source changed since the last review, **fidelity findings must be
re-derived even where no code changed**. The implementation may have been correct
against the old design and wrong against the new one, and nothing in the diff will
reveal that.

Say which side moved. "Design updated since last review — 3 fidelity findings are new
against the revised source, no code change" is a materially different message to the
author than "3 new fidelity findings", and it routes to a different fix: the design may
be the thing that needs a conversation.
