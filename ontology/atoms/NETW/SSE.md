# NETW.SSE: Server-Sent Events

## Description

Receives data via Server-Sent Events (SSE), a one-way persistent HTTP streaming mechanism where the server pushes text-based events to the client over a long-lived HTTP connection. The client makes a standard HTTP request with `Accept: text/event-stream`, and the server holds the connection open, sending events in `text/event-stream` format as they occur. Communication is unidirectional: server to client only.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `EventSource` API usage (browser), SSE client library imports, `text/event-stream` content type handling, event parsing (`event:`, `data:`, `id:` field processing) |
| Static Binary | Partial | EventSource API references, `text/event-stream` string constants |
| Runtime/Dynamic | Yes | HTTP response with `Content-Type: text/event-stream`, long-lived HTTP connection with incremental text data, event-formatted messages (lines starting with `data:`, `event:`, `id:`) |

## Disambiguation

- **vs NETW.WS**: Both maintain persistent connections. SSE is unidirectional (server→client) over standard HTTP. WebSocket is bidirectional with its own framing protocol after an HTTP upgrade. SSE is simpler, HTTP-native, and supported by standard HTTP infrastructure without upgrade negotiation.
- **vs NETW.HTTP**: SSE uses HTTP as transport but the connection is long-lived and streaming rather than request-response. A standard HTTP request that returns and closes is `NETW.HTTP`. An HTTP connection held open for streaming events is `NETW.SSE`.

## Structural Relationships

- **Often co-occurs with**: `NETW.HTTP` (SSE is built on HTTP), `LOAD.EVAL` / `EXEC.*` (received events processed and acted upon)
- **May imply**: A server-side event source is actively pushing data to this client

## Notes

SSE is increasingly common in AI applications (streaming token-by-token responses), live dashboards, and notification systems. It is lighter than WebSocket for server-to-client push because it uses standard HTTP (no upgrade negotiation, works through HTTP proxies natively). The `text/event-stream` content type and event format are the distinguishing structural markers.
