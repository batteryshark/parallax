# FSYS.READ: File Read

## Description

Reads the contents of a file from the local filesystem. Encompasses opening a file, reading its data (full or partial), and using the contents within the program. The target file path, the amount of data read, and how the content is subsequently used are key structural properties.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | File open/read API calls (`open()`, `readFile()`, `fread()`, `FileInputStream`), file path strings as arguments |
| Static Binary | Yes | File I/O function imports, file path string literals in data sections |
| Runtime/Dynamic | Yes | File descriptor opens, read system calls, file access timestamps updated |

## Disambiguation

- **vs FSYS.SENSITIVE**: `FSYS.READ` is the operation. `FSYS.SENSITIVE` is a classification based on the target path. Reading `~/.ssh/id_rsa` is both `FSYS.READ` (the operation) and `FSYS.SENSITIVE` (the target). Reading `./config.json` is `FSYS.READ` only.
- **vs CRED.***: When the file being read is a known credential store, both `FSYS.READ` and the appropriate `CRED.*` subtype apply. FSYS captures the method; CRED captures the target classification.

## Structural Relationships

- **Often co-occurs with**: `FSYS.ENUM` (locating files before reading), `NETW.*` (transmitting read data), `XFRM.ENCODE` (encoding read data), `FSYS.SENSITIVE` (when targeting sensitive paths)
- **May imply**: The target file exists and is accessible with current process permissions

## Notes

The target path is the most important structural data. File reads are ubiquitous in software. The analytical value comes entirely from WHAT is being read and WHERE that data flows afterward.
