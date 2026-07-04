# XFRM.ENCODE: Data Encoding

## Description

Applies a reversible encoding scheme to transform data representation. Common schemes include base64 (the most widely used), base32 (uppercase A-Z + digits 2-7, no case sensitivity), base58 (omits visually ambiguous characters, standard for Bitcoin addresses, IPFS hashes, and cryptocurrency infrastructure), base85/ascii85 (more compact, wider printable ASCII range), hex encoding, and URL encoding. Encoding may be single-layer or nested (output of one encoding used as input to another). The encoded data may be decoded at runtime for use, or may exist as a transport/storage representation.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Encoding/decoding function calls (`btoa`, `atob`, `base64.b64decode`, `Buffer.from(..., 'base64')`), encoded string literals matching known encoding character sets |
| Static Binary | Yes | Encoded string literals in data sections, import of encoding library functions, encoding lookup tables |
| Runtime/Dynamic | Yes | Decoding operations producing cleartext output, encoded data in network payloads or file writes |

## Disambiguation

- **vs XFRM.ENCRYPT**: Encoding is reversible without a key, the scheme itself is the only information needed to recover the original data. Encryption requires key material. Base64 is encoding; AES is encryption; XOR with a hardcoded single-byte key straddles the line (technically encryption, but trivially reversible, flag both `XFRM.ENCODE` and `XFRM.ENCRYPT` when uncertain).
- **vs XFRM.BITWISE**: Encoding uses a defined, standardized scheme (base64, hex). Bitwise manipulation uses ad-hoc operations (XOR loops, shifts). If the transformation follows a recognized encoding standard, it's `XFRM.ENCODE`. If it uses custom bitwise operations, it's `XFRM.BITWISE`.

## Structural Relationships

- **Often co-occurs with**: `XFRM.STRCON` (encoded data assembled from fragments), `ARTF.URL` / `ARTF.IP` (encoded network targets), `LOAD.EVAL` / `EXEC.SHELL` (decoded output fed to execution)
- **May imply**: A corresponding decode operation exists somewhere in the execution path
- **Commonly part of idioms**: Decode-and-execute chain (encoded data → decode → execution primitive)

## Notes

The choice of encoding scheme carries contextual information. Base58 is the standard encoding for cryptocurrency infrastructure, its presence in non-blockchain code is a contextual signal. Base32's case-insensitivity makes it suitable for case-insensitive transports. These are factual properties of the encoding schemes, useful for recognition regardless of analytical lens.
