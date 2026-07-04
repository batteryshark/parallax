# PRST.STARTUP: Startup / Login Item Registration

## Description

Adds entries to operating system startup locations that cause code to execute automatically when the system boots or a user logs in. Includes Windows Run/RunOnce registry keys (`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`), macOS LaunchAgents and LoginItems, Linux XDG autostart desktop entries, shell profile modifications (`.bashrc`, `.profile`, `.zshrc`, `.bash_login`), and crontab `@reboot` entries. The registered artifact executes once per boot or login event, then exits (or is not managed by a service supervisor for restart).

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Registry key writes to `Run`/`RunOnce` paths, plist creation targeting `~/Library/LaunchAgents`, file writes to `~/.config/autostart/`, shell profile append/modification operations, `@reboot` crontab entries |
| Static Binary | Yes | Registry path strings, LaunchAgent plist keys (`RunAtLoad`), XDG autostart path strings, shell profile path strings, crontab invocation patterns |
| Runtime/Dynamic | Yes | New registry keys in startup locations, new plist files in LaunchAgents, modified shell profile files (mtime/hash changes), new autostart desktop entries, new `@reboot` crontab lines |

## Disambiguation

- **vs PRST.SCHED**: `PRST.STARTUP` registers code triggered by boot or login events. `PRST.SCHED` registers code triggered by time intervals or specific clock times. A crontab `@reboot` entry is `PRST.STARTUP` (boot-triggered). A crontab `*/5 * * * *` entry is `PRST.SCHED` (interval-triggered). The trigger condition is the distinction: system lifecycle event vs. clock/timer.
- **vs PRST.SERVICE**: `PRST.STARTUP` items execute and exit without OS service supervisor management. `PRST.SERVICE` items are registered with the OS service manager (systemd, Windows SCM, launchd with KeepAlive) and are automatically restarted on failure. A LaunchAgent with `RunAtLoad: true` but no `KeepAlive` is `PRST.STARTUP`. The same plist with `KeepAlive: true` is `PRST.SERVICE`.
- **vs FSYS.WRITE**: Writing a file is `FSYS.WRITE`. Writing a file to a startup location (LaunchAgents, autostart, shell profile) is `FSYS.WRITE` + `PRST.STARTUP`. The persistence atom describes the semantic consequence of the write location.

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (writing the startup entry or script), `EXEC.SHELL` (the registered command invokes a shell), `ENVI.MASQ` (startup entry named to resemble legitimate OS component), `XFRM.*` (registered payload is transformed/encoded)
- **May imply**: The registered code will execute with the logged-in user's privileges on every subsequent login or boot
- **Commonly part of idioms**: Install-and-persist (package installs payload then registers it for startup), shell profile injection (append to `.bashrc`/`.profile` to intercept every interactive shell session)

## Notes

Shell profile modification (`.bashrc`, `.profile`, `.zshrc`) is a particularly subtle form of startup persistence because it executes in the context of every new interactive shell session, not just at login. The modification may be a single line appended to a large file, making it difficult to notice. The content of the appended line and whether it sources external files, sets environment variables (overlapping with `PRST.HOOK` for PATH manipulation), or executes commands directly are key structural observations.
