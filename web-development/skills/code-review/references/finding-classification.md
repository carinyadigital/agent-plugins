# Finding classification

Every review finding is classified on three independent axes: **Category**
(what kind), **Severity** (how bad), and **Confidence** (how certain). Sub-agents
attach all three to each finding; the main review ranks by severity and
gates/verifies by confidence using the risk matrix below.

## Category

| Category | Covers | Primary source |
| -------- | ------ | -------------- |
| Security | Vulnerabilities, secrets, dependency/SCA risk — cite CWE/OWASP when known | security-checklist, bug-scan |
| Bug Risk | Logic errors, edge cases, crashes | bug-scan-reviewer |
| Stability | Resilience and availability under failure | quality-checklist (Resilience) |
| Maintainability | Structure, design, anti-patterns, readability | architecture-reviewer, quality-checklist |
| Performance | Inefficiency, N+1, resource use | quality-checklist (Performance) |
| Best Practices | Library/framework/version-correct usage | best-practices-reviewer |
| Scope / AC | Alignment with linked acceptance criteria and declared scope (any source) | acceptance-criteria / design-drift |

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

| Severity ↓ / Confidence → | High | Medium | Low |
| ------------------------- | ---- | ------ | --- |
| **High** (Critical/Major) | blocking | blocking | verify further |
| **Medium** (Moderate) | warning | warning | drop |
| **Low** (Minor/Trivial) | suggestion | suggestion | drop |

- **verify further** — the main review runs an independent re-check (or flags for a human); promote to blocking if confirmed, drop if refuted. This is the only cell that triggers extra evaluation.
- **Override:** Security-category findings at Medium+ confidence are always **blocking**, regardless of severity band.
- **Rank** findings within each action tier by severity (highest first).
- **Verdict:** FAIL if any blocking finding remains after verification.

## Who uses what

- **Sub-agents** — attach Category, Severity, and Confidence (with a one-line rationale and evidence) to each finding. Drop only **Speculative** findings; return the rest. Severity is a first estimate — the main review may adjust it with full-diff context.
- **Main review** — rank by severity, apply the matrix to assign the action label, verify the *verify further* cells, then produce the verdict.
