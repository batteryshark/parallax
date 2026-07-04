# CRPT.RNG: Cryptographic Random Number Generation

## Description

Accesses cryptographically secure random number generators (CSPRNGs): `/dev/urandom`, `CryptGenRandom`, `SecRandomCopyBytes`, `crypto.getRandomValues()`, Python's `secrets` module, `openssl rand`, or equivalent platform-specific secure random sources. Distinguished from general-purpose RNG (`math.random`, `rand()`, `Random()`) by the cryptographic quality guarantee. Also covers detection of deliberately weak RNG, using predictable seeds or non-cryptographic generators for operations that should use CSPRNGs.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `secrets.token_bytes()`, `os.urandom()`, `crypto.getRandomValues()`, `SecureRandom`, `/dev/urandom` reads, `CryptGenRandom` calls |
| Static Binary | Yes | CSPRNG API imports, entropy source file paths, secure random function references |
| Runtime/Dynamic | Yes | Reads from OS entropy sources, CSPRNG API invocations |

## Disambiguation

- **vs CRPT.KEYGEN**: RNG generates random bytes. KEYGEN produces structured key material (which may use RNG as an input). When random bytes are generated and directly used as a symmetric key, both atoms apply. When random bytes are used for non-key purposes (nonces, IVs, random identifiers), only CRPT.RNG applies.
- **vs general-purpose RNG**: `math.random()`, `random.random()`, `rand()` are not CRPT.RNG, they don't provide cryptographic guarantees. CRPT.RNG applies specifically to CSPRNG access. However, the use of non-cryptographic RNG in a context that requires cryptographic randomness (generating encryption keys with `math.random`) is a notable observation, it indicates deliberately or accidentally weak cryptography.

## Structural Relationships

- **Often co-occurs with**: `CRPT.KEYGEN` (random bytes as key material input), `CRPT.SYMENC` (IV/nonce generation), `CRPT.SIGN` (nonce generation for signing schemes)
- **May imply**: The code is performing operations that require unpredictable random data

## Notes

Whether CSPRNG or non-CSPRNG is used for a given purpose is a structural observation. Using `os.urandom()` for an encryption IV is expected. Using `random.randint()` for the same purpose indicates either a mistake or intentionally weak cryptography. The RNG source, the amount of randomness requested, and what the output feeds into are the key structural data points.
