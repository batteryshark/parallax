# ARTF.HASH: Embedded Hash Value

## Description

Cryptographic hash digests present as string literals in source or binary. Identifiable by fixed length and hexadecimal character set: MD5 (32 hex chars), SHA-1 (40 hex chars), SHA-256 (64 hex chars), SHA-512 (128 hex chars). May also appear as base64-encoded digests or raw byte arrays of corresponding lengths. Used in comparisons, integrity checks, content addressing, or as lookup keys. The artifact is the hash value itself, a fixed-length digest embedded in the code.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Hexadecimal string constants of characteristic lengths (32, 40, 64, 128 chars), variables named `hash`, `digest`, `checksum`, `md5`, `sha256`, comparison operations against hex constants |
| Static Binary | Yes | Fixed-length hex strings in data sections, byte arrays of 16/20/32/64 bytes near comparison logic |
| Runtime/Dynamic | Yes | Hash constants used in `==` or `memcmp` comparisons, hash values checked against computed digests, hash strings used as dictionary keys or cache identifiers |

## Disambiguation

- **vs CRPT.HASH**: `ARTF.HASH` is the static presence of a hash value in code or binary. `CRPT.HASH` is the runtime operation of computing a hash. When code computes a SHA-256 digest and compares it against an embedded hex string, the computation is `CRPT.HASH` and the embedded value is `ARTF.HASH`. Both commonly co-occur.
- **vs ARTF.CREDENTIAL**: Hash values are fixed-length digests used for comparison or integrity verification. Credentials are authentication material used to authorize access. An SHA-256 digest of a known file is `ARTF.HASH`. An API key string is `ARTF.CREDENTIAL`. Some token formats resemble hex strings, length and context (authentication use vs. comparison use) disambiguate.
- **vs ARTF.CRYPTO_ADDR**: Ethereum addresses are 40 hex characters (same length as SHA-1). Bitcoin addresses are base58-encoded (similar visual appearance to base58-encoded hashes). Address-specific format markers (`0x` prefix, version bytes, checksums) and context (payment vs. integrity) disambiguate.

## Structural Relationships

- **Often co-occurs with**: `CRPT.HASH` (computing a hash to compare against the embedded value), `FSYS.READ` (reading file content to hash and verify), `ENVI.TAMPER` (hash used in integrity self-check), `NETW.HTTP` (hash used to verify downloaded content)
- **May imply**: The code performs integrity verification, content validation, or comparison against known-good values

## Notes

Hash length identifies the algorithm family. 32 hex characters is almost certainly MD5. 40 hex characters is SHA-1 (or RIPEMD-160). 64 hex characters is SHA-256. 128 hex characters is SHA-512. Base64-encoded hashes are shorter but identifiable by their encoded length (24 chars for MD5, 28 for SHA-1, 44 for SHA-256). The hash algorithm choice, what data is being verified, and the comparison outcome handling are the key structural data points.
