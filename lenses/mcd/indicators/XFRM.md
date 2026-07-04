# MCD Lens: XFRM (Data & Code Transformation) Indicators

> **Core MCD position:** Obfuscation in a dependency is itself suspicious. Legitimate production libraries do not XOR-cipher their strings, base64-encode their logic, or build URLs from scattered character codes. The rare exception is copy protection or DRM, which is uncommon in open-source and package ecosystems. The question is not "what does the transformed code do?", it is "why is this transformed at all?"

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `XFRM.ENCODE` | Medium | Single-layer encoding of config values may be benign; encoding of operational strings (URLs, commands, paths) is higher |
| `XFRM.ENCRYPT` | Medium-High | Encryption of embedded content implies deliberate concealment; combined with `LOAD.EVAL` → Very High |
| `XFRM.STRCON` | Medium | String construction is common in programming; severity depends on what the constructed string resolves to |
| `XFRM.RENAME` | Low-Medium | Standard in frontend minification; in backend/library/non-web code, medium |
| `XFRM.CTRLFLOW` | Medium | Control flow restructuring in distributed libraries is unusual outside specific protection tools |
| `XFRM.PACK` | Medium-High | Packed binaries and self-extracting scripts add a layer that must be penetrated before analysis |
| `XFRM.UNICODE` | Medium-High | Unicode tricks serve very few legitimate purposes in package code |
| `XFRM.STEG` | Medium-High | Embedding executable content in non-code resources has very limited benign justification in packages |
| `XFRM.BITWISE` | Medium | In high-level code with no binary protocol handling; combined with `LOAD.EVAL` or `XFRM.STRCON` → escalates sharply |
| `LOAD.MEMCHAIN` | High | Multi-stage in-memory decode-and-execute chains have very limited benign justification in dependency code |

## Escalation Factors

The following conditions increase the MCD suspicion level of any XFRM finding:

- **Transformation is applied to operational strings.** Encoded or constructed URLs, IP addresses, file paths, shell commands, or domain names are significantly more suspicious than encoded configuration values or data blobs. What was the author trying to hide? If the decoded content is a URL or a command, the answer is clear.
- **Multiple transformation layers are present.** Base64-encoded content that, when decoded, reveals XOR-encrypted content that, when decrypted, reveals a shell command. Each layer adds intent. One layer could be engineering convenience. Three layers is deliberate concealment.
- **Transformation was introduced in a recent version.** Code that was clear in v1.2.3 and is transformed in v1.2.4 demands investigation. Diff the versions, what specifically was transformed, and why would a legitimate maintainer do that?
- **Transformed code is in install-time or build-time paths.** Transformations in code that runs during `npm install`, `pip install`, `setup.py`, or build hooks are a very strong signal. There is almost no legitimate reason to transform an install script's content to be unreadable.
- **The decoded or deobfuscated content feeds into an execution primitive.** `XFRM.*` → `LOAD.EVAL` or `XFRM.*` → `EXEC.SHELL` is the canonical payload delivery chain. The transformation exists specifically to conceal what is being executed.
- **The package has no documented reason for transformation.** A DRM library or a license-protected commercial component may legitimately transform code. An open-source utility library has no reason to. The stated purpose of the package is the primary context.
- **Transformation is selective.** Only specific functions or code blocks are transformed while the rest of the codebase is clear. This suggests the transformed sections contain something the author wanted to hide, not that the entire project uses a build process that produces transformed output.
- **The encoding scheme is unusual for the context.** Base58 in a non-cryptocurrency package. Base32 in code that has no case-sensitivity constraints. The choice of encoding scheme can itself be a signal about what the encoded content is or what ecosystem the author operates in.

## De-escalation Factors

The following conditions reduce, but do not eliminate, MCD suspicion:

- **The package's stated purpose involves transformation or encoding.** A compression library, a serialization library, or a build tool may legitimately produce output that appears transformed. Verify that the transformation patterns are consistent with the stated purpose.
- **The transformation is the output of a standard, documented build process.** Frontend JavaScript minification via webpack, Terser, or similar tools produces `XFRM.RENAME` and sometimes `XFRM.CTRLFLOW` patterns. This is expected in browser-targeting code, the same patterns in a Node.js backend library, a Python package, or server-side code are not explained by minification.
- **The encoded content, when decoded, is clearly benign.** A base64-encoded PNG asset, a hex-encoded binary blob that matches a documented data format, or an encoded string that resolves to a well-known public endpoint. The act of decoding and verifying IS the investigation, the encoding alone is not proof of benignity.
- **The transformation has been present since the package's initial release** and is consistent across all versions. A package that has always shipped minified code is less suspicious than one that suddenly started. However, this does not eliminate suspicion, a malicious package can be transformed from day one.
- **Source maps or untransformed source is available.** If the publisher provides source maps alongside minified code, or if the original source is in the repository and the build process is reproducible, the transformation is less suspicious because it can be independently verified against the original.

> **Caveat:** Transformation that appears in a commonly benign pattern (e.g., minified JavaScript) can still be weaponized. An attacker can hide malicious code inside minified bundles precisely because reviewers expect minification and skip it. De-escalation reduces priority; it does not grant a pass.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `XFRM.*` + `LOAD.EVAL` or `EXEC.SHELL` | Obfuscated payload being decoded and executed, canonical payload delivery chain | Very High |
| `XFRM.ENCODE` + `ARTF.URL` or `ARTF.IP` | Encoded network target, the author is hiding where the code communicates | High |
| `XFRM.STRCON` + `ARTF.CMD` | Shell command assembled from fragments to avoid string detection | High |
| `XFRM.ENCRYPT` + `CRPT.SYMENC` | Encrypted payload with the decryption key embedded nearby, encryption for concealment, not security | High |
| `LOAD.MEMCHAIN` + `XFRM.ENCODE` | Multi-layer decode-and-execute chain, staged malware delivery | Very High |
| `XFRM.*` + `PKGM.INSTALL` | Obfuscated install-time code, no legitimate reason to hide what an install script does | Very High |
| `XFRM.BITWISE` + `LOAD.EVAL` | Bitwise-transformed data fed into code execution, hand-rolled decryption of a payload | Very High |
| `XFRM.UNICODE` + `AITM.INVISIBLE` | Unicode tricks hiding AI-targeted prompt injection, dual-target attack on human reviewers and AI agents | High |
| `XFRM.*` + `EVSN.*` | Code that is both concealed and environmentally aware, combination of concealment and activation control | High |

## MCD-Specific Disambiguation

### XFRM.ENCODE vs. legitimate data handling
Base64 encoding is used extensively in legitimate contexts: data URIs, binary data in JSON, email attachments, JWT tokens. The MCD signal is not "base64 exists", it is "base64 is being used to conceal operational strings that would trigger investigation if visible." Always decode before assessing. The content determines the MCD classification, not the encoding.

### XFRM as severity multiplier
Through the MCD lens, any `XFRM` atom acts as a severity multiplier on co-occurring atoms. A hardcoded URL (`ARTF.URL`) is low-medium. An encoded hardcoded URL (`ARTF.URL` + `XFRM.ENCODE`) is high, the encoding implies the author wanted the URL to be non-obvious. This multiplier effect is an MCD interpretation, not a structural property.

### XFRM + EVSN composition
Code that is both transformed (concealed) and environment-aware (evasion) through the MCD lens is read as: "the author hid what the code does AND made it check where it's running." The combination of concealment and activation control is a stronger malice indicator than either alone.
