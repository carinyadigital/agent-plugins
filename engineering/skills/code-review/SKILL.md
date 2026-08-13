---
name: code-review
description: >
  Use when the user wants a code review of a branch, PR, MR, or working diff
  against its acceptance criteria and declared scope, in whatever form they take
  in this repo. Triggers on "review my branch", "review this PR", "check this
  diff before I raise it", "is this ready to merge". Works with any language,
  delivery process, or issue tracker. Produces a structured verdict with
  blocking, warning, and suggestion findings; writes no source changes. Do NOT
  use to address or fix review findings (code-review-fix), to implement work
  (implement), to publish a review to a provider as its reviewer
  (merge-request-review), to sign off completion of a larger body of work
  (validate), or to review rendered UI (ux-design-review).
license: MIT
compatibility: Requires git. Hosted PR/MR features require gh, glab, or an equivalent provider MCP tool.
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebFetch
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(glab:*)
  - Write(reviews/**)
  - Write(docs/work/**/reviews/**)
  - Edit(.gitignore)
argument-hint: "[branch-or-pr] [--since <sha>] [--full]"
metadata:
  author: Carinya Parc
  version: "1.1"
  owner: engineering
  work_shape: review-and-gate
  output_class: decision-support
  review_cadence: as-needed
---

Read artefacts from `docs/work/` and `docs/architecture/`.

# Code review

You are a Senior Software Engineer reviewing a change. You judge the code and
report. You do not change it.

## Read-only contract

This skill writes exactly two things: an entry in the shared review-tracking
file at `reviews/code-review.local.json`, and a human-readable report at
`docs/work/{work-item}/reviews/code-review-{nn}.local.md` (or
`reviews/code-review-{branch}.local.md` when no work item resolved). It
MUST NOT modify source, tests, configuration, or documentation (except
`.gitignore` as below), and MUST NOT commit, push, or comment on a provider.

`reviews/` is local state and MUST never be committed. Before the first write
into it, ensure the target repo's `.gitignore` contains a root-only `/reviews/`
entry. If it is missing, append:

```
# Local review state — never commit
/reviews/
```

Do not `git add` anything under `reviews/`.

When the review is done, point the reader at `code-review-fix` to action the
findings. Naming the next step is not the same as taking it — do not invoke it,
and do not offer a mode that would.

## Steps

1. **Eligibility** — decide whether to review at all, and how hard.
2. **Context** — build the Review Context bundle once.
3. **Summary** — describe the change and size the review.
4. **Lenses** — inline review, or parallel sub-agents.
5. **Merge** — dedupe and consolidate candidate findings.
6. **Verify** — rate each candidate independently.
7. **Gate** — apply the risk matrix, assign action labels.
8. **Report** — produce the verdict, persist review state.

---

## 1. Eligibility

Cheap checks first. Do not spend six agents on a lockfile bump.

**Skip entirely**, saying why in one line:

- PR/MR is closed or already merged.
- PR/MR is a draft, unless the user asked explicitly.
- The diff is empty, or contains only generated files, lockfiles, or vendored
  dependencies.
- Authored by a bot and touching nothing else.

**Reduce scope** rather than skipping:

- If `reviews/code-review.local.json` has an entry for this branch and
  `--full` was not passed, this is an **incremental** review. Review the delta
  from the recorded SHA. See
  [references/context-resolution.md](references/context-resolution.md) §6.

## 2. Context

Build the Review Context bundle following
[references/context-resolution.md](references/context-resolution.md): intent,
acceptance criteria, scope reference, guidelines, CI signal and existing analysis
output, review state, and applicable learnings.

Gather **once**. Pass the bundle to every sub-agent. Do not let agents re-fetch
it — duplicated discovery is the main way a parallel review wastes its budget.

Default scope: `git diff`. The user may name a branch, PR, MR, or file list.

## 3. Summary and effort

Write the change summary before reviewing. It orients the reader and it sizes
everything downstream.

Rate effort from lines changed, files touched, and whether the diff reaches
security-sensitive paths (auth, crypto, input handling) or data paths
(migrations, schemas, persisted payloads):

| Effort | Shape | Lens budget | Verification |
| ------ | ----- | ----------- | ------------ |
| **S** | < ~50 lines, < ~5 files, no sensitive or data paths | Inline only, no sub-agents | Your own judgement (no priors to check) |
| **M** | Ordinary feature or fix | At most 3 lenses: `bug-scan`, then the two highest-value triggered | Blocking and warning candidates |
| **L** | Large, structural, security-sensitive, or data-affecting | Every triggered agent | Every candidate |

Sensitive or data paths force **L** regardless of size. A three-line change to a
migration or an auth check is not a small review.

**Effort caps and triggers are ANDed.** Effort sets the ceiling on how many
lenses may run; the trigger table in §4.1 decides which are eligible. A lens runs
only if it is both triggered and within budget. At **M**, when more than three
trigger, keep `bug-scan` and choose the two with the strongest input: a resolved
acceptance criterion or a guideline file beats a speculative architecture pass.

## 4. Lenses

At **S**, review inline using the steps in §4.2 and skip to §5.

### 4.1 Sub-agents

Spawn in parallel. Only those whose trigger fires — never all of them by reflex.

Five lenses and one verifier. Each lens owns a distinct **input source**; that is
what earns it a separate context window, not the topic it covers.

| Agent | Reads | Trigger | Tier |
| ----- | ----- | ------- | ---- |
| [bug-scan-reviewer](agents/bug-scan-reviewer.md) | Diff hunks, git blame | Always, whenever spawning | standard |
| [requirements-reviewer](agents/requirements-reviewer.md) | Acceptance criteria, scope reference | Criteria **or** a scope/design reference was resolved in §2 | standard |
| [conventions-reviewer](agents/conventions-reviewer.md) | AGENTS.md/CLAUDE.md/rules, prior PR review comments | Repo has guideline files, **or** hosted PR with prior history on the touched files | standard |
| [best-practices-reviewer](agents/best-practices-reviewer.md) | External library docs | Manifest or lockfile changed, **or** the diff introduces an import not already used in that module | standard |
| [architecture-reviewer](agents/architecture-reviewer.md) | Sibling modules, architecture docs, ADRs | Diff adds modules, crosses layer boundaries, or adds cross-component dependencies | standard |
| [finding-verifier](agents/finding-verifier.md) | One candidate finding, in isolation | Once per candidate, at step 6 | fast |

Two lenses each cover both directions of one question, which is why there are
five rather than seven. `requirements-reviewer` checks both under-delivery
(uncovered criteria) and over-delivery (scope drift) against the same resolved
source — and can therefore spot when an unmapped hunk *is* the uncovered
criterion, built in the wrong place. `conventions-reviewer` reads both written
rules and rules that were only ever said in a past review comment; both produce
"your team requires X, here is the source".

`finding-verifier` is not a lens. It is a pipeline stage whose value comes
entirely from isolation, so it can never be merged into anything.

The `best-practices` trigger is deliberately narrow: it is the only lens that
reaches the network, and "touches a library" fires on nearly every diff.

**Model tiers** are declared as `metadata.model_tier` on each agent rather than
as model names, so runners without model selection inherit and still work:

| Tier | Use | Claude mapping | Where |
| ---- | --- | -------------- | ----- |
| fast | Mechanical predicates, retrieval, summarisation, per-finding verification | Haiku | Steps 1–3, `finding-verifier` |
| standard | Judgement against a bounded context | Sonnet | All five lenses |
| deep | Whole-system reasoning | Opus | Synthesis only (steps 5–8) |

No sub-agent runs at `deep`. Every lens works within a bounded context and an
explicit reading budget, which is exactly what a standard-tier model handles
well. Depth is needed where the whole picture comes together — merging,
gating, and writing the verdict — and that runs on the session's own model, not
in a sub-agent.

Verification is the highest-leverage use of the fast tier: it is what makes
running one verifier per candidate finding affordable, and independent
verification is worth more than a larger model rating its own work.

### 4.2 Inline review

Whether reviewing inline or supplementing agent output, cover:

1. Read the diff. Confirm what changed and why, against the resolved intent.
2. Check each change against the resolved acceptance criteria.
3. Security pass — [references/security-checklist.md](references/security-checklist.md).
4. Data and contracts, if the diff touches persistence, schemas, or published
   APIs — [references/quality-checklist.md](references/quality-checklist.md).
5. Error handling at every failure point.
6. Tests cover the acceptance criteria, including error and edge states.
7. Consistency with existing codebase patterns.
8. Reuse audit — search for an existing helper before accepting a new abstraction.
9. No unnecessary files, no scope creep.
10. Doc comments stand on their own inline — no issue-system keys, working-document
    paths, or other external references
    ([../../references/doc-comments.md](../../references/doc-comments.md)).

Apply [references/quality-checklist.md](references/quality-checklist.md)
throughout.

## 5. Merge

Consolidate every lens's output per
[references/merge-protocol.md](references/merge-protocol.md): dedupe on file plus
overlapping lines plus shared root cause, resolve category by precedence, take
maximum severity, raise confidence where **independent** agents corroborate,
surface contradictions rather than resolving them silently.

Corroboration is the reason to run parallel lenses at all. Do not discard it by
treating merged findings as a flat list.

## 6. Verify

Verification applies to whatever the effort budget in §3 covers: every candidate
at **L**, blocking and warning candidates at **M**, none at **S** — at S no
sub-agent raised a prior, so there is nothing independent to check and your own
reading stands.

Send each candidate in scope to
[finding-verifier](agents/finding-verifier.md), one invocation per finding, in
parallel.

The verifier receives the finding, its diff hunk, any quoted guideline, and the
Review Context — and **not** the raising agent's reasoning, name, or confidence
prior. That independence is the whole mechanism. An agent that has argued a
defect exists cannot also judge whether it is real.

The verifier's rating replaces the prior.

## 7. Gate

Apply the risk matrix in
[references/finding-classification.md](references/finding-classification.md) to
assign each finding an action label: `[blocking]`, `[warning]`, or
`[suggestion]`. Rank by severity within each tier.

Security findings at Medium+ confidence are always blocking. High-severity
findings the verifier could not confirm are surfaced as `[warning] unverified`,
never silently dropped.

## 8. Report and persist

Produce the verdict in the format below, then persist review state per the
schema in [references/context-resolution.md](references/context-resolution.md)
§6:

1. Update (or create) this branch's entry in the shared
   `reviews/code-review.local.json`, so the next run can go incremental.
2. Write the human-readable verdict to
   `docs/work/{work-item}/reviews/code-review-{nn}.local.md`, where
   `{work-item}` is the ID resolved in §2 (folder rules per
   [delivery-conventions.md](../../references/delivery-conventions.md)) and
   `{nn}` is the next sequential two-digit number among existing
   `code-review-*.local.md` files in that folder (do not count other skills'
   reports). Numbered history applies only under
   `docs/work/{work-item}/reviews/`. When no work item resolved, write
   `reviews/code-review-{branch}.local.md` instead (`/` in the branch
   name replaced with `-`) — latest-only: overwrite that file; do not invent
   numbering on the branch-level path.

These are the only review-artefact paths this skill writes. The only other
allowed write is appending `/reviews/` to `.gitignore` when that entry is
missing.

---

## Do not report

- Pre-existing issues, or anything on lines the author did not modify.
- Anything a linter, typechecker, compiler, or CI would catch. Do not build or
  typecheck. Where CI has already failed, acknowledge each failure rather than
  re-deriving it.
- Rules explicitly silenced in code (lint-ignore comments and equivalents).
- Changes clearly intentional or directly serving the broader change.
- Injection, ReDoS, SSRF, or path traversal on input that is provably not
  attacker-controlled. Trace provenance first — a regex in a test matcher is not
  production ReDoS.
- Findings a `dismissed` entry in the review state already covers, for unchanged
  code.
- Pedantic nitpicks a senior engineer would not raise.

## Quality rules

- Every finding carries evidence: file path, line, observed behaviour.
- No subjective style nits.
- Do not contradict an explicit design decision; if one looks wrong, raise it as
  a suggestion naming the decision.
- Prefix every finding with its action label, then
  `Category | Severity | Confidence`, so `code-review-fix` can route it.
- Group by action: Blocking, Warnings, Suggestions.
- Flag comments that cite issue systems, working documents, or any other
  external source. They MUST stand on their own so they can be read inline.

## Must not

- Rewrite code or propose refactoring beyond the diff — raise a follow-up instead.
- Include business or strategic rationale that belongs in a product doc.
- Restate acceptance criteria already in the resolved context — reference them.
- Return PASS while CI failures are unacknowledged.
- Modify any file outside `reviews/`, `docs/work/*/reviews/`, and `.gitignore`
  (the `/reviews/` entry only).
- Commit anything under `reviews/`.

## Output format

<example>
## Code Review

**Result:** PASS | FAIL
**Risk level:** Low | Medium | High
**Scope reviewed:** `git diff` (or branch/PR), incremental from `a1b2c3d` | full
**Review effort:** S | M | L
**Lenses run:** bug-scan, acceptance-criteria, guideline-compliance

### Change summary

What changed and why, in 2-4 sentences, grouped by area.

### Blocking Issues

- **[blocking] Security | Severity: Critical | Confidence: Confirmed**
  **File:** src/auth.ts:42
  **Issue:** ...
  **Evidence:** ...
  **Remediation:** ...

### Warnings

- **[warning] Data Integrity | Severity: Major | Confidence: Probable**
  **File:** migrations/0007_add_tenant.sql:12
  **Issue:** ...
  **Evidence:** ...
  **Remediation:** ...

### Suggestions

- **[suggestion] Maintainability | Severity: Minor | Confidence: Probable**
  **File:** src/context/assembler.test.ts:12
  **Issue:** ...
  **Remediation:** ...

### Acceptance Criteria Coverage

Criterion → pass | fail | partial → evidence (path:line).

### Since last review

(incremental runs only) Fixed: 2. Still open: 1. Newly introduced: 1.

### CI and existing analysis

Each failing check acknowledged. Scanner findings referenced or rebutted with
provenance.

### Summary

One paragraph. Then: to action these findings, run `code-review-fix`.
</example>

## References

- [references/context-resolution.md](references/context-resolution.md) — discovering intent, criteria, scope, CI signal, review state, learnings
- [references/merge-protocol.md](references/merge-protocol.md) — dedupe, precedence, corroboration, contradiction
- [references/finding-classification.md](references/finding-classification.md) — category, severity, confidence, risk matrix
- [references/quality-checklist.md](references/quality-checklist.md) — timeless review checklist
- [../../references/doc-comments.md](../../references/doc-comments.md) — comments must stand on their own; no issue systems or working documents
- [references/security-checklist.md](references/security-checklist.md) — security pass, input provenance
- [../tasks/references/delivery-conventions.md](../../references/delivery-conventions.md) — `docs/work/{work-id}/` path rules
