# Static Source Analysis

Examination of source code, configuration files, and package metadata without executing the software.

## Capabilities

- **Structure and logic flow:** Control flow graphs, call graphs, data flow between functions and modules
- **Dependencies:** Direct and transitive dependency declarations, version constraints, dependency resolution
- **Embedded values:** Hardcoded strings, URLs, IP addresses, paths, credentials, cryptographic material
- **Code patterns:** Atom identification (function calls, API usage, system interactions), idiom recognition
- **Transformation detection:** Encoding layers, string construction, obfuscation patterns visible in source
- **Structural relationships:** Co-occurrence of atoms, proximity, reachability through call/data flow
- **Package metadata:** Manifest files, install scripts, declared entry points, lifecycle hooks

## Blind Spots

- **Runtime behavior:** Cannot observe what actually executes, only what *could* execute
- **Dynamic targets:** URLs constructed at runtime, computed file paths, environment-derived values are opaque
- **Conditional branches:** Cannot determine which branch executes without knowing runtime state
- **External dependencies' behavior:** Can see that a function is called, not what that function does internally (unless source is also available)
- **Time-dependent behavior:** Cannot observe what happens when `TIME.CMP` conditions are met
- **Reflection and metaprogramming:** `LOAD.EVAL`, `LOAD.REFLECT`, dynamic imports may be partially or fully opaque
- **Compiled extensions:** Native modules, WASM binaries, pre-compiled components within the package

## Tools

Source-level linters, AST parsers, taint analysis frameworks, dependency analyzers, SAST tools, code search (grep/semgrep/CodeQL), manifest parsers.

## When to Use

- **Starting point for most investigations.** Static source is typically the first method applied: it's fast, scales well, and produces a broad initial observation set.
- **When source is available.** Open-source packages, internal code, anything with published source.

## When to Transition Away

- **Opaque code paths:** When `LOAD.EVAL`, heavy obfuscation, or dynamic dispatch makes static analysis insufficient → transition to **dynamic analysis**
- **Unknown destinations:** When hardcoded URLs, IPs, or domains need reputation/history → transition to **OSINT**
- **Install-time behavior:** When package lifecycle hooks are the concern → transition to **dynamic analysis** in a sandboxed environment via **scaffolding**
- **Binary components:** When native extensions or compiled code is present → transition to **static binary analysis**

## Atom Categories Most Visible

XFRM, ARTF, LOAD, PKGM, FSYS (path-based), CRED (path-based), EXEC (command construction), NETW (target identification), ENVI (check patterns), TIME (comparison patterns), SYSI (query patterns)

## Atom Categories Least Visible

RSRC (consumption is a runtime property), PRST (installation is a runtime action), PRIV (escalation is runtime), AITM (interaction with AI systems is runtime)
