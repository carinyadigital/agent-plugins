# Finding classification

Every review finding is classified on three independent axes: **Category**
(what kind), **Severity** (how bad), and **Confidence** (how certain).

Confidence starts as a **prior** attached by the raising sub-agent. For
provisional blocking and warning findings, plus every Security finding, that
prior is replaced by an independent rating from `finding-verifier`, which never
sees the raising agent's reasoning. Suggestion-only findings retain the merged
prior and cannot be promoted without verification.

Pipeline: sub-agents raise → [merge-protocol.md](merge-protocol.md) dedupes and
adjusts for corroboration → the risk matrix assigns a provisional action →
`finding-verifier` independently rates findings in scope → the final matrix
assigns the action label.

## Category

Listed in **precedence order**. When one defect attracts several categories, the
merged finding takes the highest-precedence one (see
[merge-protocol.md](merge-protocol.md) step 2).

| Category | Covers | Primary source |
| -------- | ------ | -------------- |
| Security | Vulnerabilities, secrets, dependency/SCA risk — cite CWE/OWASP when known | security-checklist, bug-scan |
| Bug Risk | Logic errors, edge cases, crashes | bug-scan-reviewer |
| Stability | Resilience and availability under failure | quality-checklist (Resilience) |
| Data Integrity | Data correctness and persistence: schema and migration safety, backfills, contract and payload compatibility, integration boundaries | quality-checklist (Data and contracts) |
| Scope / AC | Alignment with linked acceptance criteria and declared scope (any source) | requirements-reviewer |
| Best Practices | Library/framework/version-correct usage | code-reviewer |
| Performance | Inefficiency, N+1, resource use | quality-checklist (Performance) |
| Maintainability | Local rules, structure, design, anti-patterns, readability | code-reviewer, quality-checklist |

**Data Integrity** exists as its own category because schema migrations,
backfills, and contract changes have blast radius far beyond the diff that
introduces them, and they are frequently irreversible once deployed. A finding
that would be Moderate as a Bug Risk is often Major as Data Integrity, because
the failure mode is corrupted or unrecoverable data rather than a crash.

## Issue severity

Likelihood the issue occurs multiplied by its impact. Answers "how bad if real".

| Severity rating | Range | Meaning |
| --------------- | ----- | ------- |
| Critical | 91–100 | Likely to occur with severe impact — data loss, security breach, outage |
| Major | 76–90 | Real defect with significant impact, or a definite rule violation |
| Moderate | 51–75 | Real but limited impact or lower likelihood |
| Minor | 26–50 | Small functional impact |
| Trivial | 0–25 | Negligible; optional polish |

## Confidence

Certainty the finding is a true positive, not a false alarm. Answers "how sure".

| Confidence rating | Range | Meaning |
| ----------------- | ----- | ------- |
| Confirmed | 91–100 | Verified against the code; definitely real |
| Probable | 76–90 | Strong evidence; very likely real |
| Possible | 51–75 | Plausible but not fully verified |
| Tentative | 26–50 | Weak evidence; may be a false positive |
| Speculative | 0–25 | Little evidence; likely false positive or pre-existing |

## Risk matrix

Group each axis into High / Medium / Low, then read the action:

- **Confidence:** High = Confirmed/Probable, Medium = Possible, Low = Tentative/Speculative.
- **Severity:** High = Critical/Major, Medium = Moderate, Low = Minor/Trivial.

For provisional blocking and warning candidates, confidence entering this
matrix is the **verifier's** rating, not the raising agent's prior. Suggestions
that are not independently verified retain their merged confidence prior and
cannot be promoted above suggestion without verification.

| Severity ↓ / Confidence → | High | Medium | Low |
| ------------------------- | ---- | ------ | --- |
| **High** (Critical/Major) | blocking | blocking | escalate |
| **Medium** (Moderate) | warning | warning | drop |
| **Low** (Minor/Trivial) | suggestion | suggestion | drop |

- **escalate** — a high-severity finding the verifier could not confirm. Do not
  drop it and do not block on it. Surface it under Warnings, labelled
  `[warning] unverified`, stating what could not be established and what the
  reader should check. A possible critical defect is worth a human's attention
  even when the evidence is thin; silently dropping it is the worse error.
- **Override:** Security-category findings at Medium+ confidence are always
  **blocking**, regardless of severity band.
- **Rank** findings within each action tier by severity (highest first).
- **Verdict:** FAIL if any blocking finding remains.

## Who uses what

- **Sub-agents** — attach Category, Severity, and a Confidence **prior** (with a
  one-line rationale and evidence) to each finding. Drop only **Speculative**
  findings; return the rest. Both severity and confidence are first estimates.
- **Merge step** ([merge-protocol.md](merge-protocol.md)) — dedupe, resolve
  category by precedence, take max severity, adjust confidence for independent
  corroboration.
- **`finding-verifier`** — rates provisional blocking and warning candidates,
  plus every Security candidate, independently and without the raising agent's
  reasoning. Its rating replaces the prior where verification runs.
- **Main review** — rank by severity, apply the matrix to assign the action
  label, then produce the verdict.

## Data Integrity severity guidance

Because reversibility dominates impact for this category, rate it against
recoverability rather than immediate blast:

| Situation | Floor |
| --------- | ----- |
| Irreversible migration with no rollback path, or a destructive backfill | Critical |
| Breaking change to a published contract, event payload, or shared schema with live consumers | Major |
| Additive schema change with a locking risk on a large table | Major |
| Reversible migration missing a documented rollback | Moderate |

These are floors, not ceilings. Raise them when consumer count or data volume
warrants it.
