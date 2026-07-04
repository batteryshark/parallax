# PRIV.CAP: Capability Modification

## Description

Modifies Linux capabilities on files or processes. Capabilities subdivide root privileges into discrete units (`CAP_NET_BIND_SERVICE`, `CAP_SYS_ADMIN`, `CAP_SYS_PTRACE`, `CAP_DAC_OVERRIDE`, etc.), allowing specific elevated operations without full root access. Setting capabilities on binaries (file capabilities) grants those specific privileges to any execution of that binary. Setting capabilities on processes (ambient/inheritable capabilities) modifies the privilege set of the running context. Also covers reading or enumerating current capability sets.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `setcap` / `getcap` command invocations, `capset()` / `capget()` syscall wrappers, `prctl(PR_CAP_AMBIENT, ...)` calls, capability constant references (`CAP_SYS_ADMIN`, `CAP_NET_RAW`, etc.) |
| Static Binary | Yes | Capability-related function imports, `prctl` constants, capability string constants, `/proc/self/status` path references for capability field parsing |
| Runtime/Dynamic | Yes | `capset` / `prctl` syscalls in trace output, capability changes in `/proc/[pid]/status`, new file capabilities visible via `getcap` on modified binaries |

## Disambiguation

- **vs PRIV.SUID**: SUID grants the binary full execution-as-owner (typically root). Capabilities grant specific privilege subsets without full root. Both are persistent filesystem-level privilege attributes on binaries, but the granularity differs.
- **vs PRIV.EXPLOIT**: `PRIV.CAP` uses the OS-provided capability API, the standard interface for managing granular privileges. `PRIV.EXPLOIT` interacts with kernel internals, modules, or driver interfaces outside the standard API surface.

## Structural Relationships

- **Often co-occurs with**: `NETW.LISTEN` (granting `CAP_NET_BIND_SERVICE` to bind privileged ports), `EXEC.PROC` (launching binaries with set capabilities), `FSYS.WRITE` (writing binaries before setting capabilities)
- **May imply**: The code is granting or requesting specific kernel-level privileges without full root elevation

## Notes

The specific capabilities being set or requested are the key structural data. `CAP_NET_BIND_SERVICE` (bind ports below 1024) has a narrow, well-understood scope. `CAP_SYS_ADMIN` is a catch-all that grants a wide range of kernel operations, effectively near-root. `CAP_SYS_PTRACE` enables cross-process debugging and memory access. `CAP_DAC_OVERRIDE` bypasses file permission checks entirely. The breadth of the capability relative to the code's stated purpose is the structural signal.
