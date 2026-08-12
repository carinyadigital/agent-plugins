# Capture protocol

Drive the browser **once**, produce an evidence bundle, hand the bundle to every lens.

Driving a browser is the most expensive and most stateful operation in this skill. Three
lenses each navigating, setting up states, and screenshotting costs three times as much
and produces three different renders of the same state — so when two lenses disagree,
there is no way to tell which was looking at the truth.

The skill already resolves the environment and the design source once and shares them.
This applies the same rule to the evidence.

## 1. Determinism first

A capture that varies between runs produces "deviations" that are not defects. Stabilise
before capturing anything, or the conformance lens will generate false positives fast
enough to destroy trust in the whole review.

Before every capture:

- [ ] **Fonts loaded** — await `document.fonts.ready`. Text reflows after webfont swap,
      which moves everything below it.
- [ ] **Network idle** — no in-flight requests; skeletons and lazy images resolved.
- [ ] **Animation disabled** — inject a stylesheet forcing
      `animation-duration: 0s !important; transition-duration: 0s !important;
      animation-delay: 0s !important; scroll-behavior: auto !important`, and wait one
      frame. Do **not** achieve this by emulating `prefers-reduced-motion`: see the
      warning below.
- [ ] **Time and data frozen** where the app allows it — fixed clock, seeded fixtures.
      Relative timestamps ("2 minutes ago") change between captures by definition.
- [ ] **Carousels, autoplay, and live counters** paused or masked.
- [ ] **Scroll position** deterministic — scroll to top unless the state requires
      otherwise.

### The reduced-motion trap

Disabling animation to stabilise a screenshot and verifying the app honours
`prefers-reduced-motion` are **opposite operations on the same setting**. Emulating the
media query to stabilise captures silently destroys the ability to test whether the app
respects it — a well-behaved app looks identical either way, so the check passes
vacuously.

Keep them separate:

- **Stabilise** with the injected CSS override, which is independent of the media query.
- **Verify** reduced-motion as a dedicated capture pair: one with the query emulated,
  one without. If the two are identical for an animated component, the app honours it.
  If the animation runs in both, it does not.

## 2. Capture twice

Capture every screenshot twice, a short interval apart, and compare.

Any region that differs between the two is **unstable**. Mark it in the manifest and
exclude it from conformance findings. Do not report the difference as a deviation — it
is flake, and reporting it teaches the reader to distrust the review.

This is the cheapest possible version of what visual-testing platforms build elaborate
machinery for. It costs one extra screenshot and removes most of the false-positive
surface.

## 3. The matrix

Capture the cross product of **state × viewport**, for the pages and components the diff
touched.

**Viewports:** 1440×900 (desktop), 768 (tablet), 375 (mobile). Add 320-equivalent when
checking reflow (WCAG 1.4.10).

**States**, per changed component:

| State | How to reach it |
| ----- | --------------- |
| Default | as rendered |
| Hover / focus / active / disabled | drive the element directly |
| Loading | throttle the network or stub a pending response |
| Empty | remove the data |
| Error | invalid input, or force a failing response |
| Long content | overflow the longest realistic string |

A state you cannot reach is **recorded as unreachable**, never assumed to pass. That
record is what makes the coverage statement honest.

If the app implements a theme (dark mode, forced-colors), it doubles the matrix. Decide
explicitly: capture both, or capture one and state the omission. Do not leave it
implicit.

## 4. Keyboard traversal

Script this into the capture. Otherwise the accessibility lens still needs live browser
access and the whole consolidation is defeated for the highest-value lens.

For each changed flow, drive Tab from the top and record per stop:

- Ordinal position and the element that received focus.
- Whether a visible focus indicator appeared — capture a screenshot at each stop.
- Whether the element is operable by Enter and Space.
- Whether focus ever leaves the flow unexpectedly, or fails to escape a widget.

Then record: focus movement into any dialog opened, and back to the trigger on close;
Escape behaviour on overlays.

This record is what lets a lens judge WCAG 2.4.3 (focus order), 2.4.7 (focus visible),
2.1.1 (keyboard), and 2.1.2 (no keyboard trap) — none of which any automated scanner
detects at all. See [accessibility-checklist.md](accessibility-checklist.md).

## 5. Also capture

- **Axe results** per page and per significant state, as JSON with rule IDs.
- **Console** errors and warnings collected across the whole session.
- **Accessibility tree** snapshot per page — roles, names, and structure, which lets a
  lens judge semantics without re-rendering.

## 6. Bundle layout

Write to a gitignored scratch directory. **Never commit captures.**

```
.ux-review/
  screenshots/{page-or-component}-{state}-{viewport}.png
  axe/{page}.json
  console/{page}.log
  a11y-tree/{page}.json
  keyboard/{page}-traversal.json
  manifest.json
```

`manifest.json` is the contract between the capture step and every lens:

```json
{
  "environment": "dev-server http://localhost:3000",
  "captured_at": "2026-07-19T09:00:00Z",
  "viewports": [1440, 768, 375],
  "theme": "light only — app implements no dark mode",
  "pages": [
    {
      "path": "/checkout",
      "states_captured": ["default", "loading", "error", "empty"],
      "states_unreachable": [
        { "state": "payment-declined", "why": "requires a live gateway sandbox" }
      ],
      "unstable_regions": [
        { "selector": ".order-timer", "why": "differs across paired captures" }
      ],
      "masked": [".session-id"]
    }
  ]
}
```

## 7. What the lenses get

Every lens reads the bundle. Most need no browser access at all, which drops them a
tier and removes their flake surface entirely.

The verifier is the exception: it may re-render a single state to settle one finding.
That is a targeted, bounded re-capture, not a second review pass.

## 8. Degradation

When the environment ladder in
[environment-resolution.md](environment-resolution.md) bottoms out at static-only, there
is no bundle. Say so in the manifest and the verdict, run only the lenses that read
static code, and mark every live-only check **unverified** rather than passed.

A static-only review can still FAIL on what it can see. Its PASS is always partial.
