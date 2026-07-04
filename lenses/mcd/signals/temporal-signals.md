# Temporal Signals

| Signal | Description | Confidence Effect |
|---|---|---|
| **Abandonment followed by activity** | Long-dormant package suddenly receives updates | May indicate account compromise |
| **Coordinated publication** | Multiple related packages published in short window by same/related accounts | May indicate coordinated campaign |
| **Pre-event timing** | Published/updated shortly before a known compromise or incident | Temporal correlation may indicate the package was part of the attack |
| **Pre-staged clean version** | Clean version published shortly before malicious version to build registry history and bypass "new package" heuristics. Axios attacker published `plain-crypto-js@4.2.0` (clean) 18 hours before malicious `@4.2.1`. | High: indicates attacker awareness of and deliberate evasion of registry scanning |

Relates to: `PKGM.PUBLISH`, `ARTF.TIMESTAMP` atom observations
