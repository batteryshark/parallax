# MCD Lens: Contextual Signals

Observations about the ecosystem, metadata, and provenance of an artifact that are not detectable within the code itself. Contextual signals do not generate findings independently; they modify confidence in findings from atom observations and behavioral compositions.

A medium-confidence finding in a package with multiple adverse contextual signals should be treated as high-confidence.

## Signal Categories

| Category | Description |
|---|---|
| [Package Metadata](package-metadata.md) | Publication history, maintainer changes, download anomalies, provenance |
| [Dependency Graph](dependency-graph.md) | New dependencies in patches, transitive anomalies, unpopular dependencies |
| [Source-to-Binary Drift](source-to-binary-drift.md) | Behavioral drift, build irreproducibility, unexpected native extensions |
| [Temporal Signals](temporal-signals.md) | Abandonment patterns, coordinated publication, pre-staged versions |
| [Execution Context](execution-context.md) | CI/CD targeting, security tooling context, privileged orchestration |
| [Network Destination](network-destination.md) | Jurisdictional risk, bulletproof hosting, recently registered domains |
