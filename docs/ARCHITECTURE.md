# Architecture

## Scope
Hermes Atlas contains canonical project-documentation guidance, schemas and templates, two optional manually connected skill packs, and Python standard-library tooling with tests. It contains no application implementation. No product runtime flow, persistence, deployment, or external integration is asserted.

## Tool boundaries
- `validate_atlas.py` checks this repository's Atlas layout and contracts; it is not a generic third-party validator.
- `validate_project.py` checks generic core documents and local Markdown links for an explicitly supplied Git root.
- `manage_project_docs.py` bootstraps only absent files or refreshes the explicitly managed source-map block. It does not stage, commit, delete files, or modify Hermes settings.
- Tests use isolated temporary Git fixtures.

## Unknowns
Application architecture, runtime, persistence, deployment, and external integrations are outside this repository's implemented scope.
