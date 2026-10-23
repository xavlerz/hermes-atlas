# Documentation update checklist

- Discover the documentation layout: prefer `docs/` when `docs/INDEX.md` exists and follow its canonical links; only fall back to available root-level legacy docs when that entry point is absent.
- Do not require root docs in docs-first repositories or assume every legacy repository has a `docs/` directory.
- In partial or mixed trees, treat the discovered entry point and valid links as authoritative; report gaps/conflicts instead of silently merging duplicates.
- Keep `INDEX.md` as navigation map separate from the `ARCHITECTURE.md` code map.
- Identify docs affected by changed behavior and paths.
- Re-read source and tests; don't copy stale statements forward.
- Keep roadmap proposals distinct from verified state.
- Update internal links and optional status only when document state changes.
- Run the stdlib checker and documented test scenarios; inspect `git diff --check` and exact staged paths.
- Report unresolved discrepancies with ownership and evidence.
