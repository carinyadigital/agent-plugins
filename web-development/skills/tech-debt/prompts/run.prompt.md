# Tech debt

Systematically identify, categorize, and prioritize technical debt.

## Categories

| Type | Examples | Risk |
|------|----------|------|
| **Code debt** | Duplicated logic, poor abstractions, magic numbers | Bugs, slow development |
| **Architecture debt** | Monolith that should be split, wrong data store | Scaling limits |
| **Test debt** | Low coverage, flaky tests, missing integration tests | Regressions ship |
| **Dependency debt** | Outdated libraries, unmaintained dependencies | Security vulns |
| **Documentation debt** | Missing runbooks, outdated READMEs, tribal knowledge | Onboarding pain |
| **Infrastructure debt** | Manual deploys, no monitoring, no IaC | Incidents, slow recovery |

## Prioritization framework

Score each item on:

- **Impact**: How much does it slow the team down? (1–5)
- **Risk**: What happens if we don't fix it? (1–5)
- **Effort**: How hard is the fix? (1–5, inverted — lower effort = higher priority)

Priority = (Impact + Risk) × (6 − Effort)

## Output

Produce a prioritized list with estimated effort, business justification for each item, and a phased remediation plan that can be done alongside feature work.

## Scope

When the user names a repo area, service, or epic, limit the audit to that scope. Otherwise scan the codebase or area they describe.
