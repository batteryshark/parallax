# MCD Lens: XFRM (Data & Code Transformation) Verification

Investigation questions for XFRM findings, organized for MCD triage. Questions tagged `[lens-neutral]` are applicable across multiple lenses and may be factored to the shared investigation framework later. Questions tagged `[MCD]` assume an MCD evaluation context.

## General: Any XFRM Atom

1. **What is the decoded/detransformed content?** Before assessing anything else, reverse the transformation. The content determines severity. An encoded PNG is fundamentally different from an encoded shell command. `[lens-neutral]`

2. **Where in the codebase does this appear?** Install script, application code, test file, build artifact? Location within the project structure is a primary contextual factor. `[lens-neutral]`

3. **Is this transformation present in previous versions?** If it was introduced in a recent update, diff the versions to identify exactly what changed. Behavioral changes between versions are relevant to multiple lenses. `[lens-neutral]`

4. **Does the package's stated purpose explain the transformation?** A crypto library may legitimately contain encoded test vectors. A string utility library should not contain encoded URLs. Consistency with stated purpose is the primary MCD evaluation context. `[MCD]`

5. **Is the transformation selective or pervasive?** Are specific functions or strings transformed while the rest is clear? Selective transformation targeting specific code sections is a different signal than pervasive transformation from a build process. `[lens-neutral]`

## XFRM.ENCODE: Data Encoding

6. **What encoding scheme is used, and is it typical for this ecosystem?** Base64 in a JavaScript package is common. Base58 in a non-crypto Python package is contextually unusual. The scheme choice narrows the likely domain of the encoded content. `[lens-neutral]`

7. **How many encoding layers are present?** Decode iteratively. If the output of one decode is another encoded string, count the layers. Through the MCD lens, each additional layer increases the inference of deliberate concealment. `[MCD]`

## XFRM.STRCON: String Construction

8. **What string does the construction produce?** Reconstruct the full string. Determine whether it resolves to a URL, file path, shell command, domain name, or other recognizable artifact type. `[lens-neutral]`

9. **Where do the fragments come from?** Are they all hardcoded in the source, or do some originate from network responses, environment variables, or decoded/decrypted data? Dynamic fragment sources change the nature of the construction: the resulting string cannot be fully determined statically. `[lens-neutral]`

## XFRM.ENCRYPT: Data Encryption

10. **Where is the key material?** Is the decryption key hardcoded adjacent to the encrypted data, derived from a predictable source, or fetched at runtime? Key proximity to ciphertext is a structural observation; through the MCD lens, hardcoded adjacent keys indicate concealment rather than protection. `[MCD]`

## LOAD.MEMCHAIN: In-Memory Execution Chain

11. **How many stages are in the chain?** Trace each decode-and-execute hop. Each stage may contain independent indicators. The full chain must be unraveled to understand the final payload. `[lens-neutral]`

12. **Does any stage write to disk?** If no intermediate artifact touches the filesystem, all analysis must happen through the decode chain: there are no files to scan separately. This determines the investigation method required (static chain analysis vs. filesystem artifact analysis). `[lens-neutral]`

## XFRM.BITWISE: Bitwise Data Manipulation

13. **Does the bitwise pattern correspond to a known algorithm?** XOR with a repeating key, TEA/XTEA, RC4: recognizable algorithms help predict what the output should look like and how to reverse it. Unknown patterns require more investigation effort. `[lens-neutral]`

## Cross-Cutting

14. **Does the transformed content feed into an execution primitive?** Trace the data flow from the transformation output. If it reaches `eval()`, `exec()`, `subprocess`, `Function()`, `CreateThread`, or similar, the transformation is in the execution path, not just a data representation choice. `[lens-neutral]`

15. **Is there a documented build process that explains the transformation?** Check for build scripts, CI configuration, webpack/rollup/esbuild config, Makefile targets, or documented obfuscation tools. If the build process is reproducible and the transformation is explainable, it reduces MCD priority. `[MCD]`
