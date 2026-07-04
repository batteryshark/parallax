# FSYS.DELETE: File Deletion

## Description

Removes files or directories from the local filesystem. Encompasses single file deletion, recursive directory removal, and secure/overwrite deletion. The target path and the context (what else happened before the deletion) are key structural properties.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Deletion API calls (`os.remove()`, `fs.unlink()`, `shutil.rmtree()`, `DeleteFile()`), target path arguments |
| Static Binary | Yes | Deletion function imports, target path strings |
| Runtime/Dynamic | Yes | File deletion system calls, files disappearing from filesystem, directory entries removed |

## Disambiguation

- **vs EVSN.FORENSIC**: `FSYS.DELETE` is the filesystem operation. `EVSN.FORENSIC` (when it exists in the ontology) describes deletion in the context of evidence removal. A package deleting its own temp files is `FSYS.DELETE`. A package deleting files it wrote during anomalous activity is `FSYS.DELETE` + the evasion lens interpretation.

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (write then delete, staging with cleanup), `FSYS.ARCHIVE` (archive then delete originals), `EXEC.*` (execute then delete, run and clean)
- **May imply**: Something existed at the target path that is no longer needed or no longer wanted

## Notes

The deletion target and timing are the key structural data. Deletion of temp files during normal cleanup is structurally different from deletion of logs, written payloads, or evidence of prior operations.
