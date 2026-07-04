# Static Binary Analysis

Examination of compiled binaries, bytecode, or packaged artifacts without executing them.

## Capabilities

- **Actual instructions:** Disassembly reveals what the binary will do, regardless of what the source claims
- **Embedded data:** Strings, URLs, IP addresses, certificates, cryptographic keys compiled into the binary
- **Linked libraries:** Import tables, dynamic library references, system call usage
- **Binary metadata:** Compiler identification, build flags, debug symbols, signing information
- **Security mitigations:** Presence or absence of ASLR, DEP/NX, stack canaries, CFG, RELRO
- **Source-to-binary drift:** Comparison with expected output from published source and build instructions
- **Packing and protection:** Detection of packers, protectors, obfuscation tools applied post-compilation
- **Architecture and platform:** Target platform, calling conventions, ABI compatibility

## Blind Spots

- **Original intent:** Without symbols or source, variable names, comments, and architectural reasoning are lost
- **Untriggered paths:** Like static source, cannot determine which branches execute at runtime
- **Runtime unpacking:** Self-modifying code, runtime decryption of payloads, JIT-generated code is invisible until execution
- **High-level abstractions:** Design patterns, module boundaries, and architectural structure are difficult to recover
- **Interpreted components:** Embedded scripts, configuration-driven behavior, plugin systems

## Tools

Disassemblers (IDA, Ghidra, Binary Ninja), hex editors, binary diffing tools (BinDiff, Diaphora), format parsers (readelf, objdump, PE-bear), signature scanners (YARA), decompilers, bytecode viewers (javap, dnSpy, uncompyle6).

## When to Use

- **Source unavailable:** Pre-compiled dependencies, native extensions, closed-source components
- **Source-to-binary verification:** When build reproducibility is in question, compare published source against the actual distributed artifact
- **Packing/protection analysis:** When static source shows nothing suspicious but the distributed binary has unexpected characteristics
- **Post-build injection detection:** When the supply chain concern is between build and distribution

## When to Transition Away

- **Runtime-decrypted payloads:** When binary analysis reveals encrypted or packed sections that only resolve at runtime → transition to **dynamic analysis**
- **Network behavior:** When binary contains network code but destinations are computed → transition to **network analysis** + **dynamic analysis**
- **Identity of publishers:** When binary signing or distribution metadata raises questions → transition to **OSINT**
- **Build pipeline concerns:** When drift is detected and the question is "where in the pipeline did this happen?" → transition to **build & CI analysis**

## Atom Categories Most Visible

EXEC (syscalls, process creation), CRPT (algorithm identification from constants/structures), ARTF (embedded strings), XFRM (packing, encoding routines), LOAD (dynamic loading, memory operations), ENVI (API-level detection checks)

## Atom Categories Least Visible

PKGM (package-level metadata is above binary level), TIME (timing logic may be inlined), AITM (AI interaction is typically through high-level APIs)
