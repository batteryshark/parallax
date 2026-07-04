# PKGM.UNDECLARED: Imported But Undeclared Dependency

## Description

A module that the package's source imports (or requires) but that no manifest declares as a dependency, and that is not a standard-library or runtime builtin, nor a local module shipped in the package. The import resolves at install or run time to whatever the registry serves under that name, with no pin and no provenance. This is the inverse of `PKGM.PHANTOM` (declared but never used) and is the code-level smell behind slopsquatting: a language model emits a plausible-looking import, the name is never pinned, and a squatter who registers it supplies attacker-controlled code.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | An `import` / `require` / `from X import` of a bare package name that appears in no manifest dependency section, is not a stdlib/builtin, and is not a local module or the package's own name. Comparing the import set against the declared set across all source files is definitive at the manifest level. |
| Static Binary | N/A | Manifest-and-source observation |
| Runtime/Dynamic | Partial | At install/resolve time the name is fetched from the registry; what resolves depends on who owns the name then |

## Disambiguation

- **vs PKGM.PHANTOM**: `PKGM.PHANTOM` is declared in the manifest but never imported. `PKGM.UNDECLARED` is imported in source but never declared. A package can have both kinds of mismatch.
- **vs namespace / monorepo packages**: An import that resolves to a sibling workspace package or a local module is not undeclared. Local top-level modules and the package's own name are excluded before flagging.
- **vs conditional or optional imports**: An import guarded by a try/except or a platform check can still be undeclared; the resolution risk is the same when the guard is taken. The atom records the missing declaration, not whether the import always executes.

## Structural Relationships

- **Often co-occurs with**: `PKGM.TYPOSQUAT` (a hallucinated import name that is also a look-alike of a popular package), `PKGM.DEPMOD` (resolution mechanics changed so the name resolves somewhere unexpected)
- **May imply**: Unpinned, unprovenanced resolution that a registry squatter can fill, especially for AI-generated or vibe-coded source

## Notes

Undeclared imports are common in throwaway scripts, so this is a low-confidence signal on its own and is most useful as an amplifier: an undeclared import whose name is also a look-alike (`PKGM.TYPOSQUAT`) is a strong slopsquatting indicator. Local modules, the package's own name, and standard-library names are excluded to keep the signal honest.
