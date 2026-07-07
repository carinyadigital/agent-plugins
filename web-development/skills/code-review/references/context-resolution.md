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
- Already handled by `guideline-compliance-reviewer` — reuse its discovery,
  do not duplicate.

## 5. Signal (CI status)

- If reviewing a hosted PR/MR, fetch CI/check status via `gh`/`glab` or the
  relevant MCP tool once. Acknowledge each failure in the verdict rather than
  re-running checks locally.
- If reviewing a local diff with no PR/MR, there is no CI signal — say so
  rather than guessing.

## Output: Review Context bundle

Produce a short bundle and reuse it verbatim across the review and every
sub-agent — do not re-fetch per agent:

```text
Intent: <what & why, 1-3 sentences, with source>
Acceptance criteria: <found | not found> — <source path/URL, or "none — using stated intent">
Scope/design reference: <found | not found> — <source path/URL, or "none — judging against intent only">
Guidelines: <found | not found> — <file list>
CI signal: <status per check | not applicable (no PR/MR)>
```

## Terminology

This skill reviews a **change under review** — a diff, branch, or PR/MR tied
to any unit of work (story, task, sub-task, bug fix, spike, or an untracked
change). Nothing here assumes an "epic" or a specific tracker; adapt the
bundle to whatever the repo and tracker actually provide.
