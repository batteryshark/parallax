# MCD Lens: PRIV (Privilege Operations) Verification

Investigation questions for PRIV findings. Questions tagged `[lens-neutral]` are applicable across multiple lenses. Questions tagged `[MCD]` assume an MCD evaluation context.

## General: Any PRIV Atom

1. **What is the target identity and scope of the privilege operation?** Identify the specific identity being assumed, the privilege level being requested, and the scope of access it provides. Root/Administrator? A specific service account? A narrow capability? `[lens-neutral]`

2. **Is the privilege operation triggered at install time, import time, or runtime?** Install-time and import-time privilege operations execute without explicit user invocation. Runtime operations gated behind explicit function calls have a different exposure profile. `[lens-neutral]`

3. **Is there a chain from the privilege operation to persistence or credential access?** Trace forward: after privilege is obtained, does the code install persistence mechanisms (`PRST.*`), access credentials (`CRED.*`), or perform other operations that rely on the elevated context? `[MCD]`

4. **Is the privilege state restored after use?** Does the code explicitly drop privileges after the elevated operation completes? Verify the drop is unconditional, not gated behind error handling or conditional logic that could leave the process elevated on failure paths. `[lens-neutral]`

5. **Is the dependency's stated purpose consistent with privilege operations?** A JSON parser, logging utility, or string manipulation library has no inherent need for privilege elevation. A system administration tool or platform installer might. `[lens-neutral]`

6. **Is the escalation path reachable without attacker-controlled input?** Can the privilege operation execute automatically through normal code paths, or does it require specific triggering conditions? Automatically-reachable paths are higher concern. `[lens-neutral]`

## PRIV.SUID

7. **Is the SUID target binary an interpreter or shell?** Setting SUID on `/bin/bash`, `/bin/sh`, `python`, `perl`, or any general-purpose interpreter creates an unrestricted elevation path. A narrowly-scoped binary with SUID is structurally different from an interpreter with SUID. `[lens-neutral]`

## PRIV.TOKEN

8. **Is the token manipulation scoped to the current process or does it cross process boundaries?** Thread-level impersonation confined to the current process is narrower than `CreateProcessWithTokenW` or equivalent operations that spawn new processes under the manipulated identity. `[lens-neutral]`

## PRIV.ACCOUNT

9. **What account is being created or modified, and what group memberships are assigned?** Identify the account name, shell, home directory, and group memberships. Membership in `sudo`, `wheel`, `Administrators`, or `docker` grants persistent elevated access. `[lens-neutral]`

10. **Does the account name resemble a legitimate system service account?** Names like `syslogd`, `crond`, `svchost`, or `systemd-*` may be designed to avoid detection during casual review. Compare against actual system service accounts on the target platform. `[MCD]`

11. **Is the account created via OS management utilities or direct database manipulation?** `useradd` and `net user` enforce validation and generate audit logs. Direct writes to `/etc/passwd`, `/etc/shadow`, or SAM bypass these controls. The method indicates the level of stealth intended. `[lens-neutral]`

12. **Does the account have a hardcoded password or SSH authorized key?** A hardcoded credential in the account creation code means anyone with access to the package source has the credential for the created account. `[lens-neutral]`
