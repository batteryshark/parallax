# TIME.SCHED: In-Process Scheduled Execution

## Description

Sets timers, alarms, or schedules callbacks for future execution within the current process lifetime. APIs: `setTimeout()`/`setInterval()` (JavaScript), `threading.Timer` (Python), `ScheduledExecutorService` (Java), `time.AfterFunc()` (Go), `alarm()` (POSIX), `dispatch_after()` (macOS GCD), `Timer` (C#/.NET). The scheduled execution lives and dies with the process. It does NOT survive process termination. The scheduling operation registers a callback or handler to execute after a specified delay or at recurring intervals, managed by the process's own runtime.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Timer/scheduler API calls (`setTimeout(fn, delay)`, `setInterval(fn, interval)`, `threading.Timer(delay, fn)`, `alarm(seconds)`), callback function references, interval/delay constants |
| Static Binary | Yes | Timer API imports, callback function pointers, delay/interval constants, signal handler registrations (for `alarm()`) |
| Runtime/Dynamic | Yes | Timer registrations in runtime event loops, scheduled callback invocations, periodic execution patterns, SIGALRM signal delivery |

## Disambiguation

- **vs PRST.SCHED**: `TIME.SCHED` is in-process: the scheduled execution is managed by the process's runtime and dies when the process terminates. `PRST.SCHED` is OS-level (cron jobs, Windows Task Scheduler entries, systemd timers, launchd plists) and survives process termination and system reboots. The survivability test: if the scheduling process exits, does the scheduled execution still fire? If yes, `PRST.SCHED`. If no, `TIME.SCHED`.
- **vs TIME.DELAY**: `TIME.DELAY` blocks the current thread for a duration. `TIME.SCHED` registers a callback for future execution without blocking. `time.sleep(60)` pauses for 60 seconds (`TIME.DELAY`). `setTimeout(fn, 60000)` continues execution immediately and runs `fn` later (`TIME.SCHED`).
- **vs EXEC.***: `TIME.SCHED` schedules future execution within the same process. `EXEC.PROC` spawns a new process. When a scheduled callback spawns a new process, both `TIME.SCHED` (the scheduling) and `EXEC.PROC` (the spawning) apply.

## Structural Relationships

- **Often co-occurs with**: Polling loops, periodic health checks, deferred initialization, heartbeat/keepalive patterns, event loop management
- **May imply**: The process has long-running lifecycle expectations; scheduling future execution is meaningful only if the process is expected to remain alive long enough for the callback to fire
- **Commonly part of idioms**: Deferred execution (schedule callback after initialization completes), periodic polling (setInterval for status checks), debounced operations (reset timer on each trigger)

## Notes

The callback content, the delay/interval duration, and the scheduling context are the key structural data. A `setInterval` polling a health endpoint every 30 seconds is a standard operational pattern. A `setTimeout` that fires once after a long delay to execute a network call or shell command follows a different structural pattern. Whether the scheduled execution is one-shot or recurring, and what the callback does when it fires, determine the finding's significance. The in-process constraint means `TIME.SCHED` is inherently bounded, it cannot outlive its host process without cooperation from persistence mechanisms.
