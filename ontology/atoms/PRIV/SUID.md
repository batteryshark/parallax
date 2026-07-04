# PRIV.SUID: SUID / SGID Permission Modification

## Description

Sets or modifies SUID (Set User ID) or SGID (Set Group ID) bits on executables. SUID causes the executable to run as its owner (often root) regardless of who invokes it. SGID causes the executable to run with the group privileges of the file's group owner. Also covers identifying and cataloguing existing SUID/SGID binaries on the system, enumerating the set of binaries that already run with elevated privileges.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `chmod` calls with `u+s`, `g+s`, `4755`, `2755`, or equivalent octal modes; `find` commands searching for SUID/SGID binaries (`-perm -4000`, `-perm -2000`); `stat` calls checking permission bits |
| Static Binary | Yes | Chmod mode constants with setuid/setgid flags, SUID search command strings, permission bit mask constants |
| Runtime/Dynamic | Yes | Permission bit changes on executables visible via filesystem monitoring, `find` scans across filesystem for SUID binaries, new SUID binaries appearing in monitored directories |

## Disambiguation

- **vs PRIV.SUDO**: `PRIV.SUID` sets a persistent filesystem attribute that causes a binary to always execute as its owner. `PRIV.SUDO` invokes an elevation utility for a specific command execution. SUID is a standing permission; SUDO is per-invocation elevation.
- **vs FSYS.PERM**: `FSYS.PERM` covers general file permission modifications. `PRIV.SUID` specifically covers the SUID/SGID bits, the subset of permission changes that affect execution identity. Setting `chmod 755` is `FSYS.PERM`. Setting `chmod 4755` is `PRIV.SUID` (and also `FSYS.PERM` for the base permissions).
- **vs PRIV.CAP**: Capabilities provide granular privilege assignment to binaries without full SUID-root. `PRIV.SUID` grants the binary full execution-as-owner; `PRIV.CAP` grants specific capability subsets.

## Structural Relationships

- **Often co-occurs with**: `FSYS.PERM` (SUID is a permission modification), `FSYS.WRITE` (writing the binary before setting SUID), `EXEC.PROC` (executing existing SUID binaries), `FSYS.ENUM` (enumerating SUID binaries on the system)
- **May imply**: The code is either creating a new persistent privilege escalation path or mapping existing ones

## Notes

Enumeration of existing SUID binaries is a distinct behavior from setting SUID bits. Both are `PRIV.SUID`, the atom covers the full scope of SUID-related operations. The target binary matters structurally: setting SUID on a shell interpreter (`/bin/bash`, `/bin/sh`) or a scripting language interpreter (`python`, `perl`) creates an unrestricted privilege escalation path, while setting SUID on a narrowly-scoped utility is more constrained.
