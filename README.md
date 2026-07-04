# Parallax Taxonomy

A tool-agnostic model for reasoning about what code **can do**: reading code and systems as affordances, decisions, and brittleness rather than lines and defects.

The premise is that no single viewpoint tells you what a system truly is. You need a shared, judgment-free vocabulary for what code does, several interpretive lenses for what those behaviors mean, and an honest account of how sure you are and what would change that.

The model keeps fact and judgment in separate layers. An atom records a mechanical fact: `EXEC.SHELL` means "invokes a shell subprocess", never "suspicious". A lens supplies the judgment, reading the same facts through one question: is this malicious, what breaks if it is abused, where does it decide whom to trust. Severity (how bad, if the reading is right) is always reported apart from confidence (how sure we are), and every interpretation names what would disprove it.

Three guardrails follow from that separation and hold everywhere in the model. Capability is not accusation: naming what code can do says nothing about intent. Suspicion is not proof: a lens reading carries a confidence and a disproof criterion, not a verdict. Absence of a finding is not a safety guarantee: every method of observation declares what it cannot see.

The model extends to agent surfaces. The tools and skills an agent holds are code, and they change what the agent can be tricked into; that risk is capability combined with steerability, not maliciousness. The same atoms describe what a tool set can reach, and the same lenses read what that reach means once a steerable agent holds it.

## The layers

| Layer | Question it answers |
|---|---|
| Ontology (atoms) | What does the code or system do? (judgment-free) |
| Enrichment | What external facts add context to that? (judgment-free) |
| Lens | Why does that behavior matter, from this viewpoint? |
| Confidence | How sure are we, and what would disprove it? |
| Investigation | What should we check next, and with which method? |
| Response | What should someone do about it? |

The observation is shared; the judgment changes with the lens. A package install script that reaches the network is a malicious-code signal through the MCD lens, an expanded blast radius through the capability lens, and a build-fragility point through the architecture lens. Same fact, different reading.

## What is here

- [`ontology/`](ontology/): the judgment-free behavior vocabulary: 129 atoms across 18 categories (16 core plus the experimental MEM and TYPE), and the idioms that compose them. An atom records a mechanical fact (`EXEC.SHELL`, `NETW.HTTP`, `CRED.CLOUD`), never a verdict.
- [`signatures/`](signatures/): machine-readable signature-pack contracts for stable mappings from observed code surfaces to ontology atoms. These are data, not parser mechanics; scanner implementations own extraction. The YAML packs are the source of record; [`scripts/build-signature-json`](scripts/build-signature-json) regenerates their JSON mirrors.
- [`enrichment/`](enrichment/): lens-neutral external facts that modify confidence (domain age, package provenance, build drift, and the like). Like atoms, these are facts, not judgments; each lens decides whether a datum amplifies, attenuates, or is neutral to its reading.
- [`lenses/`](lenses/): the interpretation layer. Each lens reads the shared atoms through one question: MCD (is this malicious?), decisions (where does it decide trust, dispatch, authority?), capability (blast radius if abused), curiosity (what is surprising for its stated purpose?), and architecture (brittleness and operational risk). Each lens keeps severity separate from confidence and states what would disprove a finding.
- [`investigation/`](investigation/): the confidence algebra and the methods of observation, including their declared blind spots.
- [`ARCHITECTURE.md`](ARCHITECTURE.md): the framework and its design philosophy.

## Design principles

- Atoms are mechanical and lens-neutral. Anything that encodes intent (malicious, stealthy, suspicious) lives in a lens, never in the ontology.
- Severity and confidence are independent dimensions, always reported separately.
- Every interpretation is falsifiable: it names what would change the assessment.
- Methods of observation carry their own blind spots, so silence is never read as safety.

## Using it

The model is meant to be read, cited, and implemented. This repository is the source of record for the vocabulary, lenses, confidence model, investigation methods, and response guidance.

Implementations can map observed code surfaces to ontology atoms, enrich those atoms with external context, and then apply one or more lenses to produce an interpretation. The shared vocabulary keeps observations stable while allowing different tools, reviews, or research workflows to ask different questions of the same facts.

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
