# Self-hosted runner for `build.yml`

Only needed to turn on automatic mod builds. Everything else in this repository works without it:
manifests are validated and the catalog is regenerated on GitHub-hosted runners.

## Why a self-hosted runner at all

Every mod's `.csproj` references the game's own `BepInEx/interop/*.dll` (`Assembly-CSharp.dll`,
`UnityEngine.*.dll`). Those are proprietary game binaries. They cannot be committed here, and a
GitHub-hosted runner has no way to obtain them. A build machine therefore has to be one that already
has Task Bar Hero and BepInEx installed, which means one of yours.

## Read this part before you register anything

This repository is public. GitHub's own guidance is not to use self-hosted runners with public
repositories, and the reason is specific: anyone can fork a public repository and open a pull
request. If a workflow runs that pull request's code on your runner, a stranger has just executed
code on your machine.

`build.yml` is written so that cannot happen, and it depends on three things staying true:

1. **No pull request triggers.** The workflow runs on `push` to `master` and on manual dispatch.
   Both mean a maintainer has already looked. Adding `pull_request` or, worse,
   `pull_request_target` would hand the runner to anyone who can open a PR.
2. **The `mod-build` environment has a required reviewer.** Step 3 below. Without it, the approval
   gate in the workflow is decorative.
3. **You actually read the pinned commit before merging.** The job's whole purpose is to compile
   third-party code. No amount of workflow configuration replaces reading what you are about to
   compile.

The runner should be a machine you would not mind reinstalling. A spare desktop or a VM with the
game installed is a better fit than your main workstation.

## 1. Prepare the machine

Needs, on Windows:

- Task Bar Hero installed, with BepInEx set up, so `BepInEx/interop/` exists.
- The .NET SDK the mods target.
- Python 3.12 or newer, for `scripts/build_from_source.py`.
- Git.

Check that a local build works before involving GitHub at all. If this fails, the runner will fail
in exactly the same way, with more moving parts in between:

```bash
python scripts/build_from_source.py
```

## 2. Register the runner

In the repository: **Settings, Actions, Runners, New self-hosted runner**, pick Windows, and follow
the commands it shows. They are generated per repository and carry a short-lived token, so take them
from that page rather than from here.

When it asks for labels, the defaults are fine: `build.yml` asks for `self-hosted` and nothing more.

Install it as a service so it survives a reboot:

```bash
./svc.sh install
```

```bash
./svc.sh start
```

## 3. Create the approval gate

This is the step that is easy to skip and should not be.

In the repository: **Settings, Environments, New environment**, named exactly `mod-build`. Open it,
tick **Required reviewers**, and add yourself.

From then on every run stops and waits for you to press approve before a single command executes on
the runner. `build.yml` already points at this environment; if the environment does not exist, the
job simply runs unattended, which is the situation this is meant to prevent.

## 4. Confirm it works

**Actions, Build from source, Run workflow.** The run should pause for your approval, then build,
then publish a `mod-builds` artifact containing each mod's DLL and its hash.

## What comes after

A verified build is the missing piece for the store's install button, which is deliberately disabled
in the app today, with the reason shown in plain text. Once the runner produces hashed artifacts on
every merge there is something real to hand the app, and the button can be wired to download it and
check the hash before installing anything.

## Turning it off

Stop and remove the service on the machine, then remove the runner in **Settings, Actions, Runners**.
Nothing else in the repository depends on it. `build.yml` will simply queue with no runner available,
and the header comment in `scripts/build_from_source.py` explains how to produce the same artifacts
by hand.
