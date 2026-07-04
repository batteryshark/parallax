# BP-WORM: Worm / Propagation

Replicates to other systems or repositories without user initiation. Spreads by exploiting vulnerabilities, abusing trust relationships, or using package registry access.

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | `SYSI.NET` | Discovering propagation targets |
| **Required** | `NETW.*` | Communicating with targets |
| **Required** | `EXEC.*` or `FSYS.WRITE` | Delivering payload to targets |
| Supporting | `CRED.SSH` | Using stolen SSH keys for movement |
| Supporting | `PKGM.*` | Publishing malicious packages to registries |
| Supporting | `SYSI.SW` | Identifying vulnerable software on targets |

## Investigation Guidance

- **Verify:** What propagation mechanism? What systems/registries targeted? Self-replicating or one-shot?
- **Escalates:** Automated discovery and exploitation. Stolen credentials for movement. Publication to registries.
- **De-escalates:** Network scanning is documented feature. File copying within documented deployment scope.
