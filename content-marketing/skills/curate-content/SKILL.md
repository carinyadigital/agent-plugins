---
name: curate-content
description: >
  Rank assets from an approved media inventory for upcoming social posts. Use
  when selecting what to post next, curating from inventory JSON, or choosing
  seasonal assets. Reads brand from the instance repo. Do NOT use for analysing
  a single image (analyse-media) or writing captions (write-captions).
license: MIT
allowed-tools: Read Glob Grep
argument-hint: "<inventory json> [--date YYYY-MM-DD]"
metadata:
  author: Carinya Parc
  version: "0.1.0"
  owner: content-marketing
  review_cadence: quarterly
  work_shape: orchestrate-delivery
  output_class: decision-support
---

# Curate content

You select the best assets to post next from an approved inventory. Pass inventory
JSON after the skill name; optional `--date` (default today).

Read [content-conventions.md](../../references/content-conventions.md). Load
`brand-voice.md` and `seasonal-calendar.md` from the resolved brand path.

## Inputs

| Input            | Location                                     | Required   |
| ---------------- | -------------------------------------------- | ---------- |
| Inventory        | JSON array of approved assets with tags      | Yes        |
| Recent posts     | Array of recently posted mediaKeys           | If known   |
| Curation date    | `--date YYYY-MM-DD` or today                 | No         |
| Brand voice      | `<resolved-brand-path>/brand-voice.md`       | If present |
| Seasonal calendar| `<resolved-brand-path>/seasonal-calendar.md` | If present |

Inventory items include: `mediaKey`, `subjects`, `season`, `moods`, `qualityScore`,
`contentType`, `processedAt`.

## Steps

1. Resolve brand. Derive active seasonal events from the seasonal calendar for the
   curation date's month.
2. Rank candidates by priority: (1) seasonal relevance, (2) content variety —
   no consecutive same primary subject, (3) recency balance — prefer recent but
   surface older when seasonally relevant, (4) quality when other factors equal.
3. Select up to 3 assets. Rank best-to-post-next (rank 1 first). One-sentence
   reason each. Only select `mediaKey`s present in inventory.
4. Enforce subject diversity: no two adjacent ranks share the same primary subject.
5. Set `lowInventoryWarning` when fewer than 7 unposted assets remain.
6. Respond ONLY with valid JSON in the output format below.

## Quality rules

- All `mediaKey`s must exist in the input inventory
- Reasons cite seasonal or variety rationale
- Rank 1 is the recommended next post
- Selection only — captioning is downstream (`write-captions`)

## Output format

```json
{
  "selections": [
    { "rank": 1, "mediaKey": "", "reason": "" }
  ],
  "inventoryDepth": 0,
  "lowInventoryWarning": false
}
```
