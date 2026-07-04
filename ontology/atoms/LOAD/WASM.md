# LOAD.WASM: WebAssembly Loading

## Description

Loads and instantiates WebAssembly (WASM) modules. WASM is a portable binary instruction format, a compiled binary that runs in a sandboxed execution environment. The module's capabilities are determined by its import section: host functions explicitly granted to the module at instantiation time. Without imports, a WASM module can compute but cannot interact with the filesystem, network, or process environment.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `WebAssembly.instantiate()`, `WebAssembly.compile()`, WASM loader library usage, `.wasm` file references, import object construction |
| Static Binary | Yes | WASM magic bytes (`\0asm`), WASM module binary structure, import/export section definitions |
| Runtime/Dynamic | Yes | WASM module instantiation events, host function calls from WASM context, WASM memory operations |

## Disambiguation

- **vs LOAD.DYLIB**: Native libraries execute with full process privileges. WASM executes in a sandbox with only explicitly imported capabilities. The trust model is inverted: native libraries can do anything; WASM can only do what the host permits.
- **vs LOAD.EVAL**: Eval interprets source-level strings. WASM executes compiled binary instructions. WASM is opaque to source-level analysis, it must be disassembled or decompiled to understand its logic.

## Structural Relationships

- **Often co-occurs with**: `NETW.HTTP` (WASM module fetched at runtime), `FSYS.READ` (WASM module loaded from disk), host function imports (filesystem, network, execution capabilities granted to the module)
- **May imply**: Compiled binary logic is executing within the process, opaque to source-level analysis

## Notes

The WASM import section is the critical structural data, it defines the capability boundary. A module that imports no host functions is compute-only. A module that imports filesystem, network, or execution functions has explicit capability grants. WASI (WebAssembly System Interface) provides standardized host function sets for system interaction. The source of the WASM module (bundled vs. fetched at runtime) and the import grants are the key observations.
