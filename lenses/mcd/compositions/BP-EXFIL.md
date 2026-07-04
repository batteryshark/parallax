# BP-EXFIL: Data Exfiltration

Collects data from the local system and transmits it externally. Distinct from credential theft in scope: targets arbitrary valuable data (source code, databases, documents, configuration), not specifically authentication material.

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | `FSYS.READ` or `FSYS.ENUM` or `CRED.*` or `SYSI.PROCMEM` | Reading, discovering, or collecting target data |
| **Required** | `NETW.*` | Transmitting data externally, any network channel |
| Supporting | `ARTF.EMAIL` | Hardcoded email exfiltration target |
| Supporting | `ARTF.URL` or `ARTF.IP` or `ARTF.DOMAIN` | Hardcoded exfiltration destination |
| Supporting | `NETW.WEBHOOK` | Exfiltration via messaging APIs (Discord, Telegram) |
| Supporting | `FSYS.ARCHIVE` | Bundling data for efficient exfiltration |
| Supporting | `XFRM.ENCODE` or `CRPT.SYMENC` | Encoding/encrypting data before transmission |
| Supporting | `NETW.DNS` | DNS tunneling for covert exfiltration |
| Supporting | `SYSI.*` | Profiling system to identify high-value targets |
| Supporting | `ENVI.*` | Rate-limiting or timing exfiltration to avoid detection |

## Investigation Guidance

- **Verify:** What data is read? Where is it sent? Who controls the destination?
- **Escalates:** Large volumes. Destination is hardcoded IP, recent domain, free email, or personal webhook. Source code or database access. Covert channel (DNS, steganography). Data encrypted before transmission.
- **De-escalates:** Standard telemetry/crash reporting. Well-known analytics service. Documented transmission.
