# Methods of Observation

Methods are how practitioners (or automated tools) gather information about systems. They are a first-class concept in Parallax because different methods produce different types of observations, each method has structural blind spots, and the investigation cycle's power comes from knowing when to switch methods.

Methods are not ranked. They are complementary. A complete investigation typically requires multiple methods, and the investigation cycle explicitly recommends method transitions when current evidence has gaps.

## Defined Methods

| Method | Primary Output | Key Blind Spots |
|---|---|---|
| [Static Source Analysis](static-source.md) | Structure, logic flow, dependencies, embedded values | Runtime behavior, actual destinations, dynamic targets |
| [Static Binary Analysis](static-binary.md) | Actual instructions, embedded data, linked libraries | Original intent, variable names, untriggered paths |
| [Dynamic Analysis](dynamic.md) | Runtime behavior, actual calls, memory contents, timing | Dormant paths, time-bombed behavior, untriggered branches |
| [OSINT / External Intelligence](osint.md) | Domain history, maintainer identity, threat intel, publication patterns | Nothing about the code itself |
| [Build & CI Analysis](build-ci.md) | Pipeline integrity, reproducibility, source-to-artifact drift | Runtime behavior |
| [Network Analysis](network.md) | Actual traffic, protocol behavior, payload contents | Code logic, dormant capabilities |
| [Environment Scaffolding](scaffolding.md) | Controlled conditions for other methods | Is itself a meta-method; scaffolding choices reveal practitioner hypotheses |

## Method Transitions

The investigation cycle suggests method transitions when current evidence has gaps that the current method cannot fill. Common transitions:

| When you see... | Current method likely... | Switch to... |
|---|---|---|
| Hardcoded URL/IP in source | Static source | OSINT (reputation, registration) |
| Obfuscated payload | Static source | Dynamic (observe decoded output) |
| Environment-gated branch | Static source | Environment scaffolding → dynamic |
| Source-to-binary mismatch | Build & CI | Static binary (analyze actual binary) |
| Suspicious network atoms | Static source/binary | Network analysis (observe actual traffic) |
| Unknown maintainer | Any code analysis | OSINT (identity, history) |
| Time-gated behavior | Static source | Environment scaffolding (manipulate clock) → dynamic |

## Provenance and Multi-Method Confirmation

When multiple methods independently confirm the same observation, confidence in that observation increases. See [confidence algebra](../confidence-algebra.md) for the formal treatment of provenance weighting.

The strongest evidence comes from methods with non-overlapping blind spots confirming the same finding. For example, static source analysis identifying a suspicious code path and dynamic analysis confirming that path executes with the predicted behavior.
