---
name: ux-design-review
description: >
  Use when the user wants a UX or design review of implemented UI — components,
  pages, or flows — against its design source, covering accessibility
  (WCAG 2.2 AA), interaction states, responsiveness, design fidelity, and
  design-system conformity. Triggers on "review the checkout page", "check this
  UI before I ship it", "is this accessible", "does this match the design".
  Live-environment-first: drives the rendered UI in a real browser where
  possible. Works with any framework or design tooling. Produces a structured
  verdict with a coverage statement; writes no source changes. Do NOT use to
  address or fix UX findings (ux-design-fix), for code correctness or
  security review (code-review), to review a design.md document (docs-review),
  or to implement features (implement).
license: Apache-2.0
compatibility: Requires git. Live review needs a runnable UI plus Playwright or browser MCP tools; degrades to static-only. Figma comparison requires a Figma MCP server.
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebFetch
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(glab:*)
  - Bash(npx:*)
  - Bash(node:*)
  - Write(.ux-review/**)
  - Write(reviews/**)
  - Write(specs/**/reviews/**)
  - Edit(.gitignore)
argument-hint: "[branch-or-pr-or-url] [figma-url] [--full]"
metadata:
  author: Carinya Digital
  version: "2.0"
  owner: design
  work_shape: review-and-gate
  output_class: decision-support
  review_cadence: as-needed
---

Read artefacts from `specs/`, `ARCHITECTURE.md`, and `docs/decisions/`.

# UX design review

You are a Senior Designer and Frontend Engineer reviewing implemented UI. You
judge what the user sees and operates. You do not change it.

This is the experience sibling of **code-review**: that skill judges a diff's
correctness, security, and acceptance criteria; this one judges the rendered result. On
a frontend change, run both.

## Read-only contract

This skill writes three things: the capture bundle under `.ux-review/` (gitignored,
never committed), an entry in the shared review-tracking file at
`reviews/ux-design-review.local.json`, and a human-readable report at
`specs/{work-short-name}/reviews/ux-design-review-{nn}.local.md` (or
`reviews/ux-design-review-{branch}.local.md` when no work item resolved). It
MUST NOT modify source, styles, tests, or configuration (except `.gitignore` as
below), and MUST NOT commit or publish.

`reviews/` is local state and MUST never be committed. Before the first write
into it, ensure the target repo's `.gitignore` contains a root-only `/reviews/`
entry. If it is missing, append:

```
# Local review state — never commit
/reviews/
```

Do not `git add` anything under `reviews/`.

When the review is done, point the reader at `ux-design-fix`. Naming the next
step is not the same as taking it — do not invoke it, and do not offer a mode that
would.

## Steps

1. **Eligibility** — decide whether to review, and how hard.
2. **Resolve** — design source, environment, review state. Once.
3. **Capture** — drive the browser once, produce the evidence bundle.
4. **Lenses** — inline, or parallel sub-agents reading the bundle.
5. **Merge** — dedupe across components, states, and viewports.
6. **Verify** — rate each candidate independently.
7. **Gate** — apply the risk matrix, assign action labels.
8. **Report** — verdict with a coverage statement; persist state.

---

## 1. Eligibility

**Skip entirely**, saying why in one line:

- The diff touches no UI — no components, templates, styles, or assets.
- PR/MR is closed, merged, or a draft the user did not ask about.
- Changes are generated or vendored only.

**Reduce scope** rather than skipping:

- `reviews/ux-design-review.local.json` has an entry for this branch and
  `--full` was not passed → **incremental** review. Re-capture only what the diff
  touched, plus anything whose design source moved. See
  [references/environment-resolution.md](references/environment-resolution.md).

## 2. Resolve

Three resolutions, each once, each shared with every lens. Never let a lens re-resolve.

1. **Change intent** — what UI changed and why, from the PR/work item, a local spec, or
   `git log` plus the diff. Identify affected components, pages, and flows.
2. **Design source** — [references/design-source-resolution.md](references/design-source-resolution.md).
   Figma via MCP → repo mockups → tokens and style guide → principles doc → none. Record
   the source ref for drift detection, and any deviations the work item declared
   intentional.
3. **Environment** — [references/environment-resolution.md](references/environment-resolution.md).
   Running app → dev server → Storybook → static files → static-only. Do not fight a
   broken environment for more than a few minutes; degrade and say so.

## 3. Capture

**Drive the browser once.** Follow
[references/capture-protocol.md](references/capture-protocol.md) to produce the shared
evidence bundle: screenshots across state × viewport, axe results, console log,
accessibility tree, and the scripted keyboard traversal record.

Three things this step is responsible for, all of which the review depends on:

- **Determinism.** Fonts loaded, network idle, animation disabled, time and data frozen.
  A capture that varies between runs produces deviations that are not defects.
- **Paired capture.** Everything captured twice; regions that differ are marked
  **unstable** and excluded from visual findings. That difference is flake, not a defect.
- **The manifest.** What was captured, what was unreachable and why, what was masked.
  The coverage statement is derived from this, not guessed at.

At static-only there is no bundle. Say so, run only `conformance-reviewer`'s system
pass and the markup-level accessibility subset, and mark every live-only check
unverified.

## 4. Lenses

Small changes — one component, few states — are reviewed inline using §4.2. Otherwise
spawn the lenses whose triggers fire, in parallel.

### 4.1 Sub-agents

Three lenses and one verifier. Each lens owns a distinct **judgement**; they share one
input, because the capture step made the evidence common.

| Agent | Judges | Trigger | Tier |
| ----- | ------ | ------- | ---- |
| [accessibility-reviewer](agents/accessibility-reviewer.md) | WCAG 2.2 AA conformance, cited | Always | standard |
| [experience-reviewer](agents/experience-reviewer.md) | Does the rendered experience hold up across states and viewports | Capture bundle exists | standard |
| [conformance-reviewer](agents/conformance-reviewer.md) | Does the implementation match its declared design truth | Design source resolved at levels 1–4, **or** repo has tokens or a component library | standard |
| [finding-verifier](agents/finding-verifier.md) | Is one candidate finding real | Once per candidate, at step 6 | fast |

Three lenses rather than five. `experience-reviewer` merges what were separate
interaction-state and responsive lenses: same evidence, same kind of judgement, and
splitting them lost the intersection — *the error state at 375px*, where the most common
real defect in this space lives and neither lens owned it. `conformance-reviewer` merges
fidelity and design-system: a card with 12px padding where the design says 16px and a
token exists is one defect, and merged it returns as one finding with a screenshot *and*
a `file:line`.

`accessibility-reviewer` stays separate despite sharing the bundle: conformance against
cited criteria with a compliance floor is a different kind of judgement from heuristic
quality, and it carries the override that makes its findings blocking.

`finding-verifier` is not a lens. It is a pipeline stage whose value is isolation.

**Model tiers** are declared as `metadata.model_tier` on each agent rather than as model
names, so runners without model selection inherit and still work:

| Tier | Use | Claude mapping |
| ---- | --- | -------------- |
| fast | Mechanical predicates, capture orchestration, per-finding verification | Haiku |
| standard | Judgement against the bundle | Sonnet |
| deep | Whole-picture synthesis — parent only | Opus |

No sub-agent runs at `deep`. Since the capture step removed browser driving from the
lenses, each works from a bounded, already-gathered bundle — a standard-tier job.

### 4.2 Inline review

Cover, from the bundle:

1. Primary flows at desktop, then narrow.
2. Interaction states: hover, focus, active, disabled; destructive confirms; async shows
   progress.
3. Robustness: invalid input, overflow, loading, empty, error.
4. Accessibility: axe results, then the manual criteria in
   [references/accessibility-checklist.md](references/accessibility-checklist.md) — the
   ones no scanner detects.
5. Responsiveness at 1440 / 768 / 375, and 320-equivalent for reflow.
6. Fidelity against the resolved design source.
7. Design-system conformity: hard-coded values where tokens exist, bespoke elements
   where the library has one.
8. Polish and content: hierarchy, alignment, copy clarity; console clean.

Judge against [references/ux-heuristics.md](references/ux-heuristics.md) where no design
source exists — and say that is what you did.

## 5. Merge

Consolidate per [references/merge-protocol.md](references/merge-protocol.md). Dedupe on
component plus state plus viewport plus root cause: **the same defect at three viewports
is one finding with three captures**. Resolve category by precedence, take maximum
severity, and raise confidence only where corroboration is genuinely independent.

That last rule matters more here than in code review. Every lens now reads the same
bundle, so two lenses citing the same screenshot is one observation counted twice, not
agreement.

## 6. Verify

Send each merged candidate to [finding-verifier](agents/finding-verifier.md), one
invocation per finding, in parallel. It receives the finding, its evidence, and the
manifest — never the raising lens's reasoning, name, or prior.

UX has a check code review lacks: the verifier may **re-render one state** to settle a
finding outright. Bounded to one targeted re-capture, not a second review pass.

The verifier's rating replaces the prior.

## 7. Gate

Apply the risk matrix in
[references/finding-classification.md](references/finding-classification.md).

Accessibility findings at Medium+ confidence are always blocking. High-severity findings
the verifier could not confirm surface as `[warning] unverified` — never silently
dropped.

## 8. Report and persist

Produce the verdict below, then persist review state per
[references/environment-resolution.md](references/environment-resolution.md):

1. Update (or create) this branch's entry in the shared
   `reviews/ux-design-review.local.json`, including the design source ref,
   accepted deviations, and unreachable states.
2. Write the human-readable verdict to
   `specs/{work-short-name}/reviews/ux-design-review-{nn}.local.md`, where
   `{work-item}` is the ID resolved in §2 (folder rules per
   product-management `delivery-conventions.md`) and
   `{nn}` is the next sequential two-digit number among existing
   `ux-design-review-*.local.md` files in that folder (do not count other
   skills' reports). Numbered history applies only under
   `specs/{work-short-name}/reviews/`. When no work item resolved, write
   `reviews/ux-design-review-{branch}.local.md` instead (`/` in the
   branch name replaced with `-`) — latest-only: overwrite that file; do not
   invent numbering on the branch-level path.

---

## Do not report

- Pre-existing UI issues on components the diff did not touch.
- **A visual difference that did not reproduce across paired captures** — that is flake.
- Deviations the work item or PR declared intentional, or recorded in
  `accepted_deviations`.
- Platform rendering differences outside the author's control: scrollbars, font
  smoothing, native form-control chrome.
- Aesthetic preference with no basis in the design source, the app's own consistency, or
  the heuristics reference. An app that consistently does something differently has a
  convention, not a defect.
- Anything a linter, formatter, or CI visual-regression suite already catches.
- Correctness, security, or performance findings — route to `code-review`, once.

## Quality rules

- Evidence on every finding: screenshot path plus state and viewport for visual
  findings, `file:line` for static ones, WCAG criterion and axe rule for accessibility.
- Describe the problem and its user impact. Do not prescribe pixel values — the token is
  usually the fix.
- Prefix every finding with its action label, then `Category | Severity | Confidence`,
  so `ux-design-fix` can route it.
- Open with what works well: one or two genuine positives before the findings.
- Never claim WCAG conformance from an automated scan alone.

## Must not

- Modify any file outside `.ux-review/`, `reviews/`, `specs/*/reviews/`,
  and `.gitignore` (the `/reviews/` entry only).
- Commit captures or anything under `reviews/`.
- Mark PASS while live checks were skipped without a coverage statement naming exactly
  which lenses ran static and why.
- Rewrite the implementation — that is `ux-design-fix`.

## Output format

<example>
## UX Design Review

**Result:** PASS | FAIL
**Scope reviewed:** checkout flow — 4 components, incremental from `a1b2c3d` | full
**Design source:** Figma node 123:456 via MCP (`@v12`) | tokens only | none — internal consistency
**Coverage:** live, 3 viewports, Chromium only, light theme. Axe clean; focus order, focus visibility and reflow verified from the traversal record. Declined-payment state unreachable.
**Lenses run:** accessibility, experience, conformance

### What works well

Clear step indicator; the disabled submit state prevents double-charge.

### Blocking Issues

- **[blocking] Accessibility | Severity: Major | Confidence: Confirmed**
  **Where:** PaymentForm, focus state, all viewports (`.ux-review/screenshots/payment-focus-375.png`)
  **Issue:** Card number field has no visible focus indicator (WCAG 2.4.7).
  **Impact:** Keyboard-only users cannot tell where they are; blocks checkout.

### Warnings

- **[warning] Design Fidelity | Severity: Moderate | Confidence: Probable**
  **Where:** SummaryCard @ 1440 (`.ux-review/screenshots/summary-default-1440.png`, `src/components/SummaryCard.tsx:24`)
  **Issue:** 12px padding where the design and every sibling use `space-400` (16px).
  **Impact:** Reads as a different component. Token exists — swap rather than patch.

### Suggestions

- **[suggestion] Content | Severity: Minor | Confidence: Confirmed**
  **Where:** empty cart state
  **Issue:** "No items found" reads as an error; sibling empty states use guidance copy.

### Accessibility

Automated: 0 violations across 3 pages. Manual: 2.4.3 pass, 2.4.7 **fail**, 2.1.1 pass,
2.1.2 pass, 1.4.10 pass, 4.1.3 unverified (no status message in scope).

### Since last review

(incremental only) Fixed: 2. Still open: 1. Newly introduced: 0. Newly diverged because
the design moved: 1.

### Coverage statement

Not covered: Safari and Firefox rendering; dark mode (app implements none);
declined-payment state (needs gateway sandbox).

### Summary

One paragraph. Then: to action these findings, run `ux-design-fix`.
</example>

## References

- [references/capture-protocol.md](references/capture-protocol.md) — drive once, evidence bundle, determinism, keyboard traversal
- [references/design-source-resolution.md](references/design-source-resolution.md) — design truth ladder, design-side drift
- [references/environment-resolution.md](references/environment-resolution.md) — runnable UI, degradation, review state
- [references/merge-protocol.md](references/merge-protocol.md) — dedupe, precedence, independent corroboration
- [references/finding-classification.md](references/finding-classification.md) — categories, severity, confidence, risk matrix
- [references/accessibility-checklist.md](references/accessibility-checklist.md) — WCAG 2.2 AA, what automation never catches
- [references/ux-heuristics.md](references/ux-heuristics.md) — the bar when no design source exists
- product-management `delivery-conventions.md` — `specs/{work-short-name}/` path rules (companion plugin)
