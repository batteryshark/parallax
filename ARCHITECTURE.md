# Parallax: A Framework for Systematic Understanding of Systems

> "No single viewpoint tells you what something truly is. You need multiple perspectives to triangulate."

## Overview

Parallax is a framework for the systematic understanding of software (and eventually hardware) systems through observation, decomposition, and multi-perspective interpretive analysis. It provides a shared vocabulary for describing what systems do, a structured set of interpretive lenses for evaluating what those behaviors mean in different contexts, and an iterative investigation process for refining understanding over time.

The core insight: **the same observable behavior means different things depending on why you're looking at it.** An HTTP request during a package install is a potential exfiltration vector (security lens), a build-time side effect and fragility point (architecture lens), and an expanded blast radius (capability lens). The behavior is the same. The judgment differs. The vocabulary should be shared.

Parallax separates what has historically been conflated:

- **What something IS** (observable behavior, judgment-free)
- **What it SUGGESTS** (interpretation through a specific analytical lens)
- **How certain we are** (confidence: a spectrum, never binary)
- **How to learn more** (investigation: a cycle that produces new observations)
- **What to do about it** (response, only when confidence warrants action)

## Background & Motivation

This architecture emerged from the recognition that the MCD (Malicious Code Detection) taxonomy, while effective, was interleaving multiple concerns in each entry: behavior definitions, suspicion indicators, confidence guidance, and investigation steps. As the vision expanded to include a sister taxonomy for design patterns/antipatterns, agent capability assessment, and software health analysis, it became clear that these are all **different lenses applied to the same underlying observations**.

Rather than build parallel taxonomies with duplicated vocabularies, Parallax factors out the shared foundation (what systems do) and lets each analytical purpose define its own interpretive layer on top.

The name comes from the astronomical concept: the apparent displacement of an object when viewed from different positions. Astronomers use parallax to determine the true distance to stars. You need multiple viewpoints, because no single observation gives you truth. Parallax-the-framework works the same way: multiple analytical lenses applied to the same system converge toward genuine understanding.

## Architecture

```
+----------------------------------------------------------+
|            METHODS OF OBSERVATION                         |
|     (how you gather information)                          |
|                                                           |
|  Static Source | Static Binary | Dynamic | OSINT          |
|  Build/CI      | Network       | Scaffolding | ...        |
|                                                           |
|  Each has: capabilities, blind spots, tools required      |
|  Investigation cycle suggests method transitions          |
+----------------------------+-----------------------------+
                             | produce
                             v
+----------------------------------------------------------+
|            SOFTWARE BEHAVIOR ONTOLOGY                     |
|         (what you observe: shared vocabulary)             |
|                                                           |
|  Atoms:  Individual behaviors (NETW.HTTP, EXEC.SHELL)    |
|  Idioms: Recognized mechanisms, probabilistic,            |
|          spectrum of confidence, never binary              |
|          "Decode-and-execute chain"                       |
|          "Credential store sweep"                         |
|          "Remote shell"                                   |
|                                                           |
|  All observations carry:                                  |
|  - Provenance (which method produced this)                |
|  - Confidence (how certain, always a spectrum)            |
|  - Relationships (structural, not interpretive)           |
+----------------------------+-----------------------------+
                             | enriched by
                             v
+----------------------------------------------------------+
|                  ENRICHMENT                               |
|       (added context: facts, not judgments)               |
|                                                           |
|  Domain age, geo, hosting, maintainer history, package    |
|  publication timeline, threat intel, CVE associations,    |
|  code similarity, build reproducibility...                |
|                                                           |
|  Sourced by OSINT, build analysis, network analysis, etc. |
+----------------------------+-----------------------------+
                             | interpreted through
                             v
+----------------------------------------------------------+
|                    LENSES                                  |
|        (why it matters: interpretive frames)              |
|                                                           |
|  MCD         "Is this malicious?"                         |
|  Decisions    "Where does it decide trust or authority?"  |
|  Capability   "What's the blast radius if abused?"        |
|  Curiosity    "What's interesting or weird here?"         |
|  Architecture "Is this well-built? Where will it break?"  |
|  ...                                                      |
|                                                           |
|  Each lens provides:                                      |
|  - Indicators (what observations mean through this lens)  |
|  - Compositions (named patterns meaningful to this lens)  |
|  - Confidence modifiers (what matters to certainty here)  |
|  - Suggested verifications (including WHICH METHOD)       |
+----------------------------+-----------------------------+
                             |
                             v
+----------------------------------------------------------+
|            INVESTIGATION CYCLE                            |
|       (the engine: a process, not a layer)                 |
|                                                           |
|  1. Observations evaluated through active lenses          |
|  2. Lenses suggest verifications + which METHOD           |
|     can produce the needed observation                    |
|  3. Practitioner (or automation) executes method          |
|  4. New observations feed back to ontology                |
|  5. ALL lenses re-evaluate with new evidence              |
|  6. Confidence adjusts, up OR DOWN, across all lenses         |
|  7. Some relationships strengthen, some weaken            |
|  8. New verifications suggested (or not)                  |
|  9. Cycle continues until:                                |
|     - Confidence threshold met (for some lens)            |
|     - Available methods exhausted                         |
|     - Practitioner judgment says "enough"                 |
|                                                           |
|  Every verification can DISPROVE as well as confirm.      |
+----------------------------+-----------------------------+
                             | when confident enough
                             v
+----------------------------------------------------------+
|                   RESPONSE                                |
|          (per-lens, context-dependent)                    |
|                                                           |
|  MCD:          Contain, escalate, remediate               |
|  Architecture: Refactor, document debt, add tests         |
|  Capability:   Restrict permissions, add guardrails       |
|  Health Check: Report posture, recommend controls         |
+----------------------------------------------------------+
```

