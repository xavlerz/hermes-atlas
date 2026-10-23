---
name: project-docs-maintainer
description: Audit, plan, update, and validate project documentation against code evidence while preventing factual drift.
---
# Project Documentation Maintainer

Use when creating, auditing, or updating a project's documentation system.

## Lifecycle
1. **Audit:** inspect repository instructions, documentation layout, current docs, source/tests, Git status and task-owned diffs. Preserve unrelated and untracked work. Prefer `docs/` when `docs/INDEX.md` exists and use its canonical links. Only when that entry point is absent, fall back to available root-level legacy documents; do not require root docs in a docs-first tree or assume every legacy repository has `docs/`.
2. **Classify:** label every substantive claim factual (cite file/command/evidence), inferred (state basis and uncertainty), or proposed (not implemented). Never convert a plan into a claim of completion.
3. **Plan:** maintain the core `INDEX.md`, `ARCHITECTURE.md`, `ROADMAP.md`, and `PROJECT_STATE.md` within the discovered canonical layout. Keep the `INDEX.md` navigation map distinct from the `ARCHITECTURE.md` code map and the project overview. In partial or mixed trees, treat the discovered entry point and its valid links as authoritative; report gaps or conflicts rather than silently merging duplicate documents.
4. **Update:** edit only relevant docs; align links, code paths, tests, commands, statuses, and verification dates. Avoid duplicating large source explanations.
5. **Check:** run the repository's documentation validator and relevant tests; inspect diffs and links. Report gaps and exact evidence, not a blanket claim of correctness.

## Safety
- Discover and preserve existing work before editing; do not stage or commit unrelated files.
- Audit only the requested repository. Never apply this repository's validator to unrelated projects.
- Hermes external directories can be writable: require owner review and explicit config change; do not silently modify profile/global configuration.
- Separate source-level verification from runtime, deployment, and production evidence.

See [claim taxonomy](references/claim-taxonomy.md) and [update checklist](references/update-checklist.md).
