# MCD Lens: PKGM (Package & Build Operations) Indicators

> **Core MCD position:** PKGM addresses the delivery mechanism of supply chain attacks. Install-time code execution, dependency manipulation, and build system abuse are the vectors through which malicious payloads enter development environments. The delivery mechanism is often the first indicator, and the most automatable to detect.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `PKGM.INSTALL` + `NETW.*`/`EXEC.*` | Very High | Install hook with network or execution behavior, primary supply chain primitive |
| `PKGM.BINDOWN` | High | Downloaded binary bypasses source-level analysis entirely |
| `PKGM.PHANTOM` | High | Zero source references means no legitimate code-level purpose for the dependency |
| `PKGM.DEPMOD` | Medium-High | Dependency resolution modification, significance depends on what changed and who changed it |
| `PKGM.HOOK` | Medium-High | Build system injection, broader attack surface than package manager hooks, often less reviewed |
| `PKGM.PUBLISH` | Low (alone) | Publication metadata contextualizes other findings; rarely significant in isolation |

## Escalation Factors

- **`PKGM.INSTALL` + `NETW.*`.** Install hook makes network calls. The package reaches out to external infrastructure during installation. The combination of automatic execution and network communication is the canonical supply chain delivery mechanism.
- **`PKGM.PHANTOM` with install hook.** A declared-but-never-imported dependency that has its own install hook is the canonical supply chain injection pattern. The dependency exists solely for its install-time side effects. This is the exact pattern observed in the Axios npm incident and the `plain-crypto-js` PyPI attack.
- **`PKGM.BINDOWN` from non-canonical host.** Binary downloaded from infrastructure not associated with the project's known build/release pipeline. Custom domains, personal hosting, URL shorteners, or recently-registered domains hosting build artifacts.
- **`PKGM.BINDOWN` without checksum or signature verification.** Downloaded binary is placed and executed without integrity verification. The absence of verification is a structural observation: the install script contains no hash comparison or signature check against the downloaded artifact.
- **`PKGM.PUBLISH` version gap + authorship change.** Version numbering jumps (e.g., 1.2.3 to 1.2.7) combined with a different maintainer account publishing the new version. Consistent with account compromise or unauthorized publication.
- **`PKGM.DEPMOD` against pinned lock file.** Lock file modification in a project that uses pinning indicates the resolution path was deliberately altered. If the lock file change is not attributable to a reviewed dependency update, the modification is unexplained.
- **`PKGM.HOOK` in transitive dependency.** Build system hook modification in a dependency the consumer did not directly choose. Transitive dependencies receive less review; build hooks in transitive dependencies are a high-value hiding spot.
- **High downstream reach.** Any PKGM finding in a package with high download volume or many reverse dependencies amplifies impact. Supply chain attacks target popular packages because the blast radius is larger.
- **`PKGM.INSTALL` script is obfuscated.** An install hook whose content is encoded, minified beyond readability, or constructed from fragments (`XFRM.*`) is resisting analysis. Legitimate install scripts are typically straightforward build commands.
- **`PKGM.PHANTOM` name is a plausible variant of a legitimate package.** The unreferenced dependency has a name that closely resembles a popular package (typosquatting). The combination of zero source references and a typosquatted name is a strong structural indicator.

## De-escalation Factors

- **`PKGM.INSTALL` script is auditable and version-stable.** The install hook contains straightforward, readable build commands (`node-gyp rebuild`, `make`, `cargo build`) that have been present across multiple versions with consistent content. Legitimate native extensions require install-time compilation.
- **`PKGM.BINDOWN` from official, integrity-verified URL.** Binary downloaded from the project's documented release infrastructure (GitHub Releases for the same organization, official CDN) with checksum or signature verification against a known-good value. This is standard practice for distributing pre-built native extensions.
- **`PKGM.PHANTOM` is optional/platform-specific with documented reason.** The dependency is declared as optional or platform-specific, documented in the project's README or contributing guide, and a conditional import path exists even if it is not taken in all environments.
- **`PKGM.DEPMOD` attributed to authenticated dependency update tool.** Lock file modification is the result of a Dependabot, Renovate, or equivalent automated dependency update tool, visible in commit history with the tool's authenticated identity and a corresponding reviewed PR.
- **`PKGM.PUBLISH` anomaly explained by documented project transfer.** Maintainer change or version gap is documented in the project's changelog, blog post, or registry announcement as an intentional transfer of ownership.

