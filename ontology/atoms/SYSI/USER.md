# SYSI.USER: User Identity Query

## Description

Queries current username, user ID, group membership, home directory, or enumerates system user accounts. APIs and mechanisms include `os.getlogin()`, `getpass.getuser()`, `os.getuid()`, `os.getgid()` (Python), `os.userInfo()` (Node.js), `getpwuid()`, `getpwnam()` (POSIX), `whoami`, `id` (Unix commands), `net user`, `net localgroup` (Windows commands), `GetUserName` / `LookupAccountSid` (Windows API), `/etc/passwd` reads, `WMI Win32_UserAccount` queries, and Active Directory / LDAP user enumeration. The code retrieves identity metadata about users on the system.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `os.getlogin()`, `getpass.getuser()`, `os.userInfo()`, `whoami` subprocess calls, `net user` invocations, `/etc/passwd` file reads, LDAP query construction |
| Static Binary | Yes | User enumeration API imports, `/etc/passwd` path strings, `net user` command strings, LDAP query strings |
| Runtime/Dynamic | Yes | System calls for user identity (getuid, getpwuid), subprocess execution of user enumeration commands, file reads of `/etc/passwd`, LDAP network traffic |

## Disambiguation

- **vs CRED.\***: `SYSI.USER` queries identity metadata, who the user is, what groups they belong to, what accounts exist. `CRED.*` accesses stored credentials and secrets, passwords, tokens, keys. Reading `whoami` output is `SYSI.USER`. Reading `~/.ssh/id_rsa` is `CRED.SSH`. The boundary is identity metadata vs. authentication material.
- **vs ENVI.ENVCHECK**: When a username or user property is queried and then used to gate behavior (e.g., only execute if user is `root` or matches a specific name), both `SYSI.USER` and `ENVI.ENVCHECK` apply.

## Structural Relationships

- **Often co-occurs with**: `SYSI.OS` (combined system profiling), `CRED.*` (user identity informs credential path selection), `FSYS.ENUM` (enumerating user home directories), `ENVI.ENVCHECK` (user identity feeding activation decisions)
- **May imply**: The code needs to know who is running it or what user accounts exist on the system

## Notes

User identity queries serve many legitimate purposes: permission checks, home directory resolution, audit logging, and multi-user application logic. Enumerating all system accounts (`net user`, `/etc/passwd` parsing) is a broader action than querying the current user. The scope of the query (current user identity vs. full account enumeration) and the destination of the collected data are the key structural observations.
