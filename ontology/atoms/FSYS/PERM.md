# FSYS.PERM: Permission Modification

## Description

Changes file or directory ownership, permissions, or access control lists (ACLs). Includes `chmod`, `chown`, `SetFileAttributes()`, `SetSecurityInfo()`, `icacls`, and equivalent operations across platforms. Modifies who can read, write, execute, or manage a filesystem object.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Permission modification APIs (`os.chmod()`, `fs.chmod()`, `SetFileAttributes()`), permission values (octal modes, ACL structures), target paths |
| Static Binary | Yes | Permission function imports, permission constant values, target path strings |
| Runtime/Dynamic | Yes | Permission change system calls, file metadata updates, ACL modifications |

## Disambiguation

- **vs PRIV.***: `FSYS.PERM` modifies filesystem object permissions. `PRIV.*` atoms change the process's own privilege or identity context. Making a file executable (`chmod +x`) is `FSYS.PERM`. Calling `setuid(0)` is a privilege operation (`PRIV.*`). They may co-occur (change privilege, then modify file permissions).

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (write file then set permissions), `EXEC.*` (set executable permission then execute), `FSYS.HIDDEN` (set hidden attribute)
- **May imply**: The process has ownership or sufficient privilege over the target filesystem object

## Notes

The target path, the before/after permission values, and the direction of change (more restrictive vs. less restrictive) are the key structural data. Making a newly written file executable is a different observation than removing read permissions from a log file.
