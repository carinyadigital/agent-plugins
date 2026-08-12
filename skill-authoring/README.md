# skill-authoring

Quality gate and authoring tooling for skills in this catalogue.

## Skills

| Skill | Purpose |
| ----- | ------- |
| **skills-qa** | Evaluate a skill against the Agency Skill Design Framework |
| **skill-review** | Research, review, and enhance skills on a cadence |

```
/skill-authoring:skills-qa path/to/SKILL.md
/skill-authoring:skill-review implement
```

## Agents

| Agent | Purpose |
| ----- | ------- |
| **eval-grader** | Grade skill eval runs against `evals/evals.json` assertions |

Agent prompt: `agents/eval-grader.md`

## Tooling

| Script | Purpose |
| ------ | ------- |
| `scripts/validate_skills.py` | Catalogue skill frontmatter, Ralph hooks, preset graphs |
| `scripts/mutation-test.py` | Mutation tests for Ralph hook suites (`ralph-loop/`) |

Run from repo root:

```bash
python3 skill-authoring/scripts/validate_skills.py
python3 skill-authoring/scripts/mutation-test.py
```

## References and templates

- `references/agency-skill-design-framework.md` — design parameters and verdict bands
- `spec/agent-skills-spec.md` — local Agent Skills spec notes
- `template/SKILL.md` — starter template for new skills
