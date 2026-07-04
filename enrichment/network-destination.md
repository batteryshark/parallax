# Network Destination

Facts about the network endpoints a package references: how old the domain is,
where and how it is hosted, its jurisdiction, and its reputation. Sourced from
WHOIS, DNS, hosting data, and threat intelligence.

| Id | Data point | What it factually states | Primary source |
|---|---|---|---|
| `ENR.NET.DOMAINAGE` | Domain age | The registration date of a referenced domain, and its age relative to the release | WHOIS |
| `ENR.NET.HOSTING` | Hosting type | The hosting provider and type for an endpoint: cloud, CDN, shared, or bulletproof | OSINT, DNS |
| `ENR.NET.JURISDICTION` | Jurisdiction | The registration and hosting jurisdiction or geography of an endpoint | WHOIS, OSINT |
| `ENR.NET.REPUTATION` | Threat-intel reputation | Whether the IP or domain appears in threat-intelligence feeds, and with what classification | threat intel |

Judgment-free: this records the endpoint facts. Whether a recently registered
domain on bulletproof hosting is alarming is a lens call. The architecture lens,
for instance, treats domain age as neutral: its concern is the external
dependency itself, not who owns it. The MCD lens's weighting is in
[`../lenses/mcd/signals/network-destination.md`](../lenses/mcd/signals/network-destination.md).
