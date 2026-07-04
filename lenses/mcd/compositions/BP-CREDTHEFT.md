# BP-CREDTHEFT: Credential Theft

Code that locates, reads, and exfiltrates authentication material. The most common objective of supply chain attacks: the attacker wants AWS keys, SSH keys, browser passwords, or API tokens. Pattern: find credentials, collect them, send them out.

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | `CRED.*` or `FSYS.SENSITIVE` | Access to credential stores, sensitive paths, or environment secrets |
| **Required** | `NETW.*` | Exfiltration channel for stolen credentials |
| Supporting | `XFRM.*` | Concealing what credentials are being targeted |
| Supporting | `SYSI.OS` or `SYSI.USER` | Profiling system to locate platform-specific credential stores |
| Supporting | `FSYS.ARCHIVE` | Packaging multiple credential files for exfiltration |
| Supporting | `ARTF.PATH` | Hardcoded paths to known credential locations |

## Real-World Analogues

The Telnyx PyPI attack (2026), npm attacks targeting `.npmrc` tokens and `.env` files. Attacker reads `~/.aws/credentials`, `~/.ssh/id_rsa`, browser databases, sends to remote endpoint.

## Investigation Guidance

- **Verify:** What specific files or credential stores are accessed? Where does the data go?
- **Escalates:** Multiple stores targeted. Data encrypted/encoded before transmission. Destination is IP or recently registered domain. Triggered at install time.
- **De-escalates:** Package is documented credential management tool. Access to own config files. No network transmission.
