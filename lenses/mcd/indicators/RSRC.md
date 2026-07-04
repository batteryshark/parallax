# MCD Lens: RSRC (Resource Consumption) Indicators

> **Core MCD position:** Resource consumption findings require determining who benefits from the computation. If the result is returned to the calling application, usage is likely legitimate. If transmitted to an external endpoint, it's malicious regardless of resource type. The combination of compute consumption + cryptocurrency addresses + network communication is the canonical cryptojacking signature. Resource abuse is the most commercially motivated malware category: attackers monetize stolen compute, bandwidth, and storage directly.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `RSRC.CPU` | Medium | Context-dependent, legitimate compute-heavy libraries exist; escalates sharply with external output or crypto artifacts |
| `RSRC.MEM` | Medium | Notable when unbounded or disproportionate to stated purpose; exhaustion patterns escalate |
| `RSRC.GPU` | High (non-ML/graphics) | GPU compute access in a package with no ML, graphics, or scientific computing role is a strong finding |
| `RSRC.DISK` | Medium | Notable for scale or inode exhaustion patterns; escalates in library/dependency context |
| `RSRC.FORK` | High | Unbounded process/thread creation has no legitimate application in library code |
| `RSRC.NET` | Medium-High | Network bandwidth consumption disproportionate to application function; relay/proxy patterns escalate |

## Escalation Factors

- **Cryptocurrency artifacts are present (`ARTF.CRYPTO_ADDR`).** Wallet addresses, mining pool hostnames, stratum protocol URLs, or coin-specific configuration alongside any RSRC atom is the canonical cryptojacking indicator. This single co-occurrence moves any RSRC finding to High or Very High.
- **GPU compute in a non-ML/graphics library.** `RSRC.GPU` in a package whose stated purpose has nothing to do with machine learning, graphics rendering, video processing, or scientific computing. GPU access requires deliberate implementation. Its presence is never accidental.
- **Resource consumption is conditioned on environment checks (`ENVI`).** Resource-intensive code that activates based on environment detection (CI vs production, cloud provider, container presence, CPU count thresholds) suggests targeted or evasive resource abuse.
- **Resource consumption is unbounded or dynamically scaled to the system maximum.** Code that queries available cores (`SYSI.HW`) and spawns workers to match, or queries available RAM and allocates proportionally, maximizes resource extraction from the host.
- **Resource activity routes through external C2 or telemetry.** Computation results, bandwidth relay traffic, or resource utilization metrics sent to an external endpoint indicate the resource consumer serves an external beneficiary.
- **`RSRC.FORK` in any library or dependency context.** Unbounded process/thread creation in a library has no legitimate use case. Even bounded but high-count process creation in a library is suspect. Libraries should not manage system-level resources at scale.
- **Resource consumption present only in post-install hooks or hidden execution paths.** Resource abuse hidden in lifecycle scripts, import-time execution, or code paths not reachable from the documented API is a supply chain pattern.
- **Resource activity absent from source repository but present in published artifact.** Build-time injection of resource-consuming code that does not appear in the auditable source: the published package differs from the reviewed source.

## De-escalation Factors

- **Documented, bounded, user-controlled resource limits.** The resource consumption has explicit, enforced upper bounds that the user configures. Pool sizes, iteration counts, memory caps, and timeout values are visible and adjustable.
- **Resource use is load-bearing for the package's stated purpose.** A video transcoder consuming CPU, a database engine consuming disk, a physics simulator consuming GPU: the resource consumption is the product, not a side effect.
- **Transparent, metered, opt-in resource usage.** The package documents its resource requirements, provides metering/monitoring interfaces, and resource-intensive operations require explicit user invocation rather than running automatically.
- **Resource consumption is proportional to user-supplied input.** Computation scales with the data the user provides, not with the hardware available on the host. Input-proportional scaling is structurally different from hardware-maximizing scaling.

> **Caveat:** Legitimate resource consumption is common in compute-heavy libraries. De-escalation based on the resource type alone is never sufficient: who benefits from the resource consumption, whether the output stays local, and whether the consumption matches the stated purpose are the determining factors.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `RSRC.CPU` + `ARTF.CRYPTO_ADDR` | CPU-based cryptocurrency mining, canonical cryptojacking | Very High |
| `RSRC.GPU` + `ARTF.CRYPTO_ADDR` | GPU-accelerated cryptocurrency mining, high-value cryptojacking | Very High |
| `RSRC.CPU` + `NETW.*` | Compute results transmitted externally, resource theft with exfiltration | High |
| `RSRC.NET` + `NETW.LISTEN` | Bandwidth consumption with listening, DDoS participation or botnet relay | High |
| `RSRC.FORK` + `TIME.DELAY` | Timed fork bomb, delayed denial of service, potentially evasion of install-time monitoring | Very High |
| `RSRC.CPU` + `LOAD.EVAL` | Runtime-loaded CPU-intensive computation, dynamically delivered mining payload | Very High |
| `RSRC.GPU` + `ENVI.ENVCHECK` | Environment-gated GPU access, selective activation based on host characteristics | High |
| `RSRC.CPU` + `SYSI.HW` + `NETW.*` | Hardware-aware compute scaling with external output, optimized resource theft | Very High |
| `RSRC.FORK` + `EXEC.SHELL` | Shell-based fork bomb, classic denial of service primitive | Very High |
| `RSRC.DISK` + `FSYS.ARCHIVE` | Archive extraction consuming disproportionate disk, decompression bomb / zip bomb | High |
| `RSRC.NET` + `NETW.SOCKET` + `NETW.DNS` | Raw socket traffic with DNS, potential DNS amplification attack participation | High |
| `RSRC.MEM` + `LOAD.DESER` | Unbounded memory allocation from deserialized data, deserialization-driven exhaustion | Medium-High |

## MCD-Specific Disambiguation

### RSRC.CPU vs legitimate computational libraries
Through the MCD lens, `RSRC.CPU` in a compression library, cryptographic library, or scientific computing package is expected. The escalation trigger is not CPU consumption itself but the combination of CPU consumption with indicators that the computation serves an external beneficiary: network exfiltration of results, cryptocurrency artifacts, hardware-maximizing scaling, or environment-gated activation. A numpy matrix multiplication is `RSRC.CPU` at the atom level but carries no MCD signal without additional context.

### RSRC.GPU vs legitimate ML/graphics
Through the MCD lens, `RSRC.GPU` has a higher baseline severity than `RSRC.CPU` because GPU compute access requires deliberate implementation and specific API usage: it cannot appear accidentally. In packages with a declared ML, graphics, or scientific computing purpose, `RSRC.GPU` is expected. In all other package categories, GPU compute access is a strong standalone finding that warrants immediate investigation of what computation is being dispatched and where the output goes.

### RSRC.NET vs normal network activity
Through the MCD lens, `RSRC.NET` is distinct from `NETW.*` atoms. A package making API calls exhibits `NETW.HTTP`, normal network communication. `RSRC.NET` applies when the network traffic volume is disproportionate to the application's needs, the traffic serves no function for the calling application (relay/proxy), or the traffic pattern matches known attack signatures (amplification, flooding). The test is whether the bandwidth consumption benefits the application's user or an external party.
