# RSRC.FORK: Process / Thread Exhaustion

## Description

Creating processes or threads in an unbounded or rapidly scaling fashion. Includes fork bombs (`:(){ :|:& };:`), exponential process creation, thread pool creation without upper bounds, rapid `spawn`/`fork`/`pthread_create` in loops without join or termination conditions, and any pattern of process or thread creation where the count is not bounded by an enforced upper limit. The atom describes the resource exhaustion aspect of process/thread creation, not process creation as a general execution mechanism.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Recursive `fork()`/`spawn()` calls, process/thread creation in unbounded loops, absence of join/wait/pool-size-limit alongside creation calls, self-invocation patterns |
| Static Binary | Yes | Fork/spawn/thread-create imports in recursive or loop contexts, absence of wait/join calls, process creation without termination conditions |
| Runtime/Dynamic | Yes | Rapid PID/TID consumption, process table exhaustion, system-wide process count limits reached, thread count growth without plateau, OS-level resource limit violations (`ulimit`, `RLIMIT_NPROC`) |

## Disambiguation

- **vs EXEC.PROC**: `EXEC.PROC` describes process spawning as an execution mechanism, launching a specific binary to perform a task. `RSRC.FORK` describes the resource exhaustion aspect of unbounded process or thread creation. When process creation is unbounded or rapidly scaling, both atoms may apply: `EXEC.PROC` for the spawning mechanism and `RSRC.FORK` for the exhaustion pattern.
- **vs RSRC.CPU**: Fork bombs and thread exhaustion consume CPU as a secondary effect of process/thread scheduling overhead. `RSRC.CPU` describes sustained computation within processes; `RSRC.FORK` describes exhaustion of the process/thread resource itself. Both may co-occur.

## Structural Relationships

- **Often co-occurs with**: `EXEC.PROC` (the process creation mechanism being exercised), `EXEC.SHELL` (shell-based fork bombs), `TIME.DELAY` (delayed or scheduled process/thread creation), `RSRC.CPU` (CPU consumed by scheduling overhead of many processes/threads), `RSRC.MEM` (memory consumed by per-process/thread allocations)
- **May imply**: System-wide denial of service, process table exhaustion, inability to create new processes for any user on the system, potential kernel-level resource pressure

## Notes

The key structural data points are: whether the process/thread creation count has an enforced upper bound, the growth rate (linear, exponential, recursive), whether created processes/threads are joined or awaited, and whether self-invocation is present. A thread pool with a fixed size of 8 is not RSRC.FORK. A recursive fork with no termination condition is the canonical example. The presence or absence of `ulimit`/`setrlimit`/pool-size configuration is a critical structural property.
