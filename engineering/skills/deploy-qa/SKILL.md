---
name: deploy-qa
description: >
  Prepare a QA workspace — checkout a branch or MR ref, install dependencies,
  and verify the environment is ready for test execution. Use before running
  automated or exploratory QA. Do NOT use for running tests (run-automated-suite),
  exploratory validation (exploratory-pass), or fixing code (implement).
license: MIT
allowed-tools: Read Bash Glob Grep
argument-hint: "<branch-name-or-mr-url>"
metadata:
  author: Carinya Parc
  version: "0.1.0"
  owner: engineering
  review_cadence: as-needed
  work_shape: orchestrate-delivery
  output_class: tracking-update
---

# Deploy QA

Prepare an isolated QA workspace for validation (first step of the delivery-qa
crew flow). Pass branch name or MR/PR URL after the skill name.

## Steps

1. Confirm the branch exists — `git branch -a` or source-control MCP.
2. Checkout the target branch: `git fetch origin` then `git checkout <branch>`
   (create tracking branch if needed).
3. Install dependencies per project conventions — read `package.json` or
   `AGENTS.md` first (`pnpm install`, `npm ci`, etc.).
4. If the repo documents a deploy or preview script for QA, run it. Treat
   non-zero exit as an infrastructure failure.
5. Verify readiness — build artefacts, env files, or preview URL documented.

## Constraints

- Do not push commits, open merge requests, merge, or approve MRs
- Do not modify application source — only checkout and install steps
- If checkout or install fails, stop and report — do not claim deploy succeeded

## Output format

Report:

- Branch checked out
- Dependencies installed (command used)
- Any deploy/preview step run and result
- Blockers preventing test execution (if any)
