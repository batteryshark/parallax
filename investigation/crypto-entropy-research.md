# Cryptographic key quality and lifecycle research

Research snapshot: 2026-10-21. This note separates published evidence from proposed Parallax modeling. The incident investigation remained open when reviewed; later root-cause findings may supersede the provisional explanation.

## Incident evidence

Mozilla's Dennis Jackson reports independently recovering eight eMudhra P-384 intermediate private keys after Wayne's disclosure. All eight scalars were below 256. This concerns the B/C intermediate series created in April 2025, not a demonstrated recovery of a root private key. Root distrust is a response, not evidence that the root key itself was recovered. [Mozilla incident, comment 5](https://bugzilla.mozilla.org/show_bug.cgi?id=2083449#c5).

Scott Helme reports reproducing recovery from the published certificates. His table gives the following decimal private scalars; these values are attributed to that reproduction, not to a new experiment performed for this note. [Helme's first-person reproduction](https://scotthelme.co.uk/eight-bits-of-trust-emudhras-ca-keys-cracked-in-milliseconds/).

| Intermediate | Private scalar |
|---|---:|
| EM DV TLS CA - G3B | 156 |
| EM DV TLS CA - G3C | 230 |
| EM EV TLS CA - G3B | 115 |
| EM EV TLS CA - G3C | 56 |
| EM OV TLS CA - G3B | 155 |
| EM OV TLS CA - G3C | 4 |
| EM OV CS CA - G3B | 66 |
| EM OV CS CA - G3C | 237 |

Thus `0x73` is 115, distinct from the scalar-4 example. A scalar below 256 represented as a fixed-width 48-byte P-384 integer has 47 leading zero bytes. “Single-byte value” describes its numeric range, not the length of a certificate or serialized private-key object. This is arithmetic applied to the reported values.

eMudhra attributes the weak replacement keys to a wrap/unwrap step in its key-generation ceremony and says its root-cause investigation continues. It also states that infrastructure was not compromised and data was not breached. These are the operator's statements, not independent findings by Parallax. [eMudhra statement, October 21, 2026](https://emudhra.com/en/press-release/emudhra-statement-distrust-global-tls-intermediate-root-ca).

The incident record also ties previous invalid CRL signatures to different key material, according to the CA's explanation. That makes end-to-end key identity continuity worth examining, beyond initial random generation. The available evidence does not establish deliberate insider sabotage. [eMudhra response, comment 11](https://bugzilla.mozilla.org/show_bug.cgi?id=2083449#c11).

## Why a validity check is not an entropy guarantee

NIST separates correct generation, private-key range validity, public-key validity, and pairwise consistency. It explicitly explains that correct random selection cannot be verified after the fact. A small nonzero EC scalar can satisfy range checks, and its correctly derived public key can satisfy pairwise consistency; neither proves unpredictable generation. The cited document addresses key establishment, while its distinction between these assurances is useful to Parallax's broader key-lifecycle model. [NIST SP 800-56A Rev. 3, sections 5.6.1–5.6.2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-56Ar3.pdf).

OpenSSL documents EC private-key and pairwise checks in terms of those separate assurances. Therefore, observing a call such as `EVP_PKEY_private_check` must not become a finding that sufficient entropy was established. [OpenSSL EC validation documentation](https://docs.openssl.org/master/man7/EVP_PKEY-EC/).

Entropy-source validation and health testing address how randomness is produced. NIST SP 800-90B describes noise sources, conditioning, min-entropy assessment, and health tests; its tests are not a universal Shannon-entropy threshold for individual production keys. [NIST SP 800-90B](https://csrc.nist.gov/pubs/sp/800/90/b/final). Statistical test suites cannot establish cryptographic suitability on their own. [NIST SP 800-22 Rev. 1a](https://csrc.nist.gov/pubs/sp/800/22/r1/upd1/final).

Key managers also support importing caller-supplied material. AWS explicitly assigns responsibility for imported material to the customer; import events can be audited through CloudTrail. This is evidence of a distinct lifecycle boundary, not evidence that AWS lacks internal checks. Public documentation's silence about a particular screen cannot establish that the implementation omits it. [AWS imported-key responsibility](https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html), [AWS import operation and audit events](https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys-import-key-material.html).

## Measurement limits

The following are analytical consequences and proposed interpretation rules:

- Entropy describes a source distribution or an explicitly modeled uncertainty, not a property provable from one byte string. A byte histogram is a descriptive statistic. Store the estimator, representation, sample size, window, and assumptions alongside its result.
- For a sample containing `n` bytes, empirical byte-frequency Shannon entropy is at most `log2(min(n, 256))` bits per byte. A 32-byte sample therefore cannot score above 5 by that estimator, even if every byte differs. A universal “near 8 bits per byte” requirement would reject ordinary short keys.
- A fixed public hash can look statistically random while being completely predictable. Hashing a constant seed cannot create secret uncertainty. Conversely, structured key containers, fixed-width integer padding, curve-specific encodings, and short samples can look nonuniform without proving insecure generation.
- Exact weak-pattern checks can be useful defense in depth: known test material, public constants, repetitions, unexpectedly small scalars, deterministic public seeds, truncation, and key reuse. Record the tested predicate and algorithm. Passing a bounded screen excludes only the tested family.
- A public EC point generally does not reveal the private scalar's byte distribution. A successful bounded candidate match is concrete recovery evidence; an unsuccessful search does not certify key strength.
- Opaque HSM/KMS handles may make private bytes unobservable. Preserve this as unknown. Inspect generation provenance, applicable module health status, key identity, import events, policy enforcement, and production use without exporting secrets for scoring.

## Ciphertext is a separate evidence problem

AEAD distinguishes ciphertext from associated data that is authenticated but not encrypted. It also imposes algorithm-specific nonce requirements and rejects unauthentic ciphertext on decryption. These semantics are more meaningful than a file-wide byte histogram. [RFC 5116, sections 2–3 and 5.1.1](https://www.rfc-editor.org/rfc/rfc5116.html).

Proposed interpretation: normalize only a documented encoding and identify the actual encrypted payload before measuring. A low score on hex, base64, headers, padding, or a short record cannot establish plaintext exposure. A high score on compressed or otherwise transformed data cannot establish encryption. Record low distributional entropy as a triage observation; corroborate with runtime data flow, format validation, expected authentication behavior, or a controlled canary showing plaintext reaches the output. Never export production secrets or plaintext into investigation fixtures.

## Recommended Parallax improvements

These are design recommendations, not vendor findings:

| Layer | Improvement | Evidence boundary |
|---|---|---|
| Ontology | Distinguish key loading/import/unwrap from generation, and key validation from certificate validation | An API invocation records a behavior; it does not prove a successful check or secure key |
| Enrichment | Capture algorithm, key role/origin, lifecycle stage, representation, production reachability, measurements, predicates, check outcomes, enforcement, and coverage | Do not store private bytes; separate unobserved, observed failure, bypass, and bounded absence |
| MCD | Model deliberate weakening as weak or substituted material reaching protected use, with contextual evidence of tampering, selective activation, bypass, or concealment | Severe cryptographic impact alone does not establish malicious intent or identify an insider |
| Architecture | Identify gaps in generation, import, wrap/unwrap, restore, rotation, activation, and alert handling | Require a bounded path or control inventory before claiming a missing check |
| Decisions | Identify the exact admission decision and whether rejected/unknown results block use | A check whose result is ignored is not an enforced gate |
| Capability | Trace signing/decryption/impersonation authority of recoverable material and its reachable consumers | Possibility and blast radius remain separate from observed exploitation |
| Investigation | Follow one key identity from creation through transfers and production use; examine return values, public-key fingerprints, audit events, and failure paths | Account for controls inside libraries, services, hardware, and deployment policy |

Insider threat should therefore be an investigable hypothesis: a person or malicious change could replace protected randomness with reproducible material and enable later recovery without exporting an original key. Alternatives include implementation errors, test fixtures, encoding mistakes, failed imports, and intentional deterministic derivation from an adequately protected secret. Preserve these alternatives and specify what would distinguish them.

A useful operational review tests three outcomes independently: defective material is detected, activation is prevented where required, and an accountable alert/audit event occurs. Review the strong-key-to-weak-key substitution path as well as weak initial generation. Capture results in scanner-owned evidence; Parallax supplies the vocabulary and interpretation contracts rather than becoming a key manager or production entropy scanner.
