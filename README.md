# Beacon Store

A community mod directory for [Beacon](https://github.com/iurysenck/tbh-beacon). Every mod listed
here is a `mods/<id>.json` manifest pointing at a specific pinned commit in its own repo -- this
repo never hosts mod source or built DLLs directly, it only indexes them.

## How it works

1. A mod author opens a PR adding `mods/<id>.json` (see `schema/manifest.schema.json`).
2. `validate.yml` checks the manifest's shape automatically.
3. A maintainer reviews the source at the pinned commit and merges.
4. `build.yml` clones that exact commit, builds it, and hashes the result -- see
   `scripts/build_from_source.py`. **Note:** this step needs a runner with the actual game +
   BepInEx installed (proprietary binaries, can't run on GitHub-hosted runners) -- see the
   comment at the top of `build.yml`.
5. The built DLL + hash get published, so anyone installing it can verify what they got matches
   what was reviewed.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full submission process.

## License

AGPL-3.0-only — see [LICENSE](LICENSE). Note this covers the manifests/schema/CI in *this* repo;
each listed mod carries its own license (see its `license` field).
