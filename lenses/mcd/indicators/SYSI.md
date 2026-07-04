# MCD Lens: SYSI (System Inspection) Indicators

> **Core MCD position:** System inspection is the intelligence-gathering phase that precedes targeted action. Individual queries are low severity; knowing the OS or username is structurally unremarkable. Aggregated collection constituting a system profile, especially when combined with network exfiltration, is the signature of supply chain implant reconnaissance. The pattern is: collect broadly, transmit quietly, act on the collected intelligence in a later stage.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `SYSI.OS` | Low | Ubiquitous in cross-platform code; severity from context, not the query itself |
| `SYSI.USER` | Low-Medium | Current user query is common; full account enumeration is higher |
| `SYSI.NET` | Medium | Network configuration exposure; port scanning elevates significantly |
| `SYSI.PROC` | Medium | Process listing is common in monitoring; process name checklists are higher |
| `SYSI.SW` | Low-Medium | Software inventory queries; cross-ecosystem enumeration is higher |
| `SYSI.HW` | Medium | Hardware fingerprinting; composite fingerprint generation is higher |
| `SYSI.PROCMEM` | High-Critical | Cross-process memory reading has very limited legitimate use in dependency code |

All SYSI atoms escalate when combined with `NETW.*`. The transition from local inspection to remote transmission is the critical boundary.

## Escalation Factors

- **Collected results transmitted over the network.** Any `SYSI.*` + `NETW.*` combination crosses the local-to-remote boundary. System information collected and kept local is diagnostics. System information collected and transmitted is reconnaissance. The transmission target (known telemetry endpoint vs. unrecognized domain vs. IP literal vs. webhook) further modulates severity.
- **Results feed an activation decision (ENVI overlap).** When SYSI output flows into conditional logic that gates subsequent behavior (process list checked against security tool names, OS version selecting a payload variant), `ENVI.*` atoms also apply. The system inspection becomes operational intelligence.
- **`SYSI.PROC` targets security tools by name.** A hardcoded list of process names matching known AV, EDR, or sandbox agent processes transforms generic process listing into security tool detection. The specificity of the list (generic monitoring terms vs. exact product executable names) indicates sophistication.
- **`SYSI.HW` collects VM detection primitives.** When hardware queries target CPUID hypervisor bit, MAC OUI prefixes for VMware/VirtualBox/Hyper-V, DMI strings containing virtualization keywords, or low core/RAM thresholds, the hardware inspection serves sandbox detection. `ENVI.SANDBOX` co-applies.
- **Cross-platform enumeration.** Code that collects OS info, network config, and hardware IDs with platform-specific branches for Windows, Linux, and macOS is building a universal profiler. The cross-platform investment indicates systematic design, not incidental diagnostics.
- **Breadth constitutes a full system profile.** Multiple SYSI subtypes present in the same package (OS + user + network + processes + software + hardware) produce a comprehensive machine profile. The aggregation itself is the escalation factor, even before considering transmission.
- **Collection executes at install or import time.** `postinstall`, `setup.py`, `__init__.py`, and equivalents run at package installation or first import. System inspection at install time has no user-initiated context. The package is profiling the system before the developer has called any of its functions.
- **Code performing the collection is obfuscated or encoded.** `SYSI.*` + `XFRM.*`: system inspection hidden behind encoding, encryption, or control flow obfuscation indicates deliberate concealment. Legitimate diagnostic code has no reason to obscure its collection logic.
- **`SYSI.PROCMEM` targets any process.** Cross-process memory reading in dependency code is inherently high severity. When the target is a credential-holding process (browser, `lsass.exe`, ssh-agent), severity is critical.
- **`SYSI.USER` enumerates all system accounts.** Querying the current username is routine. Enumerating all user accounts via `net user`, `/etc/passwd` parsing, or LDAP queries indicates reconnaissance beyond the current execution context.
- **`SYSI.NET` performs active scanning.** Port scanning or host sweeping crosses from passive configuration inspection to active network reconnaissance.

## De-escalation Factors

