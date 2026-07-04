# LOAD.DYLIB: Dynamic Library Loading

## Description

Loads shared libraries (`.so`, `.dll`, `.dylib`) at runtime via `dlopen()`, `LoadLibrary()`, `ctypes.CDLL()`, `ffi.load()`, or equivalent OS-level library loading mechanisms. The loaded library is native machine code linked into the calling process's address space, executing with the process's full privileges. The library may or may not be declared in the package's build system or dependency manifest.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `dlopen()`, `LoadLibrary()`, `ctypes.CDLL()`, `ctypes.cdll.LoadLibrary()`, `ffi.load()` calls, library path arguments |
| Static Binary | Yes | Dynamic linker function imports, library path strings, runtime loading patterns |
| Runtime/Dynamic | Yes | Shared library load events, new memory mappings, library file access |

## Disambiguation

- **vs LOAD.IMPORT**: `LOAD.IMPORT` loads language-level modules. `LOAD.DYLIB` loads OS-level native libraries. The loaded artifact is native machine code that bypasses language-level sandboxing.
- **vs LOAD.EVAL**: Eval interprets strings within the language runtime. Dynamic library loading executes pre-compiled native code. The trust boundary is different, language sandboxes that restrict eval may have no control over native library loading.

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (writing a library file before loading it), `NETW.HTTP` (downloading a library before loading), `XFRM.ENCODE` (library path or content obfuscated), `EXEC.SYSCALL` (native code making direct system calls)
- **May imply**: Native code execution within the process, bypassing language-level restrictions

## Notes

The library path (whether it's a system library at a canonical path, a bundled library within the package, or a file in a temp/writable directory) is the primary structural data. A library path not present in the package's distribution suggests it was placed there by a prior stage.
