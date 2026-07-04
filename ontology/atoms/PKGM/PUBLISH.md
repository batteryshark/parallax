# PKGM.PUBLISH: Package Publication Metadata

## Description

Observable properties of package publication: version numbering patterns, authorship metadata, publication timing, maintainer account history, and registry metadata. These are structural observations about the publication event and the package's registry presence, not behavioral code observations. Version number gaps, authorship changes between versions, bulk publication patterns, publication timing relative to other package events, and maintainer account age/activity are all metadata properties accessible through registry APIs.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Partial | Version field in manifest files, author/maintainer fields in `package.json`/`setup.cfg`/`Cargo.toml`, but these are self-reported and may not match registry state |
| Static Binary | N/A | Publication metadata is a registry-level observation |
| Runtime/Dynamic | N/A | Publication metadata is observable at analysis time through registry APIs, not at code runtime |
| Registry API | Yes | Version history with timestamps, maintainer account metadata (creation date, other packages published, account age), publication frequency, version number sequences, authorship changes across versions |

## Disambiguation

- **vs behavioral atoms**: `PKGM.PUBLISH` describes metadata properties of the publication event, not code behavior. It contextualizes other findings rather than standing alone as a behavioral observation. A package with suspicious `PUBLISH` metadata and no behavioral findings is different from one with suspicious `PUBLISH` metadata alongside `PKGM.INSTALL` + `NETW.*`.
- **vs PKGM.DEPMOD**: `PKGM.PUBLISH` observes the publication event's metadata (who published, when, version numbering). `PKGM.DEPMOD` observes changes to dependency resolution (what resolves, from where). A dependency confusion attack involves both: `PKGM.PUBLISH` (new package published to public registry with internal name) and `PKGM.DEPMOD` (resolution now picks up the public version).

## Structural Relationships

- **Often co-occurs with**: `PKGM.DEPMOD` (coordinated publication and resolution change, dependency confusion pattern), `PKGM.INSTALL` (newly published version adds install hooks), `PKGM.PHANTOM` (newly published package is added as an unreferenced dependency)
- **May imply**: The package's publication history and authorship have been assessed as part of analysis context

## Notes

Publication metadata is contextual rather than behavioral. It describes the circumstances of the package's appearance in the registry, not what the package's code does. A newly created maintainer account publishing a package with a name similar to a popular package, with a `postinstall` hook, at 3 AM UTC on a weekend. Each of these metadata observations individually is unremarkable, but they compose a recognizable pattern. `PKGM.PUBLISH` captures these metadata observations so they can be combined with behavioral findings from other atoms.
