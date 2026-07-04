# SYSI.SW: Software Inventory Query

## Description

Queries installed software, package lists, application versions, or checks for the presence of specific applications. APIs and mechanisms include `dpkg -l`, `dpkg --get-selections` (Debian/Ubuntu), `rpm -qa` (RPM-based), `brew list` (macOS Homebrew), `pip list`, `pip freeze` (Python), `npm list`, `npm ls -g` (Node.js), `gem list` (Ruby), `wmic product get` (Windows), Windows Registry `SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall` enumeration, `system_profiler SPApplicationsDataType` (macOS), `Get-Package` (PowerShell), and application-specific version checks via executable invocation or file presence tests. The code inspects what software is installed, not what is currently running (which is `SYSI.PROC`).

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Package manager subprocess calls (`dpkg -l`, `pip list`, `npm list`), registry key enumeration of software hives, `system_profiler` invocations, version-check command executions |
| Static Binary | Yes | Package manager command strings, registry path strings for software enumeration, application name strings in checklist comparisons |
| Runtime/Dynamic | Yes | Subprocess execution of package manager commands, registry reads of software inventory keys, file existence checks for application-specific paths |

## Disambiguation

- **vs SYSI.PROC**: `SYSI.SW` queries the installed software inventory, what is available on the system. `SYSI.PROC` queries running processes, what is currently executing. `pip list` is `SYSI.SW`. `ps aux` is `SYSI.PROC`. A package may be installed but not running, or running but not formally installed.
- **vs ENVI.ENVCHECK**: When software inventory results are used to branch execution (e.g., proceed only if a specific application is installed), both `SYSI.SW` and `ENVI.ENVCHECK` apply.

## Structural Relationships

- **Often co-occurs with**: `SYSI.OS` (OS + installed software = fuller system profile), `SYSI.PROC` (installed vs. running software), `NETW.*` (transmitting inventory data), other `SYSI.*` subtypes (aggregated system profile)
- **May imply**: The code needs to know what software is available, for compatibility checking, dependency verification, or system profiling

## Notes

Software inventory queries are common in configuration management, compatibility checks, and diagnostic tools. The breadth of the query is a key structural observation: checking for one specific dependency differs from enumerating all installed packages across multiple package managers. Cross-ecosystem enumeration (querying pip, npm, brew, and system packages in the same code) produces a comprehensive software profile.
