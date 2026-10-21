# BP-CRYPTOWEAK: Deliberate Cryptographic Weakening

Hypothesis: a reachable path substitutes predictable key material, bypasses key
admission controls, or returns unprotected output to preserve unauthorized access
or enable forgery/decryption. This includes a possible insider mechanism without
requiring the actor to extract an existing production key.

**Status:** specification for downstream engines; callee matches alone do not
implement this composition.

## Constituent Evidence

| Role | Observation | Requirement |
|---|---|---|
| Required: mechanism, key variant | `CRPT.KEYLOAD` or `CRPT.KEYGEN` feeding `CRPT.SIGN`, `CRPT.SYMENC`, `CRPT.ASYMENC`, or `CRPT.KEYEX` | Trace selected/predictable material to consequential use, or demonstrate a changed admission check permitting it |
| Required: mechanism, output variant | `FSYS.WRITE` or `NETW.*` carrying a payload required to be encrypted | Trace encryption bypass/failure to unprotected output; an absent encryption atom or low entropy alone is insufficient |
| Required: context | `ENR.CRYPTO.MATERIAL` / `ENR.CRYPTO.OUTPUT` + `ENR.CRYPTO.USE` | Establish the security requirement and deployment scope; co-location is insufficient |
| Required for supported malicious reading | Independent change/control evidence | Corroborated unauthorized substitution, selective bypass, concealment, or alert suppression linked to the mechanism |
| Supporting | `CRPT.KEYCHECK`, `ENVI.ENVCHECK`, `ARTF.CREDENTIAL`, `ENR.CRYPTO.CHANGE`, `ENR.CRYPTO.ORIGIN` | Ignored results, conditional activation, embedded constants, and provenance gaps are threads to verify |

## Severity and Confidence

High impact where a predictable secret enables production forgery or disclosure;
potentially critical for broadly trusted CA or release-signing keys. Bound impact
by actual relying parties, validity periods, key usage and trust distribution.
Do not infer that compromise of a signing key decrypts all historical TLS traffic.

A confirmed weak-key defect may have high confidence while malicious intent has
low confidence. Without independent corroboration, report the defect and retain
this composition only as an investigative hypothesis. Do not sum correlated
observations (padding, small scalar, and low byte score from the same key) as
independent confirmations.

## Verification and Disproof

- Trace generation → import/unwrap → check → activation → use for the same key version, including fallback, recovery, rotation, and alternate provider paths.
- Establish who could change material or controls and correlate deployed changes with audit evidence. Do not attribute a human actor from key shape alone.
- Test rejection and alert delivery with synthetic fixtures in an isolated environment; do not activate weak keys in production to prove a finding.
- Disprove the production claim with verified fixture isolation or a correctly enforced boundary on every claimed path. Disprove the mechanism with traced output showing the actual payload is protected at the stated boundary.
- An independently reproduced accidental import or generation defect attenuates the deliberate hypothesis but does not reduce the confirmed exposure's severity.

## Response

Contain confirmed affected key use through the owner's incident process; preserve
non-secret provenance and audit evidence. Replace compromised material through a
verified generation/admission path and assess revocation, reissuance, dependent
signatures and data exposure. Repair bypasses and monitor activation/override/alert
events. Escalate an insider allegation only with corroborated evidence, keeping
remediation of the security defect independent of attribution.
