# XFRM.PACK: Packing / Compression

## Description

Wraps code or data in a compressed, packed, or self-extracting container. The original content is recoverable by unpacking or decompressing, but is not directly readable in the distributed artifact. Packing introduces a layer of indirection between the artifact as distributed and its executable logic.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Partial | Self-extracting script patterns (gzipped blob + decompression + eval), embedded compressed data with decompression routine |
| Static Binary | Yes | Packer signatures (UPX header, ASPack, Themida), high-entropy sections, compressed data preceding an unpacking stub, abnormal section names or sizes |
| Runtime/Dynamic | Yes | Unpacking/decompression operations at process startup, memory allocation for decompressed content, original code materializing in memory |

## Disambiguation

- **vs XFRM.ENCODE**: Encoding transforms data representation (base64 makes binary data text-safe). Packing compresses data for size or wraps it in an extraction container. The functional distinction: encoding preserves the data in a different representation; packing compresses or wraps the data so it must be decompressed/extracted before use.
- **vs LOAD.MEMCHAIN**: Packing produces an artifact that is unpacked before analysis, the unpacked content is the analysis target. In-memory execution chains decode and execute stages without producing a recoverable artifact. A UPX-packed binary unpacks to a file or memory image that can be dumped. A multi-stage eval chain produces no dumpable intermediate artifact.

## Structural Relationships

- **Often co-occurs with**: `XFRM.RENAME` / `XFRM.CTRLFLOW` (packing often applied alongside other transformations), `LOAD.EVAL` (script-level packing: compressed blob → decompress → eval)
- **May imply**: The distributed artifact differs structurally from the original compiled/written code

## Notes

Binary packers (UPX, ASPack, Themida, VMProtect) have well-documented signatures that tools like Detect It Easy (DIE) or PEiD can identify. Script-level packing (gzip+eval, zlib+exec) follows similar patterns but lacks standardized signature databases.