- **Declared diagnostic purpose with documented scope.** The package's stated purpose explicitly involves system information collection (diagnostic tool, system monitor, hardware inventory). Documentation must predate the suspicious commit and be independently confirmable.
- **Collection gated behind explicit opt-in.** System information is collected only when the developer explicitly calls a diagnostic function, not on import, not on install, not in module initialization. The opt-in must be genuine (function call with clear name), not implicit (auto-executing on import).
- **Results used only locally and transiently.** Collected system data feeds local decisions (platform-specific path selection, resource allocation) and is not stored, serialized, or transmitted. Trace the data flow to confirm no network egress path exists.
- **Package category creates plausible expectation.** Build tools query OS and architecture. Network utilities query interfaces. Process managers list processes. The system inspection must align with the package's functional category. A date formatting library querying network interfaces has no category alignment.
- **Well-established package with transparent history.** System inspection logic has been present in the package since early versions, is consistent with the package's purpose, and has not been introduced or expanded in a suspicious maintenance update.

> **Caveat:** System inspection behaviors are individually mundane. The MCD signal comes from aggregation, timing, and data flow, not from any single query. De-escalation based on "this is just a platform check" must account for the full collection pattern across the package, not just the individual atom in isolation.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `SYSI.*` + `NETW.*` | System profile exfiltration, collected data transmitted to external endpoint | High-Critical |
| `SYSI.PROC` + `ENVI.*` | Process list feeding activation decision, security tool detection or victim profiling | High |
| `SYSI.HW` + `ENVI.SANDBOX` | Hardware queries serving as VM/sandbox detection primitives | High |
| Multiple `SYSI.*` subtypes | Aggregated system profiling, breadth indicates systematic reconnaissance | Medium-High |
| `SYSI.PROCMEM` + `CRED.*` | Process memory reading targeting credential-holding processes, the Trivy/lsass pattern | Critical |
| `SYSI.SW` + `NETW.*` | Software inventory exfiltration, mapping installed tooling for targeting | High |
| `SYSI.NET` + `NETW.SOCKET` | Network configuration enumeration + active connections, lateral movement preparation | High |
| `SYSI.USER` + `ENVI.ENVCHECK` | User identity query feeding targeted activation, named-user attack | High-Critical |
| `SYSI.*` + `XFRM.*` | System inspection concealed behind obfuscation/encoding, hidden reconnaissance | High |
| `SYSI.PROC` + `ENVI.SECDISABLE` | Process enumeration of security tools followed by disabling them | Critical |
| `SYSI.OS` + `EXEC.SHELL` | OS identification followed by platform-specific payload delivery | High |
| `SYSI.*` + `CRED.*` + `NETW.*` | Full chain: profile system, harvest credentials, exfiltrate, canonical supply chain implant | Critical |

## MCD-Specific Disambiguation

### SYSI vs. Normal Runtime Environment Detection
Through the MCD lens, the challenge is distinguishing legitimate platform adaptation from adversarial reconnaissance. The mechanical behavior is identical: both call `os.platform()`. The MCD signal comes from: what happens to the data (local use vs. transmission), when it executes (user-invoked function vs. install/import time), how much is collected (single query vs. comprehensive profile), and whether the collection aligns with the package's purpose. No single factor is dispositive; the combination pattern drives the assessment.

### SYSI.PROC vs. ENVI: Process List as Activation Gate
Through the MCD lens, `SYSI.PROC` becomes `SYSI.PROC` + `ENVI.*` when the process list feeds a behavioral decision. The canonical malware pattern is: enumerate processes, check against a list of security tool names, suppress malicious behavior if monitoring is detected. The process enumeration (`SYSI.PROC`) is the collection mechanism; the name-matching and branching (`ENVI.SANDBOX` / `ENVI.DEBUG`) is the activation logic. Both atoms are required to describe the complete behavior.

### SYSI.HW vs. ENVI.SANDBOX: Hardware as VM Detection
Through the MCD lens, hardware queries become sandbox detection when they target specific virtualization indicators: CPUID hypervisor present bit, MAC OUI prefixes for virtual NICs (00:0C:29, 00:50:56 for VMware; 08:00:27 for VirtualBox), DMI strings containing "Virtual Machine" or "QEMU", or resource thresholds (< 2 cores, < 2GB RAM) used as VM heuristics. The hardware query is `SYSI.HW`; the VM-detection interpretation is `ENVI.SANDBOX`. Both apply simultaneously.

### SYSI.PROCMEM vs. EXEC.INJECT: Read vs. Write Directionality
Through the MCD lens, both are high-severity cross-process operations, but they serve different attack phases. `SYSI.PROCMEM` (reading) is intelligence gathering: extracting credentials, secrets, or runtime state from a target process. `EXEC.INJECT` (writing) is payload delivery: modifying a target process's behavior. When both appear together, it typically represents a read-then-write attack sequence: read to locate injection targets, write to inject.
