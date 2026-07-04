# Network Destination Signals

| Signal | Description | Confidence Effect |
|---|---|---|
| **Sanctioned jurisdiction destinations** | Endpoints resolving to OFAC-sanctioned or EU-sanctioned IP ranges. Triggers compliance review in addition to security investigation. | High amplifier on any `NETW.*` finding |
| **Bulletproof hosting** | Destination IP ranges associated with providers ignoring abuse complaints. Disproportionately used for C2 because infrastructure persists longer. | Medium-high amplifier: increases confidence destination is attacker-controlled |
| **Recently registered domains** | Destination domains registered within 30-90 days of package publication. Attacker C2 is typically registered shortly before campaign launch. | High amplifier: temporal correlation is characteristic of coordinated campaigns |
| **Privacy-proxied registration** | WHOIS privacy services, anonymized contacts, registrars popular with threat actors. | Low alone, medium when combined with other adverse destination signals |
| **Dynamic DNS and tunneling** | `*.duckdns.org`, `*.ngrok.io`, `*.trycloudflare.com`, etc. as apparent production infrastructure. Free, disposable, no identity verification. | High amplifier: dynamic DNS as dependency network destination has almost no legitimate explanation |
| **Residential or mobile IP ranges** | Destination resolving to residential ISP or mobile carrier, not datacenter/cloud. Indicates compromised host relay or attribution evasion. | Medium amplifier: anomalous for any documented service endpoint |
| **IP-literal destinations** | Raw IP addresses instead of DNS names. Bypasses DNS monitoring and domain reputation. | Medium-high amplifier: bypasses major monitoring layer |

Relates to: `ARTF.IP`, `ARTF.URL`, `ARTF.DOMAIN`, `NETW.*` atom observations
