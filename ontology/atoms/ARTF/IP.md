# ARTF.IP: Embedded IP Address

## Description

Raw IPv4 or IPv6 addresses present in source or binary as string literals or byte arrays. Includes both public and private addresses (RFC 1918, link-local, loopback). The artifact is the address itself, a network identifier embedded in the code. IPv4 addresses appear as dotted-quad notation (`192.168.1.1`), packed integers, or byte arrays. IPv6 addresses appear as colon-separated hex groups, sometimes with `::` zero-compression or `::ffff:` IPv4-mapped forms.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Dotted-quad string literals, `inet_addr()` / `inet_pton()` constants, IP address regex patterns in source, `socket.connect(("1.2.3.4", port))`, hex-encoded IP bytes |
| Static Binary | Yes | Dotted-quad strings in data sections, packed 4-byte or 16-byte network-order addresses, `inet_addr` import references |
| Runtime/Dynamic | Yes | IP addresses resolved from string constants, network connections to hardcoded addresses, IP strings passed to socket APIs |

## Disambiguation

- **vs ARTF.URL**: An IP address embedded standalone (e.g., `"203.0.113.50"`) is `ARTF.IP`. An IP address embedded within a URL (e.g., `"http://203.0.113.50/path"`) produces both `ARTF.URL` and `ARTF.IP`. The URL is the full resource locator; the IP is the network identifier within it.
- **vs ARTF.DOMAIN**: An IP address is a numeric network identifier that requires no DNS resolution. A domain name is a human-readable hostname that requires DNS resolution to an IP. Both serve as network targets but are structurally distinct artifacts.
- **vs NETW.***: `ARTF.IP` is the static presence of an IP address in code or binary. `NETW.*` atoms describe runtime network operations. An embedded IP may never be used in a network call, or may be used in a comparison, configuration, or allowlist.

## Structural Relationships

- **Often co-occurs with**: `NETW.SOCKET` / `NETW.HTTP` (IP used as connection target), `ARTF.URL` (IP embedded within a URL), `XFRM.ENCODE` (IP address encoded to avoid pattern matching), `XFRM.STRCON` (IP assembled from fragments)
- **May imply**: The code has a fixed network target that does not depend on DNS resolution or runtime configuration

## Notes

The address range carries structural information. RFC 1918 private addresses (`10.*`, `172.16-31.*`, `192.168.*`) and loopback (`127.0.0.1`, `::1`) are internal. Public addresses in routable space point to external infrastructure. IPv4-mapped IPv6 addresses (`::ffff:a.b.c.d`) encode an IPv4 address in IPv6 form. These are factual properties of the address, useful for classification regardless of analytical lens.
