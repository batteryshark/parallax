# MCD Lens: EXEC (Code Execution) Verification

Investigation questions for EXEC findings. Questions tagged `[lens-neutral]` are applicable across multiple lenses. Questions tagged `[MCD]` assume an MCD evaluation context.

## General: Any EXEC Atom

1. **Where in the execution lifecycle does this occur?** Install time, import time, runtime on function call, or on a scheduled trigger? `[lens-neutral]`

2. **What is the full, resolved command or target?** If construction or encoding is involved, reconstruct the final string before assessing. The literal content passed to the execution primitive is the finding. `[lens-neutral]`

3. **Is execution present in prior versions of this package?** Diff against the previous release. If execution appeared in a new version, determine what changed and who authored the change. `[lens-neutral]`

4. **Does the package's stated purpose explain why it needs to launch processes?** A data-parsing or HTTP-handling library has no inherent need for shell execution. A build tool or compiler wrapper does. `[MCD]`

5. **What happens to the spawned process output?** Is output captured and returned, or is the process fire-and-forget/detached? Captured output feeding further logic is a different pattern than a detached independent process. `[lens-neutral]`

## EXEC.SHELL

6. **Is the command string fully static and visible at analysis time?** If constructed, decoded, or received from an external source, the command cannot be assessed without reconstruction. Dynamic command strings are a fundamentally different finding than static ones. `[lens-neutral]`

7. **Does the shell command pipe to an interpreter?** Patterns like `sh -c "$(curl ...)"` or `bash <(wget ...)` download and execute in a single step, bypassing file-based analysis. `[lens-neutral]`

## EXEC.PROC

8. **Is the spawned process detached from the parent?** `nohup`, `setsid`, `DETACHED_PROCESS` flags, double-fork: the process survives the parent. What does the orphaned process do, and where was its binary sourced from? `[lens-neutral]`

9. **What binary is being launched, and from what path?** A system binary at its canonical path with static arguments is structurally different from a binary in `/tmp` that was written there moments earlier. `[lens-neutral]`

## EXEC.INJECT

10. **What is the target process?** Identify by PID resolution, name lookup, or memory map. Injection into security tools, browsers, authenticators, or privileged system processes is an escalation within an already high-severity finding. `[lens-neutral]`

11. **What is being written to the target process's memory?** Shellcode, a DLL path, patched function pointers, data structure modifications. Each implies different objectives. `[lens-neutral]`

## EXEC.SYSCALL

12. **Which system calls are being invoked directly, and are corresponding library functions available?** Identify the syscall numbers and match to their library equivalents. Direct syscalls that have standard library wrappers available suggest the code is bypassing the normal abstraction layer. `[lens-neutral]`
