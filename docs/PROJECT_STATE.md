# Project state

## Scope
This v0.1.0 snapshot contains documentation, schemas/templates, optional skill-pack source, Python standard-library tools, and tests. It does not contain an application runtime.

## Validation
Run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/validate_atlas.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/docs/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/validate_project.py /absolute/path/to/hermes-atlas
```

These checks establish repository-level documentation contracts and fixture behavior, not Hermes runtime integration. The owner confirms both optional skills were successfully tested in a Hermes v0.22.2 environment; that report is owner-confirmed and was not independently rerun for this snapshot. The skill packs are not automatically installed or connected.

## Limits
No application runtime, deployment, live skill discovery, or invocation is verified by the repository checks. Publication, repository availability, and any external Hermes configuration remain owner-controlled.
