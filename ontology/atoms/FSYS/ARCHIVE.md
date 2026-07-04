# FSYS.ARCHIVE: Archive Operations

## Description

Creates, extracts, or manipulates compressed archives: zip, tar, gzip, bzip2, 7z, rar, and equivalent formats. Archive creation bundles multiple files into a single container, often with compression. Extraction recovers files from an archive container. The source paths (for creation) or extraction target (for decompression) are key structural properties.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Archive library imports (`zipfile`, `tarfile`, `archiver`, `zlib`), archive creation/extraction calls, source/target path arguments |
| Static Binary | Yes | Archive library function imports, archive format magic bytes, path string arguments |
| Runtime/Dynamic | Yes | Archive file creation on disk, compression/decompression operations, multiple files bundled or extracted |

## Disambiguation

- **vs XFRM.PACK**: `XFRM.PACK` wraps code in a compressed/self-extracting container for execution. `FSYS.ARCHIVE` creates or extracts data archives for storage or transfer. The distinction is whether the archive contains code intended for immediate execution (PACK) or data intended for storage/transfer (ARCHIVE).

## Structural Relationships

- **Often co-occurs with**: `FSYS.ENUM` (enumerate files before archiving), `NETW.*` (transmit archive), `FSYS.READ` (read files into archive), `FSYS.DELETE` (delete originals after archiving)
- **May imply**: Multiple files are being consolidated into a single transferable unit

## Notes

The source paths for archive creation and the size/content of the resulting archive are the primary structural data. Archiving user data directories produces a large archive with many files. Archiving a single configuration file produces a small focused archive. The scope of what's archived is an important observation.
