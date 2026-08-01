"""validate_manifests.py -- checks every mods/*.json against schema/manifest.schema.json, plus
two structural rules the schema itself can't express: the "id" field must match its own filename,
and no two manifests may claim the same assemblyName (two mods shipping a DLL with the same name
would silently overwrite each other once deployed side by side in the same BepInEx/plugins dir).

Run from the repo root:
    python scripts/validate_manifests.py
Exits 1 and prints every problem found (not just the first) if anything fails -- a contributor
fixing a PR wants the full list in one pass, not one error per re-run.
"""
import json
import os
import sys

import jsonschema

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(ROOT, "schema", "manifest.schema.json")
MODS_DIR = os.path.join(ROOT, "mods")


def main() -> int:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
    validator = jsonschema.Draft202012Validator(schema)

    errors = []
    assembly_names = {}  # assemblyName -> first mod id that claimed it

    for filename in sorted(os.listdir(MODS_DIR)):
        if not filename.endswith(".json"):
            continue
        mod_id = filename[:-len(".json")]
        path = os.path.join(MODS_DIR, filename)
        with open(path, encoding="utf-8") as f:
            try:
                manifest = json.load(f)
            except json.JSONDecodeError as e:
                errors.append(f"{filename}: invalid JSON -- {e}")
                continue

        for schema_error in validator.iter_errors(manifest):
            errors.append(f"{filename}: {schema_error.message} (at {'/'.join(str(p) for p in schema_error.path) or '<root>'})")

        if manifest.get("id") != mod_id:
            errors.append(f"{filename}: \"id\" ({manifest.get('id')!r}) must match the filename ({mod_id!r})")

        assembly_name = manifest.get("assemblyName")
        if assembly_name:
            if assembly_name in assembly_names:
                errors.append(
                    f"{filename}: assemblyName {assembly_name!r} already used by "
                    f"{assembly_names[assembly_name]}.json -- two mods can't share a deployed DLL name"
                )
            else:
                assembly_names[assembly_name] = mod_id

    if errors:
        print(f"{len(errors)} problem(s) found:\n")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"All manifests valid ({len(assembly_names)} mod(s) checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