## Layer Detail

### Methods of Observation

Methods are how practitioners (or automated tools) gather information about systems. They are a first-class concept because:

- Different methods produce different types of observations
- Each method has structural blind spots, things it cannot see
- The investigation cycle's power comes from knowing when to switch methods
- A finding from static source analysis might require OSINT to interpret ("that domain is suspicious" requires checking WHOIS, a completely different method using completely different tools)

**Defined Methods:**

| Method | Produces | Cannot See |
|---|---|---|
| **Static Source Analysis** | Structure, logic flow, dependencies, hardcoded values | Runtime behavior, actual destinations, dynamic targets |
| **Static Binary Analysis** | Actual instructions, embedded data, linked libraries | Original intent, variable names (without symbols), untriggered paths |
| **Dynamic Analysis** | Runtime behavior, actual calls, memory contents, timing | Dormant paths, time-bombed behavior, environment-specific branches not triggered |
| **OSINT / External Intelligence** | Domain history, maintainer identity, threat intel, publication patterns | Nothing about the code itself, but transforms interpretation of everything else |
| **Build & CI Analysis** | Pipeline integrity, reproducibility, source-to-artifact drift | Runtime behavior |
| **Network Analysis** | Actual traffic, protocol behavior, payload contents | Code logic, dormant capabilities |
| **Environment Scaffolding** | Controlled conditions for other methods to operate | Is itself a method; scaffolding choices reveal practitioner hypotheses |

Methods are not ranked. They are complementary. A complete investigation typically requires multiple methods, and the investigation cycle explicitly recommends method transitions when current evidence has gaps.

### Software Behavior Ontology

The ontology is a judgment-free vocabulary for describing what systems do. It has two tiers.

#### Tier 1: Atoms

Individual observable software behaviors. These are the smallest unit of description, stripped of all interpretive judgment:

- `NETW.HTTP`: "Makes outbound HTTP/HTTPS requests"
- `EXEC.SHELL`: "Invokes a shell subprocess"
- `FSYS.WRITE`: "Writes data to the filesystem"
- `XFRM.ENCODE`: "Transforms data representation (base64, hex, XOR)"
- `TIME.CMP`: "Compares current time against a reference value"

An atom's definition describes **what the behavior is**, not **what it means**. No severity. No suspicion. No "this is commonly used for malicious purposes." Just: what does this code do?

Atoms specify:
- **ID and name**: unique identifier and human-readable label
- **Description**: what the behavior is, mechanically
- **Detection surface**: source, binary, runtime, or combination
- **Disambiguation**: how to distinguish from similar atoms
- **Structural relationships**: co-occurrence patterns, implies/requires relationships (structural, not interpretive)

#### Tier 2: Idioms

Recognized compositions of atoms that have a structural "what" but no interpretive "why." These are mechanisms that any practitioner would recognize as "a thing" regardless of which lens they're using.

The extracted idioms live in [`ontology/idioms/`](ontology/idioms/); the current set:

