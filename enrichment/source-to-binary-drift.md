# Source-to-Binary Drift

Facts about whether a published artifact matches the source it claims to come
from. Sourced from build analysis and, where available, dynamic comparison.
These describe the relationship between source and shipped artifact.

| Id | Data point | What it factually states | Primary source |
|---|---|---|---|
| `ENR.DRIFT.REPRO` | Build reproducibility | Whether rebuilding from the declared source produces the published artifact byte-for-byte (or within a stated tolerance) | build analysis |
| `ENR.DRIFT.BEHAVIOR` | Behavioral drift | Observable differences in behavior between what the source implies and what the shipped artifact does | build analysis, dynamic |
| `ENR.DRIFT.NATIVE` | Undeclared native components | Native or precompiled components present in the artifact that are not derivable from the source tree | build analysis |

Judgment-free: this records the drift facts. Whether irreproducibility or an
undeclared native extension indicates tampering is a lens call. The MCD lens's
weighting is in
[`../lenses/mcd/signals/source-to-binary-drift.md`](../lenses/mcd/signals/source-to-binary-drift.md).
