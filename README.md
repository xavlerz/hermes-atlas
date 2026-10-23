# Hermes Atlas

Hermes Atlas is a documentation and engineering-memory framework for Hermes Agent projects. This repository contains two optional, manually connected Hermes skill packs, canonical project-document templates, and Python-standard-library tools for validating and maintaining project documentation. It does not contain an application runtime.

> **Version:** v0.1.0 snapshot. This repository provides documentation tooling and optional skill-pack source; it is not a published package or a verified Hermes integration. Licensed under the [MIT License](LICENSE).

## Contents

- `skills/project-navigator/` — find repository files and evidence without treating a navigation map as proof of behavior.
- `skills/project-docs-maintainer/` — maintain project documentation against source evidence.
- `tools/docs/` — Atlas and generic-project documentation validators, additive bootstrap/update tooling, and tests.
- `docs/` — canonical documentation, templates, schemas, development guidance, and manual Hermes onboarding.

Start with the [canonical index](docs/INDEX.md), [v0.1.0 release notes](RELEASE_NOTES.md), [architecture](docs/ARCHITECTURE.md), [roadmap](docs/ROADMAP.md), and [project state](docs/PROJECT_STATE.md).

## Requirements

- Python 3.9 or newer (stdlib only; no third-party Python packages required).
- Git for the project-root safety check in the generic validator and bootstrap/update tool.
- Hermes Agent only if you choose to connect and use the optional skill packs; integration is manual and is not verified by the repository test suite.

## Get the source

```sh
git clone https://github.com/xavlerz/hermes-atlas.git
cd hermes-atlas
```

The canonical repository URL above is intended for this project; availability/publication is not asserted. There is no installer, PyPI package, or automatic Hermes configuration step. The tools run directly from the checkout.

## Validate this repository

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/validate_atlas.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/docs/tests -v
```

The Atlas validator checks this repository's document layout, internal core-document links, schemas, optional-document registry, and the two skill frontmatters. Tests use Python's built-in `unittest` framework and isolated temporary Git fixtures.

## Use the tools on another project

Run commands from this checkout and pass the target project's explicit absolute Git-root path. The generic validator does not impose Atlas schemas or skills:

```sh
python3 tools/docs/validate_project.py /absolute/path/to/project
```

Preview additive documentation bootstrap before applying it:

```sh
python3 tools/docs/manage_project_docs.py /absolute/path/to/project --dry-run
```

Refresh only the managed source-map block in a target's `docs/INDEX.md` by reviewing the preview first:

```sh
python3 tools/docs/manage_project_docs.py /absolute/path/to/project --update --dry-run
```

The tools report existing Git changes and preserve user content; they do not stage, commit, delete, or modify Hermes settings. See [development instructions](docs/DEVELOPMENT.md) for tool boundaries and test commands.

## Optional Hermes skills

The skill directories are not installed or connected automatically. Review [manual onboarding](docs/HERMES_ONBOARDING.md) and the active Hermes documentation before configuring an external skill directory. External skills may be writable by Hermes, and same-named skills can be shadowed by precedence; review permissions and configuration yourself. No Hermes config, installed skills, HomePanel, or runtime is modified by this repository's tools.

## Scope and limitations

Atlas currently provides repository documentation tools and skill-pack source, not an application, a managed knowledge backend, or a published integration. Unit and fixture checks prove source-level behavior only. Live Hermes skill discovery and invocation are unverified by this repository's tests; see the [project state](docs/PROJECT_STATE.md). The v0.1.0 snapshot is an isolated, fresh-history source tree; publication and repository availability remain owner-controlled.
