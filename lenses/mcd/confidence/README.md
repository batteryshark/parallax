# MCD Confidence Parameterization

How the MCD lens applies the shared [confidence algebra](../../../investigation/confidence-algebra.md) to malicious code detection.

## MCD Severity Baselines

Each atom has a baseline severity defined in the per-category [indicator files](../indicators/). Baselines reflect how suspicious the behavior is **in the context of a dependency or third-party code**: the MCD lens's primary operating context.

General principles for MCD severity assignment:

| Baseline | MCD Meaning | Examples |
|---|---|---|
| **Informational** | Expected in most software. Only meaningful in combination. | `NETW.HTTP` in a request library, `CRPT.HASH` in an integrity checker |
| **Low** | Unusual in stated context but common benign explanations exist. | `FSYS.SENSITIVE` in a utility library, `SYSI.OS` in a cross-platform tool |
| **Medium** | Could be malicious or benign, investigation required. | `CRED.ENV` reading secrets, `LOAD.EVAL` in non-template code |
| **High** | Rarely benign in dependency/third-party context. Active investigation warranted. | `EXEC.INJECT` in a library, `PRST.BOOTKIT` anywhere |
| **Critical** | Almost never benign. Immediate attention. | `EXEC.INJECT` + reachability in a transitive dependency, `AITM.INJECT` in a dependency |

Full per-atom baselines with escalation and de-escalation factors are in `../indicators/{CATEGORY}.md`.

## MCD Severity Modifiers

Two ontology categories act as severity multipliers through the MCD lens:

### XFRM (Data & Code Transformation) as Multiplier

Through the MCD lens, transformation applied to other behaviors amplifies their severity. The interpretive claim: **code that transforms its own operations to resist analysis has something worth hiding.**

- `XFRM.ENCODE` wrapping `NETW.HTTP` targets → elevates the network finding
- `XFRM.STRCON` assembling `EXEC.SHELL` commands → elevates the execution finding
- `XFRM.ENCRYPT` protecting embedded `ARTF.CREDENTIAL` → elevates the artifact finding
- Multi-layer transformation (`XFRM.*` → decode → `XFRM.*`) → compounds the elevation

**De-escalation:** Transformation that is standard for the context (minification in frontend code, compression in archive utilities, encoding in data serialization) does not act as a multiplier. The multiplier applies when transformation is **unexpected given the code's stated purpose**.

### ENVI (Environment Interaction) as Multiplier

Through the MCD lens, environment checks that gate behavior amplify the severity of the gated behavior. The interpretive claim: **code that activates only in specific environments is selecting its target.**

- `ENVI.ENVCHECK` gating `NETW.HTTP` → elevates the network finding (activates only when target conditions met)
- `ENVI.SANDBOX` gating any payload → elevates all gated findings (avoids analysis environments)
- `ENVI.DEBUG` + early exit → elevates all subsequent behavior (evades debugging)

**De-escalation:** Environment checks for legitimate feature toggling (`NODE_ENV`, `DEBUG`), platform compatibility (`process.platform`), or graceful degradation do not act as multipliers. The multiplier applies when the check **selects for conditions favorable to attack or unfavorable to analysis**.

### Modifier Interaction

When both XFRM and ENVI modify the same finding, the compound effect is greater than either alone but less than their product. A finding that is both environment-gated AND transformation-obscured is among the highest-severity signals in MCD, but the algebra applies diminishing returns to prevent over-weighting.

## MCD Combination Effects

Multiple atoms from **different** categories in the same reachable scope are more suspicious than multiple atoms from the same category. MCD-specific combination guidance:

| Combination | MCD Interpretation |
|---|---|
| `CRED.*` + `NETW.*` | Credential access paired with network capability, core credential theft signal |
| `FSYS.READ` + `NETW.*` (non-CRED paths) | Data collection paired with exfiltration channel |
| `PKGM.INSTALL` + any non-build behavior | Install-time side effect, supply chain entry point |
| `EXEC.*` + `NETW.LISTEN` | Command execution paired with inbound connectivity, backdoor signal |
| `SYSI.*` (multiple) + `NETW.*` | System profiling paired with exfiltration, reconnaissance signal |
| `CRPT.SYMENC` + `FSYS.WRITE` + `FSYS.ENUM` | Encryption of enumerated files, ransomware signal |

Full combination tables with MCD-specific interpretation are in each category's indicator file.

## Contextual Signal Integration

The MCD lens defines six categories of contextual signals that modify confidence (not severity). These are documented in `../signals/`:

| Signal Category | Confidence Effect | Reference |
|---|---|---|
| [Package Metadata](../signals/package-metadata.md) | Amplifies or attenuates based on package provenance | New packages, maintainer changes, download anomalies |
| [Dependency Graph](../signals/dependency-graph.md) | Amplifies based on structural anomalies | New deps in patch releases, unpopular transitive deps |
| [Source-to-Binary Drift](../signals/source-to-binary-drift.md) | Strong amplifier when drift detected | Behavioral drift, irreproducible builds, disabled mitigations |
| [Temporal Signals](../signals/temporal-signals.md) | Amplifies based on timing correlations | Abandonment + activity, coordinated publication |
| [Execution Context](../signals/execution-context.md) | Multiplies blast radius assessment | CI/CD targeting, security tool context, privileged orchestration |
| [Network Destination](../signals/network-destination.md) | Amplifies based on destination reputation | Bulletproof hosting, recent domains, dynamic DNS |

**Key principle:** Contextual signals modify **confidence** (how certain we are the interpretation is correct), not **severity** (how bad it would be if true). A finding's severity is determined by the atoms and their combinations. Whether we believe the finding is accurate is influenced by contextual signals.

## MCD Confidence Thresholds

MCD confidence levels drive response tier selection (see [response framework](../response/)):

| Severity | Low Confidence | Medium Confidence | High Confidence |
|---|---|---|---|
| Informational | Tier 0 (close) | Tier 0 (close) | Tier 0 (close) |
| Low | Tier 0-1 | Tier 1 | Tier 1 |
| Medium | Tier 1 | Tier 1-3 | Tier 3 |
| High | Tier 3-4 | Tier 3-4 | Tier 4-5 |
| Critical | Tier 4-5 | Tier 4-5 | Tier 5 |

These are starting points. Practitioner judgment determines the final tier. Proximity to harm can elevate the response tier even at lower confidence.

## MCD Disproof Criteria

For each MCD composition, specific observations or enrichment can substantially weaken the malicious interpretation:

**General disproof signals:**
- Behavior is documented in the package's stated API contract
- Behavior is present in the package's test suite with clear legitimate purpose
- Behavior has existed unchanged across many versions with consistent maintainership
- Behavior matches a well-known open-source pattern (e.g., standard credential helper, documented build tool)
- The package is the canonical/official implementation of the functionality (e.g., `aws-sdk` accessing cloud credentials)

**General anti-disproof signals** (resist de-escalation):
- Behavior was introduced in a patch release or by a new maintainer
- Behavior is obfuscated or structurally concealed
- Behavior activates only in specific environments (CI/CD, specific hostnames)
- Multiple independent suspicious behaviors share reachability (composition, not coincidence)
- Package metadata shows signs of campaign coordination (recent registration, typosquatting name, etc.)

Per-composition disproof criteria are in each [composition file](../compositions/).
