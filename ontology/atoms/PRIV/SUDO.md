# PRIV.SUDO: Privilege Elevation Utility Invocation

## Description

Executes commands via `sudo`, `runas`, `pkexec`, `doas`, or other OS-provided privilege elevation utilities. Transitions execution context from the current user identity to a higher-privilege identity (typically root/Administrator). The elevation utility authenticates the request (via cached credentials, password prompt, or passwordless configuration) and then executes the supplied command under the elevated identity.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `sudo`, `runas`, `pkexec`, `doas` command strings in shell invocations, `subprocess` calls with elevation utility prefixes, sudoers file path references (`/etc/sudoers`, `/etc/sudoers.d/`) |
| Static Binary | Yes | Elevation utility path strings (`/usr/bin/sudo`, `runas.exe`), sudoers path strings, command construction with elevation prefix |
| Runtime/Dynamic | Yes | Elevation utility process spawning, authentication prompts or credential cache hits, child process running under elevated identity visible in process listings |

## Disambiguation

- **vs PRIV.SUID**: `PRIV.SUDO` uses an OS-provided elevation utility to run a specific command under an elevated identity. `PRIV.SUID` sets a filesystem permission attribute on an executable so it always runs as its owner. SUDO is per-invocation elevation through a utility; SUID is a persistent filesystem attribute that affects all future executions of that binary.
- **vs PRIV.ACCOUNT**: `PRIV.SUDO` elevates privilege for a specific command execution, the elevated context is transient. `PRIV.ACCOUNT` creates or modifies persistent identity records (user accounts, group memberships) in the OS authentication subsystem.
- **vs EXEC.SHELL / EXEC.PROC**: When `sudo` prefixes a shell command, both `PRIV.SUDO` (the elevation) and `EXEC.SHELL` or `EXEC.PROC` (the execution) apply. The elevation and the execution are separate observable behaviors.

## Structural Relationships

- **Often co-occurs with**: `EXEC.SHELL` (sudo prefixing shell commands), `EXEC.PROC` (sudo launching binaries), `PKGM.INSTALL` (elevated package installation), `FSYS.WRITE` (elevated file writes to protected paths), `PRIV.ACCOUNT` (elevated account manipulation)
- **May imply**: The current execution context lacks sufficient privileges for the intended operation and is requesting escalation

## Notes

The authentication mechanism matters structurally: passwordless sudo (configured via `NOPASSWD` in sudoers) requires no interactive input, making it viable for automated or scripted escalation. Whether the sudoers configuration is being read, modified, or relied upon is a distinct observable. Modification of sudoers (`/etc/sudoers`, `/etc/sudoers.d/`) to add passwordless entries is itself a `PRIV.SUDO` + `FSYS.WRITE` finding.
