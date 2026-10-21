# Investigating Cryptographic Material and Protection Boundaries

This contract connects [key loading](../ontology/atoms/CRPT/KEYLOAD.md),
[key validation](../ontology/atoms/CRPT/KEYCHECK.md), generation, and ordinary
write/send behaviors to [cryptographic context](../enrichment/cryptographic-material.md).
It specifies engine observations and verification, not a universal entropy
threshold. The [research note](crypto-entropy-research.md) documents the incident
motivation and primary standards. Parallax provides vocabulary, signatures and
interpretation; downstream engines own decoding, dataflow, measurements and alerts.

## What to Establish

1. **Role and representation.** Identify algorithm/parameters, public versus secret material, key versus nonce/seed, encoding, and intended use. Decode representations before measuring a field; do not measure an entire PEM, certificate, DER container, or encrypted key wrapper and label that score "key entropy."
2. **Origin.** Trace fresh generation, deterministic derivation, import, unwrap, recovery, or substitution. Record RNG/provider provenance and source inputs. A KDF cannot manufacture unpredictability from a public constant, even if its output looks random. Deterministic derivation from protected high-quality secret input is not inherently defective.
3. **Structural facts.** Record fixed/all-zero values, repeated byte patterns, small EC scalars, known public test material, predictable seeds, narrowed/truncated RNG output, and key reuse where the policy requires separation. A decoded P-384 scalar of 4 is a small private value, despite its 48-byte representation. Public exponents, curve constants, leading sign padding, clamped bits, salts, and counter nonces are not interchangeable with secret key material.
4. **Admission and use.** Follow the same key handle/version through generation/import, validation, activation and actual signing/encryption/authentication. Include rotation, restore, migration, configuration overrides and error paths. For each check, record what it checks and whether failure prevents use. Successful parsing, parameter validity, pairwise consistency, proof of possession, and unpredictable generation are different claims.
5. **Monitoring.** Separate detection, blocking and alert delivery. Record reject/warn/override outcomes, activation events and policy changes; verify delivery to the configured destination with a safe synthetic event. A logged warning is not a rejection, and a rejection is not evidence an alert was delivered.
6. **Deployment and authority.** Establish production reachability and the affected trust/data boundary. Correlate generator, ceremony, import, policy and deployment changes. Identify accounts able to substitute keys or disable checks; keep actor attribution separate from control failure.

