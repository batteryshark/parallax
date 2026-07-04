# TIME.DELAY: Execution Delay

## Description

Sleep, wait, or delay operations that pause execution for a specified duration. APIs: `time.sleep()`, `Thread.sleep()`, `setTimeout()` used as a pure delay (no callback logic beyond resumption), `usleep()`, `nanosleep()`, `Sleep()` (Windows), `std::this_thread::sleep_for()`. Also includes busy-wait loops that consume CPU cycles to create a delay without calling sleep APIs. The operation suspends the current thread or process for the specified duration, then execution resumes.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Sleep API calls (`time.sleep(300)`, `Thread.sleep(300000)`, `usleep()`), busy-wait loop patterns (`while (Date.now() - start < duration) {}`), delay duration as argument |
| Static Binary | Yes | Sleep function imports, delay duration constants, busy-wait loop structures (tight loops with timing comparisons and no I/O) |
| Runtime/Dynamic | Yes | Observable pauses in execution flow, wallclock gaps between operations with no corresponding I/O, sleep syscalls (`nanosleep`, `SleepEx`), CPU-bound loops with no productive output |

## Disambiguation

- **vs ENVI.TIMING**: `TIME.DELAY` describes the delay as a temporal operation: execution is paused for a duration. `ENVI.TIMING` describes the same delay in the context of environment interaction, detecting analysis via timing measurements or outlasting sandbox analysis windows. When a delay is purely temporal with no environment-interaction context (retry backoff, rate limiting, polling interval), `TIME.DELAY` is sufficient. When the delay is positioned to interact with the analysis environment (pre-payload delay calibrated to sandbox windows, timing measurement to detect debugger slowdown), `ENVI.TIMING` is more precise. Both may apply when a delay serves dual purposes.
- **vs normal async patterns**: Retry backoff, polling intervals, rate limiting, UI debounce, animation frame timing, and connection timeout waits are standard delay patterns. `TIME.DELAY` applies to all of these mechanically, the atom is judgment-free. Context determines whether the delay is routine or notable.
- **vs TIME.SCHED**: `TIME.DELAY` blocks the current execution context for a duration. `TIME.SCHED` schedules a callback for future execution without blocking. `time.sleep(60)` is `TIME.DELAY`. `setTimeout(fn, 60000)` with meaningful callback logic is `TIME.SCHED`.

## Structural Relationships

- **Often co-occurs with**: Whatever behavior follows the delay (the delayed operation), `NETW.*` (delay before network communication), `EXEC.*` (delay before execution), retry/backoff logic
- **May imply**: The code's execution flow is time-sensitive; something needs to happen after a specific duration elapses

## Notes

The duration, placement, and proportionality of the delay are the key structural data. A 100ms delay in a retry loop is proportional to network latency. A 300-second delay in a `postinstall` hook before a network call has no proportional operational justification. A busy-wait loop that achieves the same delay as a sleep call but avoids calling sleep APIs may be deliberately evading detection of sleep-based sandbox evasion. The mechanical behavior is identical, pausing execution, but the implementation choice carries structural information.
