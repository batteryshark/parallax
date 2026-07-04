# XFRM.CTRLFLOW: Control Flow Restructuring

## Description

Alters the control flow structure of code without changing its functional behavior. Techniques include control flow flattening (replacing structured loops/branches with a single dispatcher loop and state variable), opaque predicates (branch conditions whose outcome is predetermined but non-obvious), dead code insertion, and state machine transformations that obscure the original execution order.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Switch-based dispatch loops, state variables controlling execution order, opaque predicates (`if ((x * (x + 1)) % 2 === 0)`), unreachable code blocks |
| Static Binary | Yes | Unusual control flow graph structure, flattened graphs with single-entry dispatch nodes, high cyclomatic complexity inconsistent with functional complexity |
| Runtime/Dynamic | Partial | Execution traces that visit dispatcher nodes repeatedly, state variable transitions that reveal the original linear execution order |

## Disambiguation

- **vs XFRM.RENAME**: Identifier transformation changes names; control flow restructuring changes code structure. They often co-occur (applied by the same tool) but are independently observable.
- **vs normal complex logic**: Business logic can be legitimately complex. `XFRM.CTRLFLOW` applies when the complexity is structural (the control flow graph is more complex than the logic requires) rather than inherent (the problem domain is complex). The signal is a mismatch between structural complexity and functional complexity.

## Structural Relationships

- **Often co-occurs with**: `XFRM.RENAME` (commonly applied together), `XFRM.PACK` (packed code may also have restructured control flow)
- **May imply**: A post-processing tool was applied to the code (control flow restructuring is rarely hand-written)

## Notes

Control flow obfuscation tools include JavaScript obfuscators (javascript-obfuscator, JScrambler), .NET obfuscators (ConfuserEx, Dotfuscator), and LLVM-based obfuscation passes (O-LLVM). The specific transformation patterns can sometimes identify which tool was used.
