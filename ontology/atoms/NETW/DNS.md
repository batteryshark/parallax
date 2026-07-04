# NETW.DNS: DNS Operations

## Description

Constructs and sends DNS queries programmatically, uses hardcoded or non-system DNS resolvers, or structures data within DNS query parameters (subdomain labels, TXT record payloads, CNAME chains). Distinct from standard OS-level name resolution: `NETW.DNS` applies when code interacts with DNS as a protocol rather than transparently resolving hostnames through the system resolver.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | DNS library imports (`dnspython`, `dns.resolver`, `dig` invocations), hardcoded resolver IP addresses (e.g., `8.8.8.8`), subdomain construction patterns, TXT record queries |
| Static Binary | Partial | DNS library imports, hardcoded resolver IPs in data sections, DNS packet construction routines |
| Runtime/Dynamic | Yes | DNS queries to non-system resolvers, unusually structured subdomain labels, high volume of DNS queries, DNS-over-HTTPS (DoH) requests |

## Disambiguation

- **vs standard name resolution**: Standard DNS resolution performed by the OS resolver (e.g., `socket.getaddrinfo()`, `gethostbyname()`) is infrastructure, not a `NETW.DNS` finding. `NETW.DNS` applies when code constructs queries directly, uses non-system resolvers, or manipulates DNS as a data channel.
- **vs NETW.HTTP**: DNS-over-HTTPS (DoH) to a hardcoded resolver should be classified as both `NETW.DNS` (programmatic DNS) and `NETW.HTTP` (the transport mechanism).

## Structural Relationships

- **Often co-occurs with**: `XFRM.ENCODE` (data encoded into subdomain labels or TXT records), `ARTF.IP` (hardcoded resolver addresses), `NETW.HTTP` (DoH implementations)
- **May imply**: The code is bypassing system-level DNS configuration and monitoring

## Notes

DNS has a maximum label length of 63 characters and maximum name length of 253 characters. Data encoding within DNS queries is constrained by these limits, typically using hex or base32 encoding of payload data distributed across subdomain labels. Query volume and encoding patterns are structural characteristics observable through network analysis.
