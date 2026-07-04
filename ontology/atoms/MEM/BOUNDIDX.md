# MEM.BOUNDIDX: Boundary-Adjacent Index Access

## Description

Access to neighboring elements in an array, grid, table, or spatial data structure via index arithmetic (typically `idx - 1`, `idx + 1`, `row - stride`, `row + stride`), where boundary positions (first element, last element, first row, first column, edges) cause the computed index to fall outside the allocated range.

This describes the mechanical pattern of performing relative-offset access in a bounded structure where edge cases exist. The behavior is the index arithmetic itself and the boundary conditions it creates, not the consequences of those conditions.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `buf[x - 1]`, `table[idx - stride]`, `top_xy = mb_xy - stride`, neighbor-access patterns in loop bodies, conditional guards checking `if (x > 0)` or `if (y > 0)` before neighbor access |
| Static Binary | Partial | Subtraction/addition of constants before array dereference, boundary-check comparisons preceding memory access. Compiler may reorder or eliminate checks |
| Runtime/Dynamic | Yes | Memory access patterns that approach or cross allocation boundaries at edge positions. Address sanitizers flag the concrete out-of-range accesses |

## Disambiguation

- **vs ordinary array indexing**: BOUNDIDX specifically describes relative-offset access where the structure has meaningful boundaries (grid edges, first/last positions) and the offset arithmetic can reach outside the allocation at those boundaries. Sequential iteration (`for i in range`) is not BOUNDIDX unless the loop body performs relative neighbor access.
- **vs MEM.SENTINEL**: SENTINEL describes state-marking with reserved values. BOUNDIDX describes spatial neighbor access. They are independent mechanics that can co-occur in the same data structure.

## Structural Relationships

- **Often co-occurs with**: MEM.SENTINEL (when boundary access is gated by a sentinel-based guard), loop/iteration structures, conditional boundary checks (`if x > 0`)
- **May imply**: A guard predicate that checks position before performing the neighbor access, or an assumption that callers have already validated position
- **Commonly part of idioms**: sentinel-guarded-region-access

## Notes

This pattern is pervasive in grid/spatial processing: video codec deblocking (top/left neighbor macroblocks), image convolution kernels, stencil computations, cellular automata, adjacency-based graph traversal on grid representations, and tile-based rendering. The characteristic shape is: a loop over a 2D (or ND) structure where the body accesses `current ± offset` and boundary positions require special handling.

The boundary axes are often independent: leftmost column (`x == 0`) creates different boundary conditions than top row (`y == 0`), and each axis may be guarded (or not) by different checks.
