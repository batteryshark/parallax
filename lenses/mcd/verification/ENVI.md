# MCD Lens: ENVI (Environment Interaction) Verification

## General: Any ENVI Atom

1. **What does the environment interaction gate?** Identify what executes when the check passes (or fails). If the gated code is network activity, process spawning, or file modification, severity is high regardless of how benign the check looks. `[lens-neutral]`

2. **Does the behavior appear in install-time hooks or module initialization?** `postinstall`, `setup.py`, `__init__.py`, and equivalents execute at install/import time with narrow analysis windows. `[lens-neutral]`

3. **How many ENVI subtypes are present simultaneously?** A single check may have a legitimate explanation. Two or more distinct environment interaction behaviors in the same package indicate layered, intentional design. `[MCD]`

4. **Was the behavior introduced in the same commit as other suspicious changes?** Use version diffs or `git log -S` to identify when each construct was introduced. Co-introduction with payload delivery is strong evidence of coordinated intent. `[lens-neutral]`

## ENVI.ENVCHECK

5. **Is the check additive or subtractive?** Additive: behavior fires when condition is true (targeted). Subtractive: behavior is suppressed when condition is true (suppressed in analysis, active everywhere else). `[MCD]`

6. **What specific environment properties are checked?** CI variables, usernames, hostnames, domain membership, geographic indicators? Specificity reveals targeting model: opportunistic vs. directed. `[lens-neutral]`

## ENVI.FORENSIC

7. **Is evidence being replaced or merely deleted?** Check for write operations targeting the same paths that were previously written by other operations in the package. `[MCD]`

8. **What is the timestamp manipulation target value?** A zeroed timestamp may be accidental. A precise historical date indicates automation and intent. Check consistency across multiple artifacts. `[lens-neutral]`

## ENVI.MASQ

9. **Does the masquerading name match a real signed OS component?** Verify whether the claimed name corresponds to a legitimate component. Check whether a real binary with that name exists elsewhere. Dual presence is a strong indicator. `[lens-neutral]`

## ENVI.TIMING

10. **Is the delay proportional to any stated operational purpose?** Calculate whether delay magnitude and placement are consistent with the nearest stated purpose (retry, rate limiting, polling). `[lens-neutral]`

## ENVI.SECDISABLE

11. **What specific security control is being modified?** Firewall rule, AV exclusion, exploit mitigation, security policy, or security center status. Each has different blast radius and remediation requirements. `[lens-neutral]`

12. **Is the modification scoped or blanket?** A specific-program specific-port firewall rule differs from any-program any-port. Single-file AV exclusion differs from directory tree exclusion. `[lens-neutral]`

13. **Does the excluded or weakened path overlap with `FSYS.WRITE` targets in the same package?** If the package writes to a path and also adds an AV exclusion for that path, the exclusion protects the payload. `[MCD]`

14. **Is the security modification reversed after use?** Temporary weakening with restoration = potentially legitimate tool. Permanent weakening with no restoration = infrastructure preparation. `[lens-neutral]`

## ENVI.LOG

15. **Does suppression target a specific named process or audit category, or is it generic?** Named EDR process termination is high-confidence. Generic log-level reduction is low-confidence. `[lens-neutral]`
