# Roadmap

## Status

`v0.2.1` is the latest published release (2026-10-25); tag `v0.2.1` points to the tested integration commit. The current `main` adds only release-state documentation after that commit.

## Delivered

- **v0.2.1 corrective patch** — improved skill routing/evidence guidance, corrected reconciliation CLI guidance and regression coverage, refreshed public use/release instructions. See [release notes](../RELEASE_NOTES.md).

## Proposed

1. **Broaden source-to-document routing only with evidence** — the opt-in packet uses transparent path-prefix suggestions, not dependency inference; add mappings only when maintainers can justify and test them.
2. **Review reconciliation packet quality in normal documentation changes** — proposed human process; the packet is advisory and does not modify documentation.

## Rules

Keep proposals distinct from implemented and released behavior. Record shipped tooling and completed verification in `PROJECT_STATE.md`; update release notes only for changes actually included in a release. Do not publish a version label or date in advance of an actual release.
