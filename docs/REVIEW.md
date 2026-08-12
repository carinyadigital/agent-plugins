# Carinya Parc Agent Skills — outstanding review backlog

**Original review:** `carinyaparc/skills` @ `2e7d67e` (12 Aug 2026)  
**Last pruned:** 12 Aug 2026 against `carinya-plugins` (practice-plugin layout)  
**Cleared:** all P0s (shellcheck CI, promise matcher + turn scope, `create_mr` reachability, Cursor-only `done` docs, `Edit` on `adr`/`tdd`, version scheme), §3.1 (`skill-review` → `skill-authoring`), §4.2 sibling routes, dual `trigger-queries` schema, link resolver, mutation-test in CI, `debug` skill, roadmap no longer requires backlog (Product → Solution → Roadmap → Backlog), §2.4 description budget (`tdd`/`tasks`/`solution`), root README delivery path tree + hierarchy, validator agent/orphan/description-budget contracts (P1 item 1 core), `skill-authoring/template/SKILL.md` pack convention (P1 item 5).

This file keeps **open** findings only. Fixed and superseded claims were removed so the list is reviewable as a backlog.

---

## 1. Structural gaps

### 1.1 Five state models, no shared key
Tracker pointer (`TASKS.local.md`), work-item status (`backlog.md` / `tasks.md`), review state (`docs/reviews/{skill}.local.json` keyed on **branch**), numbered review verdicts (`docs/work/{id}/reviews/`), and loop state (`.claude/loop/`) do not share a key. Nothing on disk joins task ↔ branch ↔ review ↔ MR.

Consequences still true:
- **`validate` produces no file** — Phase 8 is chat output only; no `docs/work/{id}/reviews/validation-*.md` (or equivalent). Sign-off leaves no durable artefact.
- **Numbered review history is per-working-copy** — `{nn}` from directory listing; a fresh clone restarts at `01`.
- **`docs/reviews/review-learnings.local.md` is read and never written** — specified in `code-review` context-resolution; no `--learn` (or other) writer. Mechanism is inert.

### 1.2 Status vocabulary: three enums
Schema (`work-item-schema.md`): `not started` · `in progress` · `blocked` · `done`.  
`validate` still writes `in-progress` and cannot record `blocked`.  
`backlog.template.md` still declares Title-case values including `In review`.

### 1.3 "Approved" is load-bearing and undefined
`implement` requires an **approved** `tdd.md`. Templates still ship `status: Draft`; no skill flips that field; no separate checklist gate. `[NEEDS CLARIFICATION]` has no budget and no hard consumer in `implement` / `ralph-loop-setup`.

### 1.4 Duplicated contracts that will drift
Same contracts live in sibling skill trees and have already diverged. Keep copies local to each practice/skill (no shared references package) — align wording in place and/or add a drift check on pairs that must stay identical:
- Risk matrix core table is aligned; escalate prose + Security vs Accessibility overrides still differ across the two `finding-classification.md` files
- `merge-protocol.md` UX now has a Contradiction section but still omits code's `[suggestion]` surface rule
- Review-state JSON schema (code `context-resolution` vs UX `environment-resolution`); `code-review-fix` still has **zero** markdown links
- Persist procedure inlined in both review `SKILL.md` bodies
- Provider detection: Bitbucket Cloud/Server split in `provider-resolution.md` vs collapsed Rovo routing in `provider-operations.md`
- `merge-request-babysit` still reaches into sibling `provider-resolution.md` for babysit mode
- Filename collision: UX `environment-resolution.md` (browser) vs `ralph-loop-setup/.../environment-resolution.md` (template vars) — latter not renamed

### 1.5 Review → fix ingest still half-wired
Review → fix **ingest** still not the declared default Input: `code-review-fix` / `ux-design-fix` offer conversation / path / paste — not `docs/reviews/{skill}.local.json` + `report`. Preset still tells reviews to write `{{RUN_DIR}}/review-{TASK_ID}.md` (ownership / grant mismatch).

---

## 2. Triggering, routing, naming

