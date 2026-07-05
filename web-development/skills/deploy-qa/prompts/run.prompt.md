# Deploy QA

Prepare the workspace for QA validation.

## Steps

1. Confirm the branch exists — `git branch -a` or source-control MCP.
2. Checkout the target branch:
   - `git fetch origin`
   - `git checkout <branch>` (create tracking branch if needed)
3. Install dependencies per project conventions — read `package.json` or
   `AGENTS.md` first (`pnpm install`, `npm ci`, etc.).
4. If the repo documents a deploy or preview script for QA, run it. Treat
   non-zero exit as an infrastructure failure.
5. Verify readiness — build artefacts, env files, or preview URL documented.

## Output

Report:

- Branch checked out
- Dependencies installed (command used)
- Any deploy/preview step run and result
- Blockers preventing test execution (if any)

If checkout or install fails, stop and report the infrastructure failure.
Do not claim deploy succeeded.

## Constraints

- Do not push commits or open merge requests.
- Do not modify application source — only checkout and install steps.
- Do not merge or approve MRs.
