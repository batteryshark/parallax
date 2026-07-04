# PKGM.TYPOSQUAT: Look-Alike Package Name

## Description

A package whose own name is a near-miss of a popular package: within a small edit distance (typically 1 to 2 characters), or a decorated variant such as a date or version prefix (`2022-requests`). This is the structural fact that a name resembles an established package. It covers both classic typosquatting (a human typo of a real name) and slopsquatting (a name that sounds plausible to a language model, which a squatter then registers so AI-generated projects install it). The judgment that this is malicious belongs to the MCD lens (`BP-TYPOSQUAT`), not to the atom.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | The package's declared name (manifest `name`, else the directory) is edit-distance 1 to 2 from a known popular package, or decorates one with a date/version prefix. A local popular-name list makes this deterministic. |
| Static Binary | N/A | This is a package-identity observation, not a binary one |
| Runtime/Dynamic | N/A | Name similarity is static metadata |

## Disambiguation

- **vs an intentional fork or variant**: A maintained fork or an owned namespace variant is not a squat. The atom records only the name similarity; confirming intent needs the registry (publisher, age, downloads), which is an `osint` method, not local.
- **vs a legitimate extension**: Packages that extend a popular one usually add a clear suffix and sit well beyond edit-distance 2 (`requests-oauthlib` is not close to `requests`). The small-distance bound is what separates a look-alike from an extension.
- **vs PKGM.UNDECLARED**: `PKGM.TYPOSQUAT` is about the package's own name resembling another. `PKGM.UNDECLARED` is about a dependency that source imports but the manifest never declares.

## Structural Relationships

- **Often co-occurs with**: `PKGM.INSTALL` (a look-alike that also ships an install hook is the canonical squat), `PKGM.UNDECLARED` (a hallucinated import that resolves to a squat), `LOAD.EVAL` / `NETW.HTTP` (a payload behind the familiar name)
- **May imply**: A consumer intended a different, popular package and will install this one by mistake or by model hallucination

## Notes

Name similarity alone is a real but local-only signal. It is reported at honest (medium) confidence and escalates only when the look-alike also carries a payload (install hook, execution, network, decrypt). Confirmation that a name is a squat rather than an established package requires registry evidence, so the finding always names the `osint` check to run.
