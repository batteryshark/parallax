# NETW.WS: WebSocket Communication

## Description

Establishes persistent, bidirectional communication channels using the WebSocket protocol (`ws://`, `wss://`). A WebSocket connection begins as an HTTP upgrade handshake, then transitions to a long-lived full-duplex channel where both sides can send messages at any time without repeated request-response cycles. The connection persists until explicitly closed by either party.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | WebSocket library imports (`websocket`, `ws`, `socket.io`, `WebSocket` API), `ws://` or `wss://` URL schemes, connection upgrade patterns, message send/receive handlers |
| Static Binary | Partial | WebSocket library imports, `ws://`/`wss://` URL strings, upgrade header constants |
| Runtime/Dynamic | Yes | HTTP upgrade request (`Connection: Upgrade`, `Upgrade: websocket`), WebSocket frame traffic on the wire, long-lived TCP connection with bidirectional message flow |

## Disambiguation

- **vs NETW.HTTP**: Both use HTTP as the starting transport. `NETW.HTTP` is request-response, each interaction is independent. `NETW.WS` upgrades from HTTP to a persistent bidirectional channel. After the upgrade handshake, the connection is no longer HTTP.
- **vs NETW.SSE**: Both maintain persistent connections. WebSocket is bidirectional (both sides send). SSE is unidirectional (server to client only). WebSocket uses its own framing protocol. SSE uses text/event-stream over standard HTTP.
- **vs NETW.SOCKET**: WebSocket operates over HTTP/TCP with a defined framing protocol. Raw sockets have no defined application-layer framing. If the code uses a WebSocket library or protocol, it's `NETW.WS`. If it manages raw TCP frames, it's `NETW.SOCKET`.

## Structural Relationships

- **Often co-occurs with**: `NETW.HTTP` (the upgrade handshake), `EXEC.*` (commands received over WebSocket and executed), `XFRM.ENCODE` (message content encoding)
- **May imply**: The server-side endpoint supports WebSocket upgrades; the connection is intended to be long-lived

## Notes

Many network monitoring tools inspect the initial HTTP upgrade request and then stop analyzing the connection, treating post-upgrade traffic as opaque. This is a structural property of how WebSocket interacts with HTTP-layer monitoring. The traffic is technically visible but may not be inspected by tools that only understand HTTP request-response patterns.
