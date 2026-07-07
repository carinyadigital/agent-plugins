# Provider resolution

Self-contained rules for detecting the git provider and choosing the tool to
create and monitor an MR/PR. Resolve once, up front, and reuse for every
step and sub-agent. This skill makes no assumption about which provider or
tooling is installed: it detects what exists and degrades gracefully.

## 1. Detect the provider

Parse `git remote get-url origin` (fall back to the first remote if `origin`
is absent):

| Host pattern | Provider |
| ------------ | -------- |
| `github.com` | GitHub |
| `gitlab.com` or hostname containing `gitlab` | GitLab |
| `bitbucket.org` | Bitbucket Cloud |
| hostname containing `bitbucket` or `stash` | Bitbucket Server / Data Center |
| Anything else | Self-hosted — probe below |

Self-hosted probe, in order: a configured CLI that recognises the host
(`glab auth status`, `gh auth status --hostname <host>`); an available MCP
server whose tools match the host; otherwise ask the user which provider the
remote is. Do not guess from the URL alone when the hostname is opaque.

## 2. Pick a tool tier

Within the detected provider, prefer the first tier that is actually
available. Verify availability — check for MCP tools in the current session,
`command -v gh` / `command -v glab` for CLIs — rather than assuming.

**Tier 1 — MCP tools** (preferred: works in hosted agent environments with
no CLI installed, and returns structured results):

| Provider | Typical server | Create | Read state / CI | Comments |
| -------- | ------------- | ------ | --------------- | -------- |
| GitHub | official GitHub MCP | `create_pull_request` | `pull_request_read`, `get_job_logs` | `add_comment_to_pending_review`, `add_reply_to_pull_request_comment` |
| GitLab | official GitLab MCP (18.5+) | `create_merge_request` | `get_merge_request`, `get_merge_request_pipelines`, `manage_pipeline` (retry) | `get_merge_request_notes`, `create_merge_request_note` |
| Bitbucket Cloud | Atlassian Rovo MCP | PR lifecycle tool (create/diff/comment/approve) | same tool family | same tool family |

Exact tool names vary by server version — discover what the connected server
exposes rather than hard-coding names. Older GitLab servers (pre-18.8) accept
only title and branches on create; set description, labels, and reviewers
with a follow-up update call or note.

**Tier 2 — provider CLI** (when authenticated):

| Provider | Create | Watch CI | Comments |
| -------- | ------ | -------- | -------- |
| GitHub | `gh pr create --title … --body-file …` | `gh pr checks --watch` | `gh pr view --comments`, `gh api` |
| GitLab | `glab mr create --title … --description-file …` | `glab ci status --live` | `glab mr note` |
| Bitbucket | no widely-installed CLI — use Tier 1 or Tier 3 | — | — |

**Tier 3 — plain git fallback** (always available):

- GitLab: create at push time with push options —
  `git push -u origin HEAD -o merge_request.create -o merge_request.target=<branch> -o merge_request.title="…" -o merge_request.draft`.
  (Push options cannot set a multi-line description reliably; print the
  composed body for the user to paste.)
- GitHub / Bitbucket: `git push -u origin HEAD`, then surface the create-URL
  the remote prints in the push output (`Create a pull request … <url>`).
- Universal last resort: push, print the compare/create URL, and hand the
  user the composed title and description ready to paste. Creating the MR by
  hand from prepared content is a successful outcome, not a failure.

## 3. Operation matrix (babysit mode)

What babysit needs per provider, by tier:

| Operation | GitHub | GitLab | Bitbucket |
| --------- | ------ | ------ | --------- |
| MR state + mergeability | MCP `pull_request_read` / `gh pr view --json` | MCP `get_merge_request` / `glab mr view` | Rovo MCP PR tool |
| CI results + logs | MCP `get_job_logs` / `gh run view --log-failed` | MCP `get_merge_request_pipelines` / `glab ci trace` | Pipelines via Rovo MCP |
| Retry a check | `gh run rerun --failed` | MCP `manage_pipeline` (retry) / `glab ci retry` | re-run via Rovo MCP |
| Read / reply to threads | MCP note tools / `gh api` | MCP `get_merge_request_notes` + `create_merge_request_note` / `glab mr note` | Rovo MCP comment tools |
| Event subscription | `subscribe_pr_activity` (hosted Claude Code) | none — poll or `--live` watch | none — poll |

## 4. Reviewer sources

- `CODEOWNERS` — `.github/CODEOWNERS`, `.gitlab/CODEOWNERS`, `docs/CODEOWNERS`,
  or repo root; match patterns against the changed paths.
- Provider config — GitLab approval rules, Bitbucket default reviewers.
- Suggest matches in the report; **assign only after the user confirms** —
  assignment notifies people.

## 5. Default branch

`git symbolic-ref refs/remotes/origin/HEAD --short` (strip the `origin/`
prefix); if unset, `git remote show origin` or the provider API. Never assume
`main` or `master`.
