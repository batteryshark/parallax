# SYSI.PROC: Process Enumeration

## Description

Lists running processes, queries process attributes (PID, name, owner, command line, resource usage), or checks for the presence of specific named processes. APIs and mechanisms include `ps` / `ps aux` (Unix), `tasklist` (Windows), `/proc` filesystem traversal (Linux), `EnumProcesses` / `CreateToolhelp32Snapshot` (Windows API), `psutil.process_iter()` (Python), `NSWorkspace.runningApplications` (macOS), `WMI Win32_Process` queries, `top` / `htop` output parsing, and `pgrep` / `pidof` (process name lookups). The code inspects the process table, listing what is running, not modifying it.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `ps`/`tasklist` subprocess calls, `/proc` directory reads, `psutil.process_iter()`, `EnumProcesses`, `CreateToolhelp32Snapshot`, WMI process queries, process name string comparisons |
| Static Binary | Yes | Process enumeration API imports, `/proc` path strings, process name checklist strings (e.g., security tool names), WMI query strings |
| Runtime/Dynamic | Yes | System calls for process listing, `/proc` directory traversal, subprocess execution of `ps`/`tasklist`, repeated process table queries |

## Disambiguation

- **vs ENVI.SANDBOX / ENVI.DEBUG**: `SYSI.PROC` lists processes and their attributes. When the resulting process list is checked against known security tool names (debuggers, sandbox agents, AV processes) to gate behavior, `ENVI.SANDBOX` or `ENVI.DEBUG` also applies. The mechanical act of listing processes is `SYSI.PROC`; the interpretive act of matching against security tools and branching is `ENVI.*`. Both co-occur when process enumeration feeds an activation decision targeting analysis infrastructure.
- **vs SYSI.PROCMEM**: `SYSI.PROC` queries process metadata, PID, name, owner, command line, resource usage. `SYSI.PROCMEM` reads process memory contents. Listing processes is `PROC`; reading another process's memory space is `PROCMEM`. They often co-occur (enumerate to find target, then read its memory).
- **vs EXEC.PROC**: `SYSI.PROC` queries existing processes. `EXEC.PROC` creates new processes. One is observational; the other is operational.

## Structural Relationships

- **Often co-occurs with**: `ENVI.SANDBOX` / `ENVI.DEBUG` (process list feeding security tool detection), `SYSI.PROCMEM` (enumerate then read), `SYSI.OS` (combined system profiling), other `SYSI.*` subtypes (aggregated system profile)
- **May imply**: The code needs to know what is currently running on the system, for monitoring, dependency checking, or profiling

## Notes

Process enumeration is structurally common in monitoring tools, application launchers, and resource managers. The key structural data points are: the breadth of enumeration (all processes vs. specific name lookups), whether a checklist of specific process names is present (and what those names are), and what happens with the collected process data. A hardcoded list of process names to check is a stronger structural observation than a generic process listing.
