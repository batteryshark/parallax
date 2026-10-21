# CRPT.KEYCHECK: Cryptographic Key Validation

## Description

Evaluates cryptographic key material or its provenance against explicit criteria and produces a result. Criteria include algorithm-specific parameter/range validity, public/private consistency, known-value screening, generation provenance, and local admission policy. The observation records which checks occur and how their results are consumed.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `EVP_PKEY_private_check()`, `EVP_PKEY_pairwise_check()`, `EVP_PKEY_public_check()`, explicit comparisons against a prohibited-key set, provenance-policy branches |
| Static Binary | Partial | Key validation imports and comparisons; provider implementations may be opaque |
| Runtime/Dynamic | Partial | Check results, rejection/acceptance decisions, exceptions, audit/alert events and subsequent key use |

## Disambiguation

- **vs CRPT.KEYLOAD**: Loading accepts a representation; checking evaluates a criterion. Implementations may perform both, but a load signature alone establishes only loading.
- **vs CRPT.KEYGEN / CRPT.RNG**: Generating key material or requesting randomness does not prove validation. Random-source health tests examine the source and its samples, not necessarily the resulting key.
- **vs CRPT.CERT / CRPT.SIGN**: Certificate path validation and signature verification answer different questions from key quality or origin. A valid signature can be made with a predictable private scalar.
- **vs generic entropy measurement**: Computing a distribution statistic is not key validation unless it is applied to a key-policy decision. Measurements alone are contextual evidence, not a new cryptographic operation.

## Structural Relationships

- **Often co-occurs with**: `CRPT.KEYLOAD`, `CRPT.KEYGEN`, `CRPT.CERT`, `CRPT.SIGN`
- **May imply**: A key admission decision can consume the result; whether it actually does requires control-flow evidence

## Notes

Record the check kind, algorithm/provider, policy version, result, and handling (reject, warn, ignore, override, or unknown). Range validity and pairwise consistency do not establish unpredictable generation. A scalar such as 4 can be in range and consistent with its public key. A single sample's byte-frequency score cannot certify key entropy.

Presence is not enforcement: an ignored return value, unsupported check, caught exception, or post-activation warning may leave use permitted. Absence of a matched call is not proof that a check is absent in an HSM, remote service, provider, or wrapper. See [investigation guidance](../../../investigation/cryptographic-material.md).
