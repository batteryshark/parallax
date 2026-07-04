# SYSI.OS: Operating System Information Query

## Description

Queries operating system type, version, architecture, kernel version, or distribution identity. APIs and mechanisms include `os.platform()`, `os.release()`, `os.arch()` (Node.js), `sys.platform`, `platform.system()`, `platform.release()`, `platform.machine()` (Python), `process.arch` (Node.js), `uname` / `uname -a` (Unix), `GetVersionEx` / `RtlGetVersion` (Windows), `sw_vers` (macOS), `/etc/os-release` reads (Linux), `WMI Win32_OperatingSystem` queries, and `sysctl` calls. The code retrieves informational properties about the operating system. It does not use them to gate behavior (which would be `ENVI.ENVCHECK`).

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `os.platform()`, `sys.platform`, `platform.system()`, `platform.release()`, `platform.machine()`, `os.arch()`, `uname` invocations, `/etc/os-release` reads, `GetVersionEx` / `RtlGetVersion` calls |
| Static Binary | Yes | Platform module imports, OS version API imports, `/etc/os-release` path strings, WMI class name strings |
| Runtime/Dynamic | Yes | System call traces showing `uname()`, registry reads for OS version keys, WMI queries, file reads of OS identification files |

## Disambiguation

- **vs ENVI.ENVCHECK**: `SYSI.OS` queries system properties for informational purposes, collecting, logging, or transmitting OS identity. `ENVI.ENVCHECK` queries environment state to gate behavior, branching execution based on what it finds. When OS information is retrieved AND used to branch execution, both atoms apply. Reading `sys.platform` and storing it in a telemetry payload is `SYSI.OS`. Reading `sys.platform` and executing different code paths for `"win32"` vs. `"linux"` is `SYSI.OS` + `ENVI.ENVCHECK`.
- **vs cross-platform build tooling**: Build systems, installers, and platform abstraction libraries routinely query OS identity to select correct binaries, paths, or compilation flags. The mechanism is identical, the distinction is contextual.

## Structural Relationships

- **Often co-occurs with**: Cross-platform build tools (platform-specific code selection), `SYSI.HW` (combined system profiling), `NETW.*` (transmitting collected OS data), other `SYSI.*` subtypes (aggregated system profile)
- **May imply**: The code needs to know what OS it is running on, for adaptation, reporting, or profiling

## Notes

OS information queries are among the most common system inspection behaviors and are present in virtually every cross-platform application, build tool, and diagnostic utility. In isolation, a single OS query is structurally unremarkable. The investigative value comes from what happens to the collected data, whether it stays local for adaptation or feeds into a broader collection-and-transmission pattern.
