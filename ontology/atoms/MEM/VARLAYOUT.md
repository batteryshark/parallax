# MEM.VARLAYOUT: Compile-Time Variable Memory Layout

## Description

A data structure whose memory layout (including field widths, field offsets, total size, alignment, field ordering, or field presence) varies based on compile-time configuration. The source code defines a single logical structure, but the concrete binary representation differs depending on target architecture, compiler, platform defines, or build options.

Sources of layout variability include:

- **Pointer width**: ILP32 vs LP64 vs LLP64 data models changing `sizeof(void*)` and pointer-containing fields
- **Platform-dependent type widths**: `long` (32-bit on Windows LLP64, 64-bit on Linux LP64), `size_t`, `ssize_t`, `HANDLE`, `time_t`
- **Conditional compilation guards**: `#ifdef` / `#if defined(...)` adding, removing, or substituting fields
- **Packing and alignment directives**: `#pragma pack`, `__attribute__((packed))`, `__attribute__((aligned(N)))`, MSVC vs GCC default packing differences
- **Bitfield ordering**: Bit-level layout that varies between compilers or endianness targets
- **Union reinterpretation**: Unions of differently-sized types where the effective layout depends on which member is accessed and how the compiler lays out alternatives

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `#ifdef` guards around struct fields, platform-conditional typedefs, `#pragma pack` directives, `sizeof` used in manual offset calculations, pointer types mixed with fixed-width integers in structs/unions |
| Static Binary | Partial | The resolved layout for one specific target. Variability is only detectable by comparing binaries across different targets or by observing `sizeof`-derived constants that differ from expected values. Packing/alignment artifacts visible in field offset patterns |
| Runtime/Dynamic | Partial | Actual `sizeof` values and field offsets observable at runtime for the current build. Cross-architecture variability not directly observable from a single execution |

## Disambiguation

- **vs TYPE.NARROW**: TYPE.NARROW describes a runtime behavior where a value moves between type widths during execution. VARLAYOUT describes a compile-time property where the structure's layout is fixed per build but differs across builds. They are mechanically distinct: one is a runtime narrowing operation, the other is a static layout property.
- **vs ordinary struct definition**: VARLAYOUT applies specifically when the layout is not fixed, when some compile-time condition causes the concrete representation to change. A struct with only fixed-width types (`uint32_t`, `int16_t`) and no conditional compilation or packing directives is a fixed layout, not VARLAYOUT.

## Structural Relationships

- **Often co-occurs with**: TYPE.NARROW (when variable-width fields are read into or compared against fixed-width types at runtime), serialization/deserialization code, cross-process or cross-network data exchange
- **May imply**: `sizeof`-based calculations elsewhere in the codebase, possible platform-specific code paths, build configuration variability
- **Commonly part of idioms**: (none yet defined, candidate: cross-architecture serialization, ABI boundary mismatch)

## Notes

This pattern is fundamental to systems programming and appears wherever native structures cross boundaries: network protocol implementations, file format parsers, shared memory interfaces, driver IOCTLs, foreign function interfaces, and any serialization that uses raw struct reads/writes. The key mechanical fact is that the same source-level type name maps to different binary representations depending on build context.

The detection asymmetry between source and binary analysis is notable: source analysis sees the variability (the `#ifdef` branches, the platform typedefs), while binary analysis sees only the resolved result for one target. Identifying VARLAYOUT from a single binary typically requires recognizing that field offsets or sizes imply a platform-dependent type, or comparing against a second binary built for a different target.
