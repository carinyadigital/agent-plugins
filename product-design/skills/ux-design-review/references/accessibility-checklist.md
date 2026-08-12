# Accessibility checklist — WCAG 2.2 AA, condensed

Split by how each check can honestly be performed. **Never report conformance, or an
accessibility PASS, from the automated half alone.** Scope every check to the UI the
diff introduced or touched.

## What automation actually covers

Two different numbers get quoted, and both are right about different things. Deque's
coverage study (13,000+ page states, ~295,000 issues) found:

- **By success criteria:** 16 of 50 WCAG 2.1 AA criteria are automatable — the source
  of the familiar "20–30%" figure.
- **By issue volume:** axe-core catches **57.38%** of real issues, because the
  automatable criteria are the high-frequency ones. Contrast alone is 30% of all issues
  found.

Neither number is useful at review time. What matters is *which criteria a scanner will
never catch*. In that same dataset, these had *zero* automated detections:

| Criterion | What no scanner will tell you |
| --------- | ----------------------------- |
| 2.4.3 Focus Order | Tab order follows visual order |
| 2.4.7 Focus Visible | A visible focus indicator exists |
| 1.4.11 Non-text Contrast | UI components and graphics meet 3:1 |
| 1.3.2 Meaningful Sequence | Reading order matches DOM order |
| 2.1.2 No Keyboard Trap | Focus can escape every widget |
| 1.4.10 Reflow | No horizontal scroll at 320px-equivalent |
| 4.1.3 Status Messages | Changes are announced, not just displayed |
| 2.4.4 Link Purpose | Link text makes sense out of context |
| 2.4.6 Headings and Labels | Headings and labels are descriptive |
| 1.3.3 Sensory Characteristics | Instructions do not rely on shape or position |

These are the manual pass. Skipping them is not a reduced-coverage review — it is a
review that cannot speak to conformance at all, because a clean scan says nothing about
any of them.

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

Record violations with rule IDs. Zero violations means the automatable portion passed —
nothing more. Say exactly that in the verdict, never "the accessibility scan passed".

## Manual half (from the capture bundle)

These run against the evidence captured per
[capture-protocol.md](capture-protocol.md) — the keyboard traversal record, the
accessibility tree snapshot, and the per-state screenshots. They do not need their own
browser session.

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
- In the coverage statement, name the manual criteria actually verified: "axe clean;
  focus order, focus visibility, and reflow verified from the traversal record" is a
  claim a reader can act on. "Accessibility passed" is not.
