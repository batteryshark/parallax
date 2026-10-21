# Cryptographic Material Signals

These signals modify hypotheses grounded in reachable operations. Security impact,
confidence in a defect, and confidence in deliberate weakening are separate.

| Signal | Evidence | Confidence effect on deliberate weakening |
|---|---|---|
| Predictable secret reaches production | `ENR.CRYPTO.MATERIAL` + `ENR.CRYPTO.USE`; value flow to signing, encryption, or authentication | Establishes exposure when confirmed, but accidental fixtures, import errors, and generator defects remain alternatives |
| Check result bypassed | `ENR.CRYPTO.CONTROL`; rejected/unsupported/error result followed by activation/use | Raises concern; intent requires independent change or concealment evidence |
| Unapproved key replacement or RNG substitution | `ENR.CRYPTO.CHANGE` + `ENR.CRYPTO.ORIGIN`; audit-linked deployment change | Amplifies when the changed path explains the affected production key |
| Alerts selectively suppressed | `ENR.CRYPTO.CONTROL` + `ENR.CRYPTO.CHANGE`; delivery disabled or exceptions scoped to the substituted material | Amplifies with linked evidence, not merely absent logs |
| Encryption fallback returns input | `ENR.CRYPTO.OUTPUT`; traced plaintext reaches a sink that requires encryption | Confirms protection failure for that path; malicious intent remains a separate hypothesis |
| Isolated test fixture | `ENR.CRYPTO.USE`; test-only reachability and deployment exclusion verified | Attenuates a production-weakening hypothesis; a filename alone is insufficient |
| Enforced boundary and provenance | `ENR.CRYPTO.ORIGIN` + `ENR.CRYPTO.CONTROL`; assessed import/recovery paths reject disallowed material and deliver alerts | Attenuates within tested scope; certification labels or a successful import alone do not suffice |
| Byte score alone | `ENR.CRYPTO.MEASUREMENT` without material role, provenance, or value flow | Insufficient to infer either cryptographic strength or malice |

Insider access is one possible route, alongside compromised automation, supply-chain
changes, defective tooling, and operational error. An account name in an audit
record identifies a session; it does not establish which person controlled it.
No exfiltration is needed if an actor can arrange for a known private value to
become trusted. Conversely, no exfiltration observed is not proof of that strategy.

Use [BP-CRYPTOWEAK](../compositions/BP-CRYPTOWEAK.md) only with its required evidence.
An unexplained weak key belongs in the architecture/security assessment even if
the malicious hypothesis remains unsubstantiated.
