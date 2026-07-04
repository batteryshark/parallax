# LOAD.IMPORT: Dynamic Import / Require

## Description

Loads modules by a name determined at runtime rather than by a static import statement. Uses `importlib.import_module()`, `__import__()`, `require()` with a variable argument, or equivalent dynamic module loading mechanisms. The module to be loaded cannot be determined by static analysis: it is computed from variables, configuration, user input, or other runtime data.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `importlib.import_module(var)`, `__import__(name)`, `require(computed_path)`, computed module names in import calls |
| Static Binary | Partial | Dynamic import function calls, module name construction patterns |
| Runtime/Dynamic | Yes | Module loading events for modules not in static import graph, new module entries in sys.modules |

## Disambiguation

- **vs static imports**: `import os` and `from pathlib import Path` are resolved at parse time and visible to static analysis. They are NOT `LOAD.IMPORT`. The test: can a static analyzer enumerate all possible modules the call will load? If not, it's `LOAD.IMPORT`.
- **vs LOAD.DYLIB**: `LOAD.IMPORT` operates at the language module level (Python packages, Node modules). `LOAD.DYLIB` operates at the OS native library level (`.so`, `.dll`, `.dylib`).

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (writing a module then importing it), `XFRM.STRCON` (constructing the module name), `NETW.*` (module name or content from network)
- **May imply**: The set of loadable code is determined at runtime, not at package authoring time

## Notes

Plugin systems, dependency injection frameworks, and configuration-driven module loading legitimately use dynamic imports. The structural data points are: who controls the module name (the package author, the user, or an external source), and can the set of loadable modules be bounded?
