---
name: project-navigator
description: Find files, symbols, and evidence in a project repository without confusing code maps with project overviews.
---
# Project Navigator

Use when you need to locate code, documentation, entry points, or ownership in a repository.

## Procedure
1. Confirm repository root, current branch, and worktree status before interpreting local context.
2. Discover the documentation layout. Prefer `docs/` when `docs/INDEX.md` exists; read it for navigation and follow its canonical links. Only when `docs/INDEX.md` is absent, fall back to root-level legacy documents such as `INDEX.md` and `ARCHITECTURE.md`. Do not require root docs when the docs/ entry point exists or assume every legacy repository has docs/.
3. Treat `INDEX.md` as a navigation map and `ARCHITECTURE.md` as a code/repository map; neither substitutes for source verification. For partial or mixed trees, use the discovered entry point as authoritative, follow valid canonical links, and report missing or conflicting documents rather than silently merging versions.
4. Search for the requested symbol/path using repository-native search; open the smallest relevant source and its direct callers/tests.
5. Report exact paths and line references where available. Mark claims `observed` (direct evidence) or `inferred` (reasoned, not proven).
6. If the map is missing/stale, say so and recommend an evidence-backed correction; do not invent structure.

## Guardrails
- Preserve unrelated worktree changes; never clean/reset or overwrite user files.
- Do not claim behavior solely from roadmap, names, or diagrams.

Further detail: [navigation checklist](references/navigation-checklist.md).
