# Instance profile template — digital-agency

> Written by `/agency-hub:agency-setup`. Every practice plugin reads `config/instance.json` before producing output. Edit directly for small fixes; re-run `agency-setup --redo` to refresh.

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
| `instance` | Short slug — repo name, used in `.digital-agency/target.json` pointers |
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
| `brand/*` | Brand voice and guide — populated by `/brand-creative:practice-setup` |

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
    "pointerFile": ".digital-agency/target.json",
    "pointerSchema": {
      "instance": "<instance-slug>",
      "target": "website"
    }
  },
  "artefactPaths": {
    "product": "docs/product/product.md",
    "backlog": "docs/product/backlog.md",
    "roadmap": "docs/product/roadmap.md",
    "solution": "docs/architecture/solution.md"
  }
}
```

**Target repo pointer** — after user confirms, write in the target repository:

Path: `.digital-agency/target.json`

```json
{
  "instance": "<instance-slug>",
  "target": "website"
}
```

The `instance` value matches `config/instance.json` → `instance`. Practice agents read this file to locate the instance repo.

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
  "notes": "Target schema not designed — agency-setup does not block on this"
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

<!-- Filled during agency-setup or practice setup -->

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

Practices are MECE — one self-contained plugin per practice. Cross-practice roles (Product Manager, Delivery Lead) live in a separate **`core`** plugin; practices that need them declare it as a companion install.

| Service (`services.enabled`) | Practice plugin | `core` companion | Squad charters | Notes |
|---|---|---|---|---|
| `brand-creative` | `brand-creative` | none | — | Shipped; run `/brand-creative:practice-setup` after bootstrap |
| `web-development` | `web-development` | `core` | `site`, `blog`, `recipes` | Practice pending — interim: `engineering`, `frontend-engineer`, `qa-engineer`, `webops-engineer`, `principal-architect`; needs `/core:product-manager`, `/core:delivery-lead` |
| `content-marketing` | `content-marketing` | `core` | `content` | Practice pending — interim: `content`, `content-strategist`, `content-writer` |
| `social-media` | `social-media` | TBD | `content` | Practice pending — interim: `content`, `content-strategist`, `content-writer` |
| `seo` | `seo` | TBD | `seo` | Practice pending — interim: `seo`, `seo-specialist` |

Write `services.recommendedPlugins` with the practice plugin name(s) plus `core` when applicable. Include interim catalogue entries in setup summary when the practice plugin is not yet published.
