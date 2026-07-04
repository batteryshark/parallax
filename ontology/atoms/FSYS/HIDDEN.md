# FSYS.HIDDEN: Hidden Storage Mechanisms

## Description

Uses platform-specific filesystem features to store data in locations not visible to standard file listing tools. Mechanisms include:

- **NTFS Alternate Data Streams (ADS)**: attaching data to files via `:stream` syntax (`file.txt:payload`), not shown by standard `dir` or Explorer
- **macOS extended attributes and resource forks**: storing data via `xattr` in custom or Apple-namespaced attributes, or in the legacy resource fork (`/..namedfork/rsrc`)
- **Linux extended attributes**: storing data via `setxattr()`/`getxattr()` in `user.*` or `security.*` namespaces
- **Hidden file attributes**: programmatically setting Windows hidden/system attributes (`SetFileAttributes()`, `attrib +h +s`) or creating dot-prefixed files in unexpected locations on Unix
- **Reserved/device name abuse**: on Windows, using reserved names (`CON`, `NUL`, `AUX`, `COM1`) or trailing dots/spaces in paths that are difficult to enumerate or delete with standard tools

The hidden data exists in a parallel storage layer that requires platform-specific tools or API calls to access.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | ADS path syntax (`:stream`), `xattr`/`setxattr` API calls, `SetFileAttributes()` with hidden/system flags, reserved name usage |
| Static Binary | Yes | ADS path patterns, xattr function imports, hidden attribute constants |
| Runtime/Dynamic | Yes | ADS creation events, extended attribute writes, file attribute modifications, `dir /r` revealing hidden streams |

## Disambiguation

- **vs XFRM.STEG**: Steganography hides data *within the content* of another file (pixels, audio samples, whitespace). `FSYS.HIDDEN` hides data in the *filesystem's own metadata and storage layers*. Steganography requires content-aware analysis; hidden storage requires platform-aware enumeration.
- **vs FSYS.WRITE**: `FSYS.WRITE` targets the primary data stream. `FSYS.HIDDEN` targets parallel storage. Both may co-occur on the same path (visible decoy + hidden payload).

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (visible file + hidden data on same path), `EXEC.*` / `LOAD.*` (hidden data retrieved and executed), `XFRM.ENCODE` / `XFRM.ENCRYPT` (hidden data also encoded/encrypted)
- **May imply**: The code is aware of platform-specific filesystem metadata features

## Notes

Each hidden storage mechanism has specific enumeration tools: `dir /r` for NTFS ADS, `xattr -l` for macOS, `getfattr -d` for Linux extended attributes. The host file (what the hidden data is attached to), the storage mechanism used, and the content of the hidden data are the key structural observations.
