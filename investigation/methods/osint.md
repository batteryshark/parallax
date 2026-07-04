# OSINT / External Intelligence

Gathering and analyzing publicly available information about entities referenced in or associated with the software: domains, IPs, maintainers, organizations, infrastructure, and threat intelligence feeds.

## Capabilities

- **Domain intelligence:** WHOIS history, registration dates, registrar reputation, DNS history, hosting providers, geo-location
- **IP intelligence:** ASN ownership, hosting type (datacenter/residential/mobile), reputation scores, blocklist status, geo-location
- **Maintainer identity:** Account age, publication history, cross-platform presence, organizational affiliation, contribution patterns
- **Package provenance:** Publication timeline, version history, download trends, dependency relationships across the ecosystem
- **Threat intelligence:** Known C2 infrastructure, malware family associations, campaign indicators, shared infrastructure with known threats
- **Code similarity:** Comparison against known malicious samples, code reuse from known threat actors
- **Certificate transparency:** SSL/TLS certificate issuance history for domains, revealing infrastructure setup timelines

## Blind Spots

- **Nothing about the code itself.** OSINT cannot see code structure, logic flow, or behavior. It transforms the *interpretation* of code-level findings, not the findings themselves.
- **Attribution uncertainty:** Account ownership, organizational affiliation, and identity claims are inherently lower-confidence than technical observations
- **Temporal decay:** Registration data, DNS records, and hosting arrangements change over time; historical data may not reflect current state
- **Deliberate obfuscation:** Privacy services, anonymized registrations, and infrastructure laundering are specifically designed to resist OSINT

## Tools

WHOIS lookup services, DNS history tools (SecurityTrails, PassiveDNS), IP reputation services (VirusTotal, AbuseIPDB, Shodan), package registry APIs, threat intel platforms (MISP, OTX), certificate transparency logs (crt.sh), code search engines (grep.app, Sourcegraph), social media and identity verification.

## When to Use

- **Destination investigation:** When static or dynamic analysis reveals URLs, IPs, or domains, OSINT provides the context that transforms an observation into evidence
- **Maintainer investigation:** When package metadata raises questions about who published or modified the code
- **Campaign correlation:** When multiple findings across different packages may be related, OSINT links infrastructure, accounts, and timing
- **Enrichment production:** OSINT is the primary method for producing enrichment data (domain age, hosting type, maintainer history) that modifies confidence across all lenses

## When to Transition Away

- **Code-level questions:** When OSINT raises concerns that need code-level verification (e.g., "this maintainer is suspicious, does the code they added do anything unusual?") → transition to **static source analysis**
- **Behavioral verification:** When OSINT suggests a destination is malicious but you need to confirm the code actually contacts it → transition to **dynamic analysis** + **network analysis**
- **Build pipeline concerns:** When OSINT reveals timeline anomalies (abandoned account suddenly active) and you need to verify artifact integrity → transition to **build & CI analysis**

## Enrichment Role

OSINT is the primary producer of enrichment data for the MCD lens. The six MCD signal categories (package metadata, dependency graph, source-to-binary drift, temporal signals, execution context, network destination) are largely populated by OSINT findings. The data is factual enrichment; the MCD lens interprets it.

## Atom Categories Most Informed By

ARTF (embedded URLs, IPs, domains, email addresses), NETW (destination reputation), PKGM (publication metadata, maintainer identity)

## Atom Categories Least Informed By

EXEC, FSYS, LOAD, CRPT, PRST, PRIV (code-level behaviors that OSINT cannot observe directly)
