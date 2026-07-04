# RSRC.CPU: CPU-Intensive Computation

## Description

Tight computational loops, mathematical operations, or algorithms that consume significant CPU time. Includes hash grinding, proof-of-work calculations, brute-force iteration, large-matrix operations, repeated cryptographic rounds, or any computation that produces sustained high CPU utilization. The atom describes the resource consumption pattern, not the purpose of the computation, a compression library, a cryptographic signing routine, and a cryptocurrency miner may all exhibit RSRC.CPU.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Partial | Tight loops with mathematical operations, hash iterations, modular exponentiation, nonce-grinding patterns, worker thread pools performing intensive calculations |
| Static Binary | Partial | Loop structures with arithmetic/bitwise operations, SIMD instruction usage, CPU-bound function call patterns without I/O interleaving |
| Runtime/Dynamic | Yes | Sustained high CPU utilization on one or more cores, elevated process CPU time, measurable thermal/power impact, CPU-bound thread profiles with no I/O wait |

## Disambiguation

- **vs legitimate computation**: Cryptographic libraries, compression engines, scientific computing, and media encoders all produce sustained CPU utilization. RSRC.CPU applies to the resource consumption pattern regardless of purpose, the atom is judgment-free. Whether the computation is expected for the package's stated role is an interpretive question.
- **vs CRPT.CUSTOM**: Hand-rolled cryptographic implementations are both a crypto implementation (`CRPT.CUSTOM`) and CPU-intensive computation (`RSRC.CPU`). When both apply, tag both. `CRPT.CUSTOM` describes the implementation method; `RSRC.CPU` describes the resource impact.
- **vs XFRM.BITWISE**: Bitwise operations that are CPU-intensive may co-occur with `RSRC.CPU`, but `XFRM.BITWISE` describes the transformation technique while `RSRC.CPU` describes the resource footprint.

## Structural Relationships

- **Often co-occurs with**: `CRPT.HASH` (hash grinding / proof-of-work), `CRPT.CUSTOM` (hand-rolled crypto is inherently CPU-bound), `NETW.*` (submitting computation results to a remote endpoint), `SYSI.HW` (querying CPU core count to scale workers)
- **May imply**: Thread or worker pool creation to parallelize computation, elevated power consumption, reduced responsiveness for other processes on the host

## Notes

The key structural data points are: what computation is being performed, how many CPU cores it targets, whether it scales to available hardware, and where the output goes. A fixed-iteration computation with local output is structurally different from an open-ended computation that scales to all available cores and transmits results externally. Whether the CPU consumption is bounded (finite iterations, time limits) or unbounded (runs until terminated) is a critical structural distinction.
