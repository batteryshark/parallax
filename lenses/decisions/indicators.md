# Decisions Lens: Indicators

How the decisions lens reads ontology atoms and idioms as decision points. These are **interpretations**, not new ontology. "Consequence" is the lens's severity axis; it is independent of confidence.

## Trust decisions

| Observation | Read as | Consequence | Raises consequence | Lowers consequence |
|---|---|---|---|---|
| `LOAD.DESER` (pickle/marshal/yaml.load/Java/.NET deser) | "I trust this serialized data enough to reconstruct objects from it" | High | Source is remote/user-supplied; deserializer is known-dangerous | Format is safe-by-construction (e.g., `yaml.safe_load`); data is local + trusted |
| `NETW.*` result used by `LOAD.*`/`EXEC.*`/`FSYS.WRITE` with **no** `CRPT.SIGN`/`CRPT.HASH`/`CRPT.CERT` in scope | "I trust whatever the network returned" (trust-by-default) | High | Result is executed/loaded; destination is not pinned | Integrity verified upstream; result is inert data |
| `CRPT.SIGN` / `CRPT.CERT` **present** before use | An *explicit* trust decision (verification performed) | Informational–Low | none | This is the good case; note it to contrast with omissions |
| `XFRM.ENCODE`/`XFRM.ENCRYPT` feeding `LOAD.*` | "I trust decoded bytes enough to run them" | Medium–High | Decoded content is executed | Decoded content is displayed/stored only |

**Absence is the signal.** The strongest trust finding is often a *missing* `CRPT.*` where the data flow clearly warranted it.

## Authority decisions

| Observation | Read as | Consequence | Raises | Lowers |
|---|---|---|---|---|
| `PRIV.SUDO` / `PRIV.SUID` | "I run this with elevated privilege" | High | Elevation wraps `EXEC.*`/`FSYS.WRITE` on attacker-influenced input | Elevation is narrow, audited, drops immediately |
| `PRIV.CAP` / `PRIV.TOKEN` | "I grant/assume a specific capability or token" | Medium–High | Capability is broad or long-lived | Least-privilege, short-lived, scoped |
| `PRIV.ACCOUNT` | "I decide which identity acts" | Medium | Identity is derived from untrusted input | Fixed, documented service identity |

## Dispatch decisions

| Observation | Read as | Consequence | Raises | Lowers |
|---|---|---|---|---|
| `LOAD.EVAL` | "A runtime value decides what code runs" | High | Value reachable from network/user/env | Value is a compile-time constant |
| dynamic `LOAD.IMPORT` (computed module name) | "A runtime value decides what module loads" | Medium–High | Name is constructed from input | Name from a closed allowlist |
| `EXEC.*` with a constructed command (`XFRM.STRCON` + `EXEC.SHELL`) | "Input decides what command executes" | High | Command string includes external input | Fully static argv, no shell |
| `LOAD.CODEGEN` | "I generate and then run code" | High | Generation inputs are tainted | Templates are fixed and reviewed |

## Environment-gate decisions

| Observation | Read as | Consequence | Raises | Lowers |
|---|---|---|---|---|
| `ENVI.ENVCHECK` gating divergent paths (the *environment-gated behavior* idiom) | "I behave differently depending on where I run" | Medium | Divergent path hides `EXEC.*`/`NETW.*`; gate detects sandbox/CI | Gate is a documented feature flag |
| `TIME.CMP` gating divergent paths (the *timed conditional execution* idiom) | "I behave differently depending on when I run" | Medium–High | Divergent path is dormant until a date/delay | Cache TTL, rate limiting, scheduling |

## Cross-cutting modifiers

- **Tainted-reachability dominates.** A decision on input that untrusted data can reach is categorically more consequential than the same decision on trusted/constant input. (Reachability confidence is bounded by the engine's analysis depth: an engine without dataflow uses co-location as a weak proxy; record that limitation in confidence.)
- **Stacked decisions compound.** Trust + dispatch in the same flow (run unverified remote bytes) is the highest-consequence pattern; see [compositions.md](compositions.md).
- **Confidence ≠ consequence.** "This is certainly a dispatch decision" (high confidence) says nothing about whether its input is reachable by an attacker (consequence). Report them separately, always.
