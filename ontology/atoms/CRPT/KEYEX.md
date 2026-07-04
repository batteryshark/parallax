# CRPT.KEYEX: Key Exchange / Agreement

## Description

Performs cryptographic key exchange or key agreement protocols: Diffie-Hellman (DH), Elliptic Curve Diffie-Hellman (ECDH), X25519, X448, or other key agreement mechanisms. Key exchange establishes a shared secret between two parties over a potentially observed channel, neither party transmits the secret directly, yet both derive the same value. The output is shared key material usable for subsequent symmetric encryption or authentication.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `DiffieHellman()`, `ECDH()`, `X25519()`, `KeyAgreement.getInstance()`, `crypto.diffieHellman()`, parameter generation, public value exchange |
| Static Binary | Yes | Key exchange API imports, DH/ECDH parameter constants, well-known group parameters |
| Runtime/Dynamic | Yes | Key exchange computation, public value transmission, shared secret derivation |

## Disambiguation

- **vs CRPT.ASYMENC**: Asymmetric encryption directly encrypts data with a public key. Key exchange derives a shared secret through a protocol, no data is directly encrypted, but the derived secret enables subsequent symmetric encryption. Both use public-key mathematics; the output differs (ciphertext vs. shared secret).
- **vs CRPT.KEYGEN**: Key generation creates new key material (random or derived). Key exchange is a specific protocol for two parties to arrive at the same key material through public value exchange. KEYGEN may generate the initial key pair used in key exchange, but the exchange protocol itself is KEYEX.

## Structural Relationships

- **Often co-occurs with**: `CRPT.SYMENC` (shared secret used for symmetric encryption), `CRPT.KEYGEN` (generating ephemeral key pairs for the exchange), `NETW.*` (public values exchanged over network)
- **May imply**: Two parties are establishing a shared cryptographic secret, typically for encrypted communication

## Notes

Key exchange implies bidirectional communication, both parties must exchange public values. The presence of key exchange in code that has no documented communication protocol or network role is structurally notable. Whether the exchange uses ephemeral keys (forward secrecy) or static keys, and whether the parameters are well-known standards or custom, are key structural data points.
