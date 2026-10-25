---
name: project-docs-maintainer
description: Audit and update project documentation against verified source and test evidence.
---
# Project Documentation Maintainer

Use when creating, auditing, reconciling, or updating project documentation. For code lookup without documentation work, use `project-navigator`.

## Lifecycle
1. **Scope:** identify the requested behavior and changed paths first. Read repository instructions and the documentation entry point (`docs/INDEX.md` when present); follow only links relevant to the scope. Inspect Git status/diffs when changes in the worktree could affect the answer or must be preserved.
2. **Verify:** inspect current source, relevant tests, and runnable commands for every behavioral claim. Use maps and prose to navigate, not as proof. If sources conflict or are incomplete, state the conflict and confidence rather than presenting stale documentation as fact.
3. **Classify:** distinguish `observed` facts (direct source, test, or command evidence), `inferred` conclusions (reasoning and uncertainty stated), and `proposed` changes (not implemented). Never report a plan as completed behavior.
4. **Update:** change only documents affected by the request or code changes. Keep project state, roadmap proposals, and release status distinct; preserve established structure and terminology. Update links, paths, commands, and supported-status claims when affected. Avoid duplicating source explanations.
5. **Check:** run the repository's relevant documentation validators and tests, inspect changed links and the final diff, and report checks actually performed plus unresolved discrepancies.

## Safety
- Preserve unrelated staged, unstaged, and untracked work. Never clean, reset, overwrite, or include user changes in a commit.
- Do not stage or commit unless the task explicitly authorizes it; stage only verified task-owned paths.
- In partial or mixed documentation layouts, use the discovered entry point and valid canonical links; report gaps or conflicts rather than silently merging duplicate documents. Only when `docs/INDEX.md` is absent, fall back to available root-level legacy docs.
- Audit only the requested repository. Never apply its validator to unrelated projects.
- Hermes external skill directories may be writable: do not modify profile/global configuration without explicit authorization.
- Separate static/source verification from Hermes runtime, deployment, and production evidence.

See [claim taxonomy](references/claim-taxonomy.md) and [update checklist](references/update-checklist.md).
