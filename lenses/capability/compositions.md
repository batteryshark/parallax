# Capability Lens: Compositions

Named blast-radius profiles built from capability surfaces. Where individual surfaces describe *reach*, compositions describe *multiplied reach*: the combinations where one capability makes another far more dangerous. IDs use the `CR-` (capability radius) prefix.

These are interpretive, like all lens content: a `CR-*` match is a statement about what the component *could* do if abused, not a claim that it *is* doing it. The MCD lens may read the same surfaces as `BP-DROPPER`; the capability lens reads them as "remote-execution-capable."

## CR-EXFIL: Exfiltration-capable

**Shape:** (`CAP-CRED` or `CAP-FS-READ`) + `CAP-NET`.

**Blast radius:** can collect sensitive data (secrets, files) and send it off-host. The collection+egress pair is the core of any data-theft chain.

**Reduced by:** network egress allowlist; credentials scoped to their own service; reads confined to needed paths; payloads observable.

## CR-RCE: Remote-execution-capable

**Shape:** `CAP-NET` + (`CAP-EXEC` or `CAP-DYNLOAD`).

**Blast radius:** network-reachable input can influence what code runs, the structural precondition for remote code execution. Highest-reach composition.

**Reduced by:** verified/pinned inputs; no untrusted data reaching exec/load sinks; sandboxed execution.

## CR-SELFMOD: Self-modifying-capable

**Shape:** `CAP-FS-WRITE` + (`CAP-EXEC` or `CAP-DYNLOAD`).

**Blast radius:** can write files and execute/load code, able to rewrite what it later runs, defeating point-in-time review and enabling staged payloads.

**Reduced by:** write paths disjoint from executable/loadable paths; read-only runtime filesystem.

## CR-INSTALL-AUTH: Install-time authority

**Shape:** `CAP-INSTALL` + any active surface (`CAP-EXEC` / `CAP-NET` / `CAP-DYNLOAD` / `CAP-FS-WRITE`).

**Blast radius:** capabilities run **unsupervised at install time**, before the developer invokes anything and often inside CI with credentials present.

**Reduced by:** `--ignore-scripts`; documented, reproducible, network-free install steps.

## CR-AGENT-RISK: Agentic blast radius (preview)

**Shape:** `CAP-AGENT` + any high-reach surface (`CAP-EXEC` / `CAP-NET` / `CAP-CRED` / `CAP-DYNLOAD`).

**Blast radius:** an agent-directed-content surface sits next to real capability. That is, something that can *steer an agent* is co-located with something that *acts*. This is the seed of the agentic-risk profile (capability × manipulability); the full profile composes this with the [decisions lens](../decisions/).

**Reduced by:** isolating agent-ingested content from capability; human approval between agent decision and action.

## CR-PROFILE: Component capability profile

Not a single pattern but the **roll-up** the engine emits per scan: the set of surfaces present, the overall blast-radius label (the max surface reach, escalated to *critical* when two or more dangerous compositions co-occur), and the list of matched `CR-*` combinations. This is the one-line answer to "how dangerous is this component if it turns on me?"

---

### Notes

- Composite reach assumes the surfaces are mutually reachable. An engine that aggregates per component without proving inter-surface dataflow must bound confidence accordingly and state that in the finding.
- Compositions are about *potential*, so they are deliberately generous: the capability lens would rather over-name reach (and let bounding factors talk you down) than under-name it. This is the opposite bias from MCD, which must avoid over-claiming malice.