| Idiom | Constituent Atoms | Description |
|---|---|---|
| Decode-and-execute chain | `XFRM.*` reversal feeding `LOAD.EVAL` / `EXEC.*` | Transformed data is decoded and the result is executed |
| Remote shell | `NETW.SOCKET` / `NETW.LISTEN` + `EXEC.SHELL` + I/O redirection | A shell's input and output are wired to a network peer |
| Credential store sweep | `CRED.*` + `FSYS.READ` + `ARTF.PATH` + iteration | Systematically reads through multiple credential storage locations |
| Sentinel-guarded region access | `MEM.SENTINEL` + `TYPE.NARROW` + `MEM.BOUNDIDX` + equality guard | Region access gated on sentinel values and narrowed indices |

Idioms are **probabilistic, not binary.** An idiom match is always on a spectrum:

- "I'm 85% sure this is a credential store sweep. The store paths are there, the iteration is there, but there's an unexpected branch I haven't traced yet."
- "This looks like a decode-and-execute chain, but the decoded buffer might only ever reach a config parser."

This is essential because **software is messy and human.** Real code contains:

- Half-finished refactors
- Abandoned debug scaffolding
- Easter eggs and experiments
- Copy-pasted code that does more than the developer realized
- Dead code that almost works
- Latent behaviors one configuration change away from activating

The ontology must handle "I don't know what this is" as a valid, persistent state, not a failure to classify.

#### Observation Provenance

Every observation in the ontology carries:
- **Which method produced it**: static source analysis found this, or dynamic analysis revealed it at runtime, etc.
- **Confidence**: how certain we are this observation is accurate (a spectrum)
- **Structural relationships**: connections to other observations (co-occurrence, execution flow, data flow), factual, not interpretive

### Enrichment

Enrichment adds context to observations without adding judgment. It answers factual questions about the things observed:

- A domain found in code: WHOIS shows it was registered 28 days before package publication
- A maintainer account: publication history shows 3 years dormant then sudden burst of activity
- A compiled binary: build reproducibility check shows behavioral drift from source
- A package dependency: registry metadata shows it has 12 downloads total

Enrichment is primarily sourced by OSINT and build analysis methods, but any method can produce enrichment data.

The critical distinction: **enrichment is facts, not judgments.** "This domain was registered 28 days ago" is enrichment. "This domain is suspicious because it was recently registered" is a lens interpretation of that enrichment. The MCD lens cares deeply about domain age. The architecture lens probably doesn't. Both work from the same enrichment data.

### Lenses

A lens is an interpretive frame that evaluates enriched observations and assigns meaning. Each lens answers a different question about the same system.

#### Lens Components

Every lens provides:

**Indicators**: what observations and idioms mean through this lens. The same atom gets different interpretations:

| Atom | MCD Lens | Architecture Lens | Capability Lens |
|---|---|---|---|
| `NETW.HTTP` | Potential C2/exfiltration channel | External dependency; failure point | Network reach capability |
| `XFRM.ENCODE` | Severity multiplier (hiding something) | Unnecessary complexity (code smell) | Opaque capability, harder to audit |
| `PKGM.INSTALL` | Attack entry point | Build-time side effect (antipattern) | Unsupervised execution window |
| `EXEC.SHELL` | Arbitrary code execution risk | Portability concern; injection surface | High-privilege capability |
| `TIME.CMP` | Potential logic bomb trigger | Time-coupled logic (fragility) | Conditional capability activation |

**Compositions**: named patterns built from ontology terms that are meaningful to this lens:

- MCD: `BP-SUPPLY` = `PKGM.INSTALL` + (`EXEC.*` | `NETW.*` | `FSYS.WRITE`) → "supply chain attack pattern"
- Architecture: `AP-FRAGILE-INTEGRATION` = `NETW.HTTP` + no error handling + no retry → "brittle external dependency"
- Capability: `CR-HIGH-BLAST` = `EXEC.SHELL` + `FSYS.WRITE` + `NETW.*` + `CRED.*` → "exfiltration-capable agent profile"

**Confidence modifiers**: what increases or decreases certainty for this lens. Which enrichment data matters, which contextual signals this lens weighs heavily vs. ignores.

**Suggested verifications**: what to investigate next AND which method can produce the needed observation. This is how lenses drive the investigation cycle.

#### Lenses

Five lenses are defined today under [`lenses/`](lenses/); two more are candidates.

