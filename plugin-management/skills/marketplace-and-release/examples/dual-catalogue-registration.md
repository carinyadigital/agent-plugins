# Worked example: registering in a dual-catalogue marketplace

A repo shipping to two hosts keeps two catalogue files that must carry identical
entries. Registering `changelog-helper` means the same edit, twice, in the same
change:

## `.claude-plugin/marketplace.json`

```json
{
  "plugins": [
    {
      "name": "changelog-helper",
      "description": "Writes changelog entries in this project's style.",
      "source": "plugins/changelog-helper",
      "category": "Knowledge Work",
      "homepage": "https://github.com/your-org/your-repo/tree/main/plugins/changelog-helper"
    }
  ]
}
```

## `.cursor-plugin/marketplace.json`

```json
{
  "plugins": [
    {
      "name": "changelog-helper",
      "description": "Writes changelog entries in this project's style.",
      "source": "plugins/changelog-helper",
      "category": "Knowledge Work",
      "homepage": "https://github.com/your-org/your-repo/tree/main/plugins/changelog-helper"
    }
  ]
}
```

Every field is identical between the two — `name`, `description`, `source`,
`category`, `homepage`. That's deliberate: unlike a plugin's own manifest pair (where
the validator only checks `name`/`description`/`version` for drift), treat a
marketplace **entry** as fully identical across catalogues, since there's no reason
for it to differ and a mismatch (a stale description in one, an updated one in the
other) is confusing for anyone browsing either catalogue.

## What would go wrong skipping one file

If only `.claude-plugin/marketplace.json` were updated, Claude Code users could
install `changelog-helper` but Cursor users couldn't — the plugin would look released
to half the audience and missing to the other half, with no error to signal it. This
is exactly the class of mistake the detection step in the main skill body exists to
prevent: find every catalogue file the repo actually has before registering, not just
the first one you notice.
