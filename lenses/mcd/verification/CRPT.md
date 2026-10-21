# MCD Lens: CRPT (Cryptographic Operations) Verification

## General: Any CRPT Atom

1. **Is there a declared cryptographic dependency in the package manifest?** Undeclared crypto operations that cannot be attributed to a manifest entry indicate hand-rolled implementation or smuggled code. `[lens-neutral]`

2. **Does the scope of cryptographic operations match the package's stated purpose?** Enumerate what the package claims to do and assess whether the observed crypto is necessary for that purpose. `[lens-neutral]`

3. **What is the key lifecycle?** Where is key material generated, stored, used, and destroyed? Key material transmitted outbound, persisted in cleartext, or derived from environment-specific identifiers is structurally notable. `[lens-neutral]`

4. **Does the crypto operation precede, follow, or co-occur with a network call?** Crypto before network = data preparation for transmission. Crypto after network = decryption of received content. `[lens-neutral]`

5. **Is the crypto operation reachable from a non-interactive execution path?** Operations reachable from install hooks, import-time execution, or background threads warrant higher scrutiny than those behind explicit user action. `[MCD]`

## CRPT.CUSTOM

6. **Can the implementation be matched to a named algorithm specification?** Identify the algorithm. Determine whether it matches a known standard, a known weak cipher, or no recognizable scheme. `[lens-neutral]`

7. **Why was a library not used?** Is there a documented reason for avoiding crypto library dependencies? Absence of crypto imports while crypto operations are present is the primary CUSTOM detection signal. `[MCD]`

## CRPT.CERT

8. **Which specific certificate operation is performed?** Loading for verification, disabling verification entirely, installing a new root CA, or replacing an existing CA. Each has different structural implications. `[lens-neutral]`

## CRPT.SYMENC

9. **Is the IV or nonce random, fixed, or derived, and what does the algorithm require?** Distinguish uniqueness from unpredictability; counter nonces can be appropriate, while nonce reuse under one GCM key is a serious failure. Trace the source and reuse scope without inferring intent from the construction alone. `[lens-neutral]`

## CRPT.ASYMENC

10. **Where does the public key originate?** User-provided, library-provided, or hardcoded? Hardcoded foreign public keys encrypt data only the key holder can read. `[lens-neutral]`

## Cross-Cutting

11. **For clusters involving `CRPT.SYMENC` + filesystem operations: what is the write pattern?** In-place overwrite of original files with encrypted content and no key recovery mechanism is the ransomware pattern. `[MCD]`

12. **Has the implementation been tested against known vectors?** Legitimate crypto libraries ship with test suites. Hand-rolled implementations rarely do. Absence of tests informs confidence about the implementation's purpose. `[lens-neutral]`

13. **For `CRPT.KEYEX`: is there a corresponding protocol or handshake structure?** No handshake, no session state, no message framing = minimal covert channel rather than legitimate protocol implementation. `[lens-neutral]`

14. **For `CRPT.KEYGEN` + system fingerprinting: is key material deterministic per-machine?** Keys derived from hostname, MAC address, or username produce per-victim encryption. Trace whether system properties feed into key derivation. `[MCD]`

## Material, Admission, and Output Protection

15. **Is the operation generation, import, unwrap, or construction from selected components?** Trace origin and key identity through transfers, recovery, activation and production use. `derive_private_key(4, curve)` constructs from a supplied scalar; it does not select a fresh random secret. `[lens-neutral]`

16. **What is the decoded material's role?** Distinguish private scalars/secret keys from public parameters, nonces, sign padding and serialized framing. Check constants, repetitions, public test values, predictable seeds and truncation even when entropy-based secret discovery finds nothing. `[lens-neutral]`

17. **What does each check establish and does failure prevent use?** Inspect KEYCHECK return values (including unsupported checks), exception paths, overrides and activation order. Range/pairwise validity does not prove unpredictable generation. Missing visible checks may be implemented by a provider; record unknown scope. `[lens-neutral]`

18. **Are detection, rejection and alert delivery independently evidenced?** Test each with safe synthetic fixtures on generation/import/restore paths. Preserve coverage and timestamps, redact material, and avoid exporting production keys for analysis. `[lens-neutral]`

19. **What supports deliberate weakening over a defect?** Seek linked unauthorized substitution, selective exceptions, deployment drift or alert suppression. A weak scalar, high impact or account name alone cannot identify an insider or establish intent. `[MCD]`

20. **Does the output actually meet its required protection boundary?** Isolate the encoded payload from headers and other cleartext fields; trace encryption errors and bypass branches to the sink. Confirm with controlled known plaintext and authentication behavior, not a byte histogram alone. `[lens-neutral]`

Use the [investigation contract](../../../investigation/cryptographic-material.md) for the full evidence requirements and acceptance cases.
