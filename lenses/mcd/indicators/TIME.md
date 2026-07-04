# MCD Lens: TIME (Temporal Operations) Indicators

> **Core MCD position:** Time-based logic is the foundation of logic bombs: code that activates only after a specific date, during specific hours, or after a delay designed to outlast analysis windows. `TIME.CMP` against a hardcoded date is the canonical logic bomb pattern. In dependency code, hardcoded temporal activation conditions have extremely limited benign justification. Trial expirations and deprecation cutoffs exist but are rare and typically accompanied by corresponding user-facing UX.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `TIME.GET` | Low | Ubiquitous: logging, metrics, session management, and caching all retrieve time |
| `TIME.CMP` (configurable threshold) | Medium | Comparison against a configurable or retrieved threshold, such as a feature toggle or trial expiration |
| `TIME.CMP` (hardcoded date) | High | Comparison against a hardcoded date literal or epoch constant: the canonical logic bomb signature |
| `TIME.DELAY` (short/proportional) | Low | Short delays proportional to operational context, such as retry backoff or rate limiting |
| `TIME.DELAY` (long/disproportionate) | Medium | Long delays disproportionate to operational context: potential sandbox evasion |
| `TIME.SCHED` | Low-Medium | In-process scheduled execution, standard in event-driven architectures; severity depends on what is scheduled |

## Escalation Factors

- **Hardcoded activation date (`ARTF.TIMESTAMP`).** A date literal or epoch constant embedded directly in the comparison is the strongest single indicator of a logic bomb. The timestamp is a forensic artifact. It encodes the attacker's intended activation timeline.
- **Delay duration calibrated to sandbox analysis windows.** Delays of 3-7 minutes in install hooks or initialization paths are calibrated to outlast automated analysis environments (typically 2-5 minute execution windows). Busy-wait implementations that achieve the same delay without calling sleep APIs indicate awareness of sleep-based sandbox detection.
- **Time check precedes sensitive operations.** `TIME.CMP` gating `EXEC.*`, `NETW.*` (outbound), `CRED.*`, or `FSYS.WRITE` to sensitive paths means the time condition controls when a payload activates. The gated behavior determines the actual severity.
- **Time logic is obfuscated or decomposed.** Timestamp values split across variables, encoded as byte arrays, computed through arithmetic, or retrieved from seemingly unrelated data structures indicate deliberate concealment of the activation condition. `XFRM.*` applied to temporal logic is a strong escalation.
- **Multiple independent time checks converging.** Two or more distinct temporal conditions that must all pass before execution (date range AND time-of-day window AND day-of-week) indicate targeted activation with narrow operational windows.
- **Time check absent from documentation.** Temporal gating not mentioned in README, changelog, or API documentation suggests the time-dependent behavior was not intended to be discovered by users or reviewers.
- **Time comparison appears in a dependency or transitive dependency.** Logic bombs in direct application code may be insider threats; in dependency code, they are supply chain attacks. Dependencies have less scrutiny and wider blast radius.
- **Delay positioned at install time or import time.** `TIME.DELAY` in `postinstall`, `setup.py`, `__init__.py`, or module-level code runs before the consumer has any opportunity to evaluate the dependency's behavior.
- **Scheduled execution targets a sensitive callback.** `TIME.SCHED` scheduling `EXEC.*`, `NETW.*`, or `CRED.*` operations, particularly with long delays or at specific times, is a deferred payload delivery mechanism.

## De-escalation Factors

- **Time used for logging or metrics only.** `TIME.GET` whose value flows exclusively into log messages, metric labels, or telemetry timestamps with no conditional branching. Verify through data-flow analysis that no comparison exists downstream.
- **Delay is user-configurable with documented operational justification.** Retry backoff with configurable base delay, polling interval from configuration, rate limiting with documented policy. The delay duration must be externally controllable with reasonable defaults.
- **Scheduled execution is documented product feature.** `setInterval` for documented health checks, `setTimeout` for documented deferred initialization, `threading.Timer` for documented periodic tasks. Feature must appear in public documentation predating the suspicious commit.
- **Comparison target is deprecation or trial cutoff with corresponding user-facing UX.** A hardcoded date that triggers a deprecation warning, feature limitation message, or trial expiration dialog visible to the user, not a silent behavioral change. The UX must be proportional and discoverable.
- **Time comparison is part of cache TTL or session expiration.** Standard cache invalidation and session timeout patterns using time comparison. The comparison target must be a relative duration, not an absolute date.

