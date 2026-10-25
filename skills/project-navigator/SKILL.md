---
name: project-navigator
description: Locate files, symbols, and source evidence; not for documentation maintenance.
---
# Project Navigator

Use this skill to find code, documentation, entry points, ownership, and repository evidence. If the request audits, reconciles, creates, or changes project documentation, use `project-docs-maintainer` instead.

## Procedure
1. Search for the requested symbol or path with repository-native search. Read the smallest relevant source and direct callers/tests; follow further dependencies only as needed to answer.
2. Consult the documentation entry point when it helps identify ownership or related components. Prefer `docs/` when `docs/INDEX.md` exists and follow its canonical links. Only when `docs/INDEX.md` is absent, fall back to available root-level legacy docs. In partial or mixed layouts, follow the discovered entry point and valid links; report gaps/conflicts instead of silently merging duplicate docs.
3. Treat maps and prose as navigation aids, not proof of behavior. Verify behavioral claims in current source, tests, or command output. If docs appear stale or contradictory, state the evidence and suggest a correction; do not edit docs unless asked.
4. Inspect repository root, branch, and Git status/diffs only when local changes affect the answer. Cite paths/line references where available and label claims `observed` or `inferred`.

## Guardrails
- Preserve unrelated worktree changes, including untracked files. Never clean, reset, stage, or overwrite user files.
- Do not claim behavior solely from roadmap, names, or diagrams.

See [navigation checklist](references/navigation-checklist.md) for focused lookup practices.
