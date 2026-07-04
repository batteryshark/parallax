# FSYS.SENSITIVE: Sensitive Path Access

## Description

Accesses filesystem locations that are known to contain sensitive data by their path structure: SSH directories (`~/.ssh/`), cloud credential files (`~/.aws/credentials`, `~/.azure/`, `~/.config/gcloud/`), browser profile directories, password database files, keychain/credential manager stores, certificate stores, and similar well-known paths. The path itself (not the content) triggers this classification. The content may be credentials (`CRED.*`), configuration, certificates, or other sensitive data.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Well-known sensitive path strings (`~/.ssh/`, `~/.aws/credentials`, `Login Data`, `key4.db`), path construction targeting these locations |
| Static Binary | Yes | Sensitive path string literals in data sections |
| Runtime/Dynamic | Yes | File access to known sensitive paths, directory enumeration of credential stores |

## Disambiguation

- **vs FSYS.READ / FSYS.WRITE / FSYS.ENUM**: `FSYS.SENSITIVE` is a path classification that co-occurs with the operation atom. Reading `~/.ssh/id_rsa` is `FSYS.READ` + `FSYS.SENSITIVE`. Enumerating `~/.aws/` is `FSYS.ENUM` + `FSYS.SENSITIVE`.
- **vs CRED.***: `FSYS.SENSITIVE` identifies the path as belonging to a sensitive location. `CRED.*` identifies the content as credential material. They overlap when the sensitive path contains credentials (which is common) but `FSYS.SENSITIVE` also covers non-credential sensitive data (certificates, private configs, browser history).

## Structural Relationships

- **Often co-occurs with**: `FSYS.READ` (reading from the sensitive path), `FSYS.ENUM` (enumerating the sensitive directory), `CRED.*` (credential content at the path), `NETW.*` (transmitting data read from the sensitive path)
- **May imply**: The code has knowledge of well-known sensitive filesystem locations

## Notes

The set of "sensitive paths" is platform-dependent. On Linux/macOS: `~/.ssh/`, `~/.gnupg/`, `~/.aws/`, `~/.config/gcloud/`, browser profile directories under `~/.mozilla/` or `~/Library/Application Support/`. On Windows: `%USERPROFILE%\.ssh\`, credential manager stores, browser profile directories under `%LOCALAPPDATA%`. Hardcoded absolute paths to these locations (as opposed to constructing them from `$HOME` or `%USERPROFILE%`) are a structural observation worth noting.
