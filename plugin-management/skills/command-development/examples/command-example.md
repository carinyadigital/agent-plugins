# Worked example: a legacy `commands/*.md` file

If you were adding this to a real plugin, it would live at
`commands/rotate-api-key.md` — note the filename is illustrative prose here, not a
real discoverable command in this plugin.

```markdown
---
description: Rotate a service's API key and update it everywhere it's stored.
argument-hint: "[service-name]"
---

Rotate the API key for $ARGUMENTS and update every place it's configured.

## Preflight

- Confirm $ARGUMENTS names a service this repo knows how to rotate a key for; list
  known services and stop if it doesn't match one.
- Confirm the secrets-manager CLI is on PATH; if not, explain how to install it and
  stop.
- Confirm the working tree is clean before editing any config file that isn't secret
  storage itself.

## Plan

State before doing anything:
- The new key will be generated in the secrets manager.
- Every config reference to the old key will be updated to the new one.
- The old key will be revoked only after every reference is confirmed updated.

⚠ Revoking the old key is irreversible once it's rotated out — **require explicit
user confirmation** before the revoke step runs.

## Commands

1. Generate a new key via the secrets-manager CLI.
2. Update each known config location to reference the new key (never print the key
   value itself in this output — reference it by name only).
3. Confirm every location was updated.
4. Revoke the old key only after explicit confirmation per the Plan section above.

## Verification

- Re-read each updated config location to confirm it now references the new key's
  name, not the old one.
- Confirm the old key shows as revoked in the secrets manager.

## Summary

## Result
- **Action**: rotate-api-key <service>
- **Status**: success | partial | failed
- **Details**: new key name, locations updated, revocation status

## Next Steps

- Redeploy any service that caches the key in memory rather than reading it live.
- Confirm downstream consumers aren't still using the old key by checking recent
  auth-failure logs after rotation.
```

Notice the six headings — `Preflight`, `Plan`, `Commands`, `Verification`, `Summary`,
`Next Steps` — and the `⚠`/"explicit" confirmation language next to the one
destructive step (key revocation). Both are what a structural validator checks for;
see `command-development`'s own body for the enforcement table.
