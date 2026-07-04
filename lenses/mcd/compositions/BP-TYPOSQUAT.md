# BP-TYPOSQUAT: Typosquat / Dependency Confusion

Package impersonates a legitimate package through name similarity, namespace confusion, or version manipulation. Typosquatting is a delivery strategy, not a payload type. The package may contain any behavioral composition as its payload.

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | `PKGM.PUBLISH` | Publication anomalies (name similarity, new account, rapid publication) |
| **Required** | *Any payload composition* | The typosquat must deliver a payload |
| Supporting | `PKGM.DEPMOD` | Dependency confusion (internal name on public registry) |
| Supporting | `XFRM.*` | Transformed payload |
| Supporting | `PKGM.INSTALL` | Install-time execution of payload |

## Investigation Guidance

- **Verify:** What legitimate package does this resemble? Account age? What does the payload do?
- **Escalates:** Name is edit-distance-1 from popular package. New publishing account. Contains any malicious composition.
- **De-escalates:** Long publication history. Name similarity coincidental. No malicious payload.
