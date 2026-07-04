# Architecture Lens

*"Is this well-built? Where will it break?"*

The Architecture lens evaluates software behaviors for quality indicators, design patterns and antipatterns, brittleness, implicit assumptions, and areas needing compensating controls.

## Components

- **Indicators**: what ontology atoms and idioms suggest about build quality, resilience, and design intent
- **Compositions**: named patterns (fragile integration, time-coupled logic, unhandled failure modes, etc.)
- **Confidence modifiers**: signals like test coverage, documentation presence, version maturity, error handling patterns
- **Assessment playbooks**: investigation guidance for understanding design decisions and their consequences
- **Remediation guidance**: refactoring recommendations, technical debt documentation, compensating controls

## Status

Implemented as the MVP in the prlx reference engine. The engine's `architecture` lens reads the shared atoms as operational risk through five compositions: fragile install path (`PKGM.INSTALL` with network, exec, or filesystem-write side effects), opaque runtime loading (`LOAD.*`), external control dependency (`NETW.*`), environment-shaped behavior (`ENVI.*`), and unbounded side-effect surface (`RSRC.*` / `FSYS.WRITE` / `FSYS.DELETE` / `EXEC.*`). Each keeps severity operational (low or medium), separate from confidence, and names a compensating control. The lens fires on ordinary code; that is the map, not an alarm. The temporal-coupling target below is specified but deferred in the engine, because the `TIME.*` atoms flood on benign timestamping.

The Architecture lens should start as a brittleness map, not a generalized code-quality score. Its first job is to identify places where system behavior is opaque, fragile, environment-dependent, hard to reproduce, or one change away from operational failure.

## MVP Interpretation Targets

| Observation Pattern | Architecture Interpretation |
|---|---|
| `PKGM.INSTALL` + `NETW.*` / `EXEC.*` / `FSYS.WRITE` | Build or install path has side effects outside normal dependency resolution. |
| `LOAD.*` with computed input | Runtime behavior is opaque to static review and likely harder to test. |
| `NETW.*` in build, install, or startup path | System has an external service dependency in a sensitive lifecycle phase. |
| `ENVI.*` + divergent behavior | Behavior changes by environment, increasing reproduction and debugging cost. |
| `TIME.*` gating behavior | Temporal coupling may make failures intermittent or hard to reproduce. |
| `RSRC.*` without clear bounds | Resource consumption may be unbounded or poorly isolated. |
| `CRED.*` / `FSYS.SENSITIVE` in broad utility code | Trust boundary may be implicit or poorly encapsulated. |
| `XFRM.*` before `LOAD.*` | Executed behavior is hidden behind transformation, reducing reviewability. |

## Initial Composition Candidates

- **Fragile install path:** install or build step performs network, filesystem, or process operations that can fail independently of source correctness.
- **Opaque runtime loading:** code loads executable behavior from computed strings, generated code, reflected objects, deserialized input, or runtime-fetched artifacts.
- **Hidden external control plane:** runtime behavior depends on network destinations, webhooks, brokers, or remote configuration without clear fallback.
- **Environment-shaped behavior:** environment checks produce materially different behavior across CI, local development, production, or sandboxed contexts.
- **Unbounded side-effect surface:** code can write, delete, execute, or consume resources without narrow scope or explicit guardrails.

## Confidence Modifiers

Architecture confidence should increase when:

- risky behavior is reachable from common lifecycle paths
- tests do not cover the behavior
- documentation omits the behavior
- errors are suppressed
- dependencies or destinations are computed dynamically
- behavior differs across environments

Architecture confidence should decrease when:

- behavior is isolated behind a narrow interface
- inputs are allowlisted
- artifacts are checksummed or reproducible
- failure modes are explicit and tested
- documentation accurately describes the operational dependency
- monitoring exists at the behavior boundary
