# Navigation checklist

- Discover the documentation layout: prefer `docs/` when `docs/INDEX.md` exists; follow its canonical links.
- Only if `docs/INDEX.md` is absent, use available root-level legacy documents; do not assume all four exist.
- `INDEX.md` is the navigation map; `ARCHITECTURE.md` is the code/repository map.
- In partial or mixed trees, use the discovered entry point as authoritative, follow valid canonical links, and report gaps or conflicts; do not silently merge duplicates.
- Search symbol definition and relevant callers; follow only enough dependencies to answer.
- Verify claims in current files, not cached prose.
- Include paths and separate confirmed facts from hypotheses.
- Flag missing docs, broken links, and map drift with a minimal update suggestion.
