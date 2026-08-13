<!--
TASKS.local.md — machine-written pointer, repo root.
This is not the work-item task list (that lives at
specs/{work-short-name}/TASKS.local.md when a local breakdown is required).
Written once per resolution by any delivery skill after it resolves the work
item source system to Linear or Jira (see references/work-item-resolution.md).
Add this file to .gitignore — it can name environment-specific sites,
workspaces, and project keys.
Do not hand-edit the Source/Site/Project fields; delete the file to force
re-resolution if they go stale.
-->

# Task source

- **Source:** <!-- linear | jira -->
- **Site / workspace:** <!-- e.g. yourteam.atlassian.net, or the Linear workspace name -->
- **Project / team key:** <!-- e.g. CHK, ENG -->
- **Resolved:** <!-- YYYY-MM-DD -->
- **Resolved by:** <!-- skill name -->

Work item IDs in this repo are `{PROJECT}-{n}` keys from the system above.
Skills read this file before attempting source-system detection and skip the
interview in `work-item-resolution.md` while it is current. Delete this file,
or update it, if the team switches tracker.
