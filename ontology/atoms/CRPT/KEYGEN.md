# CRPT.KEYGEN: Cryptographic Key Generation

## Description

Generates cryptographic key material: symmetric keys, asymmetric key pairs, or keys derived from passwords/passphrases via key derivation functions (PBKDF2, HKDF, scrypt, argon2 used for key derivation rather than password storage). Includes both direct random key generation and deterministic key derivation from input material. The output is key material suitable for use in cryptographic operations.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `os.urandom(32)`, `RSA.generate()`, `crypto.generateKeyPairSync()`, `PBKDF2()`, `HKDF()`, `KeyGenerator.getInstance()`, key size parameters |
| Static Binary | Yes | Key generation API imports, KDF function references, key size constants |
| Runtime/Dynamic | Yes | Random byte generation, key derivation computation, key pair generation (measurable compute time for RSA) |

## Disambiguation

- **vs CRPT.RNG**: Random number generation produces random bytes. Key generation uses random bytes (and potentially other inputs) to produce structured key material. CRPT.RNG may be a component of CRPT.KEYGEN, but KEYGEN also covers deterministic derivation (KDFs) where no fresh randomness is required.
- **vs CRPT.CREDHASH**: Key derivation functions (PBKDF2, scrypt, argon2) appear in both atoms. When the output is used as key material for encryption/decryption, classify as CRPT.KEYGEN. When the output is stored or compared as a password hash for authentication, classify as CRPT.CREDHASH. The function is the same; the usage determines the atom.

## Structural Relationships

- **Often co-occurs with**: `CRPT.SYMENC` or `CRPT.ASYMENC` (generated keys used for encryption), `CRPT.RNG` (randomness source for key generation), `CRPT.SIGN` (generated keys used for signing)
- **May imply**: New cryptographic key material is being created for subsequent cryptographic operations

## Notes

The key lifecycle (where keys are generated, how they're stored, how they're transmitted, and when they're destroyed) is the primary structural data for this atom. Keys generated, used locally, and discarded differ structurally from keys generated and transmitted externally. Key material derived from runtime-specific inputs (hostname, MAC address, process ID) produces deterministic per-environment keys, which is structurally different from keys derived from secure random sources.
