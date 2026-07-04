# PKGM.PHANTOM: Unreferenced Dependency Declaration

## Description

A dependency declared in a package manifest (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`, `Gemfile`, etc.) that is never imported, required, or referenced in any of the package's source files. The dependency exists in the manifest but no code path uses it. A grep across all source files confirming zero usage is a definitive structural observation.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Dependency entry in manifest with no corresponding `import`, `require`, `use`, `from X import`, or equivalent in any source file. Zero-reference analysis across all package source files is definitive. |
| Static Binary | N/A | Phantom dependencies are a source/manifest-level observation |
| Runtime/Dynamic | Partial | The dependency is installed (present in `node_modules`/`site-packages`/equivalent) but never loaded at runtime. Its install hooks, if any, still execute during installation regardless of whether the package's source code references it. |

## Disambiguation

- **vs PKGM.DEPMOD**: `PKGM.PHANTOM` describes a declared-but-unused dependency, the anomaly is in the absence of any source reference. `PKGM.DEPMOD` describes modification of resolution mechanics, the anomaly is in what resolves. A dependency can be both: its resolution was modified (`DEPMOD`) and it is never imported (`PHANTOM`).
- **vs optional/platform-specific dependencies**: Some ecosystems support conditional dependencies that are only imported under specific conditions (platform checks, feature flags, optional imports wrapped in try/except). Before confirming `PKGM.PHANTOM`, verify whether any conditional import path exists. If a conditional import exists, the dependency is not phantom, it has a code path, even if it is not taken in all environments.
- **vs devDependencies / test dependencies**: Dependencies declared in development or test sections and imported only in test files are not phantom if test files are included in the analysis scope. Scope the source-file search to match the dependency section.

## Structural Relationships

- **Often co-occurs with**: `PKGM.INSTALL` (the phantom dependency has install hooks that execute despite no source reference; this is the canonical supply chain pattern), `PKGM.DEPMOD` (resolution was modified to introduce the phantom dependency)
- **May imply**: The dependency serves a purpose other than providing code to the declaring package; its install hooks, its transitive dependencies, or its mere presence in the dependency tree is the intended effect

## Notes

A dependency with zero source references has no code-level reason to exist in the manifest. This is a purely structural observation: the manifest declares it, the source never uses it. The significance depends on what the phantom dependency does when installed: if it has install hooks (`PKGM.INSTALL`), those hooks execute regardless of whether the declaring package's code ever imports it. This is the mechanical basis of the supply chain pattern where a malicious package is added as a dependency purely for its install-time side effects.
