# MCD Lens: PRST (Persistence Mechanisms) Indicators

> **Core MCD position:** Persistence is what separates a one-shot exploit from an installed backdoor. In dependency code, persistence mechanisms have almost no legitimate justification. A library or package that registers itself to survive beyond its own execution context (across reboots, logins, or process restarts) is establishing a foothold. The question is not whether persistence is suspicious in a dependency; it is whether there is any explanation other than compromise.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `PRST.STARTUP` | High | Startup/login item registration in dependency code has no standard justification |
| `PRST.SCHED` | High | Scheduled task creation in dependency code persists execution beyond the package lifecycle |
| `PRST.SERVICE` | High | Service registration in dependency code creates a continuously-running, self-healing foothold |
| `PRST.HOOK` | High | Execution hooks intercept operations outside the package's own scope |
| `PRST.EXTENSION` | High | Browser/application extension installation grants access to the host application's full capability set |
| `PRST.BOOTKIT` | Critical | Boot-level persistence executes before OS security mechanisms and survives OS reinstallation |

## Escalation Factors

- **Naming camouflage (`ENVI.MASQ` overlap).** The registered startup item, scheduled task, service, or hook binary uses a name that mimics a legitimate OS component or well-known application. This is deliberate evasion of manual inspection.
- **Cross-user or system-wide scope.** Persistence targeting system-level locations (`/etc/systemd/system/`, `HKLM\...\Run`, `/etc/ld.so.preload`, system `site-packages`) affects all users on the system, not just the installing user. Scope amplifies blast radius.
- **Registration occurs at install time or import time.** Persistence registered during `postinstall`, `setup.py`, or module `__init__.py` fires during routine dependency installation with no user awareness. This is the primary supply chain persistence vector.
- **Combined with exfiltration or C2 (`NETW.*`, `CRED.*`).** Persistence that maintains a network channel or periodically harvests credentials is operational malware infrastructure, not a misconfigured build tool.
- **Removal resistance or self-restoration.** The persistence mechanism monitors for its own removal and re-registers, uses multiple redundant mechanisms, or stores restoration material in locations that survive standard cleanup procedures.
- **Multiple redundant persistence mechanisms.** Registering both a startup item AND a scheduled task AND a service for the same payload indicates deliberate redundancy to survive partial remediation.
- **`PRST.HOOK` with broad-scope interceptors.** System-wide `LD_PRELOAD`, `.pth` files in system `site-packages`, or Git template hooks intercept operations across all processes, all Python invocations, or all Git operations respectively. The intercepted surface determines severity.
- **Persistence survives package removal.** If `pip uninstall` or `npm uninstall` does not remove the registered persistence artifact, the package has planted something outside its own managed file set.
- **Executed binary or command is not part of the package distribution.** The persistence entry points to a binary in `/tmp`, a downloaded file, or a path outside the package directory.
- **Persistence registration is conditional on environment.** Registration gated by `ENVI.ENVCHECK` (only persist on certain hosts) indicates targeted deployment.

## De-escalation Factors

- **Explicit opt-in API.** The package provides a documented CLI command or configuration option that the user must explicitly invoke to register the persistence mechanism. The persistence is not automatic on install or import.
- **Scoped to the package's own managed environment.** A development tool that creates a project-local Git hook in `.git/hooks/` (not template directory), a virtualenv-scoped `.pth` file, or a user-invoked service registration for the tool's own daemon.
- **Self-expiring artifacts.** The persistence mechanism includes an explicit expiration or self-removal mechanism that limits the duration of persistence.

> **Caveat:** Even with de-escalation, persistence in dependency code is inherently anomalous. De-escalation lowers severity; it does not normalize the behavior. The persistence mechanism still requires full investigation to confirm it matches the stated purpose.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `PRST.STARTUP` + `NETW.*` | Startup persistence maintaining network channel, installed backdoor | Very High |
| `PRST.HOOK` (`LD_PRELOAD`/`.pth`) + `CRED.*` | Execution hook intercepting authentication flow, credential interceptor | Very High |
| `PRST.SCHED` + `EXEC.SHELL` | Scheduled task periodically executing shell commands, polling backdoor | Very High |
| `PRST.STARTUP` + `XFRM.*` | Startup item with transformed/encoded payload, obfuscated persistence | Very High |
| `PRST.SERVICE` + `EXEC.PROC` | Registered service launching external binary, managed persistent agent | Very High |
| `PRST.EXTENSION` + `NETW.*` | Browser extension with network access, browsing surveillance or data exfil | Very High |
| `PRST.HOOK` (PATH shadow) + `CRED.*` | Command hijack capturing credentials passed to shadowed binary | Very High |
| `PRST.BOOTKIT` + any | Boot-level persistence combined with any other behavior, full system compromise | Critical |
| `PRST.*` + `ENVI.MASQ` | Any persistence mechanism disguised as legitimate OS component | Very High |
| `PRST.*` + `PKGM.INSTALL` | Persistence registered during package installation, supply chain persistence | Very High |
| Multiple `PRST.*` subtypes | Redundant persistence mechanisms, deliberate remediation resistance | Very High |

## MCD-Specific Disambiguation

### PRST.SCHED vs TIME.SCHED (future atom)
Through the MCD lens, the critical distinction is survivability. `PRST.SCHED` creates an OS-level scheduled task that survives process termination and reboots. It is a persistence mechanism. Process-internal timing (`setTimeout`, `setInterval`, `time.sleep` loops) dies when the process exits. It is a behavioral pattern within a running process, not persistence. The MCD severity difference is categorical: `PRST.SCHED` in a dependency is High baseline; process-internal timing is context-dependent.

### PRST.HOOK vs normal hook usage
Through the MCD lens, the distinction is scope. Git hooks in a project's own `.git/hooks/`, framework lifecycle callbacks, event emitter registrations, and middleware patterns are application-internal mechanisms operating within the package's own scope. `PRST.HOOK` intercepts execution OUTSIDE the package's scope, affecting other programs, other users, or system-wide behavior. A pre-commit hook in `.git/hooks/pre-commit` is a normal development pattern. The same hook installed via `~/.git-templates/hooks/` affects every future `git init` and `git clone` on the system.

### PRST vs EXEC.PROC (orphaning)
Through the MCD lens, an orphaned process (`nohup`, `setsid`, double-fork) achieves runtime persistence: the process outlives its parent. But it does not survive a reboot. `PRST.*` mechanisms survive reboots because they are registered with the OS for re-execution. Orphaned processes are `EXEC.PROC` with escalation; boot-surviving mechanisms are `PRST.*`. Both are high-severity in dependency code, but they require different remediation: orphaned processes need process termination; `PRST.*` mechanisms need both artifact removal and process termination.
