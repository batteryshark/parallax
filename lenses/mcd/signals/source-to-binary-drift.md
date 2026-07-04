# Source-to-Binary Drift Signals

| Signal | Description | Confidence Effect |
|---|---|---|
| **Behavioral drift** | Compiled binary contains functionality (imports, strings, behaviors) not present in published source | Very high: binary was not built from published source |
| **Build irreproducibility** | Binary cannot be reproduced from published source and build instructions | May indicate post-build injection |
| **Unexpected native extensions** | Package includes native binaries not explained by functionality | Native code is opaque to source analysis |
| **Security mitigations disabled** | Compiled binaries with exploit mitigations deliberately disabled (no ASLR, no DEP/NX, no CFG, no stack canaries, no RELRO). Requires explicit compiler/linker flags. | High: deliberate weakening has no legitimate production justification |
| **Unsigned or weakly-signed binaries** | Distributed without signatures, or signed with deprecated algorithms (SHA-1) when stronger alternatives available | Medium when stronger signing used elsewhere by same publisher |
| **Debug info in production** | Debug symbols, verbose logging enabled, development code paths compiled in | Low alone, medium when combined with other drift signals |

Relates to: `PKGM.BINDOWN`, `ENVI.SECDISABLE` atom observations
