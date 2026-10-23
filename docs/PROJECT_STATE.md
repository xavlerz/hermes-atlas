# Project state

## Scope
This v0.2.0 release-preparation tree contains documentation, schemas/templates, optional skill-pack source, Python standard-library tools, tests, and a documentation CI workflow. It does not contain an application runtime. No tag or GitHub Release has been created.

## Implemented source behavior
- `tools/docs/manage_project_docs.py`: selects a docs-first or legacy-root layout from existing core documents, refuses ambiguous/mixed layouts, creates only absent core documents and guidance on bootstrap, and updates only the marked map block when explicitly requested. The map enumerates eligible tracked files (with exclusions/limit), not untracked files.
- Managed-map updates require exactly one correctly ordered marker pair when markers exist; malformed/duplicate markers are rejected. User prose outside the block is preserved.
- `tools/docs/validate_atlas.py` runs Atlas validation, including layout, core-document links, schemas, optional-document registry, and skill frontmatter contracts. `tools/docs/validate_project.py ROOT` separately checks a target Git root's present core docs and relative links/anchors; it does not enforce Atlas schemas or skills.
- `tools/docs/reconcile_docs.py --root ROOT` emits an advisory packet from tracked Git differences. It excludes untracked paths, uses broad path-prefix routing suggestions, edits no files, and invokes no LLM. `--base REF` compares `REF..HEAD` plus worktree changes.
- `.github/workflows/docs.yml` configures tests and both validators on push and pull request for Python 3.9 and 3.x. This describes configuration only, not successful remote CI or Hermes integration.

## Validation
Locally run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/validate_atlas.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/docs/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/validate_project.py /absolute/path/to/hermes-atlas
git diff --check
```

This release-preparation check run reports 38 passing unit tests, a passing Atlas validator, a passing generic validator against this repository, and a clean `git diff --check`. These are local source checks, not remote CI results or Hermes runtime integration. The skills are not automatically installed or connected.

## Limits
No application runtime, deployment, live skill discovery, or invocation is verified by these checks. Publication, repository availability, tags/releases, remote CI status, and external Hermes configuration remain unverified or owner-controlled.
