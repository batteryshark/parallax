# RSRC.MEM: Memory Allocation

## Description

Allocating large memory regions, patterns consistent with memory exhaustion, or deliberately growing data structures without bounds. Includes `mmap` of large regions, repeated heap allocations without corresponding frees, unbounded list/buffer growth, memory-mapped file consumption, or any pattern where memory usage grows significantly relative to the task being performed. The atom describes significant or unbounded memory allocation patterns, routine application memory management is not in scope.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Partial | Large allocation size arguments (`malloc(1<<30)`), unbounded append/push loops, missing deallocation in allocation paths, `mmap` with large size parameters, growing collections without size checks |
| Static Binary | Partial | Large constant allocation sizes, allocation function imports without corresponding free imports, loop structures containing allocation calls |
| Runtime/Dynamic | Yes | Resident set size growth over time, virtual memory consumption, OOM killer invocation, swap pressure, allocation profiler showing unbounded growth |

## Disambiguation

- **vs normal memory usage**: Application memory allocation is ubiquitous. RSRC.MEM applies when allocation patterns are notable for scale (single large allocation), growth rate (rapid unbounded growth), or absence of bounds (no cap on collection size, no deallocation path). Routine object creation and buffer management are not RSRC.MEM.
- **vs FSYS.WRITE**: Memory-mapped file I/O spans both memory and filesystem domains. If the allocation backs a file mapping, both `RSRC.MEM` (memory footprint) and `FSYS.WRITE` (file I/O) may apply depending on the observable behavior.

## Structural Relationships

- **Often co-occurs with**: `RSRC.CPU` (CPU-intensive computation often requires large working memory), `NETW.*` (receiving large payloads into memory), `LOAD.DESER` (deserialization of untrusted data into unbounded structures), `SYSI.HW` (querying available RAM to scale allocation)
- **May imply**: Reduced availability for other processes on the host, potential OOM conditions, swap thrashing on memory-constrained systems

## Notes

The key structural data points are: the total allocation size, whether allocation is bounded or unbounded, whether corresponding deallocation exists, and the relationship between allocation scale and the task's data requirements. A video editor allocating a large frame buffer is structurally different from a JSON parser allocating unbounded memory proportional to untrusted input size. Whether memory growth is proportional to input size, fixed, or independent of input is a critical structural property.
