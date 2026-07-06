# install-log.yaml — schema

Append-only audit trail for community skills installed, updated, disabled, or
removed through agency-hub. The auto-updater and skill-manager
read this file to verify provenance and to compare pinned revisions.

**Path:**

```
~/.claude/plugins/config/digital-agency/agency-hub/install-log.yaml
```

Created empty by `/agency-hub:setup` if it does not exist.

## Design rules

1. **Append only.** Never rewrite or delete prior entries. Corrections are new
   entries with a `note:` field explaining the correction.
2. **`pinned_sha` is immutable per install.** Updates append a new `install` or
   `update` entry with the new SHA; they do not edit the prior entry.
3. **Tags are not SHAs.** Record only the 40-character git commit hash from the
   registry fetch. Refuse to pin branch heads or mutable tags.
4. **Trust is per revision.** The allowlist check, raw-SKILL display,
   skills-qa verdict, and human approval recorded on an entry apply only to that
   `pinned_sha`.

## Entry shape

Each list item is one action. Required fields vary by `action`.

### Common fields (all actions)

| Field | Type | Required | Notes |
|---|---|---|---|
| `skill` | string | yes | Canonical skill directory name |
| `action` | enum | yes | `install` \| `update` \| `disable` \| `enable` \| `uninstall` |
| `timestamp` | ISO 8601 | yes | UTC preferred |
| `path` | string | when applicable | Installed directory path |

### `install` and `update` actions

| Field | Type | Required | Notes |
|---|---|---|---|
| `pinned_sha` | string | yes | 40-char lowercase hex git commit SHA of the vetted revision |
| `registry_url` | string | yes | Source registry URL at install time |
| `publisher` | string | yes | GitHub org/user or marketplace publisher |
| `allowlist_mode` | enum | yes | `restrictive` \| `permissive` at install time |
| `allowlist_pass` | boolean | yes | `true` if source was on allowlist (or permissive override recorded) |
| `skills_qa_verdict` | enum | yes | `ready` \| `some_concern` \| `material_concerns` \| `refuse` |
| `skills_qa_run_at` | ISO 8601 | yes | When skills-qa completed for this revision |
| `human_approved_at` | ISO 8601 | yes | When the user typed explicit `yes` |
| `license` | string | yes | Extracted SPDX identifier or `unknown` |
| `license_source` | string | yes | Where license was read |
| `deployment_context` | string | yes | From engagement profile at install time |
| `freshness_status` | enum | yes | `fresh` \| `stale` \| `unknown` \| `n/a` |
| `last_verified` | string | no | Validated ISO date or `unknown` |
| `freshness_category` | string | no | Validated token or `unknown` |
| `freshness_window` | string | no | Validated `N <unit>` or `unknown` |
| `verified_against` | list | no | Validated URL list (hostname + path only) |
| `freshness_raw_rejected` | object | no | Fields that failed validation at install |
| `previous_pinned_sha` | string | update only | SHA replaced by this update |

### `disable`, `enable`, `uninstall` actions

Minimal audit — `skill`, `action`, `timestamp`, `path`. No SHA change.

## Example

```yaml
- skill: competitive-landscape-scan
  action: install
  timestamp: 2026-07-01T14:22:00Z
  path: ~/.claude/skills/competitive-landscape-scan/
  pinned_sha: a1b2c3d4e5f6789012345678901234567890abcd
  registry_url: https://github.com/example-org/agency-skills
  publisher: example-org
  allowlist_mode: restrictive
  allowlist_pass: true
  skills_qa_verdict: some_concern
  skills_qa_run_at: 2026-07-01T14:20:00Z
  human_approved_at: 2026-07-01T14:21:30Z
  license: MIT
  license_source: LICENSE file
  deployment_context: firm-internal
  freshness_status: unknown
  last_verified: unknown
  freshness_category: unknown
  freshness_window: unknown
  verified_against: []

- skill: competitive-landscape-scan
  action: update
  timestamp: 2026-08-15T09:00:00Z
  path: ~/.claude/skills/competitive-landscape-scan/
  pinned_sha: ffffffffffffffffffffffffffffffffffffffff
  previous_pinned_sha: a1b2c3d4e5f6789012345678901234567890abcd
  registry_url: https://github.com/example-org/agency-skills
  publisher: example-org
  allowlist_mode: restrictive
  allowlist_pass: true
  skills_qa_verdict: ready
  skills_qa_run_at: 2026-08-15T08:58:00Z
  human_approved_at: 2026-08-15T08:59:45Z
  license: MIT
  license_source: LICENSE file
  deployment_context: firm-internal
  freshness_status: fresh
  last_verified: 2026-08-01
  freshness_category: market-data
  freshness_window: 6 months
  verified_against:
    - https://example.com/benchmark-2026
```

## Consumers

| Skill / agent | How it uses install-log |
|---|---|
| `skill-installer` | Appends `install` entries after Step 7 |
| `auto-updater` | Reads latest `pinned_sha` per skill; appends `update` entries |
| `skill-manager` / `uninstall` / `disable` | Verifies hub install provenance before acting |
| `registry-sync` | Cross-checks installed SHAs against registry heads |

The installed starter pack table in `CLAUDE.md` is a human-readable summary.
`install-log.yaml` is the authoritative SHA pin and audit record.
