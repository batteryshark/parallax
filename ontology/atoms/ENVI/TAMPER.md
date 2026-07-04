# ENVI.TAMPER: Self-Integrity Verification

## Description

Code that verifies its own integrity at runtime, checking that its binary, source, bytecode, or in-memory representation has not been modified since distribution. Techniques include computing checksums or hashes of the code's own executable, comparing in-memory code sections against expected values, verifying digital signatures on the binary, detecting instrumentation hooks or patches, and checking for modified function prologues that indicate hooking. The code inspects itself for evidence of modification.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Self-referencing hash computation, file reads of the process's own executable, signature verification of own binary, comparison against embedded expected values |
| Static Binary | Yes | Embedded hash/checksum constants, self-referencing file path construction, code section address references |
| Runtime/Dynamic | Yes | File reads of own executable, memory region checksums, hash comparisons with embedded values |

## Disambiguation

- **vs CRPT.HASH**: CRPT.HASH is the general behavior of computing cryptographic hashes. ENVI.TAMPER is specifically self-directed, the code hashes or verifies itself. When a program hashes an external file for integrity, that's CRPT.HASH. When a program hashes its own code sections, that's ENVI.TAMPER (which may use CRPT.HASH as part of its mechanism).
- **vs ENVI.DEBUG**: Debugger detection checks for attached analysis tools. Tamper detection checks for modifications to the code itself. Some instrumentation (like function hooking) is detectable by both, a hook modifies code (TAMPER) and is typically placed by a debugger or analysis tool (DEBUG). When the detection mechanism checks for code modification, classify as TAMPER. When it checks for debugger presence, classify as DEBUG.

## Structural Relationships

- **Often co-occurs with**: `CRPT.HASH` (hash computation as the verification mechanism), `ENVI.DEBUG` (layered integrity and analysis detection)
- **May imply**: The code has an expected integrity baseline and will alter behavior if that baseline is violated

## Notes

Self-integrity verification appears in DRM, licensing enforcement, game anti-cheat, and security-sensitive applications. It also appears in code that resists analysis via patching or instrumentation. The mechanical behavior is identical, verify own integrity, branch on result. The embedded expected values (hashes, signatures) and the behavior on verification failure are the key structural data points.
