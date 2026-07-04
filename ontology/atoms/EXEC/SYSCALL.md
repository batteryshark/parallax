# EXEC.SYSCALL: Direct System Calls

## Description

Invokes operating system kernel calls directly, bypassing standard library wrappers. Instead of calling library functions like `open()`, `read()`, `write()`, or `execve()` through libc/NTDLL, the code issues system calls directly via `syscall()` instruction, `int 0x80`, `sysenter`, or equivalent platform-specific mechanisms. In managed/interpreted languages (Python, Java, JavaScript, C#), direct system call invocation is structurally unusual since these languages provide high-level abstractions.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Partial | `syscall()` function usage, inline assembly with `int 0x80` or `syscall` instruction, ctypes/FFI loading of kernel32/ntdll functions bypassing standard wrappers |
| Static Binary | Yes | Direct `syscall`/`sysenter`/`int 0x80` instructions, system call number constants, absence of corresponding library function imports for the operations performed |
| Runtime/Dynamic | Yes | System call traces (`strace`, `dtrace`, `procmon`) show calls without corresponding library-level call stacks |

## Disambiguation

- **vs EXEC.PROC**: `EXEC.PROC` uses standard library process creation APIs. `EXEC.SYSCALL` bypasses those wrappers. The distinction is the abstraction level, library wrappers are the normal interface; direct system calls bypass library-level instrumentation, logging, and hooks.
- **vs normal native code**: System-level software (kernels, drivers, low-level libraries like libc itself) legitimately uses direct system calls. `EXEC.SYSCALL` is structurally notable in application-level code, especially in managed/interpreted languages where the expected abstraction level is much higher.

## Structural Relationships

- **Often co-occurs with**: `LOAD.NATIVE` (loading native code that makes direct syscalls from a managed language context), `EXEC.INJECT` (direct syscalls used to perform process injection operations)
- **May imply**: The code is deliberately operating below the standard library abstraction layer

## Notes

The specific system call numbers are platform-dependent and architecture-dependent (x86 vs x86_64 vs ARM). On Linux, `execve` is syscall 59 (x86_64) / 11 (x86). On Windows, direct `NtCreateProcess` via `syscall` bypasses usermode hooks installed by security tools. The system call number and the arguments passed are the key structural data for analysis.
