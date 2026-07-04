# MCD Lens: PRIV (Privilege Operations) Indicators

> **Core MCD position:** Privilege operations in dependency code are almost never legitimate. Legitimate packages don't need sudo, SUID bits, kernel modules, or account creation. When a library or package performs privilege operations, the investigation starts from the assumption that the behavior is anomalous and works toward justified exceptions, not the reverse.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `PRIV.SUDO` | High | Elevation utility invocation in dependency code is a strong finding |
| `PRIV.SUID` | High | SUID/SGID modification in a package has no common legitimate use case |
| `PRIV.CAP` | High | Capability modification in dependency code grants kernel-level privileges |
| `PRIV.TOKEN` | High | Token manipulation in a library indicates identity context switching |
| `PRIV.EXPLOIT` | Critical | Kernel module loading or driver interaction from a package is a critical finding |
| `PRIV.ACCOUNT` | Critical | OS account creation or modification from dependency code is a critical finding, creates persistent access independent of the package lifecycle |

## Escalation Factors

- **Passwordless sudo configuration.** Code that relies on or installs `NOPASSWD` sudoers entries enables non-interactive privilege escalation: no authentication barrier between the code and root execution.
- **SUID set on an interpreter or shell.** Setting SUID on `/bin/bash`, `/bin/sh`, `python`, `perl`, or any general-purpose interpreter creates an unrestricted privilege escalation path available to any local user.
- **Kernel module loading from package context.** A dependency loading a kernel module introduces code into the highest trust domain on the system. Unsigned or unknown modules are an immediate critical finding.
- **Token manipulation crossing process boundaries.** `CreateProcessWithTokenW` or equivalent: the manipulated identity escapes the current process and creates independently-running elevated processes.
- **Capabilities exceeding the package's declared need.** `CAP_SYS_ADMIN`, `CAP_DAC_OVERRIDE`, or `CAP_SYS_PTRACE` on a binary unrelated to system administration indicates privilege over-provisioning.
- **Privilege escalation preceding persistence or credential access.** `PRIV.*` → `PRST.*` or `PRIV.*` → `CRED.*` chains indicate elevation is a means to an end: the escalated context is used for survival or credential theft.
- **Execution under package manager identity.** Privilege operations in install hooks, `setup.py`, `postinstall`, or build scripts run automatically as the installing user, often with broad permissions and no user review.
- **Account creation with admin group membership.** `PRIV.ACCOUNT` adding a user to `sudo`, `wheel`, `Administrators`, or `docker` grants the new account persistent elevated access.
- **Account modification via direct database manipulation.** Writing `/etc/passwd`, `/etc/shadow`, or SAM directly bypasses OS logging and validation, making it structurally more suspicious than using standard account management utilities.
- **Account with system-service-like names.** Account names resembling legitimate system services (`syslogd`, `crond`, `svchost`) indicate deliberate camouflage (`ENVI.MASQ` overlap).
- **Account enabling disabled built-in accounts.** Activating the Windows `Administrator` or `Guest` account provides access through a pre-existing identity that may not be monitored.

## De-escalation Factors

- **Documented privilege-drop pattern.** Code that elevates to perform a specific operation and then explicitly drops back to the original privilege level, a well-established security architecture pattern. Verify the drop actually occurs and is not conditional.
- **Test or simulation context.** Privilege operations in test fixtures, CI configuration, or documented simulation environments with clear scoping. Verify the code path is actually test-only and not reachable from production execution.
- **Platform-native signed package.** Privilege operations in OS vendor packages (apt, rpm, msi) that are signed by the platform vendor and perform documented system configuration. Does not apply to third-party packages distributed through language-level registries.
- **Account creation in documented configuration management tools.** Ansible, Chef, Puppet, Terraform, and similar infrastructure-as-code tools legitimately create accounts as part of system provisioning. The tool itself is the reviewed, audited artifact. Verify the account configuration is consistent with declared infrastructure state.

> **Caveat:** Privilege operations are structurally high-severity because they change the trust boundary. Even with de-escalation, the presence of privilege operations in dependency code warrants investigation into *why* the package requires elevated access and whether the escalation scope is minimal and necessary.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `PRIV.SUDO` + `PRST.STARTUP` | Elevated privilege installing persistence, survives reboot under elevated context | Very High |
| `PRIV.SUID` + `EXEC.SHELL` | SUID shell, unrestricted privilege escalation path | Very High |
| `PRIV.CAP` + `NETW.LISTEN` | Capability-granted network listener, privileged port binding or raw socket access | High |
| `PRIV.TOKEN` + `CRED.*` | Identity impersonation accessing credentials, lateral credential theft under assumed identity | Very High |
| `PRIV.EXPLOIT` + `EXEC.*` | Kernel-level access enabling arbitrary execution, complete system compromise | Critical |
| `PRIV.SUDO` + `PKGM.INSTALL` | Elevated package installation, installing additional packages as root during dependency install | Very High |
| `PRIV.CAP` + `FSYS.WRITE` | Capability-enabled filesystem writes, writing to protected locations via granted capabilities | High |
| `PRIV.ACCOUNT` + `PRST.*` | Account creation combined with persistence, independent survival mechanism with its own identity | Critical |
| `PRIV.ACCOUNT` + `NETW.LISTEN` | Account creation combined with network listener, backdoor access with dedicated identity | Critical |
| `PRIV.ACCOUNT` + `ENVI.MASQ` | Account with disguised name, identity designed to blend with legitimate system accounts | Critical |
| `PRIV.ACCOUNT` + `PKGM.INSTALL` | Account creation during package installation, persistent identity from install hook | Critical |
| `PRIV.ACCOUNT` + `CRED.*` | Account creation combined with credential access, new identity with harvested credentials | Critical |

## MCD-Specific Disambiguation

### PRIV vs legitimate privilege-separated architecture
Some software legitimately uses privilege separation, running a minimally-privileged main process alongside a narrowly-scoped elevated helper (e.g., `ping`, `passwd`, network daemons that bind privileged ports then drop root). Through the MCD lens, the key questions are: (1) Is the privilege-separated architecture documented and consistent with the package's purpose? (2) Is the elevated scope minimal? (3) Does the code actually drop privileges after the elevated operation? A package that claims privilege separation but retains elevated access or grants broader privileges than its purpose requires does not qualify for de-escalation.

### PRIV.EXPLOIT vs security testing tools
Security testing frameworks and kernel development tools legitimately interact with kernel interfaces. Through the MCD lens, `PRIV.EXPLOIT` in a declared security testing tool is context-dependent. However, kernel interaction from a package that is not explicitly a security testing or kernel development tool is a critical finding without qualification. The package's declared purpose must match the behavior.

### PRIV.ACCOUNT vs PRST
Account creation is inherently persistent: a created account survives indefinitely. Through the MCD lens, `PRIV.ACCOUNT` is escalated to Critical baseline (rather than High like other PRIV atoms) specifically because of this persistence characteristic. When combined with explicit persistence mechanisms (`PRST.STARTUP`, `PRST.SERVICE`), the combination represents layered survival: a new identity *and* an execution trigger. The MCD investigation must trace what the account is used for after creation. If the account is the identity under which a persistent service runs, the full chain is `PRIV.ACCOUNT` → `PRST.SERVICE` → whatever the service does.
