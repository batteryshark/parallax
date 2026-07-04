# MCD Lens: Behavioral Compositions

Named compositions of ontology atoms that, taken together, suggest a specific malicious strategy through the MCD lens. Individual atoms are observations; compositions are MCD hypotheses.

A composition is triggered when its constituent atoms are detected within a reachable scope: the atoms are plausibly connected through execution flow, not merely co-located in an artifact.

Most compositions below are specifications. Four are wired in the `prlx` engine today: BP-SUPPLY, BP-DROPPER, BP-CREDTHEFT, and BP-OBFEXEC. The rest are specification-only until the engine grows rules for them.

## Compositions

| ID | Name | Core Pattern |
|---|---|---|
| [BP-SUPPLY](BP-SUPPLY.md) | Supply Chain Payload | `PKGM.INSTALL` + payload atoms |
| [BP-CREDTHEFT](BP-CREDTHEFT.md) | Credential Theft | `CRED.*` + `NETW.*` |
| [BP-BACKDOOR](BP-BACKDOOR.md) | Backdoor | Remote access (listener + exec) or auth bypass (embedded credential) |
| [BP-DROPPER](BP-DROPPER.md) | Dropper / Downloader | `NETW.*` → `FSYS.WRITE` → `EXEC.*` |
| [BP-OBFEXEC](BP-OBFEXEC.md) | Obfuscated Code Execution | `LOAD.EVAL` + `XFRM.ENCODE`/`XFRM.ENCRYPT` |
| [BP-EXFIL](BP-EXFIL.md) | Data Exfiltration | Data collection + `NETW.*` |
| [BP-RANSOM](BP-RANSOM.md) | Ransomware | `FSYS.ENUM` + `CRPT.SYMENC` + `FSYS.WRITE` |
| [BP-TIMEBOMB](BP-TIMEBOMB.md) | Logic Bomb / Time Bomb | Trigger condition + dormant payload |
| [BP-MINER](BP-MINER.md) | Resource Hijacking | `RSRC.*` + `NETW.*` |
| [BP-ROOTKIT](BP-ROOTKIT.md) | Rootkit | System-level hooks + concealment |
| [BP-WORM](BP-WORM.md) | Worm / Propagation | Discovery + network + delivery to external systems |
| [BP-TROJAN](BP-TROJAN.md) | Trojan | Legitimate interface + concealed malicious payload |
| [BP-AGENTMANIP](BP-AGENTMANIP.md) | Agent Manipulation | `AITM.*` targeting AI systems |
| [BP-TYPOSQUAT](BP-TYPOSQUAT.md) | Typosquat / Dependency Confusion | `PKGM.PUBLISH` anomaly + payload |
| [BP-LATERAL](BP-LATERAL.md) | Lateral Movement | Internal discovery + credential/privilege + action on new targets |
| [BP-MITM](BP-MITM.md) | Traffic Interception | Trust degradation + traffic redirection |
