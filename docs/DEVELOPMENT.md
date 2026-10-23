# Project docs tools

All commands use Python's standard library. Pass a target root explicitly; tools requiring Git roots require the exact Git top-level. Existing changes are preserved. `manage_project_docs.py` reports Git status; it does not stage, commit, or delete files.

## Third-party project validation
`PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/validate_project.py /absolute/project/root`

Checks the present core documents (`INDEX.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `PROJECT_STATE.md`) and their relative links/anchors at the target Git root. It does not impose Atlas schemas, skills, or optional registry. This is distinct from Atlas validation below.

## Bootstrap / update
`PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/manage_project_docs.py /absolute/project/root --dry-run`
`PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/manage_project_docs.py /absolute/project/root`

Selects docs-first or legacy-root layout from existing core documents and rejects ambiguous/mixed layouts. Creates only missing core docs and guidance for the selected layout; existing files are not overwritten. Preview with `--dry-run` before applying. Bootstrap does not refresh the map.

Preview and then apply a managed `docs/INDEX.md` map refresh explicitly:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/manage_project_docs.py /absolute/project/root --update --dry-run
PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/manage_project_docs.py /absolute/project/root --update
```

The map includes eligible tracked files, omits untracked files and excluded/sensitive paths, and is capped at 250 paths. Only the marker-delimited block is replaced; prose outside it is preserved. Malformed/duplicate markers are rejected.

## Atlas-only validation
From this repository root: `PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/validate_atlas.py`. This checks Atlas-specific layout, core-document links, schema/registry and skill-frontmatter contracts. It takes no target-root argument and is deliberately separate from generic target-project validation.

## Opt-in documentation reconciliation
`PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/reconcile_docs.py --root /absolute/project/root` prints a deterministic advisory packet from tracked Git changes. Untracked paths are excluded. Without `--base`, it reports the worktree/index diff against `HEAD`; `--base REF` compares only the committed range `REF..HEAD` and excludes staged and unstaged worktree changes. Broad source-prefix routing is only a suggestion, not dependency analysis: verify relevance against source and tests. It never edits documents, stages files, or invokes an LLM.

## Tests
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/docs/tests -v`
