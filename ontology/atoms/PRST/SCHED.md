# PRST.SCHED: Scheduled Task Registration

## Description

Creates operating system-level scheduled tasks that execute code at specified times or intervals, persisting across process termination and system reboots. Includes cron jobs (time-pattern entries in crontab), Windows Task Scheduler tasks (via `schtasks.exe` or COM API), macOS launchd plists with `StartInterval` or `StartCalendarInterval`, and `at` jobs (one-shot future execution). The OS scheduler manages execution independently of the process that created the task, the creating process can terminate and the scheduled task will still fire.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Crontab manipulation (`crontab -l`, `crontab -e`, direct `/var/spool/cron` writes), `schtasks /create` invocations, Task Scheduler COM API calls, launchd plist creation with `StartInterval`/`StartCalendarInterval`, `at` command invocations |
| Static Binary | Yes | Crontab path strings, `schtasks.exe` references, Task Scheduler CLSID constants, launchd plist keys for interval scheduling |
| Runtime/Dynamic | Yes | New crontab entries, new Task Scheduler tasks visible in `schtasks /query`, new launchd plists with scheduling keys, `atq` job listings |

## Disambiguation

- **vs PRST.STARTUP**: `PRST.SCHED` is triggered by time (intervals, calendar patterns, specific future moments). `PRST.STARTUP` is triggered by system lifecycle events (boot, login). The distinguishing test: does it fire because the clock reached a certain time, or because the system started? A crontab `@reboot` entry is `PRST.STARTUP`; a crontab `0 * * * *` entry is `PRST.SCHED`.
- **vs TIME.SCHED (future atom)**: `PRST.SCHED` is OS-level, the scheduled task survives process termination, survives reboots, and is managed by the OS scheduler. Process-internal timing (`setTimeout`, `setInterval`, `time.sleep` loops, `threading.Timer`) dies when the process exits. The survival test: terminate the creating process; does the scheduled action still fire? If yes, `PRST.SCHED`. If no, it is process-internal timing.
- **vs PRST.SERVICE**: `PRST.SCHED` executes discretely at scheduled times (runs, completes, exits). `PRST.SERVICE` runs continuously under service supervisor management. A cron job that runs a script every hour is `PRST.SCHED`. A systemd service with `Restart=always` is `PRST.SERVICE`.

## Structural Relationships

- **Often co-occurs with**: `EXEC.SHELL` (scheduled task invokes a shell command), `EXEC.PROC` (scheduled task launches a binary), `FSYS.WRITE` (writing the task definition file), `NETW.*` (scheduled task phones home or polls for commands)
- **May imply**: Code will execute repeatedly at attacker-controlled intervals, independent of any user action, until the task is explicitly removed
- **Commonly part of idioms**: Polling backdoor (scheduled task periodically contacts C2), periodic exfiltration (scheduled task collects and transmits data on interval), scheduled dropper (task downloads and executes updated payloads at intervals)

## Notes

The schedule interval and the command executed are the two critical structural data points. A task running every minute executing a network call is structurally different from a task running weekly executing a cleanup script. The task's registered identity (name, description) and whether it mimics legitimate system maintenance tasks are also relevant observations.
