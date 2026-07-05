# Curate content

## Before running

1. Resolve brand per [../../references/content-conventions.md](../../references/content-conventions.md).
2. Load `brand/brand-voice.md` and `brand/seasonal-calendar.md`.
2. Input: inventory array (mediaKey, subjects, season, moods, qualityScore, contentType,
   processedAt), recentPosts array, currentDate, currentSeason.

## Selection criteria (priority order)

1. Seasonal relevance — match current season and active calendar events
2. Content variety — no consecutive same primary subject in ranked list
3. Recency balance — prefer recent but surface older when seasonally relevant
4. Quality — prefer higher scores when other factors equal

## Active seasonal events

Derive from `brand/seasonal-calendar.md` for the curation date's month.

## Task

Select up to 3 assets. Rank best-to-post-next (rank 1 first). One-sentence reason each.
Only select mediaKeys present in inventory.

## Output JSON

```json
{
  "selections": [
    { "rank": 1, "mediaKey": "", "reason": "" }
  ],
  "inventoryDepth": 0,
  "lowInventoryWarning": false
}
```

Respond ONLY with valid JSON.

## Post-processing

Enforce subject diversity: no two adjacent ranks share the same primary subject.
Flag lowInventoryWarning when fewer than 7 unposted assets remain.

## Review criteria

- All mediaKeys exist in input inventory
- Reasons cite seasonal or variety rationale
- Rank 1 is the recommended next post
