# Merge protocol

How to combine findings from parallel sub-agents into one review. Three lenses
can raise the same defect more than once, in different words and categories.
Without a protocol the output multiplies and the strongest available signal —
independent agreement — is thrown away.

Run this after every sub-agent returns and before applying the risk matrix in
[finding-classification.md](finding-classification.md).

## 1. Dedupe

Two findings are **the same finding** when all three hold:

- Same file.
- Overlapping line range (any overlap, not identity — agents anchor differently).
- Same root cause, not merely the same symptom.

The third test is the one that matters. "Missing await on line 42" and "unhandled
rejection on line 42" are one finding. "Missing null check on line 42" and
"missing await on line 42" are two findings that happen to share a line.

When in doubt, keep them separate. A duplicate is noise; a wrongly-merged pair
loses a real defect.

## 2. Category precedence

A merged finding takes the highest-precedence category of its members:

```
Security > Bug Risk > Stability > Data Integrity > Scope / AC >
Best Practices > Performance > Maintainability
```

Record the dropped categories in the finding's evidence. "Also flagged as
Maintainability by code-reviewer" tells the author this is not only a security
problem, which changes how they fix it.

## 3. Severity: take the maximum

Never average. One agent seeing Critical where others saw Moderate is signal, not
an outlier to be smoothed away — that agent may be the only one holding the
context that makes it Critical.

If the maximum comes from a single agent and every other agent rated it two or
more bands lower, note the spread in the finding. The verification handoff in
step 7 resolves it.

## 4. Confidence: corroboration raises it

**This is the step that justifies running parallel agents at all.** Independent
lenses arriving at the same defect from different starting evidence is the
strongest signal available in the whole review, and it is invisible to any single
agent.

| Independent agents raising it | Effect on confidence |
| ----------------------------- | -------------------- |
| 1 | Unchanged; the raising agent's rating stands as a prior |
| 2 | Raise one band (Possible → Probable) |
| 3 or more | Raise to Confirmed unless the verifier refutes it |

"Independent" means the agents did not share a derivation. `bug-scan-reviewer`
and `code-reviewer` finding the same missing error handler is
corroboration: one reasoned from the code, the other from a written rule. Two
findings resting on the same AGENTS.md line are **not** corroboration; that is
one piece of evidence counted twice. Collapse those to a single vote.

The same trap exists **inside** the multi-source lenses. `code-reviewer` finding
a rule in both a guideline and a prior review comment is one source, not two —
the agent is instructed to collapse it, and the merge step must not re-inflate
it. Likewise an uncovered criterion and its matching scope drift from
`requirements-reviewer` are one problem seen twice, not two independent votes.

## 5. Contradiction is surfaced, never silently resolved

When agents disagree about whether something is a defect at all:

- **Local rule beats external guidance.** If `code-reviewer` finds library docs
  saying "use X" while a repo rule says "never X", the repo rule wins. The
  codebase's explicit decision outranks a general recommendation.
- **Surface the conflict anyway**, as a `[suggestion]`, with both sources named.
  The team may want to revisit the rule, and that is their call to make, not the
  review's to make silently. This is also the honest outcome: the review found a
  real tension and is reporting it rather than picking a side.
- **Never** drop the losing side without recording it.

## 6. Evidence union

The merged finding keeps every member's evidence line. Three agents each
contributing a `path:line` and an observed behaviour produce a more actionable
finding than any one of them alone, and the author can see why it was flagged
from several directions.

Cap at four evidence lines; beyond that, keep the four most specific.

## 7. Hand off to verification

After merging, apply the risk matrix provisionally using the merged confidence
prior. Provisional blocking and warning candidates, plus every Security
candidate, go to `finding-verifier`
([../agents/finding-verifier.md](../agents/finding-verifier.md)), one invocation
per finding. Merge first so the verifier sees corroborated findings once, with
their full evidence union, rather than scoring fragments of the same defect
independently. Suggestions keep their merged prior and cannot be promoted
without verification.

## Output of this step

A deduped candidate list, each entry carrying:

```text
Finding: <one line>
File: <path:line>
Category: <highest-precedence category>  (also flagged: <dropped categories>)
Severity: <max across members>           (spread: <note if wide>)
Confidence: <prior, adjusted for corroboration>
Raised by: <agent list>
Evidence:
  - <path:line> — <observed behaviour>
  - ...
```

This list is the input to verification and gating. It is not yet the review
output: nothing here has been assigned an action label.
