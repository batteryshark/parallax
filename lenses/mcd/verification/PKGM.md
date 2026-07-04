# MCD Lens: PKGM (Package & Build Operations) Verification

Investigation questions for PKGM findings. Questions tagged `[lens-neutral]` are applicable across multiple lenses. Questions tagged `[MCD]` assume an MCD evaluation context.

## General: Any PKGM Atom

1. **Is this a direct or transitive dependency? How many hops from the consumer's manifest?** Direct dependencies are explicitly chosen; transitive dependencies may be inherited without review. Each hop reduces the likelihood of prior scrutiny. `[lens-neutral]`

2. **What is the package's download volume and reverse-dependency count?** High-traffic packages have greater blast radius but also more community scrutiny. Low-traffic packages with recent publication and no reverse dependencies are a different risk profile. `[lens-neutral]`

3. **Does the installed version match the lock file, and is the lock file change traceable to a reviewed commit?** Version drift between lock file and installed artifact, or lock file changes without corresponding reviewed PRs, indicate an unexplained resolution path change. `[lens-neutral]`

4. **Does the registry, repository, or maintainer account show anomalous activity?** Recently created maintainer account, bulk publication of similarly-named packages, repository URL pointing to a different project than the package name suggests, or maintainer change without documented project transfer. `[MCD]`

## PKGM.INSTALL

5. **What is the complete set of commands the install hook executes? Are they static or dynamically constructed?** Enumerate every command the hook runs. Static, readable commands (`node-gyp rebuild`, `make install`) are structurally different from dynamically constructed or decoded command strings. `[lens-neutral]`

6. **Has the install hook content changed across the last 3 published versions?** Diff the hook content across recent releases. A newly added or significantly modified install hook in the latest version, especially if other package content is unchanged, is a version-level anomaly. `[lens-neutral]`

7. **Does the install hook make network calls, write files outside its own directory, or register persistence mechanisms?** Network calls from install hooks (`NETW.*`), writes outside `node_modules`/`site-packages`/equivalent (`FSYS.WRITE`), and persistence registration (`PRST.*`) are behavioral escalations beyond normal build activity. `[MCD]`

## PKGM.PHANTOM

8. **Is there any code path, including conditional imports, platform checks, or optional feature gates, that explains why this dependency is declared but not imported?** Exhaustive search: grep all source files for any reference to the dependency name. Check for dynamic imports, lazy loading, conditional requires, and try/except import blocks. If zero references exist across all code paths, the dependency is definitively phantom. `[lens-neutral]`

9. **Does the phantom dependency have an install hook?** A dependency with zero source references and an active install hook exists solely for its install-time side effects. This is the defining structural pattern of supply chain injection via phantom dependencies. `[MCD]`

## PKGM.BINDOWN

10. **Does the download URL resolve to official project infrastructure?** Verify the download host against the project's documented release infrastructure: GitHub Releases for the same organization, the project's official CDN, or a well-known binary distribution service. URLs pointing to personal hosting, URL shorteners, recently registered domains, or unrelated infrastructure are a structural anomaly. `[lens-neutral]`

11. **Is the downloaded binary verified against a checksum or cryptographic signature?** Check whether the install script compares the downloaded artifact against a known hash or verifies a signature. The presence or absence of integrity verification is a structural observation. If verification exists, confirm the reference hash is not fetched from the same host as the binary (same-origin verification is no verification). `[lens-neutral]`

## PKGM.DEPMOD

12. **What is the specific change to the dependency specification, who made it, and is there a corresponding reviewed PR?** Identify the exact diff: version bump, source URL change, registry redirect, new dependency addition. Attribute the change to a commit author and determine whether the change passed through a code review process. Unattributed or unreviewed resolution changes are unexplained modifications. `[lens-neutral]`

## PKGM.HOOK

13. **What commands does the build hook execute, and are they consistent with the package's build requirements?** A C extension running `make` or `cmake` is expected. A JavaScript utility adding a Makefile target that runs `curl` is not. Assess whether the build hook's content matches the package's stated compilation or bundling needs. `[lens-neutral]`

14. **Is the build hook present in the upstream source repository, or was it added in the published package?** Compare the published package contents against the source repository at the tagged version. Build hooks present only in the published artifact, not in the source repo, were added during or after the publication process. `[MCD]`

## PKGM.PUBLISH

15. **When was the maintainer account created, and what other packages has it published?** A recently created account publishing a package with a name similar to a popular package has a different risk profile than a long-standing account with an established publication history. `[MCD]`

16. **Is there a documented explanation for version gaps or maintainer changes?** Check the project's changelog, release notes, blog, or registry announcement for documented ownership transfers or version numbering decisions. Unexplained gaps or changes are metadata anomalies; documented ones are context. `[lens-neutral]`
