# EXEC.INJECT: Process Injection / Memory Manipulation

## Description

Writes to another running process's memory space or manipulates its execution state. Techniques include code injection (DLL injection, shellcode injection), process hollowing, thread hijacking, APC injection, and non-code modifications (patching in-memory checks, modifying data structures, corrupting state, manipulating control flow). The defining characteristic is that the operation targets a process the current code does not own, modifying its memory, threads, or execution from the outside.

Platform-specific mechanisms include `WriteProcessMemory` (Windows), `ptrace(PTRACE_POKEDATA)` (Linux), Mach VM APIs (macOS), and `/proc/[pid]/mem` writes (Linux).

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Process memory write API calls (`WriteProcessMemory`, `ptrace`, `vm_write`), process handle acquisition (`OpenProcess`), thread manipulation APIs (`CreateRemoteThread`, `NtQueueApcThread`), `/proc/[pid]/mem` file opens |
| Static Binary | Yes | Imported process manipulation functions, shellcode byte arrays, DLL path strings for injection, process hollowing patterns (create suspended → unmap → write → resume) |
| Runtime/Dynamic | Yes | Cross-process memory writes, remote thread creation, process handle acquisition with write permissions, memory protection changes in target process |

## Disambiguation

- **vs EXEC.PROC**: `EXEC.PROC` creates a new process. `EXEC.INJECT` modifies an existing process. Creating a process suspended and then hollowing it (replacing its memory contents) is `EXEC.PROC` + `EXEC.INJECT`, both are present.
- **vs SYSI.PROCMEM**: `SYSI.PROCMEM` reads another process's memory. `EXEC.INJECT` writes to it. They are read vs. write counterparts of cross-process memory access. Both may co-occur (read to find injection point, then write to inject).
- **vs debugging**: Debuggers use the same APIs (ptrace, ReadProcessMemory/WriteProcessMemory) for legitimate debugging purposes. The mechanism is identical, the distinction between debugging and injection is context and intent, not the API calls themselves.

## Structural Relationships

- **Often co-occurs with**: `SYSI.PROCMEM` (reading target process memory before or after injection), `EXEC.PROC` (creating a target process for hollowing), `PRIV.*` (acquiring permissions needed for cross-process access), `XFRM.ENCODE` / `XFRM.ENCRYPT` (injected payload stored in encoded/encrypted form)
- **May imply**: The code has or acquires sufficient privileges to write to another process's memory space

## Notes

Process injection requires appropriate OS permissions, on Windows, `PROCESS_VM_WRITE` and often `PROCESS_CREATE_THREAD` access rights; on Linux, `ptrace` attach capability (restricted by `ptrace_scope` settings); on macOS, task port access. The target process selection (by name, PID, or characteristics) and the content being written are the key structural data. The read counterpart `SYSI.PROCMEM` is documented separately as it serves a distinct observational function.
