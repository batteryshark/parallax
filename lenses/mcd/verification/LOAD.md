# MCD Lens: LOAD (Dynamic Code Loading) Verification

## General: Any LOAD Atom

1. **What is the complete data flow from source to the LOAD call?** Trace the argument backward to its origin. Does the path include network I/O, file reads, env vars, or user input? `[lens-neutral]`

2. **Is any transformation applied before loading?** Decode, decompress, decrypt, or string manipulation in the preceding code path. `[lens-neutral]`

3. **What capabilities does the loaded code have access to?** In-process eval inherits caller's imports and globals. Identify what's in scope. `[lens-neutral]`

4. **When was this pattern introduced, and by whom?** Version control history. Introduced in a dependency update or external contributor PR = higher priority. `[lens-neutral]`

5. **Does the LOAD site execute at install, import, or only on user action?** `[lens-neutral]`

## LOAD.EVAL

6. **What does the evaluated code actually do?** If reachable in test environment, instrument to capture executed content. `[lens-neutral]`

## LOAD.DESER

7. **What serialization format and class restrictions?** Pickle with no restricted unpickler = critical. `yaml.safe_load` = lower risk. `[lens-neutral]`

## LOAD.DYLIB

8. **Is the library present in the package distribution?** Path not in package = staged payload. Signed or hash-verified? `[lens-neutral]`

## LOAD.WASM

9. **What host functions are imported by the module?** Import section defines capability boundary. `[lens-neutral]`

## LOAD.IMPORT

10. **Can loadable modules be statically enumerated?** Module name from user input or network = functionally arbitrary code execution. `[lens-neutral]`

## Cross-Cutting

11. **Is error handling suppressive?** Bare exception handlers swallowing errors around LOAD calls: a behavioral signal for anticipated failure. `[MCD]`

12. **Is there a class restriction, allowlist, or sandbox?** Assess bypass potential: canonicalization issues, inheritance chains, partial-match logic. `[lens-neutral]`
