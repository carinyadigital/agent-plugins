---
name: merge-request
description: >
  Use when the user wants to open a merge request or pull request for the
  current branch (merge-request create — the default — with a generated
  title, description, labels, and reviewer suggestions), or to babysit an
  open MR/PR to a merge-ready state (merge-request babysit) by watching CI,
  review comments, and merge conflicts. Works with
  any codebase and any git provider — GitHub, GitLab, or Bitbucket — using
  MCP tools where available, provider CLIs otherwise, and plain git as a
  last resort. Do NOT use to review code or an MR as its reviewer
  (code-review, merge-request-review) or to implement changes (implement).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Shell
  - WebFetch
argument-hint: "[create] [work-item-id] [--draft] [--target <branch>] | babysit [mr-url]"
---

# Merge request

Open a merge request / pull request for the current branch, or babysit an
open one until it is merge-ready.

## Router

1. Mode: default **create**, or `babysit`.
2. One prompt under [prompts/](prompts/).

**create** (default) — [prompts/create.prompt.md](prompts/create.prompt.md).
Resolve change context and provider once, discover the repo's MR/PR
template, compose a size-adaptive description, push, create, report the URL.
Accepts an optional work-item ID, `--draft`, and `--target <branch>`.

**babysit** — [prompts/babysit.prompt.md](prompts/babysit.prompt.md). Drive
an open MR/PR to a merge-ready state: watch CI, triage review comments, fix
objective failures, sync conflicts, escalate design decisions. Accepts an
MR/PR URL or number; defaults to the MR/PR for the current branch (typically
the one `create` just opened).

For reviewing an MR as its reviewer — inline comments, approve / request
changes — use the **merge-request-review** skill, not this one.

## Sub-agents

| Agent | File | Focus |
| ----- | ---- | ----- |
| mr-babysitter | [agents/mr-babysitter.md](agents/mr-babysitter.md) | Background monitor-to-merge loop for an open MR/PR |

Spawn `mr-babysitter` only in babysit mode, and only when the host supports
background agents (Claude Code `Agent` tool, Cursor cloud agents) — it frees
the main session while the loop runs. Otherwise run the babysit prompt
inline. `create` mode spawns no agents: MR creation is a linear workflow.

## References

- [references/provider-resolution.md](references/provider-resolution.md) — detect the git provider and pick a tool: MCP → CLI → plain git fallback
- [references/template-discovery.md](references/template-discovery.md) — find the repo's MR/PR template per provider; fall back to the packaged default
- [references/description-guidelines.md](references/description-guidelines.md) — title convention detection, size-adaptive sections, metadata, body mechanics

## Assets

- [assets/default-mr-template.md](assets/default-mr-template.md) — packaged
  default description template, used only when the repo defines none.

## Ground rules (both modes)

- Never open an MR/PR from the repository's default branch — abort with an error.
- Never push with uncommitted changes present — ask the user to commit or stash first.
- Never force-push unless the user explicitly requests it.
- Resolve context once (work item, provider, template) and reuse it — do not re-fetch per step.
- Assigning human reviewers is outward-facing: suggest from CODEOWNERS or
  provider config, but confirm with the user before assigning.
