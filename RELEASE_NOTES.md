# Hermes Atlas v0.2.0 — release preparation

This section documents the v0.2.0 preparation state; it does not assert that a tag or GitHub Release has been created.

- Adds opt-in `tools/docs/reconcile_docs.py` to print an advisory documentation review packet from tracked Git changes, with optional `--base REF` comparison.
- Extends project-doc management with explicit docs-first/legacy-safe bootstrap behavior and opt-in, marker-guarded source-map refresh limited to eligible tracked paths.
- Provides separate Atlas and generic-project validators, regression/fixture tests, and a configured documentation workflow at `.github/workflows/docs.yml`.
- Local source checks for this preparation: 38 tests, Atlas validation, generic validation, and `git diff --check` passed. Remote CI and Hermes runtime/integration are not verified here.

# Hermes Atlas v0.1.0

Initial curated source snapshot containing documentation guidance, schemas and templates, two optional manually connected Hermes skill packs, and Python standard-library documentation tooling with tests.

- Atlas-specific and generic project documentation validators.
- Additive bootstrap and managed source-map update tooling.
- Regression and isolated Git-fixture tests.
- No application runtime, installable package, or verified Hermes integration is included.
- Optional skills require owner-reviewed manual configuration; live Hermes discovery and invocation are not verified by these checks.
