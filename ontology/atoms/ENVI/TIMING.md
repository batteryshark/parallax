# ENVI.TIMING: Execution Timing Control

## Description

Uses execution timing for environment detection or behavior scheduling. Two mechanical aspects: (1) measuring execution timing to detect analysis-induced slowdown (debuggers and emulators measurably slow execution; timing comparisons detect this), and (2) introducing delays into execution flow (sleep calls, busy-wait loops, scheduled future execution). Both involve the code's relationship with execution timing, either observing it or controlling it.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `time.sleep()`, `setTimeout()`, `Thread.sleep()`, `usleep()`, busy-wait loops, `rdtsc` timing comparisons, `performance.now()` deltas |
| Static Binary | Yes | Sleep API imports, timing measurement function references, loop structures with no I/O |
| Runtime/Dynamic | Yes | Observable delays in execution, timing API calls, wallclock gaps between operations |

## Disambiguation

- **vs ENVI.DEBUG**: Timing-based debugger detection (measuring execution speed to detect single-stepping) overlaps. When timing is specifically detecting debugger presence, it is better classified as ENVI.DEBUG. ENVI.TIMING covers general execution delay introduction and timing measurements not specifically targeting debugger detection.
- **vs normal async patterns**: Retry backoff, polling intervals, rate limiting, UI debounce, and animation timers are standard execution timing patterns. ENVI.TIMING applies when delays appear in initialization paths, install hooks, or pre-payload positions with no proportional operational justification, or when timing measurements are used for environment detection.
- **vs TIME.CMP**: `TIME.CMP` checks calendar/clock time (dates, deadlines, time windows). `ENVI.TIMING` controls or measures execution duration (how long something takes, how long to wait).

## Structural Relationships

- **Often co-occurs with**: `ENVI.DEBUG` (timing-based debugger detection), `ENVI.SANDBOX` (timing to detect or outlast sandbox analysis), any atom that follows the delay (the delayed behavior)
- **May imply**: Execution flow includes intentional timing manipulation, either measurement or delay

## Notes

The duration, placement, and proportionality of timing behavior are the key structural data. A 100ms retry delay in a network client is proportional. A 5-minute sleep in an install hook before a network call has no proportional justification in that context. The mechanical behavior is the same, introducing a delay, but the structural context differs.
