# NETW.IPC: Inter-Process Communication

## Description

Uses local inter-process communication mechanisms: Unix domain sockets (`AF_UNIX`), named pipes (FIFOs, Windows named pipes), shared memory segments, D-Bus, or other OS-provided local channels. Communication is constrained to processes on the same host, no network routing is involved. IPC enables coordination between co-running processes without network exposure.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `AF_UNIX` socket creation, named pipe paths (`/tmp/...`, `\\.\pipe\...`), shared memory APIs (`mmap`, `shmget`, `CreateFileMapping`), D-Bus interface definitions |
| Static Binary | Yes | IPC-related system call imports, pipe/socket path strings, shared memory function references |
| Runtime/Dynamic | Yes | Unix socket files on filesystem, named pipe existence, shared memory segments in `/proc/*/maps` or system monitors, D-Bus message traffic |

## Disambiguation

- **vs NETW.SOCKET**: The critical distinction is locality. `NETW.IPC` covers mechanisms constrained to the local host. `NETW.SOCKET` covers TCP/UDP sockets bound to network interfaces. Check the socket family: `AF_UNIX` is IPC, `AF_INET`/`AF_INET6` is SOCKET. Loopback connections over `AF_INET` to `127.0.0.1` are still `NETW.SOCKET` (they use the network stack), not `NETW.IPC`.
- **vs FSYS.WRITE**: Named pipes and Unix sockets appear as filesystem objects but are communication channels, not data storage. If the code creates a named pipe or Unix socket for process communication, it's `NETW.IPC`. If it writes data to a regular file for another process to read, it's `FSYS.WRITE` (with the inter-process data sharing being context, not a distinct atom).

## Structural Relationships

- **Often co-occurs with**: `EXEC.PROC` (spawning a child process to communicate with via IPC), `FSYS.READ` / `FSYS.WRITE` (IPC paths appearing as filesystem operations)
- **May imply**: Multiple cooperating processes are involved in the system's operation

## Notes

Named pipe and Unix socket paths are structural data: the path location (world-writable directory vs. application-specific directory), permissions, and naming convention are observable properties. Shared memory segments have size and permission attributes that are similarly observable.
