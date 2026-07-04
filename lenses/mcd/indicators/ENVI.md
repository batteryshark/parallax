# MCD Lens: ENVI (Environment Interaction) Indicators

> **Core MCD position:** If obfuscation hides *what* code does, environment interaction controls *when and where* it does it. In dependency code, environment detection, forensic artifact manipulation, runtime masquerading, and security control modification have extremely limited benign justification. These behaviors are the operational infrastructure of supply chain attacks: the mechanisms that ensure the payload fires on the right targets, survives analysis, and evades detection.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `ENVI.DEBUG` | High | Debugger detection in library/dependency code has no legitimate purpose |
| `ENVI.SANDBOX` | High | VM/sandbox detection in library/dependency code has no legitimate purpose |
| `ENVI.ENVCHECK` | Medium-High | Environment fingerprinting, severity depends on what the check gates |
| `ENVI.TIMING` | Medium | Execution timing, requires context on duration, placement, proportionality |
| `ENVI.LOG` | Medium-High | Audit/log suppression, severity depends on specificity of target |
| `ENVI.TAMPER` | Medium | Self-integrity checks, legitimate in DRM/anti-cheat, suspicious in dependencies |
| `ENVI.FORENSIC` | High | Forensic artifact manipulation has no legitimate purpose in dependency code |
| `ENVI.MASQ` | High | Runtime artifact disguise has no legitimate purpose in dependency code |
| `ENVI.SECDISABLE` | High-Critical | Security control modification, in dependency context, any security control manipulation is critical |

## Escalation Factors

- **Environment interaction gates a payload delivery or exfiltration action.** Any ENVI behavior preceding `EXEC.*`, `NETW.*` (outbound), or persistence operations raises severity to critical. Environment interaction alone is suspicious; gating a destructive or theft-oriented payload confirms adversarial intent.
- **`ENVI.ENVCHECK` targets specific hosts, usernames, or domain membership.** Named targets indicate a targeted attack. Payload activates only on matching hosts, which also means it won't fire in generic sandbox analysis. That is by design.
- **`ENVI.ENVCHECK` is subtractive (suppresses on detection).** Checking `CI=true` to SUPPRESS behavior means the payload fires everywhere EXCEPT analysis environments. This is the dominant supply chain pattern.
- **`ENVI.FORENSIC` replaces evidence rather than deleting it.** Substituting plausible clean content for malicious artifacts is harder to detect than deletion: file-presence checks still pass.
- **Timestamp manipulation targets a specific past date.** A precise historical value suggests automation and coordination, not accidental corruption.
- **`ENVI.MASQ` uses legitimate OS binary names or paths.** The closer the masquerade is to a real signed system component, the higher the confidence.
- **Environment interaction appears in a library or dependency.** `ENVI.SANDBOX` and `ENVI.DEBUG` have no legitimate purpose in reusable libraries. In application code they are occasionally defensible (anti-cheat, licensing); in dependencies they are immediate high-severity indicators.
- **`ENVI.TIMING` delays calibrated near sandbox analysis windows.** Delays of 3-7 minutes in dependency startup or install hooks are calibrated to outlast automated analysis (typically under 5 minutes).
- **`ENVI.LOG` targets specific security tooling by name.** Explicitly disabling named EDR agents, AV processes, or audit daemons by process/service name indicates adversarial intent against a specific defensive stack.
- **Present in install-time hooks.** `postinstall`, `setup.py`, and equivalents execute at package installation with no sandboxing. Environment interaction in these hooks is particularly dangerous.
- **Multiple ENVI subtypes present simultaneously.** A single environment check may be explained. `ENVI.ENVCHECK` + `ENVI.TIMING` + `ENVI.FORENSIC` together indicates coordinated, multi-layered operational infrastructure.
- **`ENVI.SECDISABLE` targets multiple independent controls.** Disabling the firewall AND adding AV exclusions AND weakening AppLocker is staged infrastructure preparation.
- **`ENVI.SECDISABLE` creates inbound firewall rules with unrestricted scope.** Any-program, any-IP rules are indistinguishable from deliberate backdoor enablement.
- **`ENVI.SECDISABLE` adds AV exclusions for paths where the same package writes files.** Exclusion-write overlap means the exclusion exists to protect a payload.

