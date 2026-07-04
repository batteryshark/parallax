# TYPE.NARROW: Type Width Narrowing

## Description

A value produced, accumulated, or received in one type width is stored into, compared against, or cast to a narrower type. The operation discards high-order bits or changes the representable range, creating a mismatch between the value's actual range and the type's capacity.

This includes explicit casts (`(uint16_t)value`), implicit truncation on assignment to a narrower variable, and cross-type comparisons where the compiler promotes or truncates operands. The mechanical behavior is the width transition itself, a value that can represent range N is moved into a container that can represent range M, where M < N.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Explicit casts to narrower types, assignment of wider-typed expressions to narrower-typed variables, compiler warnings about implicit truncation (`-Wconversion`, `-Wshorten-64-to-32`), mixed-width comparisons |
| Static Binary | Partial | Truncation instructions (e.g., `movzx`, `and 0xFFFF`), narrowing register operations. Compiler may optimize away explicit truncation if it can prove the value fits |
| Runtime/Dynamic | Yes | Value changes observable when the wider value exceeds the narrow type's range. Sanitizers (`-fsanitize=implicit-conversion`) flag narrowing at runtime |

## Disambiguation

- **vs MEM.VARLAYOUT**: VARLAYOUT describes compile-time layout variability of data structures. NARROW describes a runtime operation where a value's type width changes during execution. A VARLAYOUT struct may contain fields that participate in NARROW operations, but they are independent mechanics.
- **vs ordinary type conversion**: NARROW specifically describes width-reducing conversions. Widening conversions (e.g., `uint16_t` to `uint32_t`) are the opposite direction and do not discard information. Same-width reinterpretation (e.g., `int32_t` to `uint32_t`) is sign reinterpretation, not narrowing.
- **vs value truncation in serialization**: When a protocol spec mandates a 16-bit field and the code truncates a wider internal value to fit, the mechanical behavior is still NARROW. The intent (protocol compliance vs. accidental truncation) is a lens-level distinction.

## Structural Relationships

- **Often co-occurs with**: MEM.SENTINEL (when a narrowed value can collide with a sentinel in the narrower type's range), input parsing (where external data is read into wider types then stored narrower), counter/accumulator patterns
- **May imply**: A range assumption somewhere; code downstream of the narrowing may assume the narrow type's range is sufficient
- **Commonly part of idioms**: sentinel-guarded-region-access

## Notes

Type narrowing is extremely common in C/C++ and other systems languages. It appears in protocol parsers (reading 32-bit wire values into 16-bit fields), loop counters (accumulating in `int` and indexing with `uint16_t`), hash functions (wide hash narrowed to table index), and cross-API boundaries (OS APIs returning `DWORD` stored into `int`).

The behavior is recognizable by the type width asymmetry: a producer operates in width W1 and a consumer operates in width W2 where W2 < W1. Whether this asymmetry is intentional or accidental is not part of the atom's description.
