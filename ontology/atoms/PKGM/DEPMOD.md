# PKGM.DEPMOD: Dependency Specification Modification

## Description

Modifies lock files, dependency specifications, or resolution configuration to alter which packages or versions resolve during installation. Includes lock file modifications (`package-lock.json`, `yarn.lock`, `Pipfile.lock`, `go.sum`), requirements file changes (`requirements.txt`, `Gemfile`), and resolution configuration changes that redirect package resolution. Also covers dependency confusion, publishing internal package names to public registries so that the public version resolves in place of the internal one.

> **Note:** The ID is `DEPMOD` for neutrality: "modification" describes the mechanical action without the judgment that "manipulation" would carry.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Lock file diffs (hash changes, URL changes, version changes), dependency specification modifications, registry URL overrides in `.npmrc`/`pip.conf`/resolution configuration, namespace mismatches between internal registry and public registry |
| Static Binary | N/A | Dependency specifications are source/configuration-level artifacts |
| Runtime/Dynamic | Yes | Package manager resolving a different version or source than expected, installation pulling from an unexpected registry, lock file content differing from repository state |

## Disambiguation

- **vs PKGM.PHANTOM**: `PKGM.DEPMOD` describes modification of resolution mechanics, changing which package or version resolves. `PKGM.PHANTOM` describes a dependency that is declared but never referenced in any source file. The anomaly in `DEPMOD` is in the resolution path; the anomaly in `PHANTOM` is in the usage (or lack thereof). A dependency can exhibit both: its resolution was modified (`DEPMOD`) and it is never imported (`PHANTOM`).
- **vs normal dependency updates**: Every dependency update modifies specification files. `PKGM.DEPMOD` applies as a structural observation when the modification is an analytical finding, version changes, source changes, resolution redirects. The atom describes the mechanical fact of modification; context determines significance.

## Structural Relationships

- **Often co-occurs with**: `PKGM.PUBLISH` (coordinated publication and resolution change), `PKGM.INSTALL` (the modified dependency has install hooks), `CRED.*` (the substituted package harvests credentials)
- **May imply**: The dependency resolution path has been altered from its prior state; the installed dependency set may differ from what the lock file previously specified

## Notes

Dependency confusion attacks are a specific pattern within `PKGM.DEPMOD`: a package name used internally is published to a public registry at a higher version number, causing resolvers that check both registries to prefer the public version. The structural observation is the same (the resolution path produces a different package than intended), but the mechanism (namespace collision across registries) is distinct from direct lock file modification. Both are `PKGM.DEPMOD` because both alter which package resolves during installation.
