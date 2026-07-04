# ENVI.DEBUG: Debugger Detection

## Description

Checks for attached debuggers, active breakpoints, or debug flags at runtime. Techniques include querying OS APIs (`IsDebuggerPresent`, `CheckRemoteDebuggerPresent`), ptrace self-attachment (on Unix systems, a process cannot be ptraced twice, self-attaching detects if a debugger is already attached), inspecting debug registers, and measuring execution timing to detect single-step execution (debugger-induced slowdown changes observable timing characteristics).

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `IsDebuggerPresent`, `ptrace(PTRACE_TRACEME, ...)`, debug register reads, timing comparison logic |
| Static Binary | Yes | Debug API imports, ptrace syscall numbers, hardware breakpoint register access |
| Runtime/Dynamic | Yes | API calls to debug detection functions, self-ptrace attempts, timing measurements |

## Disambiguation

- **vs ENVI.SANDBOX**: Debugger detection checks for active analysis tooling attached to the process. Sandbox detection checks for the execution environment itself (VM, container). Both are environment inspection but target different layers, attached tooling vs. hosting infrastructure.
- **vs ENVI.TIMING**: Timing-based debugger detection overlaps with ENVI.TIMING. When timing measurements are used specifically to detect single-stepping or breakpoint-induced delays, classify as ENVI.DEBUG. When timing is used for general execution delays or sandbox window evasion (unrelated to debugger detection), classify as ENVI.TIMING.

## Structural Relationships

- **Often co-occurs with**: `ENVI.SANDBOX` (layered environment detection), `ENVI.TIMING` (timing-based debugger detection technique)
- **May imply**: The code alters behavior based on whether analysis tooling is present

## Notes

Anti-debug techniques range from trivial (single API call) to sophisticated (timing side-channels, exception-based detection, TLS callback inspection). The detection surface varies accordingly, simple API checks are visible in static analysis; timing-based techniques may require dynamic analysis to identify. The mechanical behavior is the same regardless: query whether a debugger is present and branch on the result.
