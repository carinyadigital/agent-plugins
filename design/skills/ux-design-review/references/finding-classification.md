# Finding classification

Every UX review finding is classified on three independent axes: **Category**
(what kind), **Severity** (how bad), and **Confidence** (how certain). Same model as
the `code-review` skill, with UX categories and an accessibility override in place of
the security one.

Confidence is produced in two stages. A lens attaches a **prior** to each finding it
raises. That prior is then replaced by an independent rating from `finding-verifier`,
which never sees the raising lens's reasoning. A lens that has just spent its context
arguing a defect exists cannot also judge whether it is real.

Pipeline: lenses raise → [merge-protocol.md](merge-protocol.md) dedupes and adjusts for
independent corroboration → `finding-verifier` rates confidence → the risk matrix below
assigns the action label.

## Category

Listed in **precedence order**. A defect that attracts several categories takes the
highest (see [merge-protocol.md](merge-protocol.md) step 2).

| Category | Covers | Primary source |
| -------- | ------ | -------------- |
| Accessibility | WCAG 2.2 AA failures — cite the criterion | accessibility-reviewer |
| Interaction/UX | Broken/missing states, confusing flows, feedback gaps | experience-reviewer |
| Responsiveness | Viewport adaptation, overflow, touch ergonomics | experience-reviewer |
| Design Fidelity | Deviation from the resolved design source | conformance-reviewer |
| Design System | Hard-coded values over tokens, reinvented components, pattern drift | conformance-reviewer |
| Visual Polish | Alignment, spacing rhythm, typography, hierarchy | ux-heuristics pass |
| Content | Copy clarity, grammar, tone, terminology consistency | any lens |

Accessibility leads the order because it carries the compliance override: a defect that
is both an a11y failure and a fidelity deviation is blocking on the a11y ground,
whatever it looks like.

Correctness, security, and performance are **not** categories here — route
them to the code-review skill.

## Severity

Likelihood a user hits it multiplied by impact when they do.

| Severity rating | Range | Meaning |
| --------------- | ----- | ------- |
| Critical | 91–100 | Blocks a class of users or a primary flow — inaccessible checkout, unusable mobile layout |
| Major | 76–90 | Real barrier or definite standard/source violation with significant user impact |
| Moderate | 51–75 | Noticeable degradation; users succeed with friction |
| Minor | 26–50 | Small rough edge on a secondary path |
| Trivial | 0–25 | Negligible; optional polish |

## Confidence

Certainty the finding is a true positive.

| Confidence rating | Range | Meaning |
| ----------------- | ----- | ------- |
| Confirmed | 91–100 | Reproduced in the live UI with evidence captured |
| Probable | 76–90 | Strong evidence; very likely real |
| Possible | 51–75 | Plausible; not fully reproduced (e.g. state unreachable) |
| Tentative | 26–50 | Weak evidence; may be a false positive |
| Speculative | 0–25 | Little evidence; likely false positive or pre-existing |

Static-only findings cap at **Probable** for anything a live check could
have confirmed — reserve Confirmed for what was actually rendered and seen.

Findings resting on a region the capture marked **unstable** cap at **Tentative**: the
evidence did not reproduce across paired captures, so the difference may be flake rather
than defect. See [capture-protocol.md](capture-protocol.md) §2.

## Risk matrix

Group each axis into High / Medium / Low, then read the action:

- **Confidence:** High = Confirmed/Probable, Medium = Possible, Low = Tentative/Speculative.
- **Severity:** High = Critical/Major, Medium = Moderate, Low = Minor/Trivial.

Confidence entering this matrix is the **verifier's** rating, not the raising lens's
prior.

| Severity ↓ / Confidence → | High | Medium | Low |
| ------------------------- | ---- | ------ | --- |
| **High** (Critical/Major) | blocking | blocking | escalate |
| **Medium** (Moderate) | warning | warning | drop |
| **Low** (Minor/Trivial) | suggestion | suggestion | drop |

- **escalate** — a high-severity finding the verifier could not confirm, usually because
  the state was unreachable or the region was unstable. Do not drop it and do not block
  on it. Surface it under Warnings as `[warning] unverified`, saying what could not be
  established. A possible blocking accessibility defect deserves a human's attention
  even on thin evidence.
- **Override:** Accessibility-category findings at Medium+ confidence are
  always **blocking**, regardless of severity band — the AA bar is a
  compliance floor, the analogue of code-review's Security override.
- **Rank** findings within each action tier by severity (highest first).
- **Verdict:** FAIL if any blocking finding remains. A PASS with reduced coverage
  (static-only, unreachable states, single browser) must say so.

## Who uses what

- **Lenses** — attach Category, Severity, and a Confidence **prior**, with evidence
  (screenshot path, `file:line`, axe rule, WCAG criterion). Drop only **Speculative**
  findings; return the rest.
- **Merge step** ([merge-protocol.md](merge-protocol.md)) — dedupe across components,
  states, and viewports; resolve category by precedence; take max severity; raise
  confidence only for *independent* corroboration.
- **`finding-verifier`** — rates confidence independently. May re-render one state to
  settle a finding. Its rating replaces the prior.
- **Main review** — rank by severity, apply the matrix to assign the action label
  (`[blocking]` / `[warning]` / `[suggestion]` — the labels `ux-design-fix`
  routes on), then produce the verdict with the coverage statement.
