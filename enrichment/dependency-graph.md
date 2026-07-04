# Dependency Graph

Facts about what a package depends on and where those dependencies come from.
Sourced from manifests, lockfiles, and registry data. These describe the
dependency set, not the dependencies' code.

| Id | Data point | What it factually states | Primary source |
|---|---|---|---|
| `ENR.DEP.NEW` | Newly added dependencies | Dependencies introduced in a given version or patch, relative to the prior version | manifest/lockfile diff |
| `ENR.DEP.POPULARITY` | Dependency popularity | Each dependency's download volume, age, and maintenance activity | registry API, OSINT |
| `ENR.DEP.DEPTH` | Transitive depth | Where a dependency sits in the tree and the path through which it enters | lockfile, manifest |
| `ENR.DEP.RESOLUTION` | Resolution source | The registry or source a dependency resolves from: public, internal, or a configured mirror/override | lockfile, registry config |

Judgment-free: this records the dependency facts. Whether a new transitive
dependency from an unpopular source in a patch release is suspicious is a lens
call. The MCD lens's weighting is in
[`../lenses/mcd/signals/dependency-graph.md`](../lenses/mcd/signals/dependency-graph.md).
