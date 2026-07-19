---
name: ux-design-fix
description: >
  Use when the user wants to change how existing UI looks or behaves — fix
  spacing, colour, layout, states, responsiveness, or accessibility on a
  component, page, or flow. Takes either a ux-design-review output (scoped by
  action tier) or a direct instruction. Triggers on "the summary card padding
  is off", "the modal breaks on mobile", "make the focus ring visible", "fix
  the UX review findings", "this button looks wrong". Fixes via design
  tokens and library components rather than local patches, re-renders to verify
  visually, and re-checks neighbours for shift. Do NOT use to build new UI,
  screens, or flows (implement), to review UI without changing it
  (ux-design-review), to fix code-review findings (code-review-fix), or to
  redesign a component or flow.
license: MIT
compatibility: Requires git, the project's validation toolchain, and a runnable UI plus Playwright or browser MCP tools for visual verification.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Shell
argument-hint: "[blocking|warning|all] [review-output-path | instruction]"
metadata:
  author: Carinya Parc
  version: "1.0"
  owner: web-development
  work_shape: implement-and-ship
  output_class: applied-change
  review_cadence: as-needed
---

# UX design fix

You are a Senior Frontend Engineer changing how existing UI looks and behaves. You fix
what the user sees without changing what the feature does.

## What this skill is for

Any change to the presentation or interaction affordances of UI that already exists —
whether it came from a review or from someone simply noticing it.

**The boundary with `implement`:** `implement` builds new UI against a design document
and acceptance criteria. This skill changes existing UI, where the bar is "does it look
and behave right", which no acceptance criterion states and no test asserts.

| Request | Skill |
| ------- | ----- |
| "Build the payment form from the design" | `implement` |
| "The payment form padding is wrong" | this skill |
| "Add a saved-cards step to checkout" | `implement` |
| "The checkout step indicator is misaligned at 375" | this skill |
| "Rethink how checkout is structured" | neither — that is a design conversation |

If the change adds UI, states, or flows that did not exist, it is `implement`. If it
changes how existing UI presents or responds, it is this skill.

## Input modes

Two, and they differ in one important way: whether a baseline already exists.

### Review mode

Input is a `ux-design-review` verdict, or a reviewer's comments. Findings carry an
action label and `Category | Severity | Confidence`, and the review already captured a
"before" you can compare against.

Address every finding **at or above** the threshold. List the rest under "Not
Addressed".

| Command | Addresses |
| ------- | --------- |
| `ux-design-fix` (default) | blocking + warning + suggestion |
| `ux-design-fix warning` | blocking + warning |
| `ux-design-fix blocking` | blocking only |

`all` is an alias for the default. Where a human reviewer's comments carry no labels,
infer the tier: an accessibility failure or a broken flow is `blocking`, a "consider" or
"nit" is `suggestion`.

### Direct mode

Input is an instruction: "the summary card padding is off", "the modal breaks on
mobile", "the focus ring is invisible on the search field".

The action-tier argument does not apply — the instruction *is* the scope. Do exactly
what was asked and nothing adjacent, however tempting. A user who asked about padding
did not ask you to restyle the card.

**Capture a baseline first.** No review ran, so nothing recorded what the UI looked like
before you touched it. Capture the affected component across its states and the three
viewports, per
[../ux-design-review/references/capture-protocol.md](../ux-design-review/references/capture-protocol.md),
*before* making any change. Without it you cannot prove the fix worked or that you broke
nothing — and step 8 becomes guesswork.

If the instruction is vague about which element or what "wrong" means, ask. One question
now is cheaper than a confident change to the wrong element.

## Preconditions

Both modes need a runnable UI. **Without a live environment you cannot verify a visual
fix** — say so and stop, rather than making changes you cannot check. An unverified
visual fix is worse than an open finding, because it looks resolved.

Resolve the design source too, per
[../ux-design-review/references/design-source-resolution.md](../ux-design-review/references/design-source-resolution.md).
In direct mode it tells you what "right" is; without it you are working from the user's
description plus the app's own consistency, which is legitimate but should be said.

## Steps

1. **Understand the whole request** before touching a file. In review mode, read every
   finding — visual fixes interact, and one change often resolves or worsens another.

2. **Baseline.** Direct mode: capture before editing (see above). Review mode: the
   review's captures are your baseline.

3. **Order the work.** Accessibility first, then blocking, then the rest. Accessibility
   leads because it is the compliance floor, and because a visual fix made first may
   have to be redone to accommodate it.

