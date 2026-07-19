# Context resolution

Self-contained discovery rules for building the **Review Context** — a normalized
bundle of intent, requirements, scope, guidelines, and signal that every lens and
sub-agent reads instead of re-discovering. This skill makes no assumption about
epics, a specific issue tracker, or a fixed documentation layout: it discovers
whatever exists in the repo and degrades gracefully when something is absent.

Resolve once, up front, and pass the bundle to every sub-agent.

## 1. Work item & intent (what / why)

Resolve in priority order, stopping at the first that yields a result:

1. **Explicit argument** — the user passed an issue key, PR/MR URL, or file path.
2. **PR/MR description + linked issue** — if reviewing a hosted PR/MR:
   - `gh pr view` / `glab mr view` (or the GitHub/GitLab/Atlassian MCP tools, if
     available) for the description, linked issue, and comments.
   - Follow a linked issue reference (Jira key, Linear ID, `#123`, GitHub/GitLab
     issue URL) via the matching CLI or MCP tool to fetch its description and
     acceptance criteria, if one is linked.
3. **Local spec file** — glob for a task/spec file colocated with the change:
   `TASK.md`, `**/tasks.md`, `**/design.md`, `SPEC.md`, `ISSUE.md`, a task
   section inside `README.md`, or any project-specific equivalent named in
   `AGENTS.md`/`CLAUDE.md`.
4. **Fallback** — `git log` on the branch plus the branch name and the diff
   itself. Always available; never block on a missing tracker.

Use whichever source is richest; do not require every source to exist.

## 2. Acceptance criteria (requirement coverage)

Accept criteria in **any** shape found — do not assume Gherkin or a specific
file:

- Gherkin scenarios (`Given/When/Then`) in a tasks/spec file.
- A plain checklist or "Definition of Done" in an issue/PR description.
- EARS-style requirement statements.
- Bullet-point requirements in a ticket (Jira/Linear/GitHub/GitLab issue).
- None found — fall back to the stated intent (title + description) as the
  bar for coverage, and say so explicitly in the output rather than silently
  skipping the check.

## 3. Scope / design reference (where)

Optional — only used if discovered. Glob for candidates, in this order, and
stop at the first match (or use several if more than one is relevant):

- A design/spec doc named in the work item (explicit link or path mentioned
  in the issue/PR description).
- `**/design.md`, `**/DESIGN.md`, `**/SPEC*.md`, `**/RFC*.md` near the changed
  files or at the repo/module root.
- Architecture references: `**/solution.md`, `ARCHITECTURE.md`,
  `.agency/architecture/**`, ADR/decision folders (`**/decisions/**`,
  `**/adr/**`, `ADR-*.md`).
- A `.agency/work/{epic}/` (or similar) folder is one possible layout among many
  — treat it as a candidate, never a requirement.

If nothing is found, scope is judged against the resolved intent only (does
the diff do what the work item/PR description says, no more, no less).

## 4. Guidelines

- Root and directory-level `AGENTS.md` / `CLAUDE.md`, `.cursor/rules`,
  `CONTRIBUTING.md`.
- Already handled by `conventions-reviewer` (Part A) — reuse its discovery,
  do not duplicate.

## 5. Signal (CI status and existing analysis)

Never run linters, typecheckers, or builds. Do ingest results that already
exist — refusing to re-run is not a reason to ignore output someone else
produced.

- **Status.** If reviewing a hosted PR/MR, fetch CI/check status via `gh`/`glab`
  or the relevant MCP tool, once. Acknowledge each failure in the verdict rather
  than re-running it.
- **Output.** For failing checks, fetch the log or annotations
  (`gh run view --log-failed`, check annotations, or the provider equivalent).
  Also glob for analysis artefacts already committed or produced in the
  workspace: SARIF files, coverage reports, scanner output.
- **Reconcile, do not re-litigate.** A defect a scanner already caught is
  referenced, not raised again as if newly discovered.
- **Rebut where warranted.** Scanner findings frequently fail the provenance
  test in [security-checklist.md](security-checklist.md) — an injection or ReDoS
  flag on a static literal or a test fixture. Where the review disagrees with a
  scanner, say so explicitly, with the provenance trace. An explicit, reasoned
  rebuttal is more useful than silence, and no bundled-scanner product offers
  one.
- If reviewing a local diff with no PR/MR, there is no CI signal — say so rather
  than guessing.

## 6. Review state (incremental mode)

Look for `.agency/reviews/{branch}.json`. If present, this branch has been
reviewed before and the run is **incremental**:

- Read the last reviewed SHA and the recorded findings with their statuses
  (`open`, `fixed`, `dismissed`, `deferred`).
- Review the delta from that SHA to `HEAD`, not the whole branch.
- Re-verify `open` findings only where the diff touched their lines. Carry the
  rest forward unchanged.
- **Never re-raise a `dismissed` finding for unchanged code.** The author already
  argued it down; raising it again is how a review loses trust.
- Report the delta explicitly: fixed since last review, still open, newly
  introduced.

If the file is absent, the run is a full review and will create it.

Schema:

```json
{
  "branch": "feat/PROJ-001-context-assembler",
  "last_reviewed_sha": "a1b2c3d",
  "reviewed_at": "2026-07-19T09:00:00Z",
  "findings": [
    {
      "id": "cr-001",
      "file": "src/context/assembler.ts",
      "line": 42,
      "category": "Security",
      "severity": "Critical",
      "action": "blocking",
      "status": "open",
      "summary": "Artifact path not validated against repository root"
    }
  ]
}
```

## 7. Learnings

Look for `.agency/review-learnings.md`. These are preferences captured when a
reader rejected or corrected a previous finding — the informal counterpart to
written guidelines.

**Precedence: explicit written guidelines outrank learnings.** A rule in
AGENTS.md or CONTRIBUTING.md wins over a learning that contradicts it, because
someone chose to write the rule down. Learnings fill the gap where no rule
exists.

Apply only learnings whose scope glob matches a file in the diff. A learning
about Python exception handling must not influence a React review.

Flag entries older than six months that have never matched, so the file can be
pruned. Stale and contradictory learnings degrade review quality faster than
having none.

Entry format:

```markdown
## <short rule>
- **Scope:** `src/api/**/*.ts`
- **Why:** <the reasoning — this is what lets the rule generalise>
- **Added:** 2026-07-19, from review of feat/PROJ-001
```

Capture the reasoning, never just the rule. "Do not flag X" does not generalise;
"we keep user IDs out of error messages because those logs ship to a third-party
monitor" tells a future review how to handle the situation it has not seen.

## Output: Review Context bundle

Produce a short bundle and reuse it verbatim across the review and every
sub-agent — do not re-fetch per agent:

```text
Intent: <what & why, 1-3 sentences, with source>
Acceptance criteria: <found | not found> — <source path/URL, or "none — using stated intent">
Scope/design reference: <found | not found> — <source path/URL, or "none — judging against intent only">
Guidelines: <found | not found> — <file list>
CI signal: <status per check | not applicable (no PR/MR)>
Existing analysis: <SARIF/coverage/scanner artefacts found | none>
Review mode: <full | incremental from <sha>>
Learnings: <n applicable | none> — <matched scopes>
```

## Terminology

This skill reviews a **change under review** — a diff, branch, or PR/MR tied
to any unit of work (story, task, sub-task, bug fix, spike, or an untracked
change). Nothing here assumes an "epic" or a specific tracker; adapt the
bundle to whatever the repo and tracker actually provide.
