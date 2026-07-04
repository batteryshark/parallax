# Sentinel-Guarded Region Access

## Description

A mechanism where a sentinel-initialized lookup table tracks region membership or ownership, a runtime-derived identifier is written into table entries to claim them, and equality comparisons between table entries and the current identifier are used as guards for downstream memory operations. The guard's correctness depends on the invariant that no valid runtime identifier can equal the sentinel value.

The characteristic shape is: initialize table with sentinel, populate entries with region IDs as input is processed, then use `table[position] == current_id` (or `!= current_id`) checks to gate neighbor access, border swaps, cache operations, or other position-dependent memory operations.

## Constituent Atoms

| Atom | Role | Notes |
|---|---|---|
| MEM.SENTINEL | Core | The lookup table initialized with a reserved marker value. The sentinel encodes "no region" or "unowned." |
| TYPE.NARROW | Supporting | When the runtime ID is produced in a wider type than the table's element type, or when the sentinel sits at the boundary of the table type's representable range. Strengthens the match but the mechanism exists even without type narrowing. |
| MEM.BOUNDIDX | Supporting | When the guarded downstream operation performs neighbor access via index arithmetic. The guard is often the only thing preventing boundary positions from producing out-of-range accesses. |
| Structural: counter/accumulator | Structural | A runtime counter or ID that increments as input units are processed (slices, blocks, regions, segments). The counter is the source of values written to the table. |
| Structural: equality guard | Structural | A comparison of the form `table[idx] == current_id` or `table[idx] != current_id` that gates downstream operations. This is the mechanism's pivot point, the guard that depends on the sentinel invariant. |

## Recognition Pattern

A practitioner recognizes this mechanism by identifying:

1. A table whose initialization fills entries with a constant (sentinel)
2. A processing loop that writes a changing ID into table entries
3. Guard conditions that compare table entries against the current ID
4. Memory operations (reads, writes, swaps, copies) downstream of those guards that would be unsafe without them

The table is typically indexed by position (macroblock index, tile coordinate, pixel row, block number), and the guard's semantic meaning is "does this position belong to the same region as the current one?" The downstream operations assume the answer is reliable.

## Variations

- **Spatial region table**: Table indexed by 2D grid position, ID represents slice/tile/region. Guards gate top/left/diagonal neighbor access. Common in video codecs, image segmentation, and tiled rendering.
- **Ownership tracking table**: Table indexed by resource ID, sentinel means "unclaimed." Guards gate access to shared or neighboring resources. Common in memory allocators, connection pools, and scheduling.
- **State machine phase table**: Table indexed by processing unit, sentinel means "not yet processed." Guards determine whether dependent units can reference each other. Common in multi-pass parsers and compilers.
- **Hash table with sentinel slots**: Table initialized with sentinel keys, runtime keys inserted. Probe sequences compare against sentinel to detect empty slots. Common in open-addressing hash tables.

## What This Mechanism Is NOT

This idiom describes a data structure access pattern, a table, a sentinel, an ID, a guard, and a downstream operation. It does not describe what the downstream operation does or whether the invariant holds.

- Through one lens: this mechanism is a site where sentinel-collision can defeat safety guards (defect analysis)
- Through another lens: this is a space-efficient region-tracking scheme with O(1) membership lookup (architecture analysis)
- Through yet another: this mechanism's invariant requirements define the input validation contract for the processing pipeline (capability analysis)

## Confidence Spectrum

**Strong match:**
- Sentinel initialization visible (memset or loop fill with constant)
- Runtime ID written to same table
- Equality comparison of table entry against runtime ID in a guard position
- Memory operation downstream of the guard that depends on the guard's result

**Moderate match:**
- Table initialization and guard visible, but the ID source is indirect (passed through several layers, derived from a hash)
- Guard exists but the downstream operation is non-obvious (function call whose internals perform the sensitive access)

**Weak match:**
- Table with sentinel-like initialization but no clear guard pattern, or guard exists but no obvious position-sensitive downstream access
- Single component present (e.g., sentinel table exists but no equality guard found, may be a different usage pattern)

## Notes

This mechanism appears most frequently in media codec implementations (H.264/H.265 slice tables, VP9 segment maps, AV1 tile tracking), tiled rendering engines, spatial database indices, and any system that partitions a coordinate space into regions and needs O(1) lookup of "which region owns this position."

The sentinel value's type domain relative to the runtime ID's range is a key structural property. When the table uses a narrow type (uint8_t, uint16_t) and the ID is derived from an input-controlled counter with no hard cap, the sentinel value becomes reachable by the counter. This is a mechanical fact about the ranges involved, observable through static analysis of the types and increment logic.
