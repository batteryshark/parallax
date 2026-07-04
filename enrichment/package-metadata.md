# Package Metadata

Facts about a package's registry record: how old it is, who has owned it, how
much it is used, how it has been versioned, and how it was published. Sourced
from registry APIs and OSINT. These are facts about the record, not the code.

| Id | Data point | What it factually states | Primary source |
|---|---|---|---|
| `ENR.PKG.AGE` | Publication age | Time since the package's first publication and since the version under review | registry API |
| `ENR.PKG.OWNERSHIP` | Ownership history | The sequence of maintainers and ownership transfers, with dates | registry API, OSINT |
| `ENR.PKG.DOWNLOADS` | Download volume | Download count and its trend over time | registry API |
| `ENR.PKG.VERSIONS` | Version sequence | The published version list, including gaps, yanks, and ordering | registry API |
| `ENR.PKG.PROVENANCE` | Publish provenance | How a version was published: signed/attested (OIDC Trusted Publisher, Sigstore), CI-bound, or a manual token with no attestation | registry API, OSINT |

Judgment-free: this records the registry facts. Whether a recent ownership
change before a release is alarming, or an attestation downgrade indicates
account compromise, is a lens call. The MCD lens's weighting is in
[`../lenses/mcd/signals/package-metadata.md`](../lenses/mcd/signals/package-metadata.md);
other lenses may treat the same facts as neutral.
