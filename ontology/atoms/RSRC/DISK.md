# RSRC.DISK: Disk Space Consumption

## Description

Writing large amounts of data, creating many files, or operations that consume significant disk space or exhaust inode capacity. Includes writing large binary blobs, generating numerous small files, filling temporary directories, log amplification, or any pattern where disk consumption is significant relative to the operation being performed. The atom describes patterns of significant disk space usage, routine file writes proportional to application data are not in scope.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Partial | Large write buffers, file creation in tight loops, write operations without size checks or rotation, repeated append operations without truncation, `/dev/zero` or `/dev/urandom` read-to-file patterns |
| Static Binary | Partial | Large constant write sizes, file creation function calls in loop structures, absence of file size limit checks alongside write paths |
| Runtime/Dynamic | Yes | Disk usage growth, inode consumption, filesystem space alerts, large file creation events, sustained write I/O throughput disproportionate to application behavior |

## Disambiguation

- **vs FSYS.WRITE**: `FSYS.WRITE` is any file write operation. `RSRC.DISK` specifically describes writes notable for their scale, volume, or space consumption. A single config file write is `FSYS.WRITE`. Writing gigabytes of data or creating thousands of files is both `FSYS.WRITE` and `RSRC.DISK`.
- **vs FSYS.TEMP**: Temporary file operations may involve `RSRC.DISK` if the volume of temporary data is significant. Creating a single temp file is `FSYS.TEMP`; filling `/tmp` with gigabytes of data is both `FSYS.TEMP` and `RSRC.DISK`.
- **vs FSYS.ARCHIVE**: Extracting archives that expand to significantly larger sizes (zip bombs, decompression bombs) is both `FSYS.ARCHIVE` (the extraction operation) and `RSRC.DISK` (the space consumption pattern).

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (the underlying write operations), `FSYS.TEMP` (temporary directories as the target for bulk writes), `FSYS.ARCHIVE` (archive extraction producing large disk footprint), `RSRC.MEM` (in-memory data structures flushed to disk)
- **May imply**: Filesystem capacity pressure, potential denial of service for other processes or the host OS, inode exhaustion on filesystems with inode limits

## Notes

The key structural data points are: total volume of data written, number of files created, target directory, whether any size or count limits are enforced, and the relationship between the data written and the task being performed. A database engine writing transaction logs is structurally different from a library writing random data to `/tmp` during package installation. Whether disk consumption is bounded (known maximum), proportional to input, or unbounded is a critical structural property.
