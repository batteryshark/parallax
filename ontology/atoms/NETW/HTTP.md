# NETW.HTTP: HTTP/HTTPS Requests

## Description

Makes outbound HTTP or HTTPS requests to remote servers. Encompasses GET, POST, PUT, DELETE, and other HTTP methods via any client library (`requests`, `fetch`, `HttpClient`, `curl`) or direct socket construction of HTTP frames. The most widely supported application-layer network protocol, allowed through nearly all firewalls and proxies by default.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | HTTP client library imports/usage, URL string construction, request method calls, header construction |
| Static Binary | Partial | Imported HTTP library functions, URL string literals, HTTP method strings in data sections |
| Runtime/Dynamic | Yes | Outbound HTTP requests on the wire, DNS resolution for target domains, TLS handshakes, request/response payloads |

## Disambiguation

- **vs NETW.WEBHOOK**: `NETW.HTTP` is the general category for HTTP request-response communication. `NETW.WEBHOOK` applies specifically when the target is a messaging platform webhook URL (Discord, Telegram, Slack). A single POST to a Discord webhook URL is `NETW.WEBHOOK`, not `NETW.HTTP`.
- **vs NETW.WS**: Both use HTTP as transport. `NETW.HTTP` is request-response (each interaction is independent). `NETW.WS` upgrades from HTTP to a persistent bidirectional channel. The HTTP upgrade request itself is the boundary.
- **vs NETW.GRPC**: gRPC uses HTTP/2 as transport but with binary-serialized payloads. If the HTTP request uses standard text-based content types (JSON, XML, form data), it's `NETW.HTTP`. If it uses binary RPC framing, it's `NETW.GRPC`.

## Structural Relationships

- **Often co-occurs with**: `ARTF.URL` (target URL), `XFRM.ENCODE` (encoded request/response content), `CRED.*` (credentials in request payload or headers), `FSYS.READ` (reading data to send)
- **May imply**: DNS resolution for the target domain, TLS certificate validation (or lack thereof)
- **Commonly part of idioms**: Decode-and-execute chain (HTTP as the delivery channel for secondary payloads)

## Notes

HTTP is ubiquitous in modern software. The atom itself carries minimal signal; the analytical value comes from context: what is sent, where it's sent, when it's triggered, and what co-occurs. TLS certificate validation behavior (whether verification is enabled or disabled) is a structural property of the HTTP client configuration worth noting during observation.
