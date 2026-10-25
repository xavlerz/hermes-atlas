# Documentation update checklist

- Scope work to affected paths and user-visible claims; expand only when a linked contract or dependency requires it.
- Start from `docs/INDEX.md` when present and follow relevant canonical links; otherwise use available root-level legacy documentation.
- In partial or mixed trees, follow the discovered entry point and valid links; report gaps or conflicts rather than silently merging duplicate sources.
- Search the source map/index for candidate files, then verify each claim in current source, relevant tests, or command output.
- Keep navigation maps distinct from code/repository maps and project overviews; update only maps made stale by the change.
- Distinguish observed facts, inferences, and proposed work; roadmaps are not evidence of implementation or release.
- Preserve unrelated staged, unstaged, and untracked changes; stage only task-owned files when authorized.
- Run the repository's relevant documentation validator and tests; check links, `git diff --check`, and exact staged paths.
- Report remaining discrepancies with paths, evidence, and ownership where known.
