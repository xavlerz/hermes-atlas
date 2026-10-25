# Hermes Atlas release notes

## v0.2.1 — Published (2026-10-25)

Published GitHub Release and annotated tag `v0.2.1`, pointing to commit `9c24ca56a7a15516b18e3c9a025aaba6b6b3bc9d`.

- Corrected the `reconcile_docs.py --base REF` help and added Git-fixture coverage for committed-range scope, default tracked changes, excluded untracked files, and worktree preservation.
- Refined the `project-navigator` and `project-docs-maintainer` activation boundaries, evidence checks, and progressive context guidance; replaced a wording-only test with behavior-focused coverage.
- Improved README quick-start, checkout update instructions and tool examples; documented maintainer Git/release practices and isolated Hermes acceptance scenarios; aligned project state and roadmap.
- No runtime dependencies added. The complete suite contains 38 tests; all passed, along with both documentation validators and GitHub Actions for Python 3.9 and 3.x.
- Hermes Agent v0.22.2 in a disposable `HERMES_HOME` discovered both external skills and included them in the prompt skill index. Model-driven selection and invocation were not tested.

## v0.2.0 — Published

Published GitHub Release and tag `v0.2.0`, at commit `63edd3d2a6e1a67da3ac5ca29ace5dd280fa63cc`.

- Added opt-in `tools/docs/reconcile_docs.py` to print an advisory documentation review packet from tracked Git changes, with optional `--base REF` comparison.
- Extended project-doc management with docs-first/legacy-safe bootstrap behavior and opt-in, marker-guarded source-map refresh limited to eligible tracked paths.
- Added separate Atlas and generic-project validators, regression/fixture tests, and the documentation workflow at `.github/workflows/docs.yml`.
- The published baseline contains 38 unit-test methods; CI is configured for Python 3.9 and 3.x. A configured workflow does not imply live Hermes runtime verification.

## v0.1.0 — Published

Initial curated source snapshot containing documentation guidance, schemas and templates, two optional manually connected Hermes skill packs, and Python standard-library documentation tooling with tests.

- Atlas-specific and generic project documentation validators.
- Additive bootstrap and managed source-map update tooling.
- Regression and isolated Git-fixture tests.
- No application runtime, installable package, or verified Hermes integration.
- Optional skills require owner-reviewed manual configuration; these source checks do not verify live Hermes discovery or invocation.
