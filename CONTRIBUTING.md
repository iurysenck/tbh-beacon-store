# Contributing to Beacon Store

## Submitting a mod

1. Your mod must already build against [BeaconModKit](https://github.com/iurysenck/tbh-beacon-modkit)
   and be pushed to your own public repo.
2. Add `mods/<id>.json` following `schema/manifest.schema.json`. Run the validator locally before
   opening the PR:
   ```bash
   pip install jsonschema
   python scripts/validate_manifests.py
   ```
3. `pinnedCommit` must be the exact 40-character commit SHA you want reviewed — not a branch, not
   a tag. If you push a fix after opening the PR, update `pinnedCommit` to the new commit; the
   review restarts from that commit, not the old one.
4. Open the PR. A maintainer reviews the source at that exact commit and merges if it looks safe
   and does what the manifest claims.
5. Once merged, the build workflow clones your pinned commit, builds it, and hashes the result —
   that hash is what gets published, not anything you upload directly.

## Reporting a problem with a listed mod

Open an [issue](../../issues/new/choose) using the **Mod problem** template — say which mod
(`id` from its manifest) and what's wrong (doesn't build, manifest points at the wrong commit,
etc.). For a bug in the mod's own behavior in-game, report it on that mod's own repo instead —
this repo only tracks the listing itself.

## Code style

- One manifest, one PR — don't bundle unrelated mod submissions together.
- Keep `description` short (it's shown in a list, not a detail page).

By submitting a PR you agree the manifest/schema/CI content you contribute here is licensed under
this project's [AGPL-3.0](LICENSE).
