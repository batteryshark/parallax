# FSYS.TEMP: Temporary File Operations

## Description

Creates, writes, or operates on files in temporary directories (`/tmp`, `/var/tmp`, `%TEMP%`, `$TMPDIR`, or platform-specific equivalents). Temp directories are writable by all users, expected to contain arbitrary transient content, and typically not monitored. The file content, naming pattern, and subsequent operations on the temp file are the key structural properties.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Temp directory path references (`/tmp/`, `%TEMP%`, `tempfile.mktemp()`, `os.tmpdir()`), file creation in temp locations |
| Static Binary | Yes | Temp path string literals, temp file API function imports |
| Runtime/Dynamic | Yes | File creation events in temp directories, temp file content and naming |

## Disambiguation

- **vs FSYS.WRITE**: `FSYS.TEMP` is a specialization of `FSYS.WRITE` where the target is a temp directory. Both apply when writing to temp. `FSYS.TEMP` specifically notes the temp-directory context.
- **vs normal temp usage**: Nearly all software uses temp files for caches, build intermediates, download staging, and crash recovery. `FSYS.TEMP` captures the observation; lenses determine significance based on content and subsequent operations.

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (the write operation), `EXEC.PROC` / `EXEC.SHELL` (execute the temp file), `NETW.HTTP` (download content to temp before use), `FSYS.DELETE` (clean up temp files after use)
- **May imply**: The code needs a writable location for transient data

## Notes

The combination of temp file write + execution is structurally distinctive and recognized across multiple lenses. The temp file content (binary, script, data), naming pattern (predictable vs. random), and lifecycle (persists vs. cleaned up) are all structural observations.
