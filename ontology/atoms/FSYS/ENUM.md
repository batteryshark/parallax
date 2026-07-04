# FSYS.ENUM: Directory Enumeration

## Description

Lists directory contents, walks directory trees, or searches for files matching patterns. Produces a list of filesystem paths or file metadata. May target specific directories, recursively walk entire subtrees, or search for files by name, extension, size, or modification time.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Directory listing APIs (`os.listdir()`, `fs.readdir()`, `os.walk()`, `glob()`, `FindFirstFile()`), path arguments, filter patterns |
| Static Binary | Yes | Directory enumeration function imports, search path strings, file pattern strings |
| Runtime/Dynamic | Yes | Directory read system calls, file metadata queries, enumeration of directory entries |

## Disambiguation

- **vs FSYS.READ**: Enumeration lists what files exist in a directory. Reading retrieves the content of a specific file. Enumeration often precedes targeted reads, discovering what's available before accessing specific items.
- **vs SYSI.***: System inspection (`SYSI.*`) gathers information about the host system (OS version, hardware, network config). Directory enumeration (`FSYS.ENUM`) discovers what files exist on the filesystem. They are complementary, SYSI is system-level, FSYS.ENUM is filesystem-level.

## Structural Relationships

- **Often co-occurs with**: `FSYS.READ` / `FSYS.SENSITIVE` (enumerate then read targeted files), `FSYS.ARCHIVE` (enumerate then archive matching files), `CRED.*` (enumerate credential store locations)
- **May imply**: The code is discovering filesystem contents rather than operating on known paths

## Notes

The directories being enumerated are the primary structural data. Enumeration of the package's own install tree is functionally expected. Enumeration of user home directories, credential stores, browser profiles, or system configuration directories indicates the code is searching for targets beyond its own scope.
