# CRPT.CUSTOM: Hand-Rolled Cryptographic Implementation

## Description

Implements cryptographic algorithms from scratch rather than using established libraries (OpenSSL, libsodium, BouncyCastle, native crypto modules). Includes implementing AES rounds manually, writing RSA modular exponentiation, constructing SHA-256 from the specification, building key exchange from mathematical primitives, or implementing any named cryptographic algorithm without using a library that provides it. Also covers implementations of protocol-level cryptographic schemes (like AWS SigV4 request signing) from specification rather than using the standard SDK.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | S-box arrays, round constants, modular exponentiation loops, polynomial arithmetic, block cipher round structure, manual padding implementation, protocol signing logic without SDK imports |
| Static Binary | Yes | Embedded S-box tables, round constant arrays, large-number arithmetic, cipher structure patterns without crypto library imports |
| Runtime/Dynamic | Yes | Cryptographic operations occurring without crypto library calls in the call stack, manual block processing, custom round functions |

## Disambiguation

- **vs CRPT.SYMENC / CRPT.ASYMENC / CRPT.HASH**: The standard atoms (SYMENC, ASYMENC, HASH, etc.) apply regardless of implementation method. CUSTOM is an additional classification that applies when the implementation is hand-rolled rather than library-based. A hand-rolled AES implementation is both CRPT.SYMENC (the operation) and CRPT.CUSTOM (the implementation method). A library AES call is only CRPT.SYMENC.
- **vs XFRM.BITWISE**: Bitwise data transformation (XOR, shifts, rotations) in an ad-hoc pattern with no recognizable algorithm structure is XFRM.BITWISE. Bitwise operations that implement a recognizable cryptographic algorithm (RC4 stream generation, AES SubBytes, SHA-256 rounds) are CRPT.CUSTOM. The test: can the implementation be matched to a named algorithm specification?

## Structural Relationships

- **Often co-occurs with**: The specific algorithm atom (`CRPT.SYMENC`, `CRPT.ASYMENC`, `CRPT.HASH`, `CRPT.SIGN`) representing what algorithm is implemented, `XFRM.BITWISE` (custom crypto may be further obfuscated)
- **May imply**: Cryptographic functionality is present without a declared dependency on a cryptographic library

## Notes

Hand-rolled cryptographic implementations are structurally notable because standard practice is to use audited libraries. Implementing crypto from scratch means either (a) the developer had specific reasons to avoid a library dependency, (b) the code predates the availability of the library in the target environment, or (c) the implementation is intentionally self-contained. The absence of a crypto library in the dependency manifest while crypto operations are present is the primary detection signal. Whether the implementation matches a known algorithm specification or implements something non-standard is an additional structural data point.
