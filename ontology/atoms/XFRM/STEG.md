# XFRM.STEG: Data Embedding in Resources

## Description

Stores code or data within non-code resources: images, audio files, video files, fonts, comments, whitespace patterns, or other files not typically expected to contain executable content. The embedded content is extracted at runtime through a corresponding extraction routine that reads the resource and recovers the embedded data.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Partial | Resource loading code paired with parsing/extraction logic that goes beyond normal resource use (e.g., reading pixel values as bytes, parsing comment fields for encoded data), embedded resources with unusual file sizes or entropy |
| Static Binary | Partial | Resource sections with higher entropy than expected for their file type, resources whose size exceeds what the application visibly uses |
| Runtime/Dynamic | Yes | Resource loading followed by data extraction, decoded content appearing in memory that was not present as a readable artifact |

## Disambiguation

- **vs XFRM.ENCODE**: Encoding transforms data representation within code (a base64 string in source). Steganographic embedding places data within a non-code resource file. The distinction is the carrier: `XFRM.ENCODE` uses code-level string literals; `XFRM.STEG` uses resource files.
- **vs XFRM.PACK**: Packing wraps code in a compressed container that is the entire distributed artifact. Steganographic embedding hides data within a resource that appears to serve a legitimate purpose (an image that is also displayed, a font that is also used for rendering).

## Structural Relationships

- **Often co-occurs with**: `XFRM.ENCODE` (embedded data may also be encoded), `FSYS.READ` (reading the resource file), `LOAD.EVAL` / `EXEC.SHELL` (extracted content fed to execution)
- **May imply**: The artifact includes resource files that serve dual purposes (visual/functional + data carrier)

## Notes

Common steganographic techniques include LSB (least significant bit) embedding in image pixel data, appending data after the end-of-file marker in image formats (JPEG, PNG), embedding data in EXIF metadata fields, and encoding data in whitespace patterns (tabs vs. spaces, trailing spaces). Each technique has a different extraction pattern.
