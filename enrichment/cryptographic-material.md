# Cryptographic Material and Control Context

Facts from key inventories, provider records, deployment policy, audit logs, and
scoped artifact measurements. Observed code operations remain atoms; these facts
describe the material, its history, and the controls surrounding those operations.

| Id | Data point | What it factually states | Primary source |
|---|---|---|---|
| `ENR.CRYPTO.ORIGIN` | Generation provenance | Generated/imported/derived origin, generator/provider identity and version, ceremony or attestation evidence, and any gap between generation and activation | provider records, ceremony records, build analysis |
| `ENR.CRYPTO.MATERIAL` | Material structure | Key role, algorithm/parameters, decoded field and sample length, observed constant/repetition/small-scalar relationship, or match to a known test value | scoped source/binary analysis, approved local inspection, public-key comparison |
| `ENR.CRYPTO.MEASUREMENT` | Distribution measurement | Method/version, units, sample region, encoding, window size, score and applicable baseline; no inferred security bits | artifact inspection, dynamic analysis |
| `ENR.CRYPTO.CONTROL` | Admission and monitoring coverage | Policy/check kind, boundary, result, enforcement action, alert delivery evidence, overrides, assessed paths and unobserved paths | source/control-flow review, effective configuration, provider logs, controlled tests |
| `ENR.CRYPTO.USE` | Operational use | Key handle/version, production/test scope, usage, activation time, affected trust relationships or protected data | deployment inventory, certificate inventory, signing/encryption audit logs |
| `ENR.CRYPTO.CHANGE` | Control or material changes | Time, authenticated actor/session, approval evidence, change to generator/import policy/key version/alert routing, and source-to-deployment correspondence | change records, CI provenance, audit logs |
| `ENR.CRYPTO.OUTPUT` | Expected protection versus observed output | Expected encryption boundary, payload region, actual write/send bytes or protected comparison result, error/fallback path, and framing exclusions | format specification, runtime tracing, controlled round-trip tests |

Every record names its evidence reference, acquisition method, time, scope, and
confidence. A control has a state of **observed-enforced**, **observed-not-enforced**,
or **unknown** for the assessed path. "Not observed" is unknown; it is not a
negative finding. Evaluate rejection and alerting separately. Preserve explicit
scope limits even when one test confirms a bypass.

Use key handles or public-key fingerprints for correlation. Do not include secret
bytes, guessed private values from live systems, plaintext payloads, or unhashed
secret-derived evidence in shared reports. An ordinary hash of a low-entropy
secret is also enumerable; use a protected evidence reference instead. Synthetic
published test values are suitable for examples.

Measurements must distinguish serialized containers, decoded key fields, public
parameters, private scalars, seeds, symmetric keys, IVs/nonces, and ciphertext
payloads. PEM/base64 text, DER headers/sign padding, and fixed curve parameters
are not random samples. Small samples need explicit limitations. A high score
does not establish unpredictability or encryption; a low score does not establish
plaintext or malicious intent.

Interpretation lives in [MCD signals](../lenses/mcd/signals/cryptographic-material.md)
and the other lenses. See the [investigation contract](../investigation/cryptographic-material.md)
for required distinctions and evidence handling.
