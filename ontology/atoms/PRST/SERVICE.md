# PRST.SERVICE: System Service Registration

## Description

Registers code as an operating system service or daemon managed by the OS service supervisor. Includes systemd service units (`/etc/systemd/system/`, user units in `~/.config/systemd/user/`), Windows services (registered via `sc create`, Service Control Manager API), and macOS launchd daemons/agents with `KeepAlive` or `RunAtLoad` combined with restart directives. The OS service supervisor monitors the registered service and automatically restarts it on failure, crash, or system boot. The service runs continuously as a managed, long-lived process.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Systemd unit file creation (`[Service]` sections with `ExecStart`, `Restart=always`), `sc create` / `New-Service` invocations, Windows service registration API calls (`CreateService`), launchd plist creation with `KeepAlive: true`, `systemctl enable` commands |
| Static Binary | Yes | Systemd unit file path strings, SCM API imports (`advapi32.dll` service functions), launchd plist keys (`KeepAlive`, `RunAtLoad`), `sc.exe` command strings |
| Runtime/Dynamic | Yes | New systemd units visible in `systemctl list-units`, new Windows services in `sc query`, new launchd services in `launchctl list`, service processes running under service supervisor parentage |

## Disambiguation

- **vs PRST.STARTUP**: `PRST.SERVICE` items are managed by the OS service supervisor: they are monitored, automatically restarted on failure, and have defined lifecycle management (start, stop, restart, enable, disable). `PRST.STARTUP` items execute on boot/login and are not restart-managed. A systemd unit with `Restart=always` is `PRST.SERVICE`. A shell profile line is `PRST.STARTUP`.
- **vs PRST.SCHED**: `PRST.SERVICE` runs continuously as a long-lived process. `PRST.SCHED` runs discretely at scheduled times and exits between runs. A systemd service is `PRST.SERVICE`. A cron job is `PRST.SCHED`.
- **vs EXEC.PROC (orphaned)**: An orphaned process (`nohup`, `setsid`, double-fork) runs independently but is not registered with the OS service supervisor and will not be restarted on failure or reboot. `PRST.SERVICE` includes OS-level registration for supervised lifecycle management.

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (writing the unit file or service binary), `ENVI.MASQ` (service registered with a name mimicking legitimate OS services), `EXEC.PROC` (the service binary execution), `FSYS.PERM` (setting executable permissions on service binaries)
- **May imply**: Code will run continuously, survive reboots, and automatically restart after crashes, until the service registration is explicitly removed
- **Commonly part of idioms**: Persistent backdoor (service runs continuously, maintains C2 channel), self-healing implant (service restarts automatically after termination attempts)

## Notes

The service configuration parameters are key structural data: restart policy (`Restart=always`, `Restart=on-failure`), execution identity (user/group the service runs as), and dependencies (what the service waits for before starting). A service running as root with `Restart=always` and no dependency on user login is the most persistent form of service-level persistence: it runs from boot and recovers from termination automatically.