### 2.1 PR/MR synonym split
Both `code-review` and `merge-request-review` descriptions now mention PR and MR, but trigger quotes stay asymmetric (`"review this PR"` vs `"review this MR"`) and authorship/publication disambiguation is still weak. All three `merge-request*` skills still have **zero** evals.

### 2.2 `ralph-loop` setup contradiction + no NL triggers
Still forbids seeding via description while body/evals allow ad-hoc seed on `--prompt`. Still no quoted natural-language triggers (only command forms). Metadata classification keys are present (that part of the old finding is closed).

### 2.3 `tdd` name still costly
Still named `tdd`; short TDD disclaimer remains in the description; `implement` still adjudicates the naming collision. Rename to `tech-design` (keep `tdd.md` artefact if desired) remains the highest-leverage naming fix.

---

## 3. Review methodology — instrumentation

### 3.1 `code-review` gaps vs UX sibling
- No coverage statement when M-effort truncates lenses (UX gates PASS on a manifest-derived statement).
- No confidence provenance (`Confirmed (verified)` vs `Confirmed (self)`).
- Severity within an already-blocking finding still has no independent check (narrowed finding).
- `validate` remains the weakest machinery for the strongest claim ("production-ready"): no confidence axis, no verifier, bare `Bash` on `ac-evidence-verifier`.
- `docs-review` still borrows `blocking`/`warning`/`suggestion` without the matrix, and asserts link/orphan counts its toolset cannot check.

### 3.2 High-privilege agents still nonconformant
Validator now enforces agent contracts (`model: inherit`, constrained tools, `model_tier`, numeric budget) — these three still fail it:

| Agent | Gap |
|---|---|
| `validate/.../ac-evidence-verifier` | bare `Bash`, no `model_tier`, no reading budget |
| `merge-request-babysit/.../mr-babysitter` | full `Bash` (push-capable), no `model_tier`, no reading budget |
| `skill-authoring/.../eval-grader` | no `model_tier`, no budget |

UX `finding-verifier` still cannot re-capture (tools: Read/Grep/Glob). `architecture-reviewer` still both discovers guidelines and is told not to re-derive them.

### 3.3 Evals: assertions without an execution path
Evals exist; there is still no runner, no fixtures repo, no with/without baseline arms. CI covers structural validation + Ralph suites + mutation-test — not skill evals.

Still missing evals on high-risk write skills: `implement`, all three `merge-request*`, `skill-review`.  
`code-review/evals.json` still asserts a "security-focused pass (auth)" wording that does not match the agent roster.

### 3.4 Verifier blinding drift
`merge-protocol` prose still puts the raising agent name in **evidence** (what the verifier receives) while the output schema puts it on Category. UX verifier still lacks the code verifier's "disregard the surplus" defence sentence.

---

## 4. Coverage gaps (still absent or partial)

| Stage | Status |
|---|---|
| `AGENTS.md` authoring / audit | **Absent** (many skills read it) |
| Requirements clarification (`clarify`) | **Absent** |
| Cross-artefact consistency (`analyze`) | **Absent** |
| Standing constitution | **Absent** |
| Incident / postmortem | **Absent** |
| Prod deploy + rollback triggers | **Partial** — `deploy-qa` is QA checkout, not prod deploy |
| Release notes / changelog skill | **Absent** |
| Dependency upgrades | **Partial** — `platform-health` |
| Test strategy authoring | **Partial** — template / folded into `implement` |
| Security / performance / data review | **Partial** — inside `code-review` categories |
| Observability | **Partial** — `platform-health` |
| Spike routing | **Open contradiction** — schema → `implement` vs "never ships code" |
| Research-briefing preset | **Prose only** — not in `assets/presets/` |
| Tech-debt / refactor prioritisation | **Partial** — `tech-debt` exists; implement/fix still wall off drive-by refactors |
| Deferral → follow-up work item | **Absent** — eight deferral routes evaporate |

Cap discipline still applies: prefer modes on existing skills over unbounded new entries (~24 ceiling).

---

## 5. Outstanding recommendations