For OpenSSL's `EVP_PKEY_*check` functions, success is exactly `1`; unsupported
operations return `-2`. A generic nonzero/truthiness test can accidentally accept
failure. Check the provider and return contract rather than assuming a Boolean.
[OpenSSL return values](https://docs.openssl.org/3.5/man3/EVP_PKEY_check/#return-values).

Prefer generation inside the intended cryptographic boundary, algorithm-specific
validation, verifiable generation/import provenance, controlled exceptions, and
known-bad/test-material screening. Simple-pattern checks are supplemental: a
predictable hash of a constant can look random, and a maliciously selected
random-looking value can evade them. Do not generate repeatedly until a cosmetic
entropy score passes. Do not export non-exportable production keys to scan them;
inspect provider evidence and report unavailable properties as unknown.

## Measuring Without Inventing Security Bits

A byte-frequency Shannon estimate describes the sampled byte distribution. It
does not measure the selection process's min-entropy or attack work factor. For
`n` sampled bytes its empirical maximum is `log2(min(n, 256))` bits per byte: a
32-byte key cannot score above 5 with this estimator. An "8 bits per byte" floor
would reject every such key. Do not derive strength by multiplying the score by
length, or assign zero security solely because a sample scores low.

Record estimator/version, alphabet, units, decoded region/offset, sample length,
windowing, baseline, and uncertainty. Short samples may be inconclusive; aggregate
comparisons require comparable independent samples and an understood generator.
Source health tests assess a noise source under a model; they are not equivalent
to scanning one output key. See [NIST sources](crypto-entropy-research.md).

## Expected Ciphertext, Observed Data

Establish why the specific payload is required to be encrypted and where that
guarantee begins. Exclude headers, IVs/nonces, authentication tags, padding,
sparse regions, and permitted cleartext fields. Decode hex/base64 when applicable.
Compression can yield high scores without encryption; framing and short messages
can yield low scores without an encryption failure. A packet capture cannot see
application plaintext inside TLS, and a disk sample may be taken above transparent
storage encryption. State the layer and vantage point.

Low-entropy output is an investigation lead only. Trace whether the original
plaintext reaches the write/send sink, whether an exception returns input or an
empty/zero buffer, and whether an encryption-disabled branch is active. Confirm
using known synthetic plaintext and the actual format/cryptographic API in an
isolated environment. Where authentication is required, verify tag handling and
tamper rejection; successful round-trip alone does not establish confidentiality.
Do not infer `CRPT.SYMENC` from a random-looking blob or from a policy saying
"encrypted" when execution shows otherwise.

## Observation and Reporting Contract

Every finding includes linked atom observations, evidence references, material
role and algorithm, assessed lifecycle paths, requirement, actual control/output
result, method and blind spots, severity, confidence, alternative explanations,
disproof criterion, and a next verification step. Distinguish **observed-enforced**,
**observed-not-enforced**, and **unknown** control states for the stated scope.
No callee match is evidence of missing protection elsewhere.

Use non-secret handles/public fingerprints and protected evidence references.
Never put key literals or production plaintext in `Observation.matched_text`,
`summary`, logs, fixtures, alerts or shared reports. Do not publish an ordinary
hash of a low-entropy secret as a substitute. Scanner engines must redact before
constructing observations; the SDK's general serialization is not a redactor.
Examples below use synthetic/public values only.

## Acceptance Cases for Downstream Engines

These are semantic acceptance cases, not claims that the callee matcher performs
dataflow or computes entropy. The SDK tests separately verify the shipped API
surface mappings and their false-positive boundaries.

| Case | Expected observation / assessment | Must not conclude |
|---|---|---|
| P-384 scalar `4` supplied to `ec.derive_private_key`, traced to production signing | KEYLOAD + SIGN; small-scalar material and production-use evidence; high-impact predictable-key finding | KEYGEN from the API name; confirmed insider intent |
| A public point begins with `0x04` in uncompressed encoding | Public-format fact only | Private scalar is 4 |
| AES key is an all-zero constant used by a live encryptor | SYMENC; ARTF.CREDENTIAL for embedded secret; fixed-material finding regardless of byte score | Needs a high-entropy secret-detector match first |
| SHA-256 of a public constant feeds a key constructor | HASH → KEYLOAD → consumer; predictable derivation | High byte score establishes security |
| A private key is deterministically derived from a protected master secret with an appropriate KDF | KEYGEN and provenance context | Determinism by itself is malicious or weak |
| CSPRNG-produced short key has low empirical byte diversity | RNG / KEYGEN; measurement with sample limitation | A universal threshold establishes compromise |
| Known test key is confined to verified test-only reachability | KEYLOAD and test scope; attenuated production hypothesis | Mere presence is a backdoor |
| Test key escapes into a production fallback | Reachable KEYLOAD → consumer; actual scope overrides fixture label | A test filename exempts the use |
| Check fails or returns unsupported, caller continues to activate/use | KEYCHECK + observed-not-enforced for that path; separate alert state | Validation call proves a safeguard |
| Import API/library lacks visible validation but HSM evidence is unavailable | KEYLOAD; control state unknown | Missing callee proves missing HSM checks |
| Key is blocked but configured alert destination receives nothing | Admission observed-enforced; alert observed-not-enforced within tested scope | Blocking implies monitoring works |
| Encryption exception writes original synthetic plaintext | FSYS.WRITE and confirmed output protection failure; MCD intent unknown | Must observe successful encryption to record the failure |
| Encoded/framed short ciphertext has a low score | Representation-aware, possibly inconclusive measurement | Low score alone proves plaintext |
| Compressed plaintext has a high score | Output evidence with absent required protection when independently traced | High score proves encryption |

## Method Transitions and Blind Spots

- Static source → build/deployment analysis: establish that the inspected path and effective configuration shipped.
- Static source → isolated dynamic tests: exercise check failures, unsupported provider results, overrides and fallback output.
- Binary/import inspection → provider records: symbol presence cannot establish invocation, enforcement, or key provenance.
- Key inventory → audit/ceremony evidence: opaque material is not directly measurable; public keys can sometimes confirm a particular known small scalar without exporting secrets, but a negative bounded search proves no general security claim.
- Output anomaly → format-aware trace: identify protected region and boundary before interpreting a score.

For ordinary quality/control failures use the [architecture lens](../lenses/architecture/indicators/cryptographic-controls.md)
and [decisions lens](../lenses/decisions/compositions.md). Use
[BP-CRYPTOWEAK](../lenses/mcd/compositions/BP-CRYPTOWEAK.md) as a deliberate-weakening
hypothesis only with the evidence it requires.
