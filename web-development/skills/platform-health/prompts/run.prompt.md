# Platform health

## Before running

1. Read target repo `AGENTS.md` / `CLAUDE.md` for commands and conventions.
2. Read `.carinyaparc/target.json` on the target repo, then `config/` on the carinyaparc
   instance repo if present for instance context.
3. Confirm focus area (default: all).

## Checks

### Dependencies (`deps`)

- Run `pnpm outdated` or equivalent from repo root
- Note security advisories (`pnpm audit` if available)
- Flag pinned versions with known CVEs or major drift

### Errors (`errors`)

- Review Sentry (if MCP connected) for new/regressed issues in last 7 days
- Group by frequency and user impact
- Distinguish noise from actionable defects

### CI (`ci`)

- Check recent workflow runs on default branch (GitHub MCP or `gh run list`)
- Note flaky or failing jobs
- Verify required checks match branch protection

### Uptime (`uptime`)

- Check Vercel deployment status (if MCP connected)
- Note failed or rolled-back production deploys in last 14 days
- Confirm preview deployments succeed for open PRs when relevant

## Output

Structured report:

```markdown
## Platform health — {date}

### Summary
(one paragraph — overall status: green / amber / red)

### Findings
| Area | Severity | Finding | Recommended action |
| ---- | -------- | ------- | ------------------ |

### Suggested issues
- [ ] {title} — squad:site, type:maintenance
```

Severity: `critical`, `high`, `medium`, `low`, `info`.

## Constraints

- Do not modify application code or merge PRs.
- File recommendations as GitHub issues when actionable.
- Escalate production incidents to human immediately.
