# MCD Lens: FSYS (Filesystem Operations) Verification

Investigation questions for FSYS findings.

## General: Any FSYS Atom

1. **What is the full resolved path?** Trace path construction to its origin (hardcoded, environment variable, user input, OS API) and resolve to the actual location. `[lens-neutral]`

2. **Does the package have a plausible functional reason to access this path?** Map the accessed path against the package's stated purpose. `[MCD]`

3. **What is the full operation sequence?** Reconstruct the chain: enumerate → read → archive → transmit → delete. The sequence determines the pattern. `[lens-neutral]`

4. **When in the lifecycle does this execute?** Install hooks, import-time, background threads vs. callable functions. `[lens-neutral]`

## FSYS.WRITE

5. **Is the write followed by execution of the written file?** The single highest-value question for temp file writes. `[lens-neutral]`

## FSYS.DELETE

6. **Is deletion targeting files the package itself wrote during anomalous activity?** Deletion of temp files, logs, or downloaded content sequenced after write/archive operations. `[MCD]`

## FSYS.CLIPBOARD

7. **Is clipboard access in a callable function or autonomous code?** Explicit function call from consuming application vs. background thread, timer, or import-time hook. `[lens-neutral]`

## FSYS.HIDDEN

8. **What platform mechanism is used, and what is stored?** Identify the API, host file/path, and content of hidden data. `[lens-neutral]`

9. **Is the hidden data read back by the same package?** If the package writes and reads its own hidden data, determine what it's used for. `[lens-neutral]`

10. **Does the host file belong to the package or another component?** Hidden data attached to system files or other packages' files vs. own files. `[lens-neutral]`

## FSYS.ARCHIVE

11. **What directory is being archived, and where is the archive written?** User data directories to temp is pre-exfiltration staging. Own build output is expected. `[lens-neutral]`

## FSYS.SENSITIVE

12. **Does data from the sensitive path flow to a network transmission?** Trace through the codebase: directly, via variable, or through encode/serialize. `[MCD]`

## Cross-Cutting

13. **Are path strings obfuscated or constructed to evade analysis?** Paths assembled via concatenation, base64 decoding, or char code arrays co-indicate `XFRM.*`. `[lens-neutral]`

14. **Has this path pattern appeared in prior supply chain incidents?** Cross-reference against known IOCs. `[MCD]`
