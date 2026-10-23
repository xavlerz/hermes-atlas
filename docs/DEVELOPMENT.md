# Project docs tools

All commands are Python stdlib only. Never point tools at a project implicitly: pass its root explicitly. The root must resolve to the Git top-level. Dirty/untracked state is reported and preserved; tools do not stage, commit, or delete files.

## Third-party project validation
`python3 tools/docs/validate_project.py /absolute/project/root`

Checks only `INDEX.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `PROJECT_STATE.md` and relative links in present core docs. It does not impose Atlas schemas, skills, or optional registry.

## Bootstrap / update
`python3 tools/docs/manage_project_docs.py /absolute/project/root --dry-run`
`python3 tools/docs/manage_project_docs.py /absolute/project/root`

Creates absent core documents, `AGENTS.md`, and `docs/` templates only. Existing files are never overwritten; rerunning reports no changes. Review dry-run output first. A stale code map is surfaced as a suggested action, not rewritten automatically; manually update the map with evidence while retaining user text.

## Atlas-only validation
From this repository: `python3 tools/docs/validate_atlas.py /absolute/path/to/hermes-atlas`. This checks Atlas-specific schema/registry/skill contracts and is deliberately separate.

## Tests
`python3 -m unittest discover -s tools/docs/tests -v`
