# ARTF.DOMAIN: Embedded Domain Name

## Description

Domain names present as string literals in source or binary. A domain name is a hierarchical hostname label (`example.com`, `api.service.internal`, `c2.attacker.xyz`) without protocol scheme or path components. Includes fully qualified domain names (FQDNs), subdomains, and internal hostnames. Distinguished from URLs by the absence of protocol and path structure, a hostname only. May be used for DNS resolution, server identification, certificate validation, or configuration.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | String literals matching domain name format (labels separated by dots, valid TLD), constants named `host`, `server`, `endpoint`, `domain`, DNS lookup arguments (`dns.resolve("example.com")`), SNI/certificate hostname references |
| Static Binary | Yes | Domain-format strings in data sections, dot-separated label strings adjacent to network API references |
| Runtime/Dynamic | Yes | Domain strings passed to DNS resolution, used in HTTP `Host` headers, compared against certificate common names, used in SNI negotiation |

## Disambiguation

- **vs ARTF.URL**: A URL includes protocol, path, and possibly query/fragment components (`https://example.com/api/data`). A domain is the hostname portion only (`example.com`). If a string contains protocol or path components, it is `ARTF.URL` (and the hostname within it is implicitly a domain). If it is a bare hostname, it is `ARTF.DOMAIN`.
- **vs ARTF.IP**: A domain name requires DNS resolution to obtain an IP address. An IP address is a direct numeric network identifier. Both serve as network targets but are structurally distinct, a domain adds a DNS dependency and can resolve to different IPs over time.
- **vs NETW.DNS**: `ARTF.DOMAIN` is the static presence of a domain string. `NETW.DNS` describes runtime DNS resolution behavior. An embedded domain may never be resolved, or may be used in non-DNS contexts (certificate validation, string matching).

## Structural Relationships

- **Often co-occurs with**: `NETW.HTTP` / `NETW.DNS` (domain used as connection target), `ARTF.URL` (domain as component of a URL), `XFRM.ENCODE` (domain encoded to avoid detection), `XFRM.STRCON` (domain assembled from fragments), `SYSI.NET` (domain compared against local network configuration)
- **May imply**: The code references external infrastructure by name, introducing a DNS dependency for resolution

## Notes

Domain structure carries contextual information. TLD choice (`.com` vs `.xyz` vs `.onion` vs `.bit`), subdomain depth, and registrar are structural properties. Dynamic DNS providers (`.duckdns.org`, `.no-ip.com`, `.ngrok.io`) indicate infrastructure that can change IP resolution rapidly. Internal domains (`.local`, `.internal`, `.corp`) indicate private infrastructure assumptions. Recently registered domains versus long-established domains have different trust profiles. These are factual properties of the domain, useful for characterization regardless of analytical lens.
