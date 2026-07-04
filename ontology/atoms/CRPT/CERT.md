# CRPT.CERT: Certificate Operations

## Description

Operations on X.509 certificates and the PKI trust model: generating self-signed certificates, creating certificate signing requests, loading and parsing certificates, installing certificates into system or application trust stores, modifying certificate validation behavior (disabling verification, implementing custom verification, pinning to specific certificates), and extracting keys from certificate stores. The mechanical behavior is manipulating the certificate infrastructure that underpins TLS and other trust-based protocols.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `ssl.create_default_context()` with verification disabled, `ssl._create_unverified_context()`, `X509Certificate` operations, trust store path writes, `CERT_STORE_ADD_*` constants, `SecTrustSettingsSetTrustSettings()`, custom `verify_callback` functions |
| Static Binary | Yes | Certificate API imports, trust store path strings, PEM/DER marker strings, certificate validation function references |
| Runtime/Dynamic | Yes | Trust store modifications, certificate loading, TLS handshake with modified verification, new certificates appearing in system stores |

## Disambiguation

- **vs CRPT.SIGN**: Signing operations produce or verify signatures on data/messages. Certificate operations manage the certificate lifecycle and trust model. Certificate verification involves signature checking internally, but CERT covers the trust infrastructure, loading, installing, trusting, or distrusting certificates.
- **vs ENVI.SECDISABLE**: Disabling certificate verification is CRPT.CERT because it specifically targets the PKI trust model. Disabling firewalls, AV, or exploit mitigations is ENVI.SECDISABLE because those are host-level security controls. Both weaken security posture but target different mechanisms.
- **vs CRPT.KEYGEN**: Generating a key pair for a self-signed certificate involves both KEYGEN (the key pair) and CERT (the certificate wrapping the key). When certificate generation is the primary operation, CERT is the primary atom.

## Structural Relationships

- **Often co-occurs with**: `NETW.*` (certificates enable or modify network trust), `ENVI.SECDISABLE` (certificate manipulation as part of broader security weakening), `CRPT.KEYGEN` (generating keys for certificates)
- **May imply**: The trust model for TLS or other certificate-based protocols is being modified

## Notes

The specific operation is critical structural data. Loading a certificate from a well-known CA for verification is standard TLS usage. Disabling certificate verification entirely, installing a new root CA, or generating self-signed certificates at runtime each have different structural implications. Whether the modification is to the system trust store (affects all applications) or application-specific (scoped to this process) is also relevant.
