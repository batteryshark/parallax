# CRPT.RNG: Cryptographic Random Number Generation

## Description

Accesses random number generators intended for cryptographic use (CSPRNGs): `/dev/urandom`, `CryptGenRandom`, `SecRandomCopyBytes`, `crypto.getRandomValues()`, Python's `secrets` module, `openssl rand`, or equivalent platform-specific secure random sources. This records the source/API used, not a guarantee that its implementation, seeding, output handling, or deployment is correct.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `secrets.token_bytes()`, `os.urandom()`, `crypto.getRandomValues()`, `SecureRandom`, `/dev/urandom` reads, `CryptGenRandom` calls |
| Static Binary | Yes | CSPRNG API imports, entropy source file paths, secure random function references |
| Runtime/Dynamic | Yes | Reads from OS entropy sources, CSPRNG API invocations |

## Disambiguation

- **vs CRPT.KEYGEN**: RNG generates random bytes. KEYGEN produces structured key material (which may use RNG as an input). When random bytes are generated and directly used as a symmetric key, both atoms apply. When random bytes are used for non-key purposes (nonces, IVs, random identifiers), only CRPT.RNG applies.
- **vs general-purpose RNG**: `Math.random()`, `random.random()`, `rand()` are not CRPT.RNG. When their output feeds key generation, record KEYGEN with the observed non-cryptographic source and value-flow evidence. Do not emit a CSPRNG observation merely because the consumer requires one.

## Structural Relationships

- **Often co-occurs with**: `CRPT.KEYGEN` (random bytes as key material input), `CRPT.SYMENC` (IV/nonce generation), `CRPT.SIGN` (nonce generation for signing schemes)
- **May imply**: The code is performing operations that require unpredictable random data

## Notes

The RNG source, seed/reseed behavior where observable, amount requested, handling of errors or short reads, substitutions, truncation, and output consumer are structural data. Source health tests and measurements of final key bytes answer different questions. Record unavailable provider details as unknown and leave quality/intent judgments to the lenses. See [cryptographic material investigation](../../../investigation/cryptographic-material.md).
