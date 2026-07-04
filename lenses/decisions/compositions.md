# Decisions Lens: Compositions

Named decision patterns built from multiple observations. Each is a *decision*, not a verdict: it describes what the code commits to, with explicit disproof criteria. IDs use the `DC-` (decision composition) prefix to distinguish them from MCD's `BP-` patterns.

## DC-TRUST-EXEC: Unverified input drives execution

**Shape:** `NETW.*` (or `LOAD.DESER`, or `XFRM.ENCODE` of external bytes) → reaches → `LOAD.EVAL` / `EXEC.*` / `LOAD.IMPORT`, with **no** `CRPT.SIGN`/`CRPT.HASH` in the path.

**Decision:** "I will run whatever this external source gives me." The program has placed a trust decision and a dispatch decision back-to-back, and skipped the verification decision between them.

**Consequence:** High (code execution from untrusted input).

**Disproof:** the executed content is verified before use; the external source is closed/pinned; the "execution" is actually inert parsing.

**Verification:** `static-source` traces the value from its external origin to the exec/eval sink; `dynamic` observes what is actually delivered and run.

## DC-TRUSTED-FETCH: Remote artifact trusted by default

**Shape:** `NETW.HTTP`/`PKGM.BINDOWN` → `FSYS.WRITE` (and/or later use), no `CRPT.*` verification in scope.

**Decision:** "Whatever the network returns is safe to persist/use." Trust-by-omission.

**Consequence:** Medium–High (depends on what the artifact later feeds).

**Disproof:** integrity verified upstream (signed manifest, pinned hash, TLS pinning + trusted origin); artifact is inert data.

**Verification:** `static-source` asks whether there is any signature/hash check; `build-ci` asks whether the artifact is reproducible from pinned inputs.

## DC-GATED-DIVERGENCE: Behavior decided by environment or time

**Shape:** (`ENVI.ENVCHECK` | `TIME.CMP`) gating a branch whose divergent path contains `EXEC.*` / `NETW.*` / `LOAD.*` (the *environment-gated* / *timed conditional execution* idioms).

**Decision:** "I decide *whether* to act based on where/when I run." The gate itself is the decision; the hidden path is the consequence.

**Consequence:** Medium–High (dormant or sandbox-evasive behavior).

**Disproof:** the gate is a documented feature flag / cache TTL / scheduler; both paths are benign and disclosed.

**Verification:** `dynamic` runs under the gated and ungated conditions and diffs behavior; `static-source` reads both branches.

## DC-ELEVATED-SINK: Authority granted over a dangerous sink

**Shape:** `PRIV.SUDO`/`PRIV.SUID`/`PRIV.CAP` wrapping `EXEC.*` / `FSYS.WRITE` / `FSYS.PERM`, especially with input-derived arguments.

**Decision:** "I decide to run this powerful operation with elevated authority." 

**Consequence:** High (privileged side effects).

**Disproof:** elevation is narrowly scoped, audited, and drops immediately; arguments are fully static.

**Verification:** `static-source` traces what flows into the elevated operation, and from where.

---

### Notes on use

- Compositions require **reachability**, not co-location. An engine without dataflow uses same-file/same-scope as a weak proxy and must lower confidence accordingly (and say so). Stronger reachability (dataflow) is an engine upgrade, not a lens change.
- A single flow can match several compositions (e.g., DC-TRUSTED-FETCH + DC-TRUST-EXEC). That is expected: they describe different decisions in the same chain.
- These compositions are intentionally lens-neutral about *intent*. The MCD lens may read the same chain as `BP-DROPPER`; the decisions lens reads it as "trust + dispatch without verification." Same observations, different question.
