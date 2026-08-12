# Skill review checklist

Use during **comprehensive review** and **spec alignment**. Prefer the live
[Agent Skills specification](https://agentskills.io/specification) when anything
here disagrees.

## Frontmatter

- [ ] `name` present: 1–64 chars, `a-z` / `0-9` / `-` only, no leading/trailing
      or consecutive hyphens
- [ ] `name` matches the parent directory name
- [ ] `description` present: 1–1024 chars; WHAT + WHEN; trigger keywords;
      negative triggers where useful
- [ ] `description` is third-person / imperative for agents ("Use when…")
- [ ] Optional fields only when needed: `license`, `compatibility` (≤500),
      `metadata`, `allowed-tools` (space-separated string, not a YAML list)
- [ ] Version/author metadata consistent with the pack if applicable

## Body and layout

- [ ] `SKILL.md` is the entry point; instructions are actionable steps
- [ ] Body stays lean (aim < 500 lines / < ~5000 tokens)
- [ ] Detail lives in `references/`, `assets/`, or `scripts/` as appropriate
- [ ] File references from `SKILL.md` are relative and **one level deep**
- [ ] No Windows-style paths
- [ ] Consistent terminology (one term per concept)
- [ ] No unexplained time-sensitive instructions (or clearly marked legacy)

## Progressive disclosure

- [ ] Catalog layer works from name + description alone
- [ ] Activation layer (`SKILL.md`) sufficient to start the job
- [ ] Deep resources loaded only when instructions say so
- [ ] Long reference files have a short table of contents when > ~100 lines

## Procedure quality

- [ ] Steps are numbered/ordered with clear entry and exit
- [ ] Decision points and modes are explicit
- [ ] Inputs/outputs and required tools are stated
- [ ] Read-only vs write contract is unmistakable
- [ ] Failure paths and verification called out where fragility is high
- [ ] Single-mode skills do not keep a redundant separate prompt file

## Correctness and hygiene

- [ ] Scripts are executable or clearly documented; dependencies noted
- [ ] Cross-skill links resolve
- [ ] Examples are concrete
- [ ] Pack index / changelog updated when the public surface changes

## Optional validation

```bash
skills-ref validate ./path-to-skill
```

Record the command output in the review report when run.
