# LOAD.EVAL: Eval / Dynamic Interpretation

## Description

Executes a string or data structure as code within the language runtime using `eval()`, `exec()`, `Function()`, `new Function()`, or equivalent dynamic interpretation primitives. The code string may be hardcoded, decoded from another representation, received from the network, or constructed from fragments. The executed code has access to the runtime's object model, imported modules, and in-process state at the eval site.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `eval()`, `exec()`, `Function()`, `compile()`, `execfile()` calls, string arguments that are not simple literals |
| Static Binary | Partial | Eval function imports, dynamic dispatch patterns |
| Runtime/Dynamic | Yes | Dynamic code execution, new code paths not present in static analysis, eval argument contents |

## Disambiguation

- **vs EXEC.SHELL**: `LOAD.EVAL` executes within the language runtime (Python evaluates Python, JS evaluates JS). `EXEC.SHELL` passes a string to the OS shell. The combination (eval constructing a string that calls `os.system()`) triggers both.
- **vs LOAD.CODEGEN**: `LOAD.EVAL` interprets an existing string as code. `LOAD.CODEGEN` generates new code (bytecode, AST, native instructions) then executes it. Eval is interpretation of provided input; codegen is creation of new executable content.

## Structural Relationships

- **Often co-occurs with**: `XFRM.ENCODE` / `XFRM.ENCRYPT` (decoded content passed to eval, decode-and-execute chain), `NETW.HTTP` (code fetched and eval'd), `XFRM.STRCON` (code string assembled from fragments)
- **May imply**: The actual runtime behavior cannot be determined by static analysis alone
- **Commonly part of idioms**: Decode-and-execute chain (EVAL is the primary execution primitive)

## Notes

The data flow into the eval call is the critical structural observation. A literal string argument (`eval("1+1")`) is structurally different from a variable argument (`eval(decoded_data)`). When the argument derives from network, file, or environment sources, the set of possible executed code is unbounded from a static analysis perspective.
