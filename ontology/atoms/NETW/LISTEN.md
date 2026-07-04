# NETW.LISTEN: Network Listener

## Description

Binds to a network port and accepts inbound connections. Creates a server endpoint that external or local systems can connect to. The listener may serve content, accept commands, relay data, or perform any other server-side function. The bind address determines the listener's reachability: localhost-only, specific interface, or all interfaces (`0.0.0.0`).

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `bind()` + `listen()` + `accept()` call sequences, server framework initialization (Flask, Express, http.createServer), port number constants or configuration |
| Static Binary | Yes | Socket bind/listen/accept function imports, port number constants, server initialization patterns |
| Runtime/Dynamic | Yes | Listening port appears in `netstat`/`ss` output, inbound connection acceptance, process bound to a port |

## Disambiguation

- **vs NETW.SOCKET**: `NETW.LISTEN` specifically describes the server side, binding and accepting inbound connections. `NETW.SOCKET` describes outbound or general socket operations. A socket that `connect()`s is `NETW.SOCKET`. A socket that `bind()`s and `listen()`s is `NETW.LISTEN`.
- **vs application server frameworks**: Web frameworks (Flask, Express, Spring) create listeners as their core function. `NETW.LISTEN` applies to any code that binds a port, whether via a framework or raw sockets. The distinction between "expected server" and "unexpected listener" is a lens-level interpretation.

## Structural Relationships

- **Often co-occurs with**: `EXEC.SHELL` (shell spawned for connected clients, bind shell pattern), `FSYS.READ` / `FSYS.WRITE` (serving or receiving files), `NETW.SOCKET` (often both client and server sockets in same codebase)
- **May imply**: The process requires an available port and network permissions
- **Commonly part of idioms**: Remote shell (bind shell variant, listener accepts connection, spawns shell)

## Notes

The bind address is the critical structural property. `127.0.0.1` / `::1` restricts to loopback (local connections only). `0.0.0.0` / `::` accepts connections on all interfaces (externally reachable). A specific IP binds to one interface. This structural property is a factual observation that different lenses interpret differently.
