---
name: ux-design-review
description: >
  Use when the user wants a UX/design review of implemented UI — frontend
  components, pages, or flows — against the design source of truth (Figma
  via MCP, mockups, tokens, or style guide, whatever the repo provides),
  covering design fidelity, accessibility (WCAG 2.2 AA), interaction states,
  responsiveness, and design-system conformity; or to address UX review
  findings (ux-design-review fix, optionally scoped to an action tier).
  Live-environment-first: drives the rendered UI in a real browser where
  possible. Works with any framework or design tooling. Do NOT use for
  code correctness/security review (code-review), to review a design.md
  document (design), or to implement features (implement).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Shell
  - WebFetch
argument-hint: "[fix [blocking|warning|all]] [branch-or-pr-or-url] [figma-url]"
---

# UX design review

Review the rendered UX of a UI change against its design source; or address
findings from a prior UX review.

This is the experience sibling of **code-review**: code-review judges a
diff's correctness, security, and acceptance criteria; this skill judges
what the user actually sees and operates. On a frontend change, run both.

## Method: live environment first

Judge the interactive experience before the code. Resolve a runnable UI per
[references/environment-resolution.md](references/environment-resolution.md)
and drive it with a real browser (Playwright/Chromium, or the host's
browser MCP tools). When nothing runs, degrade to a static review and state
the reduced coverage in the verdict — never silently skip live checks.

## Sub-agents

For multi-component diffs or pre-PR review, spawn in parallel (Claude Code
agents or Cursor Task):

| Agent | File | Focus |
| ----- | ---- | ----- |
| accessibility-reviewer | [agents/accessibility-reviewer.md](agents/accessibility-reviewer.md) | WCAG 2.2 AA — axe-core scan + manual keyboard/focus/semantics pass |
| interaction-states-reviewer | [agents/interaction-states-reviewer.md](agents/interaction-states-reviewer.md) | User flows; hover/focus/disabled; loading/empty/error; robustness; console |
| design-fidelity-reviewer | [agents/design-fidelity-reviewer.md](agents/design-fidelity-reviewer.md) | Rendered UI vs the resolved design source (Figma/mockups/tokens) |
| responsive-reviewer | [agents/responsive-reviewer.md](agents/responsive-reviewer.md) | Breakpoints, overflow, touch targets, dark mode / reduced motion |
| design-system-reviewer | [agents/design-system-reviewer.md](agents/design-system-reviewer.md) | Static pass: tokens vs hard-coded values, component reuse, pattern adherence |

Spawn only the agents whose triggers fire — do not run all five on every diff:

| Condition | Spawn |
| --------- | ----- |
| Whenever spawning (default lenses) | accessibility-reviewer, interaction-states-reviewer |
| Design source resolved (Figma link, mockups, specs) | design-fidelity-reviewer |
| Diff touches layout, CSS, or breakpoints | responsive-reviewer |
| Repo has a design system, tokens file, or component library | design-system-reviewer |

Small diffs (one component, few states) skip spawning and use the inline
steps in [prompts/run.prompt.md](prompts/run.prompt.md). Merge agent outputs
into one verdict. Resolve the design source and the live environment once up
front (see the references) and share both with every sub-agent — do not
re-resolve per agent.

## References

- [references/design-source-resolution.md](references/design-source-resolution.md) — discover the design truth: Figma MCP, mockups, tokens, style guide, or none
- [references/environment-resolution.md](references/environment-resolution.md) — get a runnable UI and drive it; the degradation ladder to static review
- [references/accessibility-checklist.md](references/accessibility-checklist.md) — condensed WCAG 2.2 AA, split automatable vs manual
- [references/ux-heuristics.md](references/ux-heuristics.md) — visual hierarchy, consistency, interaction standards: the bar when no design source exists
- [references/finding-classification.md](references/finding-classification.md) — UX categories, severity, confidence + risk matrix

## Router

1. Mode: default **review**, or `fix`.
2. One prompt under [prompts/](prompts/).

**review** (default) — [prompts/run.prompt.md](prompts/run.prompt.md).

**fix** — [prompts/fix.prompt.md](prompts/fix.prompt.md). Optional action-tier
threshold after `fix`: `blocking` (blocking only) or `warning` (blocking +
warning); default (or `all`) addresses all findings.

Pass a branch, PR, running-app URL, or Figma node URL after the mode token.
Default review scope: the UI touched by `git diff`.
