# PRIV.ACCOUNT: OS Identity Record Modification

## Description

Creates, modifies, or elevates user accounts, group memberships, or identity configurations in the OS authentication subsystem. Includes account creation (`useradd`, `adduser`, `net user /add`, `New-LocalUser`), group manipulation (adding users to `sudo`, `wheel`, `Administrators`, `docker`, or other privileged groups), authentication database modification (direct edits to `/etc/passwd`, `/etc/shadow`, SAM database, or LDAP directory entries), account enablement (activating disabled built-in accounts such as the Windows `Administrator` or `Guest` account), credential reset (changing passwords on existing accounts), and service account creation. Created or modified accounts persist independently of the process that changed them, surviving reboot, package removal, and process termination.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Account management commands (`useradd`, `adduser`, `net user`, `usermod`, `groupadd`), group membership modification (`usermod -aG`, `net localgroup ... /add`), direct writes to `/etc/passwd`, `/etc/shadow`, or SAM paths, Windows account management API calls (`NetUserAdd`, `NetLocalGroupAddMembers`) |
| Static Binary | Yes | Account management utility path strings, auth database file paths, Windows account API imports, group name string constants (`sudo`, `wheel`, `Administrators`) |
| Runtime/Dynamic | Yes | New entries in `/etc/passwd` or equivalent, group membership changes, account creation events in auth logs (`/var/log/auth.log`, Windows Security Event Log), new user profiles on disk |

## Disambiguation

- **vs PRIV.TOKEN**: `PRIV.ACCOUNT` modifies persistent identity records in the OS authentication subsystem, accounts and group memberships that survive indefinitely. `PRIV.TOKEN` modifies ephemeral in-process identity through token manipulation, the identity change lasts only for the process or session lifetime.
- **vs PRST (Persistence)**: Account creation has persistence characteristics, a created account survives indefinitely until explicitly removed. However, the primary behavior is identity modification in the auth subsystem, not execution scheduling or survival mechanism installation. If the created account is combined with a persistence mechanism (`PRST.STARTUP`, `PRST.SERVICE`), both atoms apply.
- **vs CRED (Credential Access)**: `PRIV.ACCOUNT` writes to auth databases to create or modify identity records. `CRED.*` reads from credential stores to harvest existing credentials. Writing `/etc/shadow` to add a new account is `PRIV.ACCOUNT`. Reading `/etc/shadow` to extract password hashes is `CRED.*`.

## Structural Relationships

- **Often co-occurs with**: `PRIV.SUDO` (elevation needed to modify accounts), `EXEC.SHELL` (account commands executed via shell), `FSYS.WRITE` (direct auth database writes), `PRST.SERVICE` (service account paired with service installation), `ENVI.MASQ` (account named to resemble system service)
- **May imply**: The code is creating persistent access that is independent of the code's own lifecycle

## Notes

The distinction between using OS account management utilities (`useradd`, `net user`) and directly manipulating auth databases (`/etc/passwd`, `/etc/shadow`, SAM) is a structural observation. Direct database manipulation bypasses logging and validation that the standard utilities enforce. The account properties (name, group memberships, shell, home directory, password/key configuration) determine the scope of access the new or modified identity provides. Accounts with names mimicking system services (e.g., `syslogd`, `crond`, `svchost`) are structurally notable as they may be designed to avoid casual scrutiny.
