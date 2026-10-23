# Codebase map and navigation

This map describes the files included in the Hermes Atlas v0.1.0 source snapshot. It is a navigation aid, not evidence of runtime behavior. Refresh the managed source map with `python3 tools/docs/manage_project_docs.py ROOT --update --dry-run`, review the preview, then rerun without `--dry-run`.

## Entry points
- `tools/docs/validate_atlas.py` — Atlas-specific layout and contract checks.
- `tools/docs/validate_project.py` — generic core-document and relative-link checks.
- `tools/docs/manage_project_docs.py` — explicit-root additive bootstrap and managed map update.
- `tools/docs/tests/` — standard-library regression tests and isolated Git fixtures.
- `docs/` — canonical docs, schemas, templates, development instructions, and manual onboarding.
- `skills/` — optional repo-local skill packs; not installed or connected automatically.

## Canonical documents
- [Architecture](ARCHITECTURE.md)
- [Roadmap](ROADMAP.md)
- [Project state](PROJECT_STATE.md)

<!-- hermes-atlas:code-map:start -->
## Managed source map

- `.gitignore`
- `LICENSE`
- `README.md`
- `RELEASE_NOTES.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/HERMES_ONBOARDING.md`
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/optional-docs.schema.json`
- `docs/optional-docs.yaml`
- `docs/project-docs.schema.json`
- `docs/templates/ARCHITECTURE.md`
- `docs/templates/INDEX.md`
- `docs/templates/PROJECT_STATE.md`
- `docs/templates/ROADMAP.md`
- `skills/project-docs-maintainer/SKILL.md`
- `skills/project-docs-maintainer/references/claim-taxonomy.md`
- `skills/project-docs-maintainer/references/update-checklist.md`
- `skills/project-navigator/SKILL.md`
- `skills/project-navigator/references/navigation-checklist.md`
- `tools/docs/core_docs.py`
- `tools/docs/manage_project_docs.py`
- `tools/docs/tests/test_integration_fixtures.py`
- `tools/docs/tests/test_validator.py`
- `tools/docs/validate_atlas.py`
- `tools/docs/validate_docs.py`
- `tools/docs/validate_project.py`
<!-- hermes-atlas:code-map:end -->
