# BP-RANSOM: Ransomware

Encrypts files on the local filesystem and demands payment for decryption. Pattern: enumerate files, encrypt with attacker-controlled key, destroy/encrypt local key, present ransom demand.

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | `FSYS.ENUM` | Discovering files to encrypt |
| **Required** | `CRPT.SYMENC` | Encrypting file contents |
| **Required** | `FSYS.WRITE` | Writing encrypted files back |
| Supporting | `CRPT.ASYMENC` | Encrypting symmetric key with attacker's public key |
| Supporting | `ARTF.CRYPTO_ADDR` | Cryptocurrency address for ransom payment |
| Supporting | `FSYS.DELETE` | Deleting original unencrypted files |
| Supporting | `NETW.*` | C2 communication or key transmission |
| Supporting | `PRIV.*` | Privilege escalation to access more files |

## Investigation Guidance

- **Verify:** What files enumerated? Hardcoded key or generated? Ransom note or payment address present?
- **Escalates:** Asymmetric encryption of symmetric key (no self-recovery). Crypto address present. Shadow copy/backup deletion.
- **De-escalates:** Encryption applied to package's own data. Key from user input (legitimate encryption tool).
