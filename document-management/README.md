# Document Management

Set up, structure, audit, and keep current the **`docs/` tree** in whatever repo
you are in. Scaffold or reorganise to Diátaxis, then score, detect drift, check
voice, and apply approved fixes.

Two skills, two agents, `docs/`-only writes.

## Skills

| Skill | What it does | Writes? |
| :---- | :----------- | :------ |
| `docs-setup` | Scaffold a missing/stub `docs/` tree, or reorganise a messy one to Diátaxis | Yes (approval-gated) |
| `docs-improve` | Score the tree, detect drift vs code, check voice/style, then apply approved fixes | Yes (approval-gated; `report-only` never writes) |

```
/document-management:docs-setup
/document-management:docs-improve
/document-management:docs-improve report-only
```

`docs-improve` also accepts `drift` or `voice` to focus that pass.

## Agents

| Agent | Read/write | Purpose |
| ----- | ---------- | ------- |
| `docs-reviewer` | Read-only | Audit brain — scores, detects drift, classifies by Diátaxis, critiques voice |
| `docs-writer` | Write | The only writer; applies **approved** findings strictly inside `docs_root` |

Where the host supports sub-agents, skills dispatch these; otherwise they do
the same role inline. The review → approve → write ordering is a security
boundary, not a formality.

## Write boundary

The plugin only ever **writes inside `docs_root`** (default `docs/`). It may
read the rest of the repo to judge accuracy. It never edits root `README.md`,
`AGENTS.md`, `CLAUDE.md`, source, or config. Findings that belong there are
reported and deferred to a human. See [`references/docs-boundary.md`](references/docs-boundary.md).

Default **`protected_paths`** (reported, never auto-moved or auto-edited):

- `docs/architecture/`
- `docs/product/`
- `docs/design/`
- `docs/brand/`

Override via local config if a repo needs a different list.

## Brand voice

This plugin does not bundle a voice file. It consumes
`<resolved-brand-path>/brand-voice.md` the same way content-marketing does
(explicit path → instance `brand/` → target → standalone `docs/brand/`). If
that artefact is absent, it asks for tone inline and uses the plugin
[`style-guide.md`](references/style-guide.md) (Google developer docs as base,
AU spelling, sentence-case headings, no emoji).

## Optional local config

Not required. In the **target repo** (not this marketplace):

- `.claude/document-management.local.md`
- `.cursor/document-management.local.md`

Check both; prefer the host-matching file, then the other. Absent = defaults.

| Field | Default |
| ----- | ------- |
| `docs_root` | `docs/` |
| `structure` | `diataxis` (`freeform` is allowed) |
| `staleness_threshold_days` | `90` |
| `readability_target` | `10` |
| `coverage_floor` | `80` |
| `protected_paths` | the four practice trees above |
| `owner` | `docs-owner` |

## Coexistence with `/engineering:docs-review`

| Intent | Skill |
| ------ | ----- |
| "Are these docs any good / consistent?" — any document set, read-only | `/engineering:docs-review` |
| "Set up / scaffold / reorganise the `docs/` tree to Diátaxis" | `/document-management:docs-setup` |
| "Improve / fix the `docs/` tree, drift vs code, voice" | `/document-management:docs-improve` |

## References

- [`references/diataxis-structure.md`](references/diataxis-structure.md) — four types, compass, folder standard
- [`references/quality-criteria.md`](references/quality-criteria.md) — 0–100 rubric
- [`references/drift-heuristics.md`](references/drift-heuristics.md) — doc↔code staleness
- [`references/docs-boundary.md`](references/docs-boundary.md) — write boundary and protected paths
- [`references/style-guide.md`](references/style-guide.md) — mechanical style
- [`references/linters.md`](references/linters.md) — Vale if the repo has it; otherwise built-in fallbacks

## License

Licensed under the [Apache License 2.0](./LICENSE).