> **Caveat:** De-escalation lowers the baseline; it does not eliminate the finding. A version-stable install hook can be modified in a single release to add malicious behavior. Historical legitimacy is context, not clearance.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `PKGM.PHANTOM` + `PKGM.INSTALL` + `NETW.*` | Axios pattern, unreferenced dependency with install hook that makes network calls. The dependency exists solely for install-time payload delivery. | Very High |
| `PKGM.INSTALL` + `EXEC.*` + `XFRM.*` | Obfuscated install hook, install-time execution with encoded/constructed command content. Deliberate resistance to static analysis of the install script. | Very High |
| `PKGM.BINDOWN` + `EXEC.*` | Binary download followed by execution of the downloaded artifact. Source-level analysis cannot assess what runs. | Very High |
| `PKGM.DEPMOD` + `PKGM.PUBLISH` | Coordinated substitution, dependency resolution modified alongside suspicious publication metadata. Consistent with dependency confusion or account compromise. | High |
| `PKGM.HOOK` + `NETW.*` | Build system hook makes network calls during build. Build configuration is reaching out to external infrastructure. | High |
| `PKGM.PUBLISH` (new maintainer) + `PKGM.INSTALL` | New maintainer adds or modifies install hooks. Account takeover pattern, the first action of a new maintainer is adding install-time execution. | High |
| `PKGM.PHANTOM` + typosquatted name | Unreferenced dependency with a name resembling a popular package. No code uses it; its install-time side effects are the payload vector. | High |
| `PKGM.INSTALL` + `PRST.*` | Install hook establishes persistence, cron entries, shell profile modification, service registration during package installation. | Very High |
| `PKGM.BINDOWN` + `XFRM.*` | Downloaded binary is encoded/encrypted or download URL is constructed from fragments. Deliberate concealment of the binary source or content. | Very High |
| `PKGM.DEPMOD` + `CRED.*` | Substituted dependency harvests credentials. The resolution change delivers a package that accesses authentication material. | Very High |

## MCD-Specific Disambiguation

### PKGM.INSTALL vs EXEC.*
Through the MCD lens, `PKGM.INSTALL` is the trigger and `EXEC.*` is the mechanism. Both apply simultaneously. `PKGM.INSTALL` elevates the severity of any `EXEC.*` finding because it means the execution happens automatically during package installation, no consumer action required beyond `npm install` or `pip install`. An `EXEC.SHELL` finding at runtime is context-dependent; an `EXEC.SHELL` finding inside `PKGM.INSTALL` is a strong MCD finding.

### PKGM.PHANTOM vs PKGM.DEPMOD
`PKGM.PHANTOM` and `PKGM.DEPMOD` are orthogonal observations. `PHANTOM` asks: "does any source code use this dependency?" `DEPMOD` asks: "was the resolution path for this dependency modified?" A dependency can be both phantom and modified, either but not the other, or neither. In MCD analysis, `PHANTOM` is the higher-baseline finding because zero source references is a definitive structural anomaly: there is no code-level explanation for the dependency's presence.

### PKGM.HOOK vs PKGM.INSTALL
Both are code execution during build/install, but through different mechanisms. `PKGM.INSTALL` uses the package manager's native hook system and is well-known as an attack surface. `PKGM.HOOK` uses build toolchain configuration and receives less security scrutiny. Through the MCD lens, `PKGM.HOOK` in a transitive dependency is particularly concerning because build configuration files are rarely reviewed in dependencies.

### PKGM.PUBLISH as contextual signal
`PKGM.PUBLISH` alone is Low severity because metadata anomalies have many benign explanations. Its MCD value is as an escalation factor for behavioral findings. A package with `PKGM.INSTALL` + `NETW.*` that also has `PKGM.PUBLISH` anomalies (new maintainer, version gap, recently created account) is a stronger finding than the behavioral atoms alone.
