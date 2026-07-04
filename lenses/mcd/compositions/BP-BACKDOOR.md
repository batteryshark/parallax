# BP-BACKDOOR: Backdoor

Mechanisms providing unauthorized access by bypassing normal authentication. Two variants with different atom signatures but identical risk:

**Variant A (Remote Access):** Persistent remote command execution via C2 listener, reverse shell, or polling loop.

**Variant B (Authentication Bypass):** Hardcoded credentials, hidden accounts, magic tokens, or logic short-circuiting authentication checks.

## Constituent Atoms: Variant A (Remote Access)

| Role | Atom | Notes |
|---|---|---|
| **Required** | `NETW.LISTEN` or `NETW.HTTP` (polling) | Receives instructions, listening or polling |
| **Required** | `EXEC.SHELL` or `EXEC.PROC` | Executes received commands |
| Supporting | `PRST.*` | Persistence to survive reboots |
| Supporting | `XFRM.*` | Concealing backdoor logic |
| Supporting | `ENVI.*` | Evading detection while running |
| Supporting | `CRPT.SYMENC` | Encrypted command channel |
| Supporting | `ARTF.IP` or `ARTF.DOMAIN` | Hardcoded C2 infrastructure |
| Supporting | `NETW.DECENTRAL` | Takedown-resistant C2 channel |

## Constituent Atoms: Variant B (Authentication Bypass)

| Role | Atom | Notes |
|---|---|---|
| **Required** | `ARTF.CREDENTIAL` | Hardcoded password, token, API key, or crypto key granting access |
| Supporting | `ARTF.HASH` | Hardcoded hash that a known password is compared against |
| Supporting | `XFRM.ENCODE` or `XFRM.ENCRYPT` | Encoded/encrypted credentials |
| Supporting | `XFRM.STRCON` | Credential assembled from fragments |
| Supporting | `ENVI.ENVCHECK` | Bypass activates only in specific environments |
| Supporting | `NETW.LISTEN` | Hidden administrative endpoint |

## Real-World Analogues

**A:** SolarWinds SUNBURST (2020), XZ Utils (2024), LiteLLM sysmon.service daemon.
**B:** Juniper ScreenOS (2015): hardcoded password on every firewall. Default credentials in IoT.

## Investigation Guidance

- **Verify (A):** Communication pattern? Listening or polling? C2 target? Command scope?
- **Verify (B):** What does the credential grant access to? Known default or custom? Always active or conditional?
- **Escalates:** Persistence installed. Communication encrypted. C2 obfuscated. Credential grants admin access. Multiple bypass mechanisms.
- **De-escalates (A):** Documented dev server. No command execution attached.
- **De-escalates (B):** Test fixture. Well-known default expected to be changed.
