# Roadmap

## Status

`v0.2.0` is the latest published release and is the current `main` baseline. A corrective `v0.2.1` is a proposed, unreleased patch candidate; this document does not announce a release or set a release date. The candidate scope is limited to improving skill routing/evidence guidance, correcting reconciliation CLI guidance and regression coverage, and aligning public documentation with the released repository. See [release notes](../RELEASE_NOTES.md) for the candidate change list.

## Proposed

1. **Prepare the v0.2.1 corrective patch** — proposed; release only after review, validation, and maintainer approval. This candidate does not change the tool's feature scope or claim live Hermes runtime verification.
2. **Broaden source-to-document routing only with evidence** — the opt-in packet uses transparent path-prefix suggestions, not dependency inference; add mappings only when maintainers can justify and test them.
3. **Review reconciliation packet quality in normal documentation changes** — proposed human process; the packet is advisory and does not modify documentation.

## Rules

Keep proposals distinct from implemented and released behavior. Record shipped tooling and completed verification in `PROJECT_STATE.md`; update release notes only for changes actually included in a release. Do not publish a version label or date in advance of an actual release.
