# NETW.SOCKET: Raw Socket Operations

## Description

Creates and operates TCP or UDP sockets directly using OS socket APIs, below application-layer protocols. Allows arbitrary bidirectional data exchange over network connections without the structure of HTTP, gRPC, or other defined application protocols. The code controls framing, encoding, and protocol behavior directly.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Socket API calls (`socket()`, `connect()`, `send()`, `recv()`, `AF_INET`), socket option configuration, custom framing/parsing code |
| Static Binary | Yes | Imported socket functions, `AF_INET`/`SOCK_STREAM`/`SOCK_DGRAM` constants, socket descriptor operations |
| Runtime/Dynamic | Yes | TCP/UDP connections on non-standard ports, custom protocol framing on the wire, unrecognized application-layer traffic |

## Disambiguation

- **vs NETW.HTTP**: HTTP clients use sockets internally, but `NETW.SOCKET` applies when the code operates sockets directly without an application-layer protocol library. If the code uses `requests.get()` or `fetch()`, it's `NETW.HTTP`. If it creates a `socket(AF_INET, SOCK_STREAM)` and sends raw bytes, it's `NETW.SOCKET`.
- **vs NETW.LISTEN**: `NETW.SOCKET` describes outbound or general socket operations. `NETW.LISTEN` specifically describes binding to a port and accepting inbound connections. A socket that `connect()`s to a remote host is `NETW.SOCKET`. A socket that `bind()`s and `listen()`s is `NETW.LISTEN`.
- **vs NETW.IPC**: Socket family distinguishes them. `AF_INET` / `AF_INET6` sockets are `NETW.SOCKET` (network-routable). `AF_UNIX` sockets are `NETW.IPC` (local-only).

## Structural Relationships

- **Often co-occurs with**: `EXEC.SHELL` (shell I/O bound to socket, remote shell pattern), `XFRM.ENCODE` / `XFRM.ENCRYPT` (custom protocol framing), `NETW.LISTEN` (socket used for both client and server roles)
- **May imply**: A custom or non-standard protocol is in use
- **Commonly part of idioms**: Remote shell (socket + shell + I/O redirection)

## Notes

Raw socket operations give the code full control over the network protocol. This means traffic may not conform to any recognized application-layer protocol, making it opaque to protocol-specific inspection tools. The socket family (`AF_INET` vs `AF_INET6` vs `AF_UNIX`), type (`SOCK_STREAM` vs `SOCK_DGRAM`), and the connect/bind address are key structural properties to capture during observation.
