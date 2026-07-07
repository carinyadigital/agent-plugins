# Accessibility checklist — WCAG 2.2 AA, condensed

Split by how each check can honestly be performed. Automated scanners catch
roughly a third of WCAG issues; the manual half is not optional. **Never
report conformance, or an accessibility PASS, from the automated half
alone.** Scope every check to the UI the diff introduced or touched.

## Automated half (run a scanner)

Run axe-core (via `@axe-core/playwright`, browser MCP, or the project's own
a11y tooling) on each changed page/state. Reliable for:

- Color contrast — text ≥ 4.5:1; large text and UI components/graphics ≥ 3:1 (1.4.3, 1.4.11)
- Form fields without programmatic labels (3.3.2, 4.1.2)
- Images missing `alt` (1.1.1)
- Heading-level skips and empty headings (1.3.1)
- ARIA misuse — invalid roles/attributes, broken references (4.1.2)
- Duplicate IDs, missing page language/title (3.1.1, 2.4.2)
- Some WCAG 2.2 rules in axe-core 4.5+ — minimum target size, focus-appearance heuristics

Record violations with rule IDs. Zero violations means the automatable
third passed — nothing more.

## Manual half (agent-driven, in the live UI)

**Keyboard (2.1.1, 2.4.3, 2.1.2):** Tab through each changed flow — every
interactive element reachable, order follows visual order, no traps.
Enter/Space operate controls; Escape closes overlays; arrow keys work
within composite widgets (menus, tabs, radios).

**Focus (2.4.7, 2.4.11, 2.4.12):** visible focus indicator on every
interactive element (never `outline: none` without a replacement); focused
element not fully hidden behind sticky headers/footers; focus moves into
opened dialogs and returns to the trigger on close.

**Semantics & names (1.3.1, 2.4.6, 2.5.3):** controls are native
buttons/links/inputs, not clickable divs; visible label text is contained
in the accessible name; status/error messages are announced (live region or
focus move), not just displayed (4.1.3).

**WCAG 2.2 specifics:** targets ≥ 24×24px or adequately spaced (2.5.8);
any drag operation has a single-pointer alternative (2.5.7); no
newly-introduced cognitive tests at auth (3.3.8); help, when present, is
consistently located (3.2.6); previously-entered data not demanded twice in
a flow (3.3.7).

**Content & motion (1.4.4, 1.4.10, 2.3.1, 2.2.2):** page usable at 200%
zoom; reflows to 320px-equivalent without horizontal scroll; no
flashing > 3/sec; auto-moving content pausable and `prefers-reduced-motion`
respected.

**Forms (3.3.1–3.3.4):** errors identified in text next to the field, not
color alone; suggestions given where known; destructive/legal/financial
submissions confirmable or reversible.

## Static-only fallback

Without a live UI, only markup-level checks are possible from the diff:
semantic elements, label associations, alt text, ARIA validity, obvious
`outline: none`. Keyboard, focus, contrast-in-context, and announcements
remain **unverified** — list them as such; do not extrapolate a pass.

## Reporting

- Cite the WCAG criterion on every finding, plus the axe rule ID for
  scanner findings.
- Category **Accessibility**; at Medium+ confidence the risk matrix
  override makes these `blocking` — the AA bar is a compliance floor, not
  a preference.
- State who is blocked ("keyboard-only users cannot submit"), not just
  which rule fails.
