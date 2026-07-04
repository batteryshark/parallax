# CRPT.SYMENC: Symmetric Encryption

## Description

Encrypts or decrypts data using symmetric-key algorithms where the same key (or a deterministically derived key) is used for both encryption and decryption. Algorithms include AES (all modes: CBC, GCM, CTR, ECB), ChaCha20, Salsa20, 3DES, Blowfish, RC4, and other block/stream ciphers. Also covers symmetric decryption, the reverse operation where encrypted data is restored to plaintext using the same key.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `AES.new()`, `Cipher.getInstance("AES/CBC/...")`, `crypto.createCipheriv()`, `CryptoJS.AES.encrypt()`, algorithm mode constants, IV/nonce parameters |
| Static Binary | Yes | AES S-box constants, round constants, cipher API imports, block cipher mode indicators |
| Runtime/Dynamic | Yes | Cipher initialization, key schedule computation, block-by-block encryption/decryption operations, ciphertext output |

## Disambiguation

- **vs XFRM.ENCRYPT**: XFRM.ENCRYPT covers encryption applied to the artifact's own code or embedded data, string literals, configuration values, or payload blobs that are decrypted at runtime as part of the artifact's self-preparation. CRPT.SYMENC covers encryption applied to operational data, files, messages, streams, or payloads being processed. The distinction: XFRM.ENCRYPT operates on the artifact itself; CRPT.SYMENC operates on data the artifact processes.
- **vs CRPT.CUSTOM**: When symmetric encryption is implemented using a standard library (OpenSSL, libsodium, native crypto module), it's CRPT.SYMENC. When the algorithm is implemented from scratch (hand-rolled AES rounds, custom S-box, manual block operations), it's CRPT.CUSTOM. Both may apply if a custom implementation of a recognized algorithm is identified.

## Structural Relationships

- **Often co-occurs with**: `CRPT.KEYGEN` (key generation for encryption), `CRPT.ASYMENC` (hybrid encryption, symmetric key encrypted with asymmetric), `CRPT.RNG` (IV/nonce generation)
- **May imply**: Data is being transformed between plaintext and ciphertext using a shared secret

## Notes

The algorithm, mode, key source, IV handling, and what data is being encrypted/decrypted are the key structural data points. The same AES-256-GCM call appears in password managers, file encryption utilities, TLS implementations, and ransomware, context determines meaning. Whether the operation is encryption or decryption is also relevant: encryption produces ciphertext from plaintext; decryption reverses it.
