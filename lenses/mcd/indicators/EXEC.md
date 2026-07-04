# MCD Lens: EXEC (Code Execution) Indicators

> **Core MCD position:** Code execution is the terminal capability: it is where intent becomes action. Malware that can execute arbitrary commands has effectively unlimited capability on the host. In library and package code, direct shell execution is almost always suspicious.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `EXEC.SHELL` | High | Shell command execution in dependency/library code is a strong finding |
| `EXEC.PROC` | Context-dependent | Varies by what is launched, from where, and whether orphaned |
| `EXEC.PROC` (orphaned) | High | Process detached from parent survives beyond installation/execution context |
| `EXEC.SYSCALL` | Medium-High | Direct syscalls in managed-language code bypass standard instrumentation |
| `EXEC.INJECT` | Very High | Cross-process memory writes have essentially no benign application in packages |

## Escalation Factors

- **Execution occurs at install time or build time.** `EXEC.SHELL` or `EXEC.PROC` in a `postinstall` hook, `setup.py`, or build-phase script runs on the developer's machine during routine dependency install, primary supply chain attack vector.
- **The command or target is constructed rather than literal.** If the string passed to the shell or the binary path is assembled from fragments, decoded values, or network-sourced data (`XFRM.STRCON` → `EXEC.*`), the command was deliberately hidden from static analysis.
- **The spawned process is orphaned or detached.** `nohup`, `setsid`, double-fork, `start /b`, `DETACHED_PROCESS`: the child survives the parent. Legitimate library code does not spawn processes intended to outlive the calling context.
- **The execution target is in a temporary or user-writable directory.** Executing from `/tmp`, `%TEMP%`, `~/.local`, or other writable paths not part of the package distribution suggests a staged payload.
- **Execution follows a network fetch or file write.** `NETW.*` → `FSYS.WRITE` → `EXEC.PROC`/`EXEC.SHELL` is the complete dropper sequence. Each transition escalates; the full chain is very high.
- **The command or binary is not consistent with the package's stated purpose.** A JSON parser calling `curl`, a font renderer invoking `powershell`, a test utility writing cron entries.
- **Execution uses elevated privilege mechanisms.** `sudo`, `runas`, SetUID, capability-setting APIs alongside execution primitives indicate privilege-aware payload delivery.
- **`EXEC.INJECT` in any non-debug context.** Writing executable content to another process's memory has no legitimate application in a library or package.
- **The execution primitive is reached through a dynamic loading chain.** `XFRM.*` → `LOAD.EVAL` → `EXEC.SHELL` is a textbook multi-stage delivery chain.

## De-escalation Factors

- **The package is a build tool, task runner, or test framework with documented shell execution.** Linters, bundlers, compiler wrappers, and test harnesses legitimately invoke subprocesses. Verify execution is consistent with documented behavior and does not orphan processes.
- **The subprocess target is a fixed, well-known binary with static arguments.** Spawning `/usr/bin/gcc` or `git` with visible, static arguments is less concerning than dynamic paths or externally-sourced arguments.
- **Execution is gated by explicit user configuration.** Shell execution only triggered when the user supplies configuration or explicitly invokes a command-mode is meaningfully different from automatic execution on import/install.
- **Execution pattern is present in prior versions and the source is auditable.** Consistent historical presence with known maintainer authorship lowers baseline, but does not eliminate concern. Compromised packages frequently add malicious execution alongside legitimate execution flows.

> **Caveat:** Benign-seeming execution is a common camouflage strategy. Malicious execution is frequently added alongside or embedded within legitimate execution flows. De-escalation of a known-good pattern does not grant a pass to adjacent code from new contributors or version bumps.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `EXEC.SHELL` + `PKGM.INSTALL` | Shell command during package installation, canonical supply chain primitive | Very High |
| `EXEC.PROC` + `PRST.*` | Process launch activating persistent malware | Very High |
| `XFRM.STRCON` + `EXEC.SHELL` | Command constructed from fragments to hide from static analysis (absorbs former EXEC.CMDCON) | Very High |
| `NETW.*` + `FSYS.WRITE` + `EXEC.PROC` | Download → write → execute: complete dropper sequence | Very High |
| `EXEC.PROC` + `EVSN.*` | Environment-aware process spawning, targeted or evasive payload | High |
| `EXEC.PROC` (orphaned) + `PKGM.INSTALL` | Install-time orphaned process, lightweight persistence without elevated privileges | High |
| `EXEC.SHELL` + `CRED.*` | Shell execution in credential access context, exfiltration or lateral movement | High |
| `EXEC.INJECT` + `SYSI.PROCMEM` | Full cross-process read+write capability, surveillance or injection with feedback | Very High |
| `XFRM.STRCON` + `NETW.*` → `EXEC.*` | Command constructed from network-sourced data, remote code execution | Very High |
| `LOAD.MEMCHAIN` + `EXEC.SHELL` | In-memory decode chain terminating in shell execution, staged delivery | Very High |

## MCD-Specific Disambiguation

### EXEC.SHELL vs EXEC.PROC severity
Through the MCD lens, `EXEC.SHELL` is inherently higher severity than `EXEC.PROC` because shell invocation adds string interpretation: the command can be constructed, injected, expanded, and piped. `EXEC.PROC` with a dynamically-determined binary path or externally-sourced arguments approaches `EXEC.SHELL` in MCD severity.

### EXEC.CMDCON absorption
The former taxonomy subtype `EXEC.CMDCON` (command construction) is decomposed in Parallax as `XFRM.STRCON` (the construction behavior) + `EXEC.SHELL`/`EXEC.PROC` (the execution behavior). The MCD lens captures the interpretive significance: `XFRM.STRCON` → `EXEC.*` is a Very High severity combination because the construction exists specifically to conceal the command.

### EXEC.INJECT: context-independent severity
Unlike most atoms, `EXEC.INJECT` has almost no de-escalation path through the MCD lens. Writing to another process's memory is relevant to debugging tools and game modding, but those are explicit, documented use cases in their own software categories. In a library, package, or dependency, `EXEC.INJECT` is Very High severity without qualification.
