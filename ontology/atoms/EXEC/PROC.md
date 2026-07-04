# EXEC.PROC: Process Spawning

## Description

Creates child processes by launching executables directly via OS process creation APIs: `fork()`/`exec()`, `CreateProcess()`, `subprocess.Popen()` (without shell), `child_process.spawn()`, `Runtime.exec()`, or equivalent. The target binary is specified by path and arguments are passed as discrete values, without shell interpretation. The spawned process may run attached to the parent (inheriting its lifecycle), or may be deliberately detached/orphaned to run independently.

### Process Orphaning

A spawned process may be detached from its parent using `nohup`, `setsid`, `start /b`, double-fork, `DETACHED_PROCESS` flags, or similar techniques. The orphaned process is reparented to PID 1 (init/systemd) or the system equivalent and survives the termination of the parent process. This is a structural property of how the process is spawned: the orphaned process operates independently of the spawning context.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Process creation API calls (`subprocess.Popen([...])`, `child_process.spawn()`, `CreateProcess()`), target binary path, argument lists, detachment flags (`nohup`, `setsid`, `DETACHED_PROCESS`) |
| Static Binary | Yes | Process creation function imports, target binary path strings, argument arrays, detachment flag constants |
| Runtime/Dynamic | Yes | Child process creation events, process tree relationships, orphaned processes reparented to PID 1, binary path and arguments in process listings |

## Disambiguation

- **vs EXEC.SHELL**: `EXEC.PROC` launches a binary directly with explicit arguments. `EXEC.SHELL` passes a command string to a shell interpreter. The absence of shell interpretation means `EXEC.PROC` does not support pipes, globs, variable expansion, or other shell features, arguments are literal.
- **vs EXEC.INJECT**: `EXEC.PROC` creates a new, independent process. `EXEC.INJECT` operates within an existing process's memory space. These are distinct capabilities.
- **vs PRST.***: Process orphaning (detaching from parent) is a property of how the process is spawned (`EXEC.PROC`). System-level persistence mechanisms (services, cron jobs, startup entries) are `PRST.*`. Orphaning alone achieves session-surviving execution but not reboot-surviving persistence. When both co-occur, both should be flagged.

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (writing a binary before executing it), `NETW.HTTP` (downloading a binary before executing it), `PRST.*` (persistence mechanisms for the spawned process), `PKGM.INSTALL` (process spawning during installation)
- **May imply**: The target binary exists on disk (or will be written before execution)
- **Commonly part of idioms**: Decode-and-execute chain (decoded content written to disk, then executed as a process)

## Notes

The target binary path and the argument list are the key structural data. A fixed, well-known binary path (`/usr/bin/gcc`, `git`) with static arguments is structurally different from a dynamically-determined path or arguments sourced from external data. Whether the process is attached or orphaned is also a key structural property.
