"""build_from_source.py -- for every mods/*.json, clones repoUrl at EXACTLY pinnedCommit into a
throwaway directory, builds entryProject (Release), confirms assemblyName's DLL exists in the
output, and hashes it (SHA256). This is the step that makes the store trustworthy: a manifest only
points at source, this script is what proves the DLL a user eventually installs is what that
pinned commit actually produces -- not something a compromised release asset swapped in later.

Run from the repo root:
    python scripts/build_from_source.py            # every mod
    python scripts/build_from_source.py chestmod    # just one, by id

Writes dist/<id>/<assemblyName> and prints a hashes.json (id -> sha256) to stdout; the calling CI
workflow is responsible for what happens to that (upload as artifact, attach to a release, etc.) --
this script's only job is build + hash, not publish.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODS_DIR = os.path.join(ROOT, "mods")
DIST_DIR = os.path.join(ROOT, "dist")


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_one(manifest: dict) -> str:
    mod_id = manifest["id"]
    with tempfile.TemporaryDirectory(prefix=f"beacon-store-{mod_id}-") as tmp:
        clone_dir = os.path.join(tmp, "src")
        subprocess.run(["git", "clone", "--no-checkout", manifest["repoUrl"], clone_dir], check=True)
        subprocess.run(["git", "checkout", manifest["pinnedCommit"]], cwd=clone_dir, check=True)

        csproj = os.path.join(clone_dir, manifest["entryProject"])
        if not os.path.isfile(csproj):
            raise RuntimeError(f"{mod_id}: entryProject not found at {manifest['entryProject']!r} in the pinned commit")

        subprocess.run(["dotnet", "build", csproj, "-c", "Release"], check=True)

        built_dll = None
        for base, _dirs, files in os.walk(os.path.dirname(csproj)):
            if manifest["assemblyName"] in files:
                built_dll = os.path.join(base, manifest["assemblyName"])
                break
        if not built_dll:
            raise RuntimeError(f"{mod_id}: build succeeded but {manifest['assemblyName']!r} wasn't produced")

        mod_dist_dir = os.path.join(DIST_DIR, mod_id)
        os.makedirs(mod_dist_dir, exist_ok=True)
        dest = os.path.join(mod_dist_dir, manifest["assemblyName"])
        shutil.copy2(built_dll, dest)
        return _sha256(dest)


def main() -> int:
    targets = sys.argv[1:]
    hashes = {}
    failed = []

    for filename in sorted(os.listdir(MODS_DIR)):
        if not filename.endswith(".json"):
            continue
        mod_id = filename[:-len(".json")]
        if targets and mod_id not in targets:
            continue
        with open(os.path.join(MODS_DIR, filename), encoding="utf-8") as f:
            manifest = json.load(f)
        print(f"[{mod_id}] cloning {manifest['repoUrl']} @ {manifest['pinnedCommit'][:12]} ...")
        try:
            hashes[mod_id] = build_one(manifest)
            print(f"[{mod_id}] OK -- sha256={hashes[mod_id]}")
        except (subprocess.CalledProcessError, RuntimeError) as e:
            print(f"[{mod_id}] FAILED -- {e}")
            failed.append(mod_id)

    print("\n" + json.dumps(hashes, indent=2))
    if failed:
        print(f"\n{len(failed)} mod(s) failed to build from source: {failed}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
