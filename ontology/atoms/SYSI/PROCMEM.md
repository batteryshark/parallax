# SYSI.PROCMEM: Process Memory Reading

## Description

Reads the memory of other running processes to extract runtime data. Techniques include reading `/proc/[pid]/mem` or `/proc/[pid]/environ` (Linux), `process_vm_readv` (Linux), `ReadProcessMemory` (Windows API), `vm_read` / `mach_vm_read` (macOS Mach APIs), memory dumping via debug APIs (`ptrace(PTRACE_PEEKDATA)` on Linux, debug privilege escalation on Windows), and `/proc/[pid]/maps` parsing to identify readable memory regions before reading them. The extracted data exists only at runtime in the target process's address space; it was never written to disk as files. The defining characteristic is cross-process memory read access: the current code reads another process's memory space.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `/proc/[pid]/mem` file opens, `process_vm_readv` calls, `ReadProcessMemory` API calls, `vm_read` / `mach_vm_read` calls, `ptrace(PTRACE_PEEKDATA)`, `/proc/[pid]/maps` parsing, process handle acquisition with `PROCESS_VM_READ` |
| Static Binary | Yes | Process memory read API imports, `/proc/[pid]/mem` path construction patterns, memory region scanning patterns, debug API imports |
| Runtime/Dynamic | Yes | Cross-process memory read system calls, ptrace attach to target process, `/proc` filesystem reads targeting specific PIDs, process handle acquisition with read permissions |

## Disambiguation

- **vs EXEC.INJECT**: `SYSI.PROCMEM` reads another process's memory. `EXEC.INJECT` writes to another process's memory. They are read vs. write counterparts of cross-process memory access. Both may co-occur, reading to find an injection point, then writing to inject. The same APIs may support both directions (`ptrace`, Mach VM APIs), so the specific operation (read vs. write) determines which atom applies.
- **vs SYSI.PROC**: `SYSI.PROC` queries process metadata, PID, name, owner, command line, resource usage, from the process table or OS APIs. `SYSI.PROCMEM` reads the actual memory contents of a target process's address space. `ps aux` is `SYSI.PROC`. `ReadProcessMemory(handle, addr, ...)` is `SYSI.PROCMEM`. They often co-occur: enumerate processes to find the target (`SYSI.PROC`), then read its memory (`SYSI.PROCMEM`).
- **vs CRED.\***: When process memory reading targets a process known to hold credentials (e.g., reading `lsass.exe` memory, browser process memory for session tokens), both `SYSI.PROCMEM` and the relevant `CRED.*` atom apply. `SYSI.PROCMEM` describes the mechanism; `CRED.*` describes what is being targeted.

## Structural Relationships

- **Often co-occurs with**: `SYSI.PROC` (enumerate processes to find target), `EXEC.INJECT` (read then write to target), `CRED.*` (extracting credentials from process memory), `PRIV.*` (acquiring permissions for cross-process access)
- **May imply**: The code has or acquires sufficient privileges to read another process's memory space (ptrace, debug privileges, appropriate process access rights)

## Notes

Cross-process memory reading requires elevated privileges on modern operating systems. On Linux, `ptrace_scope` settings restrict which processes can be attached to. On Windows, `SeDebugPrivilege` or specific process access rights are needed. On macOS, task port access is restricted. The target process selection (by name, PID, or enumeration) and the memory regions being read are the key structural data. This atom covers only reading, any write to another process's memory is `EXEC.INJECT`.
