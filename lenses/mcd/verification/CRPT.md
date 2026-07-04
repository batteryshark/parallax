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

9. **Is the IV or nonce random, fixed, or derived?** Fixed IV breaks confidentiality for repeated plaintexts. Victim-derived IV/nonce indicates intentional per-environment tracking. `[lens-neutral]`

## CRPT.ASYMENC

10. **Where does the public key originate?** User-provided, library-provided, or hardcoded? Hardcoded foreign public keys encrypt data only the key holder can read. `[lens-neutral]`

## Cross-Cutting

11. **For clusters involving `CRPT.SYMENC` + filesystem operations: what is the write pattern?** In-place overwrite of original files with encrypted content and no key recovery mechanism is the ransomware pattern. `[MCD]`

12. **Has the implementation been tested against known vectors?** Legitimate crypto libraries ship with test suites. Hand-rolled implementations rarely do. Absence of tests informs confidence about the implementation's purpose. `[lens-neutral]`

13. **For `CRPT.KEYEX`: is there a corresponding protocol or handshake structure?** No handshake, no session state, no message framing = minimal covert channel rather than legitimate protocol implementation. `[lens-neutral]`

14. **For `CRPT.KEYGEN` + system fingerprinting: is key material deterministic per-machine?** Keys derived from hostname, MAC address, or username produce per-victim encryption. Trace whether system properties feed into key derivation. `[MCD]`
