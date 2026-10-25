# Hermes Atlas

Hermes Atlas is a Git-first toolkit for navigating project source and maintaining project documentation. It provides two optional Hermes skill packs, documentation templates and validators, safe bootstrap and source-map tooling, and an opt-in Git change review packet. It is not an application runtime, package installer, or hosted knowledge service.

> **Latest published release: [v0.2.0](https://github.com/xavlerz/hermes-atlas/releases/tag/v0.2.0).** This repository currently tracks that release on `main`. A corrective `v0.2.1` is proposed in ongoing work but is **not released**. See [release notes](RELEASE_NOTES.md). Licensed under the [MIT License](LICENSE).

## What is included

- `skills/project-navigator/` — focused source and symbol lookup, with code claims verified against current files.
- `skills/project-docs-maintainer/` — evidence-based documentation audits and updates.
- `tools/docs/` — Atlas-specific and generic-project validators, additive documentation bootstrap, managed source-map refresh, and opt-in reconciliation.
- `docs/` — canonical documentation, templates, schemas, development instructions, and manual Hermes onboarding.

Start with the [documentation index](docs/INDEX.md), then consult the [architecture](docs/ARCHITECTURE.md), [project state](docs/PROJECT_STATE.md), and [roadmap](docs/ROADMAP.md) as relevant.

## Requirements

- Python 3.9 or newer; tooling uses the standard library and has no third-party Python dependencies.
- Git for tools that inspect or modify files in a target Git repository.
- Hermes Agent only if you choose to connect the optional skills. Configuration is manual and is not tested by the automated suite.

## Get the source and run checks

```sh
git clone https://github.com/xavlerz/hermes-atlas.git
cd hermes-atlas
PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/validate_atlas.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/docs/tests -v
```

These checks validate this checkout's documentation contracts and Python tooling. They do not establish live Hermes skill discovery or invocation, nor do they report remote CI status. See [development instructions](docs/DEVELOPMENT.md) for the generic validator, bootstrap/update behavior, source-map preview, and reconciliation modes.

### Update a source checkout

From a clean checkout on `main`, fast-forward to the current main branch:

```sh
git pull --ff-only origin main
```

Review or preserve local changes before updating. Hermes Atlas is consumed directly from a source checkout; it has no package installer.

## Use the tools on a project

Run the scripts from this checkout and pass the target project's absolute Git root. The generic validator checks existing core documents and local links without requiring Atlas schemas or skills:

```sh
python3 tools/docs/validate_project.py /absolute/path/to/project
```

Preview additive bootstrap before applying it:

```sh
python3 tools/docs/manage_project_docs.py /absolute/path/to/project --dry-run
```

To preview refreshing only the managed source-map block in an existing `docs/INDEX.md`:

```sh
python3 tools/docs/manage_project_docs.py /absolute/path/to/project --update --dry-run
```

Review previews before applying them. Bootstrap does not overwrite existing documents; map refresh does not alter prose outside its managed markers.

Print an advisory packet for tracked changes in a target project:

```sh
python3 tools/docs/reconcile_docs.py --root /absolute/path/to/project
```

By default, reconciliation compares tracked index/worktree changes with `HEAD`; `--base REF` compares only committed changes in `REF..HEAD`. Untracked files are excluded. The tools do not stage or commit changes, delete files, or modify Hermes settings.

## Connect the optional Hermes skills

The skill packs are source directories, not automatically installed integrations. Follow [manual Hermes onboarding](docs/HERMES_ONBOARDING.md) and verify configuration against the current Hermes documentation. External skill directories may be writable by Hermes, and higher-precedence skills can shadow same-named external skills; review paths and permissions before connecting them. Atlas tools do not modify a Hermes profile, installed skills, or running process.

## Scope and limitations

The project provides documentation tooling and optional skill-pack source; it does not provide an application runtime, managed knowledge backend, or automatic Hermes setup. Automated tests use isolated Git fixtures and prove source-level behavior only. Live Hermes skill selection and invocation remain separate runtime checks. See [project state](docs/PROJECT_STATE.md) for verified scope and current release status.