### P1 — Make the guardrails real
1. ~~Expand `validate.py` / `validate_skills.py`: real YAML parse; description budgets; every `agents/*.md` (`model: inherit`, constrained tools, `model_tier`, numeric budget); fail on orphan `SKILL.md` outside `skills/` (excl. `template/`).~~ — landed as `scripts/validate_plugins.py` + `scripts/validate_skills.py` (orchestrated by `validate.py`); Ralph suites in `validate_ralph.py`. Optional body line-budget still open if authoring checklist requires it.
2. ~~Add `tasks/scripts/*.sh` (e.g. `check-epic-paths.sh`) to shellcheck globs~~ — removed; epic-path rules live in the tasks skill pre-save checklist and `validate_ralph.py`.
3. CODEOWNERS, PR template (CONTRIBUTING checklist), Python version matrix, markdownlint; finish manifest/version consistency checks.
4. Align duplicated review contracts in place (and/or drift-check identical pairs); rename ralph `environment-resolution.md` → `template-variable-resolution.md`. Do not introduce a shared references package.
5. Cap uncapped budgets (doc batches, L verifier fan-out, UX capture matrix); revisit whether scoped Bash on babysit/ac-evidence is still too wide.

### P2 — Close the contract gaps
7. Adopt work-item state file (e.g. `.carinya/work.json`) keyed on work item, not branch alone.
8. Define "approved" as a separate checklist with an owner; give `[NEEDS CLARIFICATION]` a budget + hard block in `implement` / setup.
9. One status enum everywhere; fix validate `in-progress` and backlog `In review`.
10. Persist validate report; make `docs/reviews/*.local.json` + `report` the default fix-skill Input; assign preset review artefact ownership.
11. Resolve or delete inert `review-learnings`; fix spike contradiction.
12. Ralph beyond P0: flock on iteration bump; Cursor `RALPH_SESSION_ID` (or qualify isolation as Claude-only); `command -v` for `perl`/`jq`; fail-closed on declared-but-missing state; wall-clock/cost ceilings; stall keyed on `current_step`; `compatibility:` frontmatter.
13. Tighten MR grants (`gh pr merge` / unscoped Write); gate publish on babysit; gate `tdd` `git mv`.
14. Symmetric PR/MR trigger quotes on `code-review` ↔ `merge-request-review`; NL triggers + resolve setup contradiction on `ralph-loop`.

### P3 — Prove it works
15. Eval runner + `fixtures/checkout-foundation/`; upgrade `eval-grader` (transcript contract, N/A, threshold, Bash for git checks).
16. Trigger/quality evals for `implement`, `merge-request*`, `skill-review`.
17. `code-review` coverage statement + confidence provenance; plant-defect calibration; fix defective security assertion; boundary tests for collision clusters.

### P4 — Adopt better mechanisms
18. Script deterministic merge-protocol pieces (dedupe, max-severity, corroboration).
19. Prompt-injection fencing on review skills; tool-scoped `Agent(...)` / path-pinned Bash.
20. `create` / `update` / `validate` mode triad on authoring skills; append-only decision log per work item; degraded-mode panels; marketplace `renames` + hash-tracked installs.

### P5 — Coverage under a cap
21. **`agents-md`** (init + audit) — highest-value addition.
22. **`clarify`** then **`analyze`** then **`constitution`**.
23. Prod **`deploy`** (rollback thresholds before deploy) and **`incident`** / postmortem — `debug` already shipped.
24. Deferral-closure mode on `tasks`.
25. Rename **`tdd` → `tech-design`**.

---

## 6. If you only do five things next

1. **Shared work-item state + approve checklist** (P2 items 7–8) — unblocks §1.1 and §1.3.
2. **Fix the three privilege agents that fail the validator** (P1 item 5 / §3.2) — contracts are enforced; agents still red.
3. **Align duplicated review contracts in place** (P1 item 4) — stops silent drift on the gate without a shared refs package.
4. **Eval runner + one fixture** (P3 item 15) — makes existing assertions runnable.
5. **`agents-md` skill** (P5 item 21) — converts the most-read, never-written dependency into a contract.