## De-escalation Factors

- **`ENVI.DEBUG` in application with documented anti-cheat or licensing.** Verify documentation predates the suspicious commit and is independently confirmable, not just a code comment.
- **`ENVI.ENVCHECK` checking CI variables to suppress noisy output or skip tests.** De-escalate only when the check gates UI behavior, not network calls, file writes, or subprocess execution.
- **`ENVI.TIMING` as rate limiter or retry backoff.** Delay must be proportional to stated purpose and not concentrated at startup or install time.
- **`ENVI.MASQ` as documented compatibility shim.** Only when destination path is documented in public changelogs and binary is signed or hash-verified.
- **`ENVI.LOG` suppressing verbose debug output in production.** Only when suppression is scoped to log level, not specific security tooling.
- **`ENVI.SECDISABLE` in documented system administration tool.** Package's primary purpose must be system/network administration, modification must be user-initiated, and scope must be bounded.

> **Caveat:** Environment interaction techniques are by definition designed to appear benign. De-escalation based on plausible explanation requires verification that the explanation is independently confirmable, predates the suspicious activity, and accounts for the specific implementation observed.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `ENVI.ENVCHECK` + `EXEC.SHELL` | Environment confirms victim profile; payload delivered only on matching hosts | Critical |
| `ENVI.TIMING` + `EXEC.SHELL` | Delay calibrated to outlast sandbox window, then execute | Critical |
| `ENVI.FORENSIC` + `ENVI.MASQ` | Evidence replaced with clean stubs; artifacts disguised as legitimate components | Critical |
| `ENVI.SANDBOX` + `ENVI.DEBUG` | Multi-layer analysis detection, coordinated refusal to execute under analysis | High |
| `XFRM.*` + `ENVI.ENVCHECK` | Transformed payload activated only when environment check passes | High |
| `ENVI.LOG` + persistence operations | Logging suppressed, persistence installed, silent implant with no audit trail | High |
| `ENVI.MASQ` + persistence operations | Persistence registered under name mimicking real OS component | High |
| `ENVI.FORENSIC` + `ENVI.TIMING` | Payload executes, waits, then wipes evidence, delayed cleanup | High |
| `ENVI.ENVCHECK` + `XFRM.*` + `EXEC.SHELL` | Environment gate + transformed payload + shell execution, canonical three-layer supply chain pattern | Critical |
| `ENVI.SECDISABLE` + `NETW.LISTEN` | Firewall opened then network listener established, backdoor enablement | Critical |
| `ENVI.SECDISABLE` + persistence operations | Security controls disabled then persistence installed, protected implant | Critical |
| `ENVI.SECDISABLE` + `FSYS.WRITE` | AV exclusion injected for path, then payload written there | Critical |
| `ENVI.SECDISABLE` + `EXEC.*` | Exploit mitigations disabled then code executed, payload runs without protection | High |
| `ENVI.SECDISABLE` + `CRPT.CERT` | Host security weakened and certificate trust manipulated, full MITM preparation | Critical |

## MCD-Specific Disambiguation

### XFRM vs. ENVI: The Core MCD Distinction
Through the MCD lens, these categories address different phases of attack execution. Transformation hides *what* the payload is. Environment interaction controls *when and where* it activates. An encoded payload is always present, merely concealed (XFRM). The same payload decoded and executed only after an environment check passes uses both: ENVI gates activation, XFRM conceals content. Both apply; neither subsumes the other.

### ENVI.ENVCHECK: Additive vs. Subtractive
Through the MCD lens, subtractive checks (suppress when condition matches) are the dominant supply chain pattern. The payload fires everywhere EXCEPT environments that look like analysis infrastructure. Additive checks (activate when condition matches) indicate targeted attacks: more sophisticated, less common. Both are high-severity through MCD, but the attacker's targeting model differs.

### ENVI.FORENSIC: The Evidence Replacement Pattern
Through the MCD lens, evidence replacement is significantly more dangerous than evidence deletion. Deletion leaves an absence that incident responders notice. Replacement leaves a plausible artifact that passes existence checks and casual inspection. The Axios compromise demonstrated this: malicious `package.json` was replaced with a pre-staged clean stub, so post-incident inspection showed a convincing forgery rather than evidence of compromise.
