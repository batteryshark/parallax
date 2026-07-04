# XFRM.BITWISE: Bitwise Data Manipulation

## Description

Uses bitwise operations (XOR, AND, OR, NOT, bit shifts, bit rotations) to transform or construct data. Common patterns include XOR loops over byte arrays, bit shifting to construct character values, rotate-and-XOR sequences, and AND/OR masking to extract or modify specific bits. In high-level application code that deals with strings, APIs, or business logic, bitwise operations on data are atypical and structurally notable.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | XOR loops (`for b in data: b ^= key`), shift operations constructing values (`chr(0x68 >> 1)`), bitwise operators applied to string/byte data rather than flags or hardware registers |
| Static Binary | Yes | Sequences of XOR/shift/rotate instructions operating on data buffers, loop structures with bitwise operations on array elements |
| Runtime/Dynamic | Yes | Data transformation visible in memory, input buffer transformed to output buffer through bitwise operations, key material or rotation constants used in the transformation |

## Disambiguation

- **vs CRPT.CUSTOM**: Both involve bitwise operations on data. The distinction is recognizability: if the bitwise operations implement a recognized cryptographic algorithm (AES S-box lookups, SHA round functions, Salsa20 quarter-rounds), classify as `CRPT.CUSTOM`. If they perform ad-hoc, unrecognizable transformations, classify as `XFRM.BITWISE`. When uncertain, flag both, the distinction does not change investigation priority and the two frequently co-occur.
- **vs XFRM.ENCRYPT**: `XFRM.ENCRYPT` describes the application of a cipher (which may internally use bitwise operations). `XFRM.BITWISE` describes the raw bitwise operations themselves when they don't correspond to a known cipher. A recognized XOR cipher is `XFRM.ENCRYPT`; a series of XOR/shift/rotate operations with no recognizable cipher structure is `XFRM.BITWISE`.
- **vs legitimate bitwise operations**: Network protocol implementations, binary file format parsers, graphics code, and hardware interface code legitimately use extensive bitwise operations. `XFRM.BITWISE` is most structurally notable when bitwise operations appear in code whose functional domain does not involve binary data manipulation.

## Structural Relationships

- **Often co-occurs with**: `CRPT.CUSTOM` (bitwise operations underlying custom cryptography), `XFRM.ENCRYPT` (bitwise operations implementing a cipher), `XFRM.ENCODE` (bitwise operations as part of a custom encoding scheme), `LOAD.EVAL` / `EXEC.SHELL` (transformed data fed to execution)
- **May imply**: A custom transformation or cipher is in use rather than a standard library

## Notes

XOR with a single repeating byte key is the most common trivial transformation, it's the "ROT13 of binary data." Multi-byte XOR keys and combined operations (XOR + rotate) increase the effort required to reverse the transformation but remain straightforward given the key or algorithm.
