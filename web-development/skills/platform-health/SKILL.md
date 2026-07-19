---
name: platform-health
description: >
  Audit platform health — dependency updates, uptime, error rates, CI status,
  and deployment hygiene. Use for "dependency audit", "check Sentry errors",
  "platform health review", or scheduled maintenance. Do NOT use for feature
  implementation (implement) or debugging a single bug (debug).
license: MIT
allowed-tools: Read Bash Glob Grep
argument-hint: "[--focus deps|errors|ci|uptime]"
metadata:
  author: Carinya Parc
  version: "0.1.0"
  owner: web-development
  review_cadence: monthly
  work_shape: monitor-and-report
  output_class: tracking-update
---

# Platform health

Dependency audit, error review, and deployment hygiene for webops workflows.
Optional focus: `deps`, `errors`, `ci`, `uptime` (default: all).

## Steps

1. Read target repo `AGENTS.md` / `CLAUDE.md` for commands and conventions.
2. Read `.agency/target.json` on the target repo, then instance `config/` if
   present.
3. Run checks for the requested focus (or all):

### Dependencies (`deps`)

- Run `pnpm outdated` or equivalent from repo root
- Note security advisories (`pnpm audit` if available)
- Flag pinned versions with known CVEs or major drift

### Errors (`errors`)

- Review Sentry (if MCP connected) for new/regressed issues in last 7 days
- Group by frequency and user impact; distinguish noise from actionable defects

### CI (`ci`)

- Check recent workflow runs on default branch (GitHub MCP or `gh run list`)
- Note flaky or failing jobs; verify required checks match branch protection

### Uptime (`uptime`)

- Check Vercel deployment status (if MCP connected)
- Note failed or rolled-back production deploys in last 14 days
- Confirm preview deployments succeed for open PRs when relevant

## Constraints

- Do not modify application code or merge PRs
- File recommendations as GitHub issues when actionable
- Escalate production incidents to a human immediately

## Output format

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

Severity: `critical` · `high` · `medium` · `low` · `info`.
