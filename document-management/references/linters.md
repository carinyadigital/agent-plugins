# Linter delegation contract

The plugin **delegates mechanical checks to existing linters** instead of re-deriving them with the model. The agent's budget goes to judgement (accuracy, completeness, content-type, voice); a linter catches dead links and misspellings for free.

This plugin does **not** ship a Vale style package. If the target repo already has Vale configured, use that config. Otherwise fall back to the built-in checks below.

## Who owns which check

| Tool | Owns | Config | Notes |
| :--- | :----- | :----- | :---- |
| **Vale** | Prose style: AU spelling, headings, banned terms, no emoji, readability grade | Repo's own `.vale.ini` + styles | Use only if present in the target repo. Do not copy a style package in. |
| **markdownlint** | Structural Markdown: heading hierarchy, list consistency, line length, trailing spaces | `.markdownlint.json`/`.yaml` | Structure only — no prose/spelling. Complements Vale. |
| **lychee** | Link health: dead URLs, broken internal links and anchors | `lychee.toml` (optional) | Fast; preferred over `markdown-link-check`. |
| **cspell** | Spelling against a project dictionary (code-aware) | `cspell.json` | Understands code identifiers; better than a prose speller for technical docs. |

## How skills call them

1. **Detect what's installed** before use, and record which path was taken so the report is reproducible:
   ```bash
   command -v vale >/dev/null && echo "vale: $(vale --version)"
   command -v markdownlint >/dev/null 2>&1 || command -v markdownlint-cli2 >/dev/null 2>&1 && echo "markdownlint found"
   command -v lychee >/dev/null && echo "lychee found"
   command -v cspell >/dev/null && echo "cspell found"
   ```
2. **Prefer structured output** and parse it, rather than scraping human output:
   ```bash
   vale --output=JSON docs/
   markdownlint --json docs/ 2>&1
   lychee --format json docs/
   ```
3. **Fold linter output into the report** so the reviewer agent never re-derives a mechanical check. Findings a linter produced are attributed to it (reproducible), separate from judgement findings.

## Vale: use the repo's config, or skip

- If `.vale.ini` (or `vale.ini`) exists in the target repo **and** `vale` is on `PATH`, run Vale against `docs_root` with that config.
- If Vale is installed but there is no config, skip Vale rather than inventing a config — fall back to built-in checks and say so.
- Never install Vale (or any linter) unprompted. Offer only if the user says yes.

## Graceful degradation (built-in fallbacks)

If a linter isn't on `PATH`, don't fail and don't install it unprompted. Fall back to these lighter checks and **record that the fallback was used**:

| Missing tool | Built-in fallback |
| :----------- | :---------------- |
| lychee (or any link checker) | `Glob` every relative path referenced in a doc — does the target exist? |
| Vale / cspell | `Grep` referenced commands and script names against `package.json` / `pyproject.toml` (do they exist verbatim?). Flag US-only spellings that the style guide overrides (organize, color, center as verb/noun pairs you can grep). |
| Vale readability | Sentence-length heuristic: flag sentences over ~30 words as a readability hint, not a confirmed grade. |
| markdownlint | Spot-check heading hierarchy while reading (one H1 from front matter, no skipped levels). |

The reader of the health report must be able to tell how deep the check actually went.
