# LOAD.REFLECT: Reflection

## Description

Uses language reflection capabilities to invoke methods, access fields, or instantiate classes by name at runtime. Enables calling methods or accessing data that are not statically referenced in the code, the target is determined by a string or runtime value rather than a direct code reference. Includes `getattr()`/`setattr()` in Python, `Class.forName()` and `Method.invoke()` in Java, `Reflect` API in JavaScript, and equivalent mechanisms.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Reflection API calls (`getattr()`, `Class.forName()`, `Method.invoke()`, `Reflect.get()`), string arguments specifying method/field/class names |
| Static Binary | Partial | Reflection API imports, method name strings, access control bypass patterns |
| Runtime/Dynamic | Yes | Method invocations not present in static call graphs, access to non-public members |

## Disambiguation

- **vs LOAD.IMPORT**: Dynamic import loads an entire module. Reflection accesses specific members (methods, fields, classes) by name within an already-loaded module or class.
- **vs LOAD.EVAL**: Eval executes arbitrary code strings. Reflection invokes specific named members. Reflection is more constrained, it accesses existing APIs by name rather than executing arbitrary logic.

## Structural Relationships

- **Often co-occurs with**: `XFRM.STRCON` (method/class names constructed from fragments), `LOAD.DESER` (deserialization gadget chains use reflection), `PRIV.*` (reflection bypassing access controls)
- **May imply**: The code accesses APIs that are not statically referenced in its call graph

## Notes

Reflection is common in framework code (dependency injection, ORM, serialization, plugin systems). The structural data points are: what members are being accessed by name, whether access controls are being bypassed (e.g., `setAccessible(true)` in Java), and who controls the member name string.
