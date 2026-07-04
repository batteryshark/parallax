# XFRM.ENCRYPT: Data Encryption

## Description

Applies encryption (XOR, AES, or other ciphers) to data within an artifact. The encrypted content is stored within the artifact and decrypted at runtime before use. This is distinct from using cryptographic libraries for their documented purpose (e.g., TLS, password hashing), `XFRM.ENCRYPT` specifically describes encryption applied to the artifact's own content to make it opaque until execution time.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Decryption function calls with hardcoded or derived keys, encrypted blobs as string/byte literals, key material adjacent to encrypted data |
| Static Binary | Partial | Encrypted data sections (high entropy byte sequences), decryption routine patterns, imported crypto library functions |
| Runtime/Dynamic | Yes | Decryption operations producing cleartext, key derivation, decrypted content passed to subsequent operations |

## Disambiguation

- **vs XFRM.ENCODE**: Encryption requires key material to reverse; encoding does not. If only the scheme identity is needed to decode, it's encoding. If a key is needed, it's encryption.
- **vs CRPT.SYMENC / CRPT.ASYMENC**: `XFRM.ENCRYPT` describes encryption applied to the artifact's own embedded content. `CRPT.*` describes the use of cryptographic primitives as functional operations (encrypting user data, establishing TLS, hashing passwords). A package that encrypts user files uses `CRPT.*`. A package that stores its own strings encrypted and decrypts them at startup uses `XFRM.ENCRYPT`.
- **vs XFRM.BITWISE**: Simple XOR with a hardcoded key can be classified as either. If the operation follows a recognizable cipher pattern (even a trivial one), prefer `XFRM.ENCRYPT`. If it's ad-hoc bitwise manipulation with no recognizable cipher structure, prefer `XFRM.BITWISE`. When uncertain, flag both.

## Structural Relationships

- **Often co-occurs with**: `CRPT.SYMENC` (encryption primitive used for the transformation), `XFRM.BITWISE` (bitwise operations implementing the cipher), `LOAD.EVAL` / `EXEC.SHELL` (decrypted content fed to execution)
- **May imply**: Key material exists somewhere in the artifact or is derived at runtime
- **Commonly part of idioms**: Decode-and-execute chain (encrypted data → decrypt → execution primitive)

## Notes

The proximity of key material to encrypted content is a structural observation. When the decryption key is hardcoded adjacent to the encrypted data, the encryption serves to make the content opaque to static analysis rather than to protect confidentiality from an attacker with access to the artifact.
