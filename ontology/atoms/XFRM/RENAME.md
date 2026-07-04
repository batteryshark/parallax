# XFRM.RENAME: Identifier Transformation

## Description

Replaces meaningful identifiers (variable names, function names, class names) with non-descriptive alternatives: single characters, random strings, sequential labels (a, b, c), or misleading names that do not reflect the identifier's purpose. The code's behavior is unchanged but its readability through static analysis is reduced.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Single-character or random-string identifiers, high density of non-descriptive names, identifier naming patterns inconsistent with surrounding code |
| Static Binary | Partial | Only visible if debug symbols are present, compiled binaries typically strip identifiers regardless, making this atom primarily relevant to source-level analysis |
| Runtime/Dynamic | No | Identifier names do not affect runtime behavior |

## Disambiguation

- **vs EVSN.MASQ**: `XFRM.RENAME` applies to source code identifiers, names within the code itself. `EVSN.MASQ` applies to runtime artifacts, files, processes, and network traffic presented as something they're not. A function named `a1b2()` is `XFRM.RENAME`. A binary placed at a path mimicking a system service is `EVSN.MASQ`.
- **vs minification output**: Frontend JavaScript minification tools (webpack, Terser, esbuild) routinely produce `XFRM.RENAME` patterns as a build artifact. The mechanical observation is identical. The distinction is context (what language, what runtime target, whether a build pipeline is documented). Context is not the atom's job; lenses evaluate context.

## Structural Relationships

- **Often co-occurs with**: `XFRM.CTRLFLOW` (identifier transformation + control flow restructuring often applied together by the same tool or process), `XFRM.PACK` (packed artifacts may also have transformed identifiers)
- **May imply**: A build or transformation step was applied to the code before distribution

## Notes

In compiled languages, identifier stripping is the default (compilers discard variable names unless debug symbols are requested). `XFRM.RENAME` is primarily meaningful in interpreted/scripted languages where identifiers normally survive into the distributed artifact.
