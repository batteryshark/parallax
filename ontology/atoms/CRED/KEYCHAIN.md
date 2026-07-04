# CRED.KEYCHAIN: OS Credential Store Access

## Description

Accesses operating system-provided credential storage: macOS Keychain, Windows Credential Manager, Linux keyrings (GNOME Keyring, KWallet, libsecret). These are OS-managed secure storage facilities designed to hold passwords, tokens, certificates, and other authentication material with access-controlled retrieval.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Keychain/credential manager API calls (`SecItemCopyMatching`, `CredRead`, `SecretService`, `keyring` library), service name/account parameters |
| Static Binary | Yes | Credential store function imports, Security framework references |
| Runtime/Dynamic | Yes | Keychain access prompts (macOS), credential manager queries, keyring daemon communication |

## Disambiguation

- **vs CRED.TOKEN / CRED.CLOUD**: `CRED.KEYCHAIN` accesses the OS-level credential store via its API. `CRED.TOKEN` and `CRED.CLOUD` access token/credential files directly on disk. Some tools store credentials in both (e.g., AWS CLI can use OS keychain or `~/.aws/credentials`). Classify by the access method: API query to OS store = KEYCHAIN; file read = CLOUD/TOKEN.

## Structural Relationships

- **Often co-occurs with**: `NETW.*` (transmitting retrieved credentials), `SYSI.OS` (determining which OS credential store to query), `FSYS.SENSITIVE` (keychain files on disk)
- **May imply**: The process has user-level permissions sufficient for credential store access

## Notes

OS credential stores typically require user-level authentication or per-application access grants. macOS Keychain prompts the user when a new application requests access. Windows Credential Manager is accessible to processes running as the user. The specific credential store queried and the service/account names requested are key structural data.
