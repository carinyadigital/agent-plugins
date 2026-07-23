# Instance profile template — digital-agency

> Written by `/agency-hub:setup`. Every practice plugin reads `config/instance.json` before producing output. Edit directly for small fixes; re-run `setup --redo` to refresh.

Tier 1 config lives in the **instance repo** (git-versioned), not in user dotfiles.

## File: `config/instance.json`

```json
{
  "status": "template",
  "instance": "",
  "business": {
    "name": "",
    "proseName": "",
    "context": "single-business"
  },
  "brand": {
    "voice": "brand/brand-voice.md",
    "taxonomy": "brand/taxonomy.md",
    "hashtags": "brand/hashtags.md",
    "seasonalCalendar": "brand/seasonal-calendar.md"
  },
  "services": {
    "enabled": [],
    "recommendedPlugins": []
  },
  "cadence": {
    "planningRhythm": "",
    "approvalGateStrictness": "standard",
    "escalationModel": ""
  },
  "riskPosture": {
    "default": "balanced",
    "constraints": []
  },
  "governance": {
    "agentsNeverPushMain": true,
    "artefactsAreDraftsUntilHumanGate": true,
    "namedApprovalGates": []
  },
  "seedMaterial": {
    "sources": [],
    "notes": ""
  },
  "setup": {
    "completedAt": null,
    "mode": null,
    "agencyHubVersion": "0.1.0"
  }
}
```

### Field notes

| Field | Values / purpose |
|---|---|
| `status` | `template` until setup completes; then `complete` |
| `instance` | Short slug — repo name, used in `.agency/target.json` pointers |
| `business.context` | `single-business` \| `agency-serving-clients` |
| `services.enabled` | Practice areas active now: `web-development`, `content-marketing`, `social-media`, `seo`, `brand-creative` |
| `services.recommendedPlugins` | Catalogue plugin names to install next |
| `cadence.approvalGateStrictness` | `relaxed` \| `standard` \| `strict` |
| `riskPosture.default` | `conservative` \| `balanced` \| `aggressive` |

Set `status: complete` and `setup.completedAt` (ISO 8601) when the interview finishes and the user confirms the write.

## Related instance files

| File | Purpose |
|---|---|
| `config/targets/<name>.json` | Per-target binding — see target skeleton below |
| `config/plugins.json` | Installed catalogue plugins for this instance |
| `config/deployments/*.json` | Scheduled agent deployments (`enabled: false` until configured) |
| `config/cadence/*.md` | Ritual templates (weekly planning, editorial review, etc.) |
| `squads/<squad>/charter.md` | Squad mission, roster, target paths, cadence, DoD |
| `brand/*` | Brand voice and guide — populated by `/brand-creative:setup` |

## File: `config/plugins.json`

```json
{
  "catalogue": "<your-org>/digital-agency",
  "plugins": []
}
```

Set `catalogue` during setup to the GitHub org/repo slug (or equivalent source identifier) where this business installs the digital-agency marketplace — not a hard-coded publisher.

## File: `config/targets/<name>.json` — website (proven)

```json
{
  "name": "website",
  "type": "website",
  "enabled": false,
  "status": "skeleton",
  "repository": null,
  "binding": {
    "pointerFile": ".agency/target.json",
    "pointerSchema": {
      "name": "<target-repo-slug>",
      "instance": "<instance-slug>",
      "target": "website"
    }
  },
  "artefactPaths": {
    "product": ".agency/product.md",
    "backlog": ".agency/backlog.md",
    "roadmap": ".agency/roadmap.md",
    "solution": ".agency/architecture/solution.md"
  }
}
```

**Target repo pointer** — after user confirms, write in the target repository:

Path: `.agency/target.json`

```json
{
  "name": "<target-repo-slug>",
  "instance": "<instance-slug>",
  "target": "website"
}
```

The `name` field carries target repo identity (typically the git repo slug). The `instance` value matches `config/instance.json` → `instance`. Practice agents read this file to locate the instance repo and resolve the target without inferring identity from paths.

**Target repo scaffold** — on bind, also create the `.agency/` directory skeleton:

```text
.agency/
  .gitignore             ← from ${CLAUDE_PLUGIN_ROOT}/references/dot-agency/.gitignore
  README.md              ← from ${CLAUDE_PLUGIN_ROOT}/references/dot-agency/README.md
  target.json
  product.md
  roadmap.md
  backlog.md
  work/
  architecture/
  reviews/               ← gitignored
```

Stub markdown files may contain placeholder headings only. Epic and architecture subdirectories are populated by practice skills.

## File: `config/targets/<name>.json` — social (proven)

```json
{
  "name": "social",
  "type": "social",
  "enabled": false,
  "status": "skeleton",
  "platforms": [],
  "binding": {
    "connector": null,
    "connectorType": "social-publishing",
    "notes": "Bind your social publishing connector when credentials are available"
  }
}
```

## File: `config/targets/<name>.json` — not yet designed

For `email`, `ads`, `analytics` — write skeleton only:

```json
{
  "name": "email",
  "type": "email",
  "enabled": false,
  "status": "not-yet-designed",
  "notes": "Target schema not designed — setup does not block on this"
}
```

## File: `squads/<squad>/charter.md`

Minimal skeleton — practice setup expands later:

```markdown
---
squad: <squad-slug>
practice: <practice-area>
status: skeleton
---

# <Squad name> charter

## Mission

<!-- Filled during agency-hub setup or practice setup -->

## Roster

Catalogue agent slugs from digital-agency (e.g. frontend-engineer, content-writer).

## Target

<!-- Which config/targets/*.json this squad works against -->

## Cadence

<!-- Rituals from config/cadence/ -->

## Definition of done

<!-- Human gates named explicitly -->
```

## Service → plugin mapping

Practices are MECE — one self-contained plugin per practice. Decomposition and sprint cadence skills live in **`delivery-practice`**; product strategy, roadmap, specs, research, metrics, and competitive briefs live in **`product-management`**. Practices that need them declare the relevant plugin as a companion install and invoke skills directly.

| Service (`services.enabled`) | Practice plugin | Companion practice | Squad charters | Notes |
|---|---|---|---|---|
| `brand-creative` | `brand-creative` | none | — | Shipped; run `/brand-creative:setup` after bootstrap |
| `web-development` | `web-development` | `delivery-practice` | `site`, `blog`, `recipes` | Practice pending — interim: `engineering`, `frontend-engineer`, `qa-engineer`, `webops-engineer`, `principal-architect`; needs `/delivery-practice:tasks --product`, `/delivery-practice:sprint-planning` |
| `content-marketing` | `content-marketing` | `delivery-practice`, `product-management` | `content` | Shipped; run `/content-marketing:setup` after bootstrap; needs `/delivery-practice:tasks --product`, `/product-management:synthesize-research` |
| `social-media` | `social-media` | TBD | `content` | Practice pending — interim: `content-marketing` skills for captions and curation |
| `seo` | `search-optimisation` | `product-management` | `seo` | Shipped; run `/search-optimisation:setup` after bootstrap; needs `/product-management:competitive-brief` |

Write `services.recommendedPlugins` with the practice plugin name(s) plus `delivery-practice` and/or `product-management` when applicable. Include interim catalogue entries in setup summary when the practice plugin is not yet published.
