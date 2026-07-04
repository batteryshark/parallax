# FSYS.WRITE: File Write

## Description

Creates new files or modifies existing files on the local filesystem. Encompasses opening files for writing, writing data (creating, appending, overwriting), and closing. The target path, the content written, and the sequence of operations around the write are key structural properties.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | File write API calls (`open(..., 'w')`, `writeFile()`, `fwrite()`, `FileOutputStream`), file path and content arguments |
| Static Binary | Yes | File write function imports, target path strings, content to be written in data sections |
| Runtime/Dynamic | Yes | File descriptor opens with write flags, write system calls, new files appearing on filesystem, file modification timestamps |

## Disambiguation

- **vs FSYS.TEMP**: `FSYS.WRITE` is the general operation. `FSYS.TEMP` applies specifically when the target is a temp directory (`/tmp`, `%TEMP%`, `/var/tmp`). A write to `/tmp/payload.sh` is both `FSYS.WRITE` and `FSYS.TEMP`.
- **vs FSYS.HIDDEN**: `FSYS.WRITE` covers the primary data stream. `FSYS.HIDDEN` covers writes to alternate streams, extended attributes, or hidden storage layers. Writing visible content AND hidden data to the same path triggers both.

## Structural Relationships

- **Often co-occurs with**: `EXEC.PROC` / `EXEC.SHELL` (write then execute, dropper pattern), `FSYS.PERM` (write then change permissions), `NETW.HTTP` (download then write), `FSYS.TEMP` (writing to temp paths)
- **May imply**: The process has write permissions to the target directory

## Notes

The content written and the subsequent operations on the written file are more significant than the write itself. A write followed by execution is structurally different from a write followed by a read-back for verification. The target path's location (package tree, temp directory, system directory, user home) is the primary contextual data.
