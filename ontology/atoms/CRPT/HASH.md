# CRPT.HASH: Cryptographic Hashing

## Description

Computes cryptographic hash digests of data: MD5, SHA-1, SHA-256, SHA-3, BLAKE2, BLAKE3, or other cryptographic hash functions. Produces a fixed-size digest from arbitrary input data. Used for integrity verification, content addressing, deduplication, fingerprinting, HMAC construction, and as a component in digital signatures and key derivation. The mechanical behavior is a one-way transformation of data into a fixed-size digest.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `hashlib.sha256()`, `MessageDigest.getInstance("SHA-256")`, `crypto.createHash()`, `CryptoJS.SHA256()`, HMAC construction |
| Static Binary | Yes | Hash function API imports, hash constant tables (SHA round constants), HMAC references |
| Runtime/Dynamic | Yes | Hash computation calls, digest output, comparison operations against known digests |

## Disambiguation

- **vs CRPT.CREDHASH**: General-purpose hashing (SHA-256 of a file, HMAC of a message) is CRPT.HASH. Password-specific hashing (bcrypt, argon2, PBKDF2 used for credential storage/verification) is CRPT.CREDHASH. When SHA-256 is used to hash a password (not recommended practice, but observed), the context determines: password verification = CREDHASH, general data integrity = HASH.
- **vs embedded hash values**: CRPT.HASH is the operation of computing a hash. A hardcoded hash value appearing as a static artifact in source or binary is a different observation, the presence of an artifact, not an operation. When code computes a hash and compares against an embedded value, the computation is CRPT.HASH and the embedded value is an artifact.

## Structural Relationships

- **Often co-occurs with**: `CRPT.SIGN` (hashing as a step in signature generation), `CRPT.KEYGEN` (hashing as input to key derivation), `FSYS.READ` (reading file contents to hash), `NETW.*` (hashing data before/after network transfer)
- **May imply**: Data integrity is being verified, content is being fingerprinted, or data is being prepared for a cryptographic operation that requires a digest

## Notes

The algorithm choice, what data is being hashed, and what happens to the digest are the key structural data points. MD5/SHA-1 for new integrity checks suggests weak collision resistance requirements (or legacy code). The hash output fed into a comparison, used as a key, or transmitted outbound each have different structural implications.
