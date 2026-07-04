# CRED.SSH: SSH Key Access

## Description

Reads SSH private keys, `authorized_keys`, `known_hosts`, or SSH agent sockets. SSH keys are filesystem-based authentication material stored in `~/.ssh/` (or equivalent). Private keys enable authentication to remote systems; `known_hosts` maps hostnames to key fingerprints; `authorized_keys` controls who can authenticate to the local system; agent sockets provide access to loaded keys.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | SSH directory path references (`~/.ssh/`, `%USERPROFILE%\.ssh\`), private key filenames (`id_rsa`, `id_ed25519`, `id_ecdsa`), SSH agent socket access (`SSH_AUTH_SOCK`) |
| Static Binary | Yes | SSH path string literals, SSH key file format markers (`-----BEGIN`), agent socket paths |
| Runtime/Dynamic | Yes | File reads from `~/.ssh/`, SSH agent socket connections, key parsing operations |

## Disambiguation

- **vs CRED.CLOUD**: Cloud credentials are for cloud API access. SSH keys are for system-level remote access. They target different infrastructure and have different downstream capabilities.
- **vs FSYS.SENSITIVE**: `~/.ssh/` is a sensitive path. Both `CRED.SSH` and `FSYS.SENSITIVE` apply.

## Structural Relationships

- **Often co-occurs with**: `FSYS.READ` (reading key files), `FSYS.ENUM` (enumerating `~/.ssh/` directory), `NETW.*` (transmitting keys or using them for remote connections), `SYSI.*` (discovering network targets for key use)
- **May imply**: The code is aware of SSH key locations and potentially of remote systems those keys grant access to

## Notes

SSH private keys may be passphrase-protected (encrypted on disk). The key file format (`PEM`, `OpenSSH`, `PKCS#8`) and whether the key is encrypted are structural observations. Access to the SSH agent socket (`SSH_AUTH_SOCK`) provides access to all keys currently loaded in the agent without needing the key files directly.
