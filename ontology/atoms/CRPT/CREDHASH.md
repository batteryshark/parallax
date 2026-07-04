# CRPT.CREDHASH: Credential Hashing / Password Operations

## Description

Uses password-specific hashing algorithms (bcrypt, scrypt, argon2, PBKDF2 when used for credential storage) or compares input against stored password hashes. These algorithms are purpose-built for credential processing: they are deliberately slow (to resist brute force), incorporate salt, and have tunable work factors. Distinguished from general hashing in that these algorithms exist specifically for password/credential handling.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `bcrypt.hashpw()`, `argon2.hash()`, `scrypt()`, `PBKDF2()` with credential context, password comparison functions, `password_verify()` |
| Static Binary | Yes | Password hashing library imports, bcrypt/scrypt/argon2 function references, work factor constants |
| Runtime/Dynamic | Yes | Deliberately slow hash computation (tunable work factor), salt generation, hash-and-compare operations |

## Disambiguation

- **vs CRPT.HASH**: General-purpose hash functions (SHA-256, BLAKE2) compute fast digests of arbitrary data. CREDHASH uses algorithms specifically designed for credential processing, slow by design, salted, with tunable cost. When PBKDF2 is used for key derivation (output feeds into encryption), classify as CRPT.KEYGEN. When PBKDF2 is used for password storage/verification, classify as CRPT.CREDHASH.
- **vs CRED.***: CRED atoms describe accessing credential stores (reading passwords from keychains, browsers, files). CRPT.CREDHASH describes the cryptographic operation of hashing or verifying credentials. Accessing stored credentials is CRED. Processing credentials through a password hash is CRPT.CREDHASH.

## Structural Relationships

- **Often co-occurs with**: `CRED.*` (credential access feeding into hash operations), `CRPT.RNG` (salt generation), authentication decision logic
- **May imply**: Credentials are being processed, either for authentication, storage, or verification

## Notes

The presence of credential hashing is contextually significant. In an authentication module, it's expected. In code that has no authentication function (a data processing library, a CLI utility, a network client), credential hashing is unexpected. The algorithm choice, work factor, and whether the operation is hashing (creating) or verifying (comparing) are the key structural data points.
