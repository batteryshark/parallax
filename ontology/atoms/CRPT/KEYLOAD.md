# CRPT.KEYLOAD: Cryptographic Key Loading / Import

## Description

Loads existing cryptographic key material into a key object, provider, keystore, or hardware module. Includes decoding serialized keys, constructing a key from supplied numeric components, and importing or unwrapping externally supplied key material. Loading does not establish how the material was generated or whether it is approved for use.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `serialization.load_pem_private_key()`, `ec.derive_private_key(value, curve)`, `crypto.createSecretKey()`, `crypto.subtle.importKey()`, `PEM_read_bio_PrivateKey()`, key import / unwrap calls |
| Static Binary | Partial | Key decoding/import symbols and key-object construction; stripped or provider-internal paths may be invisible |
| Runtime/Dynamic | Partial | Import/unwrap events, key handles, origin metadata; non-exportable private material may remain inaccessible |

## Disambiguation

- **vs CRPT.KEYGEN**: KEYGEN produces new random or derived material. KEYLOAD accepts already-selected material, including an EC scalar supplied to a function named `derive_private_key`. A name containing "create" or "derive" does not establish fresh randomness.
- **vs CRED.***: Reading a credential store is credential access. Converting the retrieved material into an operational key is KEYLOAD. Tag both when both occur.
- **vs CRPT.KEYCHECK**: Parsing, import, range checking, and quality policy are distinct operations. Emit KEYCHECK additionally only when the check itself is observed; successful import is not evidence of all checks.
- **vs CRPT.CERT**: Loading a certificate concerns the certificate object and trust infrastructure. Loading its key separately is KEYLOAD.

## Structural Relationships

- **Often co-occurs with**: `CRPT.SYMENC`, `CRPT.SIGN`, `CRPT.KEYEX`, `CRPT.KEYCHECK`, `CRED.*`, `ARTF.CREDENTIAL`
- **May imply**: A key value selected outside this operation becomes available to a cryptographic consumer

## Notes

Record public/private/symmetric role, algorithm and parameter set, input format, material origin, provider, key handle/version, and intended usage. Public-key loading does not imply access to a private key. Record import, activation, and first use separately; an import call alone proves neither production reachability nor activation. Key handles and references should be recorded without copying secret bytes into observations.

See the [cryptographic material investigation contract](../../../investigation/cryptographic-material.md) for generation provenance, validation coverage, and production-use evidence.
