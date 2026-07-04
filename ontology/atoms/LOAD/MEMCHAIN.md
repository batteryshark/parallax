# LOAD.MEMCHAIN: In-Memory Execution Chain

## Description

Multi-stage execution where each stage decodes or transforms the next and passes it directly to an execution primitive (`eval`, `exec`, `subprocess`, `CreateThread`) without writing intermediate artifacts to disk. Each stage exists in process memory only for the duration of its execution. The chain may be two stages (decode → execute) or many (decode → spawn → decode → spawn → ...). No intermediate payload is recoverable from the filesystem after execution.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Partial | Chained decode-and-execute patterns (e.g., `eval(base64_decode(...))` where the decoded content itself contains another `eval(base64_decode(...))`), nested execution primitive calls |
| Static Binary | Partial | Difficult to detect statically, the chain is only fully visible when each stage is decoded. First-stage loader may be identifiable by its decode-then-execute structure |
| Runtime/Dynamic | Yes | Process spawning chains, memory allocations for decoded payloads, execution primitive invocations with dynamically generated arguments, no corresponding file writes for the executed content |

## Disambiguation

- **vs XFRM.PACK**: Packing wraps code in a container that is unpacked before or during analysis, the unpacked content can be recovered as a file or memory dump. In-memory execution chains execute and discard each stage, producing no recoverable intermediate artifact. A UPX-packed binary can be unpacked to a file. A three-stage eval chain leaves no files.
- **vs LOAD.EVAL**: A single `eval()` of a string is `LOAD.EVAL` (dynamic code loading). `LOAD.MEMCHAIN` applies when the executed code itself loads and executes further code, creating a chain of two or more stages where intermediate payloads exist only in memory.
- **vs EXEC.PROC**: Process creation (`EXEC.PROC`) describes spawning a subprocess. `LOAD.MEMCHAIN` may use process creation as its execution primitive, but the defining characteristic is the chain, multiple stages, each producing the next, none persisted to disk.

## Structural Relationships

- **Often co-occurs with**: `XFRM.ENCODE` (each stage typically encoded/encrypted), `XFRM.ENCRYPT` (encrypted stages), `LOAD.EVAL` (eval as the execution primitive between stages), `EXEC.PROC` (subprocess spawning as the execution primitive)
- **May imply**: The payload author intentionally structured execution to avoid leaving filesystem artifacts
- **Commonly part of idioms**: Decode-and-execute chain (LOAD.MEMCHAIN is the multi-stage extreme of this idiom)

## Notes

The number of stages in the chain is a structural observation. Two-stage chains (decode → execute) are common in many contexts. Three or more stages, where each layer is independently encoded/encrypted, represent increasing structural complexity. Each stage must be individually decoded and analyzed to understand the full chain. The final payload may bear no resemblance to the first-stage loader.
