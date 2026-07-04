# CRPT.SIGN: Digital Signing and Verification

## Description

Creates or verifies digital signatures and message authentication codes: RSA-PSS, ECDSA, EdDSA, HMAC, and protocol-specific signing schemes (AWS SigV4, GCP service account signing, JWT signing). Signing operations prove that a key holder produced or endorsed a message. Verification operations confirm a signature's validity against a public key or shared secret. Also covers HMAC construction, keyed hash-based authentication that provides message integrity and authenticity.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `sign()`, `verify()`, `HMAC.new()`, `crypto.createHmac()`, `Signature.getInstance()`, JWT library usage, AWS SigV4 computation, `SigningKey` / `VerifyingKey` usage |
| Static Binary | Yes | Signing API imports, HMAC function references, signature algorithm identifiers, AWS signing constants |
| Runtime/Dynamic | Yes | Signature computation, HMAC generation, signature verification pass/fail |

## Disambiguation

- **vs CRPT.ASYMENC**: Asymmetric encryption provides confidentiality (only the private key holder can read). Signing provides authenticity (proves the private key holder endorsed). Both use key pairs; the purpose differs. RSA encryption is ASYMENC. RSA-PSS signing is SIGN.
- **vs CRPT.HASH**: Hashing produces an unkeyed digest. HMAC produces a keyed digest, it requires a secret key and provides authenticity, not just integrity. Plain SHA-256 is HASH. HMAC-SHA256 is SIGN.
- **vs CRPT.CERT**: Certificate operations (loading, installing, verifying certificates) are CERT. Signature operations on data/messages (signing a payload, verifying a JWT) are SIGN. Certificate verification involves signature verification internally, but the atom distinction is the subject: certificate lifecycle = CERT, data/message signatures = SIGN.

## Structural Relationships

- **Often co-occurs with**: `CRPT.HASH` (hashing as a step in signature generation), `CRPT.KEYGEN` (key generation for signing), `NETW.*` (signing outbound requests or verifying inbound responses), hardcoded key material
- **May imply**: Data or message authenticity is being established or verified, or a protocol authentication scheme is being implemented

## Notes

The signing scheme, key source, what is being signed, and whether the operation is sign or verify are the key structural data points. Protocol-specific signing (AWS SigV4, OAuth signatures, webhook verification) implements authentication for specific service APIs. Custom or ad-hoc signing schemes (HMAC with a hardcoded key for non-standard authentication) are structurally different from standard protocol implementations.
