# MCD Lens: PRST (Persistence Mechanisms) Verification

Investigation questions for PRST findings. Questions tagged `[lens-neutral]` are applicable across multiple lenses. Questions tagged `[MCD]` assume an MCD evaluation context.

## General: Any PRST Atom

1. **What filesystem path or registry location was the persistence artifact written to, and does it survive package removal?** Determine whether `pip uninstall`, `npm uninstall`, or equivalent package removal deletes the persistence artifact. Artifacts outside the package manager's tracked file set persist after uninstallation. `[lens-neutral]`

2. **Was the persistence registered during install/import, or does it require explicit user invocation?** Persistence in `postinstall`, `setup.py`, `__init__.py`, or module-level code fires automatically. Persistence behind a documented CLI command or configuration API requires user action. The distinction determines whether the user had any awareness of the registration. `[lens-neutral]`

3. **What command, binary, or script does the persistence mechanism invoke when it fires?** Resolve the full execution target. If the target is a shell command, reconstruct the full command string. If the target is a binary, determine its origin: part of the package distribution, downloaded at runtime, or written to a temporary path. `[lens-neutral]`

4. **What identity (user, group, privilege level) does the persistence mechanism run under?** Determine whether the registered task, service, or hook executes as the installing user, root/SYSTEM, or a specific service account. Cross-user or elevated execution amplifies blast radius. `[lens-neutral]`

5. **Does the persistence artifact naming follow OS conventions or mimic known system components?** Compare the registered name (service name, scheduled task name, startup entry name, hook binary name) against known legitimate OS components and common system services. Close matches indicate deliberate camouflage. `[MCD]`

6. **Is there network connection establishment or credential/data exfiltration co-occurring with the persistence registration?** Trace whether the persistence target or the registration code itself initiates outbound network connections, reads credential stores, or transmits collected data. Persistence + exfiltration = operational malware. `[MCD]`

7. **Does the persistence mechanism resist removal or re-register after deletion?** Check for watchdog processes, secondary persistence mechanisms that restore the primary, or scheduled tasks that verify and re-register other persistence artifacts. `[MCD]`

8. **Was the persistence registration present in previous versions of this package?** Diff against prior releases. Persistence that appears in a new version, minor update, or patch release, especially from a new contributor, is high-confidence supply chain compromise. `[lens-neutral]`

9. **Is the finding confirmed executing (dynamic analysis) or a static detection only?** Determine whether the persistence mechanism was observed to actually register during installation/runtime, or whether it was identified via static pattern matching on source code. Static-only findings require execution verification to confirm reachability. `[lens-neutral]`

## PRST.HOOK

10. **What is the blast radius of the hook?** Determine whether the hook affects user-level operations only, or intercepts system-wide. `LD_PRELOAD` via shell profile = user-level. `/etc/ld.so.preload` = system-wide. `.pth` in virtualenv `site-packages` = environment-scoped. `.pth` in system `site-packages` = all Python invocations. Git hook in `.git/hooks/` = single repository. Git hook in `~/.git-templates/hooks/` = all future repositories. `[lens-neutral]`

## PRST.STARTUP / PRST.SCHED

11. **Is the registered item name designed to blend with legitimate OS maintenance tasks or startup components?** Names like `WindowsUpdate`, `system-health-check`, `com.apple.security.agent`, or `update-manager` in a dependency context are deliberate camouflage. `[MCD]`

## PRST.EXTENSION

12. **What permissions does the installed extension request, and do they exceed the package's stated purpose?** Browser extensions requesting `<all_urls>`, `cookies`, `webRequest`, and `webRequestBlocking` have full visibility into all browser traffic. IDE extensions with terminal and file access can read and exfiltrate source code and credentials. `[lens-neutral]`
