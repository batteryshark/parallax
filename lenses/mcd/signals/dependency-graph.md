# Dependency Graph Signals

| Signal | Description | Confidence Effect |
|---|---|---|
| **New dependency in patch release** | Patch version (x.y.Z) introduces a dependency not present in the previous version | High: patches fix bugs, not add dependencies |
| **Transitive dependency anomaly** | Deep transitive dependency changes in a way not matching direct dependency's changelog | Suggests supply chain compromise at a lower level |
| **Dependency on unpopular package** | Depending on very low-download, recently published package | The dependency itself may be the attack vector |
| **Circular or self-referential dependencies** | Unusual dependency structures not typical of legitimate packages | May indicate dependency confusion or metadata manipulation |

Relates to: `PKGM.DEPMOD`, `PKGM.PHANTOM` atom observations
