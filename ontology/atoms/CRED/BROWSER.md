# CRED.BROWSER: Browser Credential Access

## Description

Reads browser-managed data stores: password databases, cookie stores, session storage, saved form data, or extension data. Targets browser profile directories for Chrome, Firefox, Safari, Edge, Brave, and other browsers. Browser credential stores use platform-specific formats (SQLite databases, JSON files, encrypted blobs) and locations (per-browser profile directories).

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Browser profile path construction (`~/Library/Application Support/Google/Chrome/`, `%LOCALAPPDATA%\Google\Chrome\User Data\`), SQLite database opens of `Login Data`, `Cookies`, `Web Data`, `logins.json`, `key4.db` |
| Static Binary | Yes | Browser profile path strings, SQLite library imports, browser-specific filenames |
| Runtime/Dynamic | Yes | File reads from browser profile directories, SQLite queries against browser databases, decryption API calls for encrypted credential fields |

## Disambiguation

- **vs CRED.TOKEN**: `CRED.BROWSER` accesses browser-managed credential stores within the browser's profile directory. `CRED.TOKEN` accesses standalone token files on disk. Reading Chrome's `Login Data` is BROWSER. Reading `~/.config/gh/hosts.yml` is TOKEN.
- **vs FSYS.SENSITIVE**: Browser profile directories are sensitive paths. Both `CRED.BROWSER` and `FSYS.SENSITIVE` apply when accessing browser profile content.

## Structural Relationships

- **Often co-occurs with**: `FSYS.READ` (reading the database files), `FSYS.ENUM` (enumerating browser profiles), `CRPT.*` (decrypting encrypted credential fields), `NETW.*` (transmitting extracted data), `CRED.KEYCHAIN` (on macOS, Chrome uses Keychain for the master encryption key)
- **May imply**: The code has knowledge of browser-specific file paths and data formats

## Notes

Modern browsers encrypt stored credentials. Chrome on macOS uses the Keychain; on Windows, DPAPI; on Linux, a locally-derived key. Firefox uses NSS (Network Security Services) with `key4.db`. Extracting usable credentials requires both the database file and the encryption key/mechanism: the presence of BOTH in the code path is a stronger structural observation than either alone.
