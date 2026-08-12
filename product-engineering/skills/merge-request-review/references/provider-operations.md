# Provider operations

Reviewer-side mechanics per provider: reading MR state and publishing a
review. Detect the provider from `git remote get-url origin` (hostname
contains `github` / `gitlab` / `bitbucket` or `stash`; opaque self-hosted
hosts: probe configured CLIs and available MCP servers, else ask). Prefer
MCP tools, then the provider CLI; this skill needs API access — there is no
plain-git fallback for publishing a review. With neither available, run with
`--no-publish` semantics and hand the user the composed review to post.

Exact MCP tool names vary by server version — discover what the connected
server exposes rather than hard-coding.

## Read operations

| Operation | GitHub | GitLab | Bitbucket |
| --------- | ------ | ------ | --------- |
| MRs awaiting my review | MCP `search_pull_requests` (`review-requested:@me`) / `gh pr list --search "review-requested:@me"` | `glab mr list --reviewer=@me` / MCP MR list | Rovo MCP PR list |
| MR details + mergeability | MCP `pull_request_read` / `gh pr view --json` | MCP `get_merge_request` / `glab mr view` | Rovo MCP PR tool |
| Diff | MCP `pull_request_read` (get_diff) / `gh pr diff` | MCP `get_merge_request_diffs` / `glab mr diff` | Rovo MCP PR diff |
| CI per check | MCP check-run tools, `get_job_logs` / `gh pr checks` | MCP `get_merge_request_pipelines` / `glab ci status` | Pipelines via Rovo MCP |
| Existing reviews + threads | MCP `pull_request_read` (get_reviews, get_review_comments) | MCP `get_merge_request_notes` | Rovo MCP comment tools |
| Local checkout (read-only) | `git fetch origin <branch> && git switch --detach FETCH_HEAD` — identical everywhere; never push to the author's branch | | |

## Publish operations

**GitHub** — reviews are transactional; use the pending-review flow so
inline comments and the verdict land as one review, not a comment storm:

1. Create a pending review (MCP `pull_request_review_write` method
   `create`).
2. Attach each inline comment (`add_comment_to_pending_review`) with path +
   line (+ side for multi-line).
3. Submit (`pull_request_review_write` method `submit_pending`) with event
   `APPROVE`, `REQUEST_CHANGES`, or `COMMENT` and the summary body.
4. Thread follow-ups: `add_reply_to_pull_request_comment`,
   `resolve_review_thread`.
   CLI fallback: `gh pr review --approve|--request-changes|--comment
   --body-file …` (verdict + summary only; inline comments need
   `gh api`).

**GitLab** — no pending-review transaction; sequence instead:

1. Inline comments as discussions on diff positions (MCP
   `create_merge_request_note` with position, or
   `glab api projects/:id/merge_requests/:iid/discussions`).
2. Summary note last, opening with the verdict.
3. Verdict: `glab mr approve` / approval API; request-changes has no first-
   class event — state it in the summary note and (where the project uses
   them) apply the convention label (e.g. `~"workflow::changes-requested"`).
4. Reply/resolve via `discussion_id` on the note tools.

**Bitbucket** — via the Rovo MCP PR tool family: inline comments with a
path + line anchor, overall comment, then approve / request changes on the
PR. Use PR *tasks* for blocking items where the workspace uses them —
Bitbucket can enforce task resolution before merge.

## Ordering rules (all providers)

- Compose everything locally first; publish in one pass — authors get one
  notification per round, not twenty.
- Inline comments before (GitHub: inside) the summary; summary carries the
  verdict rationale; verdict event last.
- On re-review, resolve/reply to old threads in the same pass as the new
  verdict.
- Write bodies to a temp file and pass by file or API parameter — never
  inline markdown through a shell string.
