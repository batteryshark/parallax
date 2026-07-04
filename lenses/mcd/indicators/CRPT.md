# MCD Lens: CRPT (Cryptographic Operations) Indicators

> **Core MCD position:** Cryptography is dual-use by nature. The same AES-256 call appears in a password manager and in ransomware. The signal comes from context: cryptographic operations in code whose stated purpose has nothing to do with cryptography are a primary thread to pull. Unexpected crypto in a dependency is often the first indicator that unravels the full attack picture. The LiteLLM attack embedded a complete hybrid RSA-4096 + AES-256-CBC pipeline plus a full AWS SigV4 implementation, none related to its stated purpose as an LLM proxy.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `CRPT.SYMENC` | Medium-High | In non-crypto libraries, severity increases with filesystem or network co-occurrence |
| `CRPT.ASYMENC` | Medium-High | Paired with hardcoded public key = High |
| `CRPT.KEYGEN` | Medium | Depends on key lifecycle, transmitted keys higher than local-only |
| `CRPT.RNG` | Low-Medium | CSPRNG access alone is common; notable when no declared crypto dependency explains it |
| `CRPT.HASH` | Low-Medium | Widely used for integrity; escalates when combined with credential or network operations |
| `CRPT.CREDHASH` | Medium-High | Outside authentication systems = suspicious |
| `CRPT.SIGN` | Medium | Escalates with hardcoded keys or unexplained signing schemes |
| `CRPT.KEYEX` | High | In non-communication code = covert channel setup |
| `CRPT.CERT` | High | Installing CAs or disabling verification = immediate escalation |
| `CRPT.CUSTOM` | High | Hand-rolled crypto is the single strongest individual CRPT signal |

## Escalation Factors

- **`CRPT.CUSTOM` is present in any capacity.** Hand-rolled crypto is the strongest CRPT signal. Legitimate developers use audited libraries. Any custom implementation warrants immediate escalation.
- **Asymmetric public key is hardcoded in source or binary.** A hardcoded attacker-controlled public key means the code encrypts data only a predetermined recipient can read. No legitimate application hardcodes a foreign public key.
- **`CRPT.KEYEX` in code with no communication or protocol role.** Key exchange establishes a shared secret between two parties. Without a documented protocol or network role, this is covert channel setup.
- **`CRPT.CERT` disables verification or installs a new root CA.** These operations have one primary illegitimate use: intercepting traffic the application isn't supposed to see.
- **Crypto operations present with no declared crypto dependency.** Undeclared crypto indicates hand-rolled implementation or smuggled code through an obscured transitive dependency.
- **`CRPT.SYMENC` or `CRPT.KEYGEN` co-located with filesystem enumeration.** Enumerating files then generating keys is the ransomware preparation sequence.
- **Key or IV material derived from victim-specific runtime data.** Keys derived from hostname, MAC address, or username produce deterministic per-victim encryption, a ransomware and C2 beacon pattern.
- **Crypto operations present only in post-install hooks or non-obvious execution paths.** Supply chain attacks hide crypto in lifecycle scripts precisely because reviewers focus on primary package code.
- **`CRPT.HASH` or `CRPT.SIGN` on outbound data immediately before network call.** Hashing or signing before exfiltration serves to verify stolen data integrity at the receiver.
- **`CRPT.CUSTOM` combined with `XFRM.*`.** Transformation layered on hand-rolled crypto is a deliberate attempt to slow analysis, the highest-confidence cluster in the CRPT category.

## De-escalation Factors

- **Well-known, audited library call with no customization.** Straightforward call to `cryptography`, `libsodium`, `OpenSSL`, or equivalent with no monkey-patching. *(Caveat: verify the import resolves to the genuine library; supply chain attacks impersonate crypto library names.)*
- **Crypto operation is the declared, documented purpose of the package.** An encryption utility or TLS wrapper will legitimately contain high CRPT concentrations. *(Caveat: when crypto scope exceeds stated purpose, as with LiteLLM's full SigV4 + RSA pipeline, treat the excess as unexplained.)*
- **`CRPT.HASH` used exclusively for integrity checking or content addressing.** Hashing for cache keys, download verification, or content-addressable identifiers is low-risk. *(Caveat: confirm hash output isn't subsequently used as key material, HMAC secret, or transmitted outbound.)*
- **`CRPT.CREDHASH` in a clearly scoped authentication module.** bcrypt/argon2 in password storage context is expected. *(Caveat: does not apply outside auth scope.)*

> **Caveat:** Cryptography is inherently dual-use. De-escalation based on the cryptographic operation itself is never sufficient: what is being encrypted, why, and what happens to the output determines intent.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `CRPT.ASYMENC` + `CRPT.SYMENC` + `CRPT.KEYGEN` | Hybrid encryption with per-victim key, ransomware key setup | Critical |
| `CRPT.CUSTOM` + `XFRM.BITWISE` | Hand-rolled crypto obfuscated with bitwise operations, highest-confidence combined signal | Critical |
| `CRPT.CERT` + `NETW.HTTP` | Certificate manipulation + network calls, MITM enablement | High |
| `CRPT.KEYEX` + `NETW.SOCKET` / `NETW.HTTP` | Key exchange + network, covert encrypted channel establishment | High |
| `CRPT.ASYMENC` + hardcoded key + `CRPT.SIGN` | Asymmetric encryption + signing with fixed key, C2 authentication | High |
| `CRPT.SYMENC` + `FSYS.ENUM` + `FSYS.WRITE` | File enumeration + encryption + write-back, ransomware execution loop | Critical |
| `CRPT.HASH` + `NETW.*` | Hashing before network send, integrity-checked exfiltration | Medium-High |
| `CRPT.CUSTOM` + `CRPT.SIGN` | Hand-rolled signing scheme, self-contained authentication without library dependency | High |
| `CRPT.KEYGEN` + `ENVI.ENVCHECK` / system fingerprinting | Key derived from victim identifiers, per-victim deterministic encryption | High |
| `CRPT.CERT` + `CRPT.CUSTOM` + `NETW.HTTP` | Full MITM stack, custom crypto + cert manipulation + outbound HTTP | Critical |

## MCD-Specific Disambiguation

### CRPT.CUSTOM vs. XFRM.BITWISE: The Key Distinction
Through the MCD lens, both are high-severity, but the combination is the highest-confidence cluster in the taxonomy. `CRPT.CUSTOM` means a recognizable cryptographic algorithm is implemented without library support. `XFRM.BITWISE` means ad-hoc bitwise operations with no recognizable algorithm structure. When custom crypto is further obfuscated with bitwise operations, the attacker has invested in both self-contained implementation (avoiding detectable library imports) and analysis resistance. This double investment is the strongest individual indicator of deliberate malicious engineering.

### CRPT.SYMENC vs. XFRM.ENCRYPT: Artifact-Level vs. Data-Level
Through the MCD lens, `XFRM.ENCRYPT` (encrypting the artifact's own strings or payload for runtime decryption) is consistently higher severity than `CRPT.SYMENC` (encrypting operational data). XFRM.ENCRYPT conceals the attack itself. CRPT.SYMENC may be the attack's mechanism (ransomware, exfil encryption) or completely legitimate (application-level encryption). The first is always suspicious in dependency context; the second requires additional context.

### CRPT in Dependencies: The Scope Test
Through the MCD lens, the primary question for any CRPT finding in a dependency is: does the cryptographic scope match the declared purpose? An LLM routing library with no documented security features implementing RSA-4096 + AES-256-CBC + full SigV4 from scratch fails the scope test catastrophically. The excess crypto (crypto beyond what the stated purpose requires) is the signal, not the crypto itself.
