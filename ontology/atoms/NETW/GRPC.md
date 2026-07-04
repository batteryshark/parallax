# NETW.GRPC: gRPC / Binary RPC Protocols

## Description

Communicates via gRPC, Protocol Buffers, Thrift, or other binary-serialized RPC frameworks over HTTP/2. Request and response payloads are binary-serialized (typically Protocol Buffers) rather than text-based, making the content opaque to text-based inspection tools. gRPC supports unary calls, server streaming, client streaming, and bidirectional streaming.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | gRPC/protobuf library imports, `.proto` file definitions, generated client/server stubs, channel creation with target addresses |
| Static Binary | Partial | Protobuf-generated code patterns, gRPC library imports, HTTP/2 frame construction |
| Runtime/Dynamic | Yes | HTTP/2 connections with `content-type: application/grpc`, binary-framed payloads, protobuf-serialized message bodies |

## Disambiguation

- **vs NETW.HTTP**: gRPC uses HTTP/2 as transport, but payloads are binary-serialized. Standard `NETW.HTTP` uses text-based content types (JSON, XML, form data). If the content type is `application/grpc` or the payload uses Protocol Buffer framing, it's `NETW.GRPC`.
- **vs NETW.SOCKET**: gRPC operates over HTTP/2 with defined RPC semantics. Raw sockets have no application-layer framing. If the code uses a gRPC library or protobuf, it's `NETW.GRPC`. If it constructs binary protocol frames over raw TCP, it's `NETW.SOCKET`.

## Structural Relationships

- **Often co-occurs with**: `NETW.HTTP` (gRPC over HTTP/2 transport), `ARTF.URL` / `ARTF.IP` (gRPC server addresses)
- **May imply**: A `.proto` definition or generated client code exists defining the service interface

## Notes

gRPC is standard infrastructure in cloud-native and microservice architectures. In those environments, gRPC traffic between services is expected and architecturally normal. The binary serialization means payload inspection requires the corresponding `.proto` definitions or runtime deserialization to interpret message content.
