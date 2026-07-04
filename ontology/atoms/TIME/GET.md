# TIME.GET: Time Retrieval

## Description

Gets the current time, date, timestamp, or epoch value. APIs: `time.time()`, `Date.now()`, `System.currentTimeMillis()`, `gettimeofday()`, `clock_gettime()`, `datetime.now()`, `std::chrono::system_clock::now()`. Returns a temporal value for use by subsequent operations. The retrieval itself is a read-only operation, it captures a point-in-time value without modifying state or making decisions.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Time retrieval API calls (`time.time()`, `Date.now()`, `System.currentTimeMillis()`), return value stored in variable or passed to further logic |
| Static Binary | Yes | Imported time retrieval functions, clock source constants (`CLOCK_REALTIME`, `CLOCK_MONOTONIC`), timestamp format strings |
| Runtime/Dynamic | Yes | System clock reads, time-related syscalls (`gettimeofday`, `clock_gettime`), returned temporal values in register/variable state |

## Disambiguation

- **vs TIME.CMP**: `TIME.GET` retrieves a temporal value with no conditional logic. `TIME.CMP` compares a temporal value against a threshold to make a decision. Many `TIME.GET` findings are promoted to `TIME.CMP` after data-flow analysis reveals the retrieved value flows into a comparison. The distinction is whether a conditional branch depends on the retrieved time.
- **vs SYSI.***: `TIME.GET` retrieves the current time. System inspection atoms query hardware, OS, or process properties. When code reads the system timezone or clock source configuration (as opposed to the current time value), that is `SYSI.*`, not `TIME.GET`.

## Structural Relationships

- **Often co-occurs with**: Logging and telemetry (timestamps on events), metrics collection, any time-dependent logic that first needs the current time, `NETW.*` (timestamped requests or responses)
- **May imply**: The code has time-dependent behavior downstream; a `TIME.GET` with no consumer is dead code or the consumer is not yet visible

## Notes

`TIME.GET` is one of the most ubiquitous operations in any codebase. Logging frameworks, metrics systems, caching layers, session management, and countless other standard patterns retrieve the current time. The atom is low-signal in isolation; its value emerges when data-flow analysis traces where the retrieved time goes. A `TIME.GET` whose value flows into a comparison becomes `TIME.CMP`; one whose value flows into a network request becomes a timestamped communication; one that goes nowhere is noise.
