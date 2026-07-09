# Software Behavior Ontology

Judgment-free vocabulary for describing what systems do.

## Atoms

Individual observable software behaviors. The smallest unit of description. Each atom specifies what a behavior IS, not what it means.

Atoms define:
- ID and name (e.g., `XFRM.ENCODE`)
- Description (purely mechanical, what the code does)
- Detection surface (source, binary, runtime)
- Disambiguation (how to distinguish from similar atoms)
- Structural relationships (co-occurrence, implies/requires, factual, not interpretive)

### Categories

Each category groups related atoms. The names are mechanical and judgment-free by design: a category says what a behavior is, not whether it is good or bad. That is why several read as deliberately neutral ("transformation" rather than "obfuscation", "system inspection" rather than "reconnaissance").

| Category | Name | Atom Count | Naming note |
|---|---|---|---|
| XFRM | Data & Code Transformation | 9 | "transformation" is mechanical; "obfuscation" would be a judgment |
| NETW | Network Communication | 13 | neutral |
| EXEC | Code Execution | 5 | CMDCON folded into XFRM.STRCON + EXEC.* |
| FSYS | Filesystem Operations | 11 | CLIPBOARD is an awkward fit, may relocate |
| CRED | Credential Access | 7 | neutral |
| LOAD | Dynamic Code Loading | 9 | includes MEMCHAIN (in-memory chain) and KERNEL_MODULE (kernel-space load) |
| ENVI | Environment Interaction | 9 | "environment interaction" is mechanical; "evasion" would be a judgment |
| CRPT | Cryptographic Operations | 10 | neutral |
| PRST | Persistence Mechanisms | 6 | mechanical |
| PRIV | Privilege Operations | 6 | "operations" is mechanical; "escalation" implies improper |
| SYSI | System Inspection | 8 | "system inspection" is mechanical; "reconnaissance" would be a judgment |
| PKGM | Package & Build Operations | 8 | "operations" is mechanical; "manipulation" would be a judgment |
| TIME | Temporal Operations | 4 | neutral |
| ARTF | Embedded Artifacts | 10 | "embedded" is neutral |
| AITM | AI-Directed Content | 4 | "content" is neutral; "manipulation" would be a judgment |
| RSRC | Resource Consumption | 6 | "consumption" is mechanical; "manipulation" would be a judgment |

### Experimental Categories

| Category | Name | Atom Count | Source | Notes |
|---|---|---|---|---|
| MEM | Memory Layout & Access Patterns | 3 | ffmpeg h264 sentinel-collision analysis | Covers structural memory patterns: sentinel initialization, boundary-adjacent indexing, compile-time variable layout |
| TYPE | Type Representation Patterns | 1 | ffmpeg h264 sentinel-collision analysis | Covers type width operations: narrowing, (future: widening, reinterpretation) |

### Category Totals

125 atoms across the 16 MCD-derived categories, plus 4 experimental atoms (MEM = 3, TYPE = 1) = 129 atoms total. No pending categories.

## Skill-Emitted Tactic Atoms

The categories above are the judgment-free MCD ontology. A second, smaller vocabulary is emitted directly by RE covert-scan skills rather than by the signature packs, and names three tactic families this ontology deliberately omits — `OBF` (obfuscation), `EVADE` (environment-keyed evasion), and `STEGO` (steganography). Those names are lens judgments (the neutral ontology uses `XFRM` for transformation and `ENVI` for environment interaction), so they do not live under `ontology/atoms/**`. Instead they are declared in a flat registry carrying each atom's family, a default confidence baseline, a mechanical description, and which skill(s) emit it.

As with the signature packs, [`atom-registry.toml`](atom-registry.toml) is the authoring source of record and `atom-registry.json` is its generated mirror — edit the TOML, then regenerate with `scripts/build-signature-json` (never hand-edit the JSON).

The registry is the definition home that lets a scanner core validate a skill-emitted atom by **exact atom** (e.g. `OBF.XOR`, `EVADE.TIMEZONE`, `STEGO.HOMOGLYPH`), not merely by family prefix. See `rekit`'s `js-covert-scan` / `py-covert-scan` skills for the emitters.

## Idioms

Recognized compositions of atoms with a structural "what" but no interpretive "why." Mechanisms any practitioner would recognize regardless of which lens they're using.

Idioms are always probabilistic: a match is on a spectrum, never binary.

### Extracted Idioms

| Idiom | Key Atoms | Status |
|---|---|---|
| [Decode-and-execute chain](idioms/decode-and-execute-chain.md) | `XFRM.*` → reversal → `LOAD.EVAL` / `EXEC.*` | Written |
| [Remote shell](idioms/remote-shell.md) | `NETW.SOCKET`/`NETW.LISTEN` + `EXEC.SHELL` + I/O redirect | Written |
| [Sentinel-guarded region access](idioms/sentinel-guarded-region-access.md) | `MEM.SENTINEL` + `TYPE.NARROW` + `MEM.BOUNDIDX` + equality guard | Written |
| [Credential store sweep](idioms/credential-store-sweep.md) | `CRED.*` + `FSYS.READ` + `ARTF.PATH` (multiple) + iteration | Written |

### Evaluated Candidates

| Candidate | Verdict | Reasoning |
|---|---|---|
| Environment-gated behavior | Rejected | Too common in normal software (feature flags, CI detection) |
| Hybrid encryption pipeline | Rejected | Intra-category crypto design pattern, not behavior composition |
| Timed conditional execution | Rejected | Too simple (TIME.CMP + branch), universal pattern |
| Install-time side effect | Rejected | Two-atom co-occurrence, not multi-step mechanism |
| Network reconnaissance | Rejected | Absorbed into SYSI + NETW combination observations |
| Cross-architecture serialization | Candidate | MEM.VARLAYOUT + network/file I/O, pending further analysis |

## Design Principles

- **Judgment-free**: Descriptions say what code does mechanically, never what it means or whether it's good/bad
- **Category names are neutral**: Categories named for what the behaviors ARE, not what a specific lens interprets them as (e.g., XFRM not OBFS)
- **Everything is a spectrum**: Idiom matches, confidence, relationships, all probabilistic
- **"I don't know" is valid**: Unclassifiable behavior is a legitimate persistent state
