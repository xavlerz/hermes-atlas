# Project state

## Scope and release status

Hermes Atlas provides project documentation, schemas/templates, optional Hermes skill-pack source, Python standard-library tools, tests, and a documentation CI workflow; it contains no application runtime. The latest published release is `v0.2.0`, represented by tag `v0.2.0` at `63edd3d2a6e1a67da3ac5ca29ace5dd280fa63cc`; that commit is the current public `main` baseline. `v0.2.1` is an unreleased corrective candidate, not a published version. The skills are optional and require manual owner-controlled configuration.

## Implemented behavior

- `tools/docs/manage_project_docs.py` selects a docs-first or legacy-root layout from existing core documents, refuses ambiguous/mixed layouts, creates only absent core documents and guidance on bootstrap, and updates only the marked map block when explicitly requested. The map enumerates eligible tracked files (with exclusions/limit), not untracked files.
- Managed-map updates require exactly one correctly ordered marker pair when markers exist; malformed/duplicate markers are rejected. User prose outside the block is preserved.
- `tools/docs/validate_atlas.py` checks Atlas layout, core-document links, schemas, optional-document registry, and skill frontmatter. `tools/docs/validate_project.py ROOT` separately checks a target Git root's present core docs and relative links/anchors; it does not enforce Atlas schemas or skills.
- `tools/docs/reconcile_docs.py --root ROOT` emits an advisory packet from tracked Git differences. It excludes untracked paths, uses broad path-prefix routing suggestions, edits no files, and invokes no LLM. Default mode compares tracked index/worktree changes against `HEAD`; `--base REF` compares only committed changes in `REF..HEAD`, excluding staged and unstaged worktree changes.
- `.github/workflows/docs.yml` configures tests and both validators on push and pull request for Python 3.9 and 3.x. Workflow configuration is not itself evidence that a particular run passed.

## Validation and runtime limits

The published `v0.2.0` baseline was validated locally with 38 unit tests and both documentation validators. Candidate changes require rerunning the complete suite and validators; results are reported with the corresponding check run. Source checks do not establish Hermes skill discovery or invocation. Live runtime behavior must be checked in an isolated, owner-controlled Hermes profile; this repository's automated suite does not perform that integration test.

No application runtime, deployment, or hosted service is verified. Hermes configuration, skill permissions, release publication, and remote CI results remain separate from local source-level checks.
