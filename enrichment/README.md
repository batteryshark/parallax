# Enrichment

Enrichment is factual context about observed things, sourced from outside the
code itself. It is the third kind of input the framework reasons over, alongside
atoms (what the code does) and structural relationships (how observations
connect). A domain's registration date, a maintainer account's activity history,
whether a published artifact rebuilds from its source: these are facts about the
artifact and its ecosystem, not statements about the code's syntax.

## Facts, not judgments

This is the same discipline the ontology follows. Enrichment records what is
true, never what it means.

- "This domain was registered 28 days before the release" is enrichment.
- "This domain is suspicious because it was registered recently" is a lens
  interpretation of that enrichment.

The MCD lens cares a great deal about domain age. The architecture lens does not.
Both read the same enrichment datum and do different things with it. Keeping the
fact separate from the interpretation is what lets one data point serve every
lens without baking any single lens's priorities into it.

## How enrichment is used

Enrichment does not produce findings on its own. It modifies confidence in
findings that come from atom observations and compositions. For a given lens,
each datum is one of three things (see
[`../investigation/confidence-algebra.md`](../investigation/confidence-algebra.md)):

- **Amplifying:** aligns with the lens's interpretation and raises confidence.
- **Attenuating:** offers an alternative explanation and lowers confidence.
- **Neutral:** irrelevant to this lens.

The same datum can be amplifying for one lens, neutral for another. A lens
declares its own weighting; enrichment only supplies the fact. The MCD lens's
weighting of these data points lives in
[`../lenses/mcd/signals/`](../lenses/mcd/signals/).

## Where enrichment comes from

Any method can produce enrichment, but OSINT and build analysis are the primary
sources (see [`../investigation/methods/`](../investigation/methods/)). WHOIS and
registry queries, publication and ownership history, build reproducibility
checks, and threat-intelligence lookups all yield enrichment. Because it is
externally sourced, enrichment carries its own confidence and can go stale, so a
datum records when and how it was obtained.

## Identifiers

Each data point has a stable `ENR.<CATEGORY>.<NAME>` id so a lens can reference
it precisely. The categories mirror the contextual-signal groupings the lenses
already use.

| Category | Id prefix | Data points |
|---|---|---|
| [Package metadata](package-metadata.md) | `ENR.PKG.*` | publication age, ownership history, downloads, version sequence, publish provenance |
| [Dependency graph](dependency-graph.md) | `ENR.DEP.*` | newly added dependencies, dependency popularity, transitive depth, resolution source |
| [Source-to-binary drift](source-to-binary-drift.md) | `ENR.DRIFT.*` | build reproducibility, behavioral drift, undeclared native components |
| [Temporal](temporal.md) | `ENR.TIME.*` | activity dormancy, coordinated publication, pre-staged versions |
| [Execution context](execution-context.md) | `ENR.EXEC.*` | lifecycle phase, privilege and orchestration, analysis-environment awareness |
| [Network destination](network-destination.md) | `ENR.NET.*` | domain age, hosting type, jurisdiction, threat-intel reputation |
