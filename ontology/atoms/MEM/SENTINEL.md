# MEM.SENTINEL: Sentinel-Initialized Data Structure

## Description

A data structure (array, table, buffer) whose entries are initialized with a reserved marker value to denote a specific state such as empty, unowned, absent, or unvisited. The sentinel value is chosen to be distinct from any expected valid entry, and downstream logic relies on comparisons against this value to determine entry state.

Common sentinel values include `0xFFFF`, `0xFFFFFFFF`, `-1`, `0`, `NULL`, and `INT_MAX`. Initialization is typically performed via `memset`, loop fill, or static initializer.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `memset(table, 0xFF, ...)`, `memset(table, -1, ...)`, loop filling with constant, `#define SENTINEL 0xFFFF`, comparisons against the marker value in guard conditions |
| Static Binary | Partial | Large constant fills in initialization paths, repeated comparison against a specific constant in branching logic. Sentinel value choice may be obscured by optimization |
| Runtime/Dynamic | Yes | Memory regions uniformly initialized to a constant value. Guard comparisons against that value visible in execution trace |

## Disambiguation

- **vs MEM.BOUNDIDX**: SENTINEL describes the initialization and state-marking of entries using a reserved value. BOUNDIDX describes arithmetic access to adjacent entries. They co-occur when a sentinel-guarded table is accessed via neighbor indexing, but each is independently recognizable.
- **vs ordinary default initialization**: SENTINEL is distinguished by the downstream dependency, code logic explicitly compares entries against the sentinel value to make control-flow decisions. A zero-initialized buffer that is simply overwritten without sentinel comparison is default initialization, not SENTINEL.

## Structural Relationships

- **Often co-occurs with**: TYPE.NARROW (when sentinel value sits at the boundary of a type's range), MEM.BOUNDIDX (when sentinel-guarded tables use neighbor access patterns)
- **May imply**: A guard predicate somewhere in the codebase that tests `entry == sentinel` or `entry != sentinel` to gate downstream operations
- **Commonly part of idioms**: sentinel-guarded-region-access

## Notes

Sentinel initialization appears across nearly all systems programming domains: hash tables (empty-slot markers), graph algorithms (unvisited-node markers), codec/parser state tables (unowned-region markers), memory allocators (free-block markers), and protocol parsers (unset-field markers). The mechanism is identical regardless of domain: a reserved value encodes state, and correctness depends on the invariant that no valid runtime value collides with it.
