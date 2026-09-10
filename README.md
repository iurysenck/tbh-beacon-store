# Beacon Store

A community mod directory for [Beacon](https://github.com/iurysenck/tbh-beacon). Every mod listed
here is a `mods/<id>.json` manifest pointing at a specific pinned commit in its own repo -- this
repo never hosts mod source or built DLLs directly, it only indexes them.

## Store page

Browse the listed mods at **https://iurysenck.github.io/tbh-beacon-store/** (Portuguese, English
and Spanish). The page is static: it reads `docs/catalog.json`, which `scripts/build_catalog.py`
generates from these same `mods/*.json` manifests, so the web page, the store inside Beacon and
this repository never disagree. `catalog.yml` regenerates it on every manifest change.

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

## Disclaimer

Beacon is an unofficial companion app, not affiliated with the game's developers.
Task Bar Hero, its names, trademarks and assets belong to TesseractStudio / Nugem Studio.
This project does not redistribute game assets: they are read from your own installation.
Game privacy policy: https://taskbarhero.wiki/privacy

Beacon e um aplicativo companion nao oficial, sem vinculo com os desenvolvedores do jogo.
Task Bar Hero, seus nomes, marcas e assets pertencem a TesseractStudio / Nugem Studio.
Este projeto nao redistribui assets do jogo: eles sao lidos da sua propria instalacao.
Politica de privacidade do jogo: https://taskbarhero.wiki/privacy

This repository stores manifests only. It collects no data, sets no cookies and runs no analytics.

## License

AGPL-3.0-only, see [LICENSE](LICENSE). Note this covers the manifests/schema/CI in *this* repo;
each listed mod carries its own license (see its `license` field).