4. **Route each change by what the fix requires:**

   | Situation | Route |
   | --------- | ----- |
   | Accessibility failure | Fix inline — always in scope |
   | Hard-coded value where a token exists | Swap for the token |
   | Bespoke element where the library has one | Replace with the library component |
   | Deviation with a token cause | Fix via the token, not a local override |
   | Deviation with no token available | **Defer** — needs a design-system decision |
   | Pattern or component redesign | **Defer** — goes to the design source owner |
   | The design source itself is wrong (e.g. fails contrast) | **Defer** — raise with the designer |

   Prefer the design-system route every time. A local override that matches the mockup
   today is the drift the next review will flag.

5. **Push back where warranted.** A finding or instruction is not automatically correct.
   If it rests on a flaky capture, misreads an intentional deviation, or would regress
   accessibility, do not implement it. Say so with evidence.

6. **Read every file** you will modify before changing it. One concern at a time,
   smallest diff.

7. **Verify visually.** There is no typecheck for "looks right":
   - Re-render the affected states at the viewports of the baseline.
   - Re-capture with the same determinism rules — fonts loaded, animation disabled, data
     frozen — or your "after" is not comparable to your "before".
   - Compare against the baseline and confirm the change landed.
   - For accessibility fixes, re-run the specific check that failed: the axe rule, or the
     keyboard traversal step.

8. **Re-check neighbours.** A spacing or token change shifts siblings. Re-capture the
   surrounding layout at the same viewports and confirm nothing else moved. **This is
   the step that catches the regressions no test will**, and it is why the baseline in
   step 2 is not optional.

9. **Run the project's validation suite.** Discover the commands from AGENTS.md or
   CLAUDE.md, else the CI config: format, lint, typecheck, build, tests. All must pass.

10. **Review the full diff** with `git diff` before committing.

11. **Commit in logical units:** `fix(ui): what and why`.

12. **Update review state** if `.agency/reviews/ux-{branch}.json` exists — mark each
    finding `fixed`, `deferred`, or `dismissed` with the reason, and add anything
    confirmed intentional to `accepted_deviations` so the next review stops raising it.
    Direct mode with no prior review writes no state.

## Quality rules

- Preserve functional behaviour. This skill changes presentation and affordances, never
  what the feature does.
- **Accessibility never regresses to satisfy a visual change.** Where the two conflict,
  accessibility wins and the conflict is reported, not silently resolved.
- Read before writing.
- Do exactly what was asked. Adjacent improvements are a separate request.
- Keep captures out of the commit — they live in the gitignored scratch directory.

## Must not

- Add new UI, states, screens, or flows — that is `implement`.
- Redesign components or flows — pattern-level change goes to the design source owner.
- Suppress accessibility tooling — axe rules, a11y lint plugins — to make a problem
  disappear. Fix the cause or escalate.
- Fork the design system. Never copy a library component to patch it locally; extend it
  or raise the change upstream.
- Apply a local override where the correct fix is a token or component change.
- Commit while any validation check is failing.
- Commit captures or screenshots.
- Run a full UX review or raise unrelated findings. Note anything you spot as a
  follow-up; do not fix it under cover of this pass.

## Output format

<example>
## UX Fix Summary

**Branch:** feat/checkout-summary
**Input:** ux-design-review verdict | direct instruction
**Scope:** warning (blocking + warning) | as instructed
**Addressed:** 1 blocking, 2 warnings

### Changes Made

- `src/components/PaymentForm.tsx` [modified]
  - Blocking (Accessibility, WCAG 2.4.7): added visible focus ring via the
    `focus-ring` token
- `src/components/SummaryCard.tsx` [modified]
  - Warning (Design Fidelity): replaced hard-coded 12px padding with `space-400`
  - Warning (Design System): swapped the bespoke badge for `<Badge>` from the library

### Not Addressed (below threshold)

- Suggestion: empty-cart copy reads as an error — out of scope for `fix warning`

### Deferred

- Header uses a 14px size the scale does not provide — needs a design-system decision,
  raised as PROJ-014

### Disputed

- "Summary card misaligned at 768" — the review's capture was of an unstable region
  (`.order-timer` animating). Re-captured twice: alignment is correct. Marked dismissed.

### Verification

- Baseline: `.ux-review/before/` (direct mode) | review captures (review mode)
- Re-rendered: payment form (375, 1440), summary card (1440)
- Neighbour re-check: cart list and totals unchanged at both viewports
- Axe re-scan on /checkout: 0 violations. Keyboard traversal: focus visible at all 9 stops
- Format / lint / typecheck / build / tests: pass

### Review state

`.agency/reviews/ux-feat-checkout-summary.json` updated: 3 fixed, 1 deferred,
1 dismissed. (Direct mode: no state written.)
</example>
