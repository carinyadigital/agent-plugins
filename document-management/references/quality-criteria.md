# docs/ quality criteria

A 0–100 rubric for a repo's `docs/` tree, used by `docs-improve` and the `docs-reviewer` agent. Split on Google's two axes (*Software Engineering at Google*, ch. 10) so the reviewer knows which findings a tool can settle and which need judgement.

- **Structural quality (~50 pts)** — is it well made? Clarity, consistency, formatting, links. Mostly automatable by the [linters](linters.md).
- **Functional quality (~50 pts)** — does it achieve its purpose? Accuracy, completeness, findability. Judged by the reader; this is what ultimately matters, and the hardest to automate — which is why the reviewer agent exists.

Report the total, the per-dimension scores, and the three highest-impact fixes. Lead with the score and the fixes, not a wall of findings.

## Structural (automatable) — 50 points

### 1. Readability (10)
Prose is within the target reading grade (Flesch–Kincaid ≤ 10 by default, configurable via `readability_target`). Short sentences, plain language. Measured by Vale's `Readability`/`metric` check when Vale is installed; otherwise a sentence-length heuristic (see [linters.md](linters.md)).

### 2. Style conformance (10)
Matches the [style guide](style-guide.md): AU spelling, sentence-case headings, no emoji, descriptive link text. When the target repo has Vale configured, fold those hits in; otherwise use the built-in fallbacks.

### 3. Structural Markdown health (10)
Clean heading hierarchy (one H1 from front matter, no skipped levels), consistent lists, no markdownlint errors.

### 4. Link health (10)
No dead internal or external links, no broken anchors (lychee when installed). Relative links used for internal targets.

### 5. Naming & IA conformance (10)
Lowercase kebab-case filenames, `index.md` landing pages present, the four [Diátaxis](diataxis-structure.md) folders signposted, front-matter contract present on every doc.

## Functional (judgement) — 50 points

### 6. Accuracy vs the code (15) — highest weight
Do the docs match what the code actually does? Commands, flags, endpoints, config, and examples are correct against the current source. Misleading docs are worse than none, so this carries the most weight. Driven by the [drift heuristics](drift-heuristics.md).

### 7. Completeness / coverage (12)
Is the public surface documented? Measure documented vs undocumented surface against the `coverage_floor` (default 80%). "Public surface" is defined per repo type — CLI commands, HTTP endpoints, exported symbols, config keys.

### 8. Content-type correctness (10)
Is each doc a clean single Diátaxis type, or is it conflated (a tutorial with a reference table bolted on)? Conflation is flagged with a split proposal.

### 9. Findability (8)
Is there a navigable path from `index.md` to every doc? Are the types cross-linked (how-to → reference, explanation → tutorial)? Can a reader find a known item and discover a related one?

### 10. Freshness (5)
Docs' `last_reviewed` dates are within the staleness window (default 90 days), and the git-age delta between a doc and the code it describes is not alarming. See [drift-heuristics.md](drift-heuristics.md).

## Scoring bands

- **90–100** — healthy; keep it current.
- **70–89** — good, with specific gaps; `docs-improve` proposes targeted fixes.
- **50–69** — structural or accuracy problems; likely needs `docs-setup` (reorganise) and a drift pass via `docs-improve`.
- **< 50** — the tree needs real work; consider `docs-setup` (fresh or reorganise) plus a staged `docs-improve` plan.

## Notes

- Every finding cites `path/to/file:line`. A claim with no citation is not a finding.
- Structural findings a linter produced are attributed to the linter (reproducible); judgement findings note their confidence and what an SME would confirm.
- This rubric is the bar `docs-setup` scaffolds toward and `docs-improve` scores against.
