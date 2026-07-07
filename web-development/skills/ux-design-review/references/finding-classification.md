# Finding classification

Every UX review finding is classified on three independent axes: **Category**
(what kind), **Severity** (how bad), and **Confidence** (how certain).
Sub-agents attach all three to each finding; the main review ranks by
severity and gates/verifies by confidence using the risk matrix below.
(Same model as the code-review skill, with UX categories.)

## Category

| Category | Covers | Primary source |
| -------- | ------ | -------------- |
| Accessibility | WCAG 2.2 AA failures — cite the criterion | accessibility-reviewer |
| Design Fidelity | Deviation from the resolved design source | design-fidelity-reviewer |
| Interaction/UX | Broken/missing states, confusing flows, feedback gaps | interaction-states-reviewer |
| Responsiveness | Viewport adaptation, overflow, touch ergonomics | responsive-reviewer |
| Design System | Hard-coded values over tokens, reinvented components, pattern drift | design-system-reviewer |
| Visual Polish | Alignment, spacing rhythm, typography, hierarchy | ux-heuristics pass |
| Content | Copy clarity, grammar, tone, terminology consistency | any lens |

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

## Risk matrix

Group each axis into High / Medium / Low, then read the action:

- **Confidence:** High = Confirmed/Probable, Medium = Possible, Low = Tentative/Speculative.
- **Severity:** High = Critical/Major, Medium = Moderate, Low = Minor/Trivial.

| Severity ↓ / Confidence → | High | Medium | Low |
| ------------------------- | ---- | ------ | --- |
| **High** (Critical/Major) | blocking | blocking | verify further |
| **Medium** (Moderate) | warning | warning | drop |
| **Low** (Minor/Trivial) | suggestion | suggestion | drop |

- **verify further** — re-test the state, re-capture, or re-run the check;
  promote to blocking if confirmed, drop if refuted. The only cell that
  triggers extra evaluation.
- **Override:** Accessibility-category findings at Medium+ confidence are
  always **blocking**, regardless of severity band — the AA bar is a
  compliance floor, the analogue of code-review's Security override.
- **Rank** findings within each action tier by severity (highest first).
- **Verdict:** FAIL if any blocking finding remains after verification. A
  PASS with reduced coverage (static-only lenses) must say so.

## Who uses what

- **Sub-agents** — attach Category, Severity, and Confidence (with
  evidence: screenshot path or file:line) to each finding. Drop only
  **Speculative** findings; return the rest.
- **Main review** — rank by severity, apply the matrix to assign the
  action label (`[blocking]` / `[warning]` / `[suggestion]` — the labels
  `ux-design-review fix` routes on), verify the *verify further* cells,
  then produce the verdict with the coverage statement.
