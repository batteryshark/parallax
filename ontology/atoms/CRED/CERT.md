# CRED.CERT: Certificate and Private Key Access

## Description

Accesses TLS/SSL certificates, private keys, or certificate stores. Includes reading PEM/DER certificate files, PKCS#12 keystores, system certificate stores, and private key files used for TLS server identity, client authentication, or code signing. The accessed material may include public certificates (identifying information) or private keys (authentication capability).

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Certificate file path references (`.pem`, `.crt`, `.key`, `.p12`, `.pfx`), certificate store API calls, X.509 parsing library usage |
| Static Binary | Yes | Certificate file format markers (`-----BEGIN CERTIFICATE-----`), certificate path strings, crypto library imports |
| Runtime/Dynamic | Yes | Certificate store queries, PEM/DER file reads, TLS context configuration with loaded certificates |

## Disambiguation

- **vs CRED.SSH**: SSH keys authenticate to SSH servers. Certificates authenticate to TLS/HTTPS services and can sign code. Both are public-key cryptographic material but serve different protocols and infrastructure.
- **vs CRPT.***: `CRPT.*` describes the use of cryptographic operations (encryption, signing, hashing). `CRED.CERT` describes accessing certificate and key material. Loading a private key file is `CRED.CERT`. Using that key to sign data is `CRPT.*`. Both commonly co-occur.

## Structural Relationships

- **Often co-occurs with**: `CRPT.*` (using the certificate/key for crypto operations), `NETW.LISTEN` (configuring a TLS server with the certificate), `NETW.HTTP` (client certificate authentication), `FSYS.READ` (reading certificate files from disk)
- **May imply**: The code configures TLS identity or performs certificate-based authentication

## Notes

Private key material is the critical component. Public certificates are, by design, not secret. The distinction between accessing a public certificate (for verification) and accessing a private key (for authentication/signing) is a key structural observation. Certificate store locations vary by platform: `/etc/ssl/`, system keychain on macOS, Windows certificate store, Java KeyStore files.
