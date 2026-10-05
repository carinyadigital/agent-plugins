# Issue writing (tracker-agnostic)

Shared rules for `/product-management:write-initiative`,
`/product-management:write-epic`, and `/product-management:write-story`.

These skills **author one work item** at a hierarchy level. They do not
decompose a product into many items — that is `/product-management:tasks`.

## Hierarchy

```text
Initiative  →  Epic  →  Story  →  Task
   ↑                ↑         ↑
 write-initiative  write-epic write-story
```

| Level | Job | Typical next skill |
| ----- | --- | ------------------ |
| Initiative | Strategic bet spanning multiple epics; outcome + scope + success signals | `write-epic` or `tasks` under the initiative |
| Epic | Delivery outcome for one phase objective; no story-level AC | `write-story` or `tasks {epic}` / `design` |
| Story | User-visible slice with independent test criterion and AC | `tasks` (sub-tasks) or `implement` |

## Resolve the destination first

Before writing anything durable, resolve the **source system** the same way
`tasks` does — read
[../skills/tasks/references/work-items.md](../skills/tasks/references/work-items.md)
§1–§2. Never guess between Linear and Jira when both are plausible.

| Destination | When | What you write |
| ----------- | ---- | -------------- |
| **Markdown (filesystem)** | No tracker resolved, or user asks for docs | Initiative / epic / story markdown under the paths below |
| **Linear** | Linear MCP reachable and chosen | Issue (or Project/Initiative when the workspace models that type) with title + description body |
| **Jira** | Atlassian MCP reachable and chosen | Issue of the matching type (`Initiative` / `Epic` / `Story`) |
| **GitHub / GitLab issues** | `gh`/`glab` or MCP, and user chose issues | Issue with labels for type (`type:epic`, `type:story`, …) |

Always **draft for review first**. Create or update the tracker/filesystem
artefact only after the user confirms, or when they explicitly said
"create it" / "write it to the backlog".

## Markdown paths

| Level | Default path |
| ----- | ------------ |
| Initiative | `docs/product/initiatives/{slug}.md` |
| Epic (row) | `docs/product/backlog.md` epic table (filesystem-only repos) |
| Epic (body) | `specs/{work-short-name}/epic.md` — optional detail alongside design/tasks |
| Story | Appended under Stories in `specs/{work-short-name}/TASKS.local.md` |

Override when the user names a path. Tracker-backed repos skip shadow
`backlog.md` — the tracker holds the epic/initiative list
(see [delivery-conventions.md](delivery-conventions.md)).

## Portable field map

Write content in portable fields, then map to the destination's native shape.
Keep the system's own type label in artefacts; map behaviour only.

| Portable field | Markdown | Linear-shaped | Jira-shaped |
| -------------- | -------- | ------------- | ----------- |
| Title | `#` heading / table Title | `title` | Summary |
| Type | frontmatter `type:` | issue type / label / project | Issue Type |
| Parent | frontmatter `parent:` / epic ID | `parentId` / project | Parent / Epic Link |
| Outcome / statement | body section | description lead | description lead |
| Priority | `P0`–`P3` | priority | Priority |
| Status | `To do` … `Done` | workflow state | Status |
| Estimate | Fibonacci | estimate | Story Points |
| Acceptance | Gherkin / EARS section | description AC | description or AC custom field |
| Links | markdown links | attachments / relations | issue links |

Do **not** hardcode one vendor's REST API, custom-field IDs, or CLI as the only
path. Prefer MCP tools for the resolved tracker; fall back to markdown the user
can paste.

## Draft → apply gate

1. Gather context (product.md, roadmap.md, parent item, research).
2. Produce a complete draft in chat (or a proposed file diff).
3. Ask whether to apply to markdown, create/update in the tracker, or both.
4. On apply: write only the declared paths / the single resolved issue; report
   IDs and paths in the summary.

## Quality bar (all levels)

- Outcome language, not solution language, at initiative and epic level.
- Stories carry AC; epics and initiatives do not duplicate story Gherkin.
- Every item names its parent (or explicitly says it is top-level).
- No invented tracker IDs — ask to create, or wait for the key.
