# RSRC.NET: Network Bandwidth Consumption

## Description

Generating large volumes of network traffic, participating in traffic amplification, or acting as a relay/proxy for third-party traffic. Includes sending floods of packets, relaying traffic between external hosts, participating in amplification attacks (DNS reflection, NTP amplification), acting as a SOCKS/HTTP proxy for third-party traffic, or any pattern where the volume or nature of network traffic exceeds what is necessary for the application's own communication needs. The atom describes significant network bandwidth consumption rather than normal application network communication.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Partial | Packet generation in tight loops, UDP flood patterns, proxy/relay logic forwarding between two external sockets, traffic amplification request construction, bandwidth-saturating send patterns |
| Static Binary | Partial | High-frequency send loop structures, raw socket usage with flood patterns, proxy/relay forwarding logic, amplification protocol request templates |
| Runtime/Dynamic | Yes | Elevated network throughput disproportionate to application function, high packet rates, traffic to/from many distinct endpoints, relay patterns (ingress from one host, egress to another), bandwidth saturation on network interfaces |

## Disambiguation

- **vs NETW.***: `NETW` atoms describe network communication behavior, making HTTP requests, opening WebSocket connections, sending DNS queries. `RSRC.NET` describes the resource consumption aspect of network traffic that is notable for volume, rate, or purpose. A single HTTP API call is `NETW.HTTP`. Sending thousands of requests per second or relaying megabytes of third-party traffic is both `NETW.*` (the communication mechanism) and `RSRC.NET` (the bandwidth consumption pattern).
- **vs NETW.LISTEN + NETW.SOCKET**: Acting as a proxy or relay involves listening for connections and forwarding traffic. `NETW.LISTEN` and `NETW.SOCKET` describe the connection mechanics; `RSRC.NET` describes the bandwidth consumption when the traffic volume is significant or the traffic serves no function for the calling application itself.

## Structural Relationships

- **Often co-occurs with**: `NETW.SOCKET` (raw or UDP sockets for packet generation), `NETW.HTTP` (HTTP-based flood or proxy traffic), `NETW.DNS` (DNS amplification), `NETW.LISTEN` (proxy/relay listening for incoming connections), `SYSI.NET` (querying network interface capabilities)
- **May imply**: Bandwidth consumption affecting other applications and users on the network, potential ISP or hosting provider policy violations, upstream traffic costs for the host operator

## Notes

The key structural data points are: the volume and rate of traffic generated, whether traffic is the application's own communication or relayed/proxied third-party traffic, the protocol used, the number of distinct destination endpoints, and whether the traffic serves any function for the application's stated purpose. A CDN node relaying cached content is structurally different from a library that silently proxies third-party traffic through the host. Whether the network consumption is proportional to user-initiated activity or occurs autonomously is a critical structural property.
