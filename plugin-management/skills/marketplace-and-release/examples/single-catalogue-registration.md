# Worked example: registering in a single-catalogue marketplace

A repo with one `marketplace.json` at the root, no dual Claude/Cursor split. Before:

```json
{
  "name": "acme-plugins",
  "displayName": "Acme Plugins",
  "owner": { "name": "Acme Platform Team" },
  "plugins": [
    {
      "name": "deploy-helper",
      "description": "Guides safe production deploys.",
      "source": "plugins/deploy-helper",
      "category": "Delivery"
    }
  ]
}
```

After registering a new `changelog-helper` plugin, closest in shape to an existing
"Delivery" category entry:

```json
{
  "name": "acme-plugins",
  "displayName": "Acme Plugins",
  "owner": { "name": "Acme Platform Team" },
  "plugins": [
    {
      "name": "deploy-helper",
      "description": "Guides safe production deploys.",
      "source": "plugins/deploy-helper",
      "category": "Delivery"
    },
    {
      "name": "changelog-helper",
      "description": "Writes changelog entries in this project's style.",
      "source": "plugins/changelog-helper",
      "category": "Delivery"
    }
  ]
}
```

One file, one edit. No second catalogue to keep in sync — the "match every existing
catalogue file" step in the main skill body is a no-op here, which is exactly the
detection step earning its keep: it doesn't force a dual-catalogue registration on a
repo that never had one.
