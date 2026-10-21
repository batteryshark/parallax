# Architecture: Cryptographic Control Gaps

**Question:** Can material with unknown or unsuitable origin become operational,
or can a path promising encryption emit unprotected data?

| Observation pattern | Operational interpretation | What would disprove it |
|---|---|---|
| KEYGEN/KEYLOAD → signing/encryption with a confirmed fixed or predictable secret | Generation/import boundary permits unsuitable production material | Material was misidentified, is public/non-secret, or cannot reach the claimed production use |
| KEYCHECK failure/unsupported result → activation/use | Validation is ineffective on the observed path | Actual control flow rejects before the same key version can be used |
| Generation checks exist but import/unwrap/restore skips admission policy | Lifecycle paths enforce different guarantees | Equivalent enforced policy and provenance on the claimed alternate path |
| Rejection without delivered alerts, or unchecked overrides | Operators may miss attempted substitution or control failure | Evidence of independent delivery and review for the tested event |
| Encryption failure/disable branch → plaintext write/send | Failure handling violates the stated protection boundary | The payload is protected at that exact boundary, or the claimed requirement does not apply |

These findings require scoped evidence; missing signatures are not missing
controls. Separate severity (forgery/disclosure scope and recovery cost) from
confidence (reachability, actual key use and enforcement evidence). No malicious
intent is required. Low-entropy measurements alone are insufficient.

Compensating controls include trusted generation, provenance checks at every
admission path, algorithm-specific validation and known-test-value screening,
blocking before activation, scoped overrides with independent review, and alerts
whose delivery is tested. Verify failure behavior using isolated synthetic cases.
For output paths, fail closed when protection is required and test that errors
cannot return original plaintext. Do not substitute a universal entropy threshold
for these controls or require exporting HSM secrets for measurement.

See the [investigation contract](../../../investigation/cryptographic-material.md)
for acceptance cases, evidence fields and blind spots. These are interpretation
specifications; runtime enforcement remains the consuming system's responsibility.
