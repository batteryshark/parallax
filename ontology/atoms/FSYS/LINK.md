# FSYS.LINK: Symbolic/Hard Link Manipulation

## Description

Creates, modifies, or follows symbolic links (symlinks) or hard links. Symlinks create a filesystem entry that points to another path (which may or may not exist). Hard links create additional directory entries pointing to the same inode. Link manipulation can redirect filesystem operations to paths different from what the apparent path suggests.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Symlink/hardlink creation APIs (`os.symlink()`, `fs.symlink()`, `CreateSymbolicLink()`), source and target path arguments |
| Static Binary | Yes | Link function imports, path string pairs (link path + target path) |
| Runtime/Dynamic | Yes | New symlink/hardlink entries on filesystem, link resolution chains |

## Disambiguation

- **vs FSYS.WRITE**: Writing creates or modifies file content. Link creation creates a new directory entry that references another path. A symlink contains no file content itself, it's a pointer.

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (link redirect followed by write to the linked target), `FSYS.READ` (link followed to read from a redirected target), `FSYS.PERM` (link permission manipulation)
- **May imply**: The code is creating path indirection; one path resolves to a different location

## Notes

Symlink attacks (TOCTOU races, path traversal via symlinks) exploit the indirection property: the apparent target of an operation can be redirected by manipulating the symlink between the check and the use. The source path, target path, and timing of link creation relative to other filesystem operations are the key structural data.
