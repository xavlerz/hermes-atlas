# Project state

## Scope and release status

Hermes Atlas provides project documentation, schemas/templates, optional Hermes skill-pack source, Python standard-library tools, tests, and a documentation CI workflow; it contains no application runtime. The latest published release is `v0.2.1` (published 2026-10-25), via annotated tag `v0.2.1` pointing to `9c24ca56a7a15516b18e3c9a025aaba6b6b3bc9d`. The current `main` contains that tagged release plus a documentation-only update recording its publication. `v0.2.0` remains available as the previous published release. The skills are optional and require manual owner-controlled configuration.

## Implemented behavior

- `tools/docs/manage_project_docs.py` selects a docs-first or legacy-root layout from existing core documents, refuses ambiguous/mixed layouts, creates only absent core documents and guidance on bootstrap, and updates only the marked map block when explicitly requested. The map enumerates eligible tracked files (with exclusions/limit), not untracked files.
- Managed-map updates require exactly one correctly ordered marker pair when markers exist; malformed/duplicate markers are rejected. User prose outside the block is preserved.
- `tools/docs/validate_atlas.py` checks Atlas layout, core-document links, schemas, optional-document registry, and skill frontmatter. `tools/docs/validate_project.py ROOT` separately checks a target Git root's present core docs and relative links/anchors; it does not enforce Atlas schemas or skills.
- `tools/docs/reconcile_docs.py --root ROOT` emits an advisory packet from tracked Git differences. It excludes untracked paths, uses broad path-prefix routing suggestions, edits no files, and invokes no LLM. Default mode compares tracked index/worktree changes against `HEAD`; `--base REF` compares only committed changes in `REF..HEAD`, excluding staged and unstaged worktree changes.
- `.github/workflows/docs.yml` configures tests and both validators on push and pull request for Python 3.9 and 3.x. Workflow configuration is not itself evidence that a particular run passed.

## Validation and runtime limits

The `v0.2.1` release commit passed all 38 unit tests and both documentation validators; GitHub Actions passed on Python 3.9 and 3.x for the merge and tag. See [the v0.2.1 release](https://github.com/xavlerz/hermes-atlas/releases/tag/v0.2.1). Reconciliation and source-map generation/update are covered by isolated temporary Git fixtures.

Hermes Agent v0.22.2 was run against a disposable `HERMES_HOME`: it detected both external skills and included them in the generated prompt skill index. No model request was made, so automatic skill selection and invocation remain unverified. Do not infer them from static validation or discovery alone.

No application runtime, deployment, or hosted service is verified. Hermes profile configuration and skill permissions remain owner-controlled.
