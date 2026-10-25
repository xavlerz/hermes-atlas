# Hermes Atlas release notes

## v0.2.1 — Unreleased candidate

This section tracks proposed corrective changes on the `v0.2.1` development line. It is not a published release; no tag or GitHub Release is created by these notes.

- Clarify that `reconcile_docs.py --base REF` compares only committed changes in `REF..HEAD`, and add isolated Git-fixture coverage proving staged, unstaged, and untracked paths are excluded without altering the worktree.
- Strengthen default reconciliation coverage for tracked staged/unstaged changes and explicit untracked-path exclusion.
- Refine the two skill descriptions and workflows to separate source lookup from documentation maintenance, verify claims against current source/tests, use indexes as navigation rather than proof, expand context only as needed, and distinguish observed evidence from inference/proposal.
- Replace a brittle test of specific skill wording with behavioral reconciliation tests; retain the existing structural layout and validator contracts.
- Align the README, roadmap, project state, and onboarding guidance with the published `v0.2.0` baseline, the unreleased candidate, and actual runtime-verification limits.

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
