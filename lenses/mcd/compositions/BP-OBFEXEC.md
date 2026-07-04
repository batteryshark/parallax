# BP-OBFEXEC: Obfuscated Code Execution

Code decodes or decrypts a blob and then executes it. The payload is stored in a form that static review cannot read, recovered at runtime, and run without ever existing in plain text in the artifact. The decode-and-execute shape is the giveaway: whatever the blob contains is hidden until it runs.

Severity: high. This composition maps to the ontology "decode-and-execute chain" idiom ([decode-and-execute-chain](../../../ontology/idioms/decode-and-execute-chain.md)).

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | `LOAD.EVAL` | The execution primitive that runs the recovered content |
| **Required** | `XFRM.ENCODE` or `XFRM.ENCRYPT` | The transformation that hides the payload, co-located with the execution |
| Supporting | `NETW.*` | The encoded/encrypted blob is fetched rather than a local constant |
| Supporting | `XFRM.PACK` | Packing/compression as the transformation; same shape |
| Supporting | `LOAD.MEMCHAIN` | Multi-stage chain where each decoded stage decodes and executes again |

The required observations are `LOAD.EVAL` co-located with `XFRM.ENCODE` or `XFRM.ENCRYPT` within a reachable scope. Co-location without a connecting data flow is a weaker match.

## Investigation Guidance

- **Verify:** Statically decode the blob and determine what the executed payload does. Determine whether the blob is a local constant or fetched from a remote source.
- **Escalates:** Blob is fetched at runtime. Multiple decode layers. Decoded content reaches a general-purpose execution primitive. Runs at install time.
- **De-escalates:** The decoded content is inert data (config, templates), not executed. The transform is a documented packaging step over trusted, in-repo content.

## Disproof

- The decoded content is inert data, not executed.
- The transformation is a documented packaging step over trusted content.

## Engine Status

Wired in the `prlx` engine today (MCD lens). Triggers when `LOAD.EVAL` and an `XFRM.ENCODE`/`XFRM.ENCRYPT` atom appear in the same file scope.
