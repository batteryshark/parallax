# Investigation Framework

Shared mechanics for the investigation cycle and confidence assessment.

## Confidence Algebra

Structural rules for how evidence composes, regardless of which lens is interpreting:
- Reachability requirements
- Cross-category accumulation
- Idiom recognition weighting
- Provenance (multi-method confirmation)
- Enrichment integration
- Disproof handling

## Methods of Observation

First-class descriptions of how practitioners gather information:
- Static source analysis
- Static binary analysis
- Dynamic analysis
- OSINT / external intelligence
- Build & CI analysis
- Network analysis
- Environment scaffolding

Each method defines its capabilities, blind spots, tools required, and when the investigation cycle should suggest transitioning to it.

## Investigation Cycle

The iterative process: observe → interpret → verify → discover more → re-evaluate. Not a layer but a process that drives refinement across all active lenses.

## Investigation Runs

[`runs/`](runs/) defines the artifact layout for recorded investigations: bounded source, binary, decompilation, or lens-verification investigations that feed back into findings and confidence. Scanner runners write the same layout in their own repositories; runs checked in here are shared evidence or worked examples.

## Status

- [x] Confidence algebra defined (`confidence-algebra.md`)
- [x] Methods of observation defined (7 methods in `methods/`)
- [x] Investigation cycle formalized (`cycle.md`)
- [x] Enrichment definitions ([`../enrichment/`](../enrichment/): lens-neutral data point definitions)