| Lens | Core Question | Primary Consumers |
|---|---|---|
| **MCD** | Is this malicious? | Security teams, SOC, supply chain security |
| **Decisions** | Where does it decide whom to trust, what to run, whether to elevate? | Code review, trust-boundary analysis, agent steering surface |
| **Capability** | What could go wrong if this is abused? What's the blast radius? | Agent safety, permission modeling, threat modeling |
| **Curiosity** | What's interesting, weird, or unexpected here? | Public content, education, community engagement |
| **Architecture** | Is this well-built? Where will it break? What are the implicit assumptions? | Engineering leads, architects, tech debt management |
| **Software Protection** (candidate) | Is this DRM/anti-tamper/licensing? Is this expected? | RE practitioners, compliance, software vendors |
| **Health Check** (candidate) | What's the overall posture? What needs compensating controls? | Engineering leadership, risk management |

The lens list is open. New lenses can be added without modifying the ontology or other lenses.

### Investigation Cycle

The investigation cycle is not a layer in the architecture. It is the **process** that uses all layers. It is the engine of refinement.

```
     OBSERVE ──> INTERPRET ──> VERIFY ──> DISCOVER MORE
        ^                                      |
        |                                      |
        +──────────────────────────────────────+
```

Key principles:

**Verification produces new observations.** "Check if the domain was recently registered" does more than confirm a suspicion. The WHOIS lookup might reveal the domain shares infrastructure with known C2, which is a new observation, which triggers new interpretation across all active lenses, which suggests new verification. Verification is generative, not terminal.

**All lenses see all observations.** When one lens's verification produces a new observation, that observation feeds back to the ontology and is available to ALL active lenses. A verification suggested by the MCD lens might produce an observation that's more interesting to the Capability lens.

**Evidence can disprove.** Confidence is not monotonically increasing. You can be 80% sure something is malicious, then discover context that drops you to 20%. Relationship strength going DOWN is as important as going up. The framework handles this explicitly.

**Method transitions are first-class.** The cycle doesn't just say "verify X." It says "verify X, and this requires switching from static source analysis to OSINT" or "you need to scaffold a dynamic analysis environment to observe this behavior at runtime." Knowing when to switch methods is a core practitioner skill that the framework makes explicit.

**The cycle terminates on judgment, not rules.** The cycle continues until:
- A confidence threshold is met for some lens (enough to act)
- Available methods are exhausted (nothing more to try)
- Practitioner judgment says "enough" (diminishing returns, acceptable uncertainty)

### Confidence

Confidence has shared structural mechanics (the algebra) and lens-specific parameterization.

#### Shared Confidence Algebra

These principles apply regardless of lens:

- **Reachability**: observations must be connected through plausible execution flow to compose into an idiom or pattern. Co-location is not composition.
- **Cross-category accumulation**: corroborating observations from different ontology categories are more significant than multiple observations from the same category.
- **Idiom recognition**: atoms that form a recognized idiom carry more weight than disconnected atoms.
- **Provenance weighting**: observations confirmed by multiple methods are stronger than single-method observations. Dynamic analysis confirming a static analysis finding is stronger than static alone.
- **Enrichment integration**: enrichment data modifies confidence in structured ways (amplifies, attenuates, or is neutral).
- **Disproof handling**: contradictory evidence weakens relationships and can invalidate interpretations. The framework explicitly tracks what would disprove a current assessment.

#### Lens-Specific Parameterization

Each lens defines:
- Which enrichment data matters to its confidence assessment
- What counts as escalating vs. de-escalating
- Confidence thresholds for different response levels
- Which verifications this lens recommends at each confidence level
- What would constitute disproof for its key compositions

### Response

Response is entirely lens-specific. Each lens defines its own response framework triggered by the combination of its severity assessment and confidence level.

The MCD lens response framework (Tiers 0-5 from the current taxonomy) is one example. The architecture lens might have: "document," "flag for refactoring," "add tests," "block deployment." The capability lens might have: "acceptable risk," "add guardrails," "restrict permissions," "isolate."

Response is the only layer that is fully decoupled from the shared architecture. It is pure lens-specific policy.

## Repository Structure

