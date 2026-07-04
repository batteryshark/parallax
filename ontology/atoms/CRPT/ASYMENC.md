# CRPT.ASYMENC: Asymmetric Encryption

## Description

Encrypts or decrypts data using public-key cryptography where different keys are used for encryption (public key) and decryption (private key). Algorithms include RSA, ECC-based encryption (ECIES), ElGamal, and post-quantum schemes. The fundamental property: data encrypted with a public key can only be decrypted by the corresponding private key holder.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `RSA.generate()`, `PKCS1_OAEP.new()`, `Cipher.getInstance("RSA/...")`, `crypto.publicEncrypt()`, PEM-formatted key loading, key size parameters (2048, 4096) |
| Static Binary | Yes | RSA modular exponentiation constants, public key material, ASN.1 key structure markers, PEM header strings |
| Runtime/Dynamic | Yes | Key loading, public-key encryption operations, large integer arithmetic |

## Disambiguation

- **vs CRPT.SYMENC**: Symmetric encryption uses a single shared key. Asymmetric encryption uses a key pair (public/private). In hybrid encryption schemes, both are used, asymmetric encrypts the symmetric key, symmetric encrypts the data. Tag both when both are present.
- **vs CRPT.SIGN**: Asymmetric encryption transforms data so only a key holder can read it (confidentiality). Digital signing proves a key holder produced a message (authenticity). Both use the same key pairs but for different purposes. RSA encryption is ASYMENC. RSA-PSS signing is SIGN.
- **vs CRPT.KEYEX**: Key exchange establishes a shared secret through a protocol (e.g., Diffie-Hellman). Asymmetric encryption directly encrypts data with a public key. Both involve public-key math but serve different cryptographic functions.

## Structural Relationships

- **Often co-occurs with**: `CRPT.SYMENC` (hybrid encryption), `CRPT.KEYGEN` (generating the key pair), hardcoded key material (embedded public keys)
- **May imply**: Data is being encrypted such that only a specific private key holder can decrypt it

## Notes

The source of the public key is critical structural data. A public key loaded from a certificate authority chain, generated locally, or hardcoded in source/binary each have very different implications. Hardcoded public key material means the code is encrypting data for a predetermined recipient. The key size (RSA-2048 vs RSA-4096), padding scheme (PKCS1 vs OAEP), and whether the operation is encryption or decryption are additional structural data points.