> **Caveat:** Logic bombs are designed to be invisible until activation. De-escalation of time-based logic in dependencies requires high confidence that the temporal condition and its gated behavior are fully understood. A plausible explanation (trial expiration, deprecation) must be independently verifiable, not just inferable from code comments.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `TIME.CMP` + `ARTF.TIMESTAMP` | Hardcoded activation date: canonical logic bomb pattern | Very High |
| `TIME.DELAY` + `EXEC.*` | Delay then execute: sandbox evasion preceding payload delivery | High |
| `TIME.CMP` + `NETW.*` | Time-gated network communication: beacon activation or scheduled exfiltration | High |
| `TIME.SCHED` + `PRST.*` | In-process scheduling combined with persistence: deferred persistent payload | High |
| `TIME.CMP` + `XFRM.*` | Concealed activation logic: obfuscated time check gates behavior | Very High |
| `TIME.DELAY` + `TIME.CMP` | Layered temporal evasion: delay outlasts sandbox, then date check gates payload | Very High |
| `TIME.GET` + `NETW.*` | Timestamped network communication: exfiltration with temporal metadata or time-synced beaconing | Medium |
| `TIME.CMP` + `EXEC.SHELL` + `PKGM.INSTALL` | Install-time logic bomb: time-gated shell execution during package installation | Critical |
| `TIME.DELAY` + `ENVI.TIMING` | Delay with environment-aware calibration: dual-purpose timing for evasion and sandbox detection | High |
| `TIME.SCHED` + `NETW.*` | Scheduled periodic network communication: heartbeat, beacon, or periodic exfiltration | Medium-High |
| `TIME.CMP` + `CRED.*` | Time-gated credential access: logic bomb targeting credential theft | Very High |
| `TIME.CMP` + `ENVI.ENVCHECK` | Temporal and environmental gates combined: narrow activation window on specific targets | Critical |

## MCD-Specific Disambiguation

### TIME.SCHED vs PRST.SCHED: The Survivability Test
Through the MCD lens, the critical distinction is survivability. `TIME.SCHED` dies with the process: a `setTimeout` or `threading.Timer` is bounded by the process lifetime. `PRST.SCHED` (cron, Task Scheduler, launchd) survives process termination and system reboots. In MCD terms, `PRST.SCHED` is a persistence mechanism; `TIME.SCHED` is an execution-timing mechanism. When both co-occur (`TIME.SCHED` triggers behavior that installs `PRST.SCHED`), the in-process scheduling is the delivery mechanism for the persistence payload.

### TIME.GET vs TIME.CMP: Promotion Through Data Flow
Through the MCD lens, `TIME.GET` alone is nearly zero signal; it is too ubiquitous to be meaningful in isolation. The finding becomes significant when data-flow analysis reveals the retrieved value flows into a comparison (`TIME.CMP`). Analysts should treat isolated `TIME.GET` findings as candidates for promotion: trace the retrieved value forward to determine whether a comparison exists downstream. Unpromoted `TIME.GET` findings can typically be suppressed without loss of coverage.

### TIME.DELAY as Obfuscated TIME.CMP
Through the MCD lens, certain delay patterns function as implicit time comparisons. A 5-minute delay in an install hook is functionally equivalent to "if more than 5 minutes have elapsed since installation started": it gates behavior on a temporal condition without an explicit comparison operation. When assessing `TIME.DELAY`, consider whether the delay is mechanically functioning as a time gate rather than a true operational pause. The distinction matters for pattern matching: a logic bomb that uses delay instead of date comparison evades date-focused detection rules.