The model lives in this repository; the runnable tools live in the [parallax](https://github.com/batteryshark/parallax) repository. The split is deliberate: the vocabulary must not depend on any scanner. (An earlier plan split the ontology and each lens into separate repositories; one model repo turned out to be easier to keep coherent.)

| Location | Contains |
|---|---|
| [`ontology/`](ontology/) | Atoms, idioms, structural relationships. The shared, judgment-free vocabulary. |
| [`enrichment/`](enrichment/) | Lens-neutral external facts that modify confidence. |
| [`lenses/`](lenses/) | The interpretation layer: MCD, decisions, capability, curiosity, architecture. |
| [`investigation/`](investigation/) | Investigation cycle mechanics, confidence algebra, method descriptions, method transition guidance. |
| [`signatures/`](signatures/) | Machine-readable mappings from stable code surfaces to ontology atoms. |
| [parallax](https://github.com/batteryshark/parallax) | One reference implementation family: the `prlx-engine` observation layer and the `prlx-understand`, `prlx-mcd`, and `prlx-agent-risk` products. |

## Design Principles

### The Ontology Is Judgment-Free

The ontology describes what systems do, not whether that's good or bad. `XFRM.ENCODE` means "transforms data representation." It does not mean "suspicious obfuscation." The MCD lens says obfuscation in a dependency is a severity multiplier. The software protection lens says obfuscation in a shipped binary is expected product behavior. The architecture lens says unnecessary obfuscation is a code smell. The ontology just says: this code encodes data.

### Everything Is a Spectrum

Nothing in the framework is binary. Idiom matches, lens interpretations, and confidence levels are all probabilistic. "I'm 85% sure this is X" is more honest and more useful than "this is X." The framework explicitly supports:

- Partial idiom matches ("three of four expected atoms present")
- Competing lens interpretations ("MCD says suspicious at medium confidence, Software Protection says expected at high confidence")
- Uncertainty as a valid state ("I don't know what this is yet, and that's fine")
- Revision ("I was sure it was X, but new evidence makes that impossible")

### Software Is Messy and Human

The framework does not assume code is a clean expression of intent. Real systems contain abandoned experiments, debug scaffolding, easter eggs, copy-pasted code that does more than the developer realized, half-finished features, and latent behaviors. "I don't know what this is" and "this appears to be unfinished/vestigial" are valid, persistent classifications, not failures to categorize.

### Verification Is a Cycle, Not a Step

Verification generates new observations. New observations feed all lenses. Lenses suggest new verifications. This cycle is the engine of understanding. It is not a terminal step in a pipeline. The framework tracks what each verification step revealed and how it changed the assessment across all active lenses.

### No Single Lens Owns Truth

Just as astronomers need parallax from multiple positions to determine a star's true distance, this framework achieves understanding through the convergence (or productive tension) between multiple analytical lenses. A system that looks benign through the MCD lens but brittle through the architecture lens and high-blast-radius through the capability lens is understood differently than any single lens would suggest.

### Methods Are First-Class

The tools and techniques used to gather observations are not incidental. They are a core part of the framework. Each method has known capabilities and structural blind spots. The investigation cycle explicitly tracks which methods have been applied, which haven't, and which method transitions might reveal new understanding.

## Open Design Questions

### Idiom Curation

How are new idioms recognized and added to the ontology? Is there a threshold for "this is a recognized mechanism" or is it purely practitioner-driven curation? Current thinking: idioms emerge from any lens's work. If MCD practitioners keep seeing a pattern, or architecture reviewers keep recognizing a mechanism, that mechanism gets proposed as an idiom. The bar is "any practitioner would recognize this as 'a thing' regardless of their lens."

### Cross-Lens Observation Flow

When one lens's verification produces observations more relevant to another lens, is there formal handoff? Current thinking: no formal handoff needed. All observations go to the ontology, all lenses see all observations, and relationship strength is tracked and adjusted naturally. Connections strengthen or weaken based on evidence. Let it be disproven rather than gatekept.

### Enrichment Boundaries

What's in scope for enrichment vs. lens interpretation? "Domain registered 28 days ago" is clearly enrichment (fact). Is "this code is similar to known malware family X" enrichment or MCD lens interpretation? Current thinking: if it's a factual comparison (cosine similarity score, structural match percentage), it's enrichment. If it requires judgment ("this similarity is suspicious"), it's lens interpretation.

### Hardware Ontology Extension

The atom/idiom model should extend naturally to hardware (firmware behaviors, FPGA configurations, chip-level operations), but the specific atom categories will differ significantly. This is a future concern; the architecture should accommodate it without requiring redesign.

## Status

- **Current state:** The framework layer is defined and populated. This document captures the architectural vision.
- **Done:** the judgment-free ontology and its idioms in [`ontology/`](ontology/), lens-neutral enrichment in [`enrichment/`](enrichment/), five lenses under [`lenses/`](lenses/), the investigation framework in [`investigation/`](investigation/), and signature packs in [`signatures/`](signatures/).
- **Reference implementation:** the [parallax](https://github.com/batteryshark/parallax) repository implements the model: a deterministic engine that emits ontology observations, and three products that read them through the lenses.

---

*This document is a living artifact. It captures architectural decisions and design rationale for the Parallax framework. It will evolve as implementation reveals new considerations.*
