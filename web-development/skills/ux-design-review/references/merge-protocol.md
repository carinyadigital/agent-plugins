# Merge protocol

How to combine findings from parallel lenses into one verdict.

Visual findings overlap far more than code findings do. A card with 12px padding where
the token says 16px is simultaneously a Design Fidelity deviation, a Design System
violation, and a Visual Polish inconsistency. Three lenses, three entries, one defect.

Run this after every lens returns and before applying the risk matrix in
[finding-classification.md](finding-classification.md).

## 1. Dedupe

Two findings are **the same finding** when all three hold:

- Same component or page region.
- Overlapping state or viewport.
- Same root cause, not merely the same symptom.

**The same defect at three viewports is one finding with three captures**, not three
findings. Report it once, list the viewports, attach the clearest capture. A reader
does not need to be told three times that a button overflows.

The exception: when a defect appears *only* at some viewports or states, that is
diagnostic and belongs in the finding. "Overflows at 375 only" is more useful than
"overflows".

## 2. Category precedence

A merged finding takes the highest-precedence category of its members:

```
Accessibility > Interaction/UX > Responsiveness > Design Fidelity >
Design System > Visual Polish > Content
```

Accessibility leads because it carries the compliance override — a finding that is both
an a11y failure and a fidelity deviation is blocking on the a11y ground regardless of
how it looks.

Record the dropped categories in the evidence. "Also a Design System violation — the
token exists" tells the author *how* to fix it, which the fidelity framing alone does
not.

## 3. Severity: take the maximum

Never average. One lens rating a finding Critical where others said Moderate is signal:
that lens may be the only one that saw the state where it actually blocks a user.

## 4. Confidence: corroboration must be independent

Independent lenses reaching the same conclusion from different evidence is the strongest
signal available. But **this skill makes double-counting easy**, because after the
capture step every lens reads the same bundle.

| Situation | Counts as corroboration? |
| --------- | ------------------------ |
| Conformance lens (design source) and experience lens (observed behaviour) both flag it | **Yes** — different evidence |
| Accessibility lens (axe rule) and conformance lens (token audit) both flag it | **Yes** — different evidence |
| Two lenses both reading the same screenshot | **No** — one observation, counted twice |
| Two lenses both citing the same axe violation | **No** — one scanner result |
| Same lens flagging it at three viewports | **No** — one finding, three captures |

When corroboration is genuine: two independent sources raise confidence one band, three
or more raise it to Confirmed unless the verifier refutes it.

## 5. Contradiction is surfaced

Where lenses disagree about whether something is a defect:

- **Accessibility wins over aesthetics, always.** If the conformance lens wants a
  lighter placeholder to match the mockup and the accessibility lens says it fails
  contrast, the design source is wrong. Report it as an accessibility finding *and*
  flag the design source as needing correction — that is a finding about the design,
  not about the code.
- **The app's own consistency beats the heuristics reference.** If the app
  consistently does something the heuristics discourage, that is a convention, not a
  defect.
- Never drop the losing side silently. Record it.

## 6. Evidence union

Keep every member's evidence: screenshot paths, `file:line` for static findings, axe
rule IDs, WCAG criteria. A merged finding carrying both a capture and a `file:line` is
substantially more actionable than either alone — the capture shows the reader the
problem, the line tells them where to fix it.

Cap at four evidence items; keep the most specific.

## 7. Hand off to verification

The deduped candidate list goes to
[finding-verifier](../agents/finding-verifier.md), one invocation per candidate, before
the risk matrix is applied. Merge first, so the verifier sees each defect once with its
full evidence union rather than scoring three fragments of it.

## Output of this step

```text
Finding: <one line>
Where: <component/page> — <states> @ <viewports>
Category: <highest-precedence>  (also: <dropped categories>)
Severity: <max across members>
Confidence: <prior, adjusted only for independent corroboration>
Raised by: <lens list>
Evidence:
  - <screenshot path> — <what it shows>
  - <file:line> — <what it is>
  - <axe rule / WCAG criterion>
```

Nothing here has an action label yet. Labels are assigned after verification.
