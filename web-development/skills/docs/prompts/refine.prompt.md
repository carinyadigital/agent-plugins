# Docs — refine mode

Sprint-end documentation pass for an epic. Resolve `{epic}` from argument or backlog.

Defaults: `.agency/architecture/solution.md`, `.agency/architecture/decisions/register.md`,
`.agency/work/{epic}/design.md`, `.agency/work/{epic}/refine-session.md`.

## Steps

1. Read `.agency/work/{epic}/design.md` — triage ADR candidates
2. Promote, inline, or defer each candidate (`adr write` when promoted)
3. Update solution.md §9 and §10
4. Archive superseded design sections with HTML comments (do not delete)
5. Write `.agency/work/{epic}/refine-session.md` using [assets/refine-session.template.md](../assets/refine-session.template.md)

## Negative constraints

- Task-level AC stays in `.agency/work/{epic}/tasks.md`
- Do not re-narrate design content in refine-session — cite sections
