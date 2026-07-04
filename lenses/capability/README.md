# Capability Lens

> **Core question:** *What can this do, and what is the blast radius if it is abused, compromised, misconfigured, or manipulated?*

The capability lens is the **affordance map**. It does not ask whether code is malicious (that is the [MCD lens](../mcd/)) or whether it is correct (that is the architecture lens). It asks what the system, dependency, automation, or agent toolchain *can do* (its reach) and how much damage that reach represents if it is turned against you.

This is the lens that makes Parallax useful **even when nothing is malicious.** A benign HTTP client is still network-capable; a build tool is still execution-capable. Capability is a property of the code, independent of intent. Naming it is what lets a human or an agent decide whether the reach is acceptable *here*.

## Blast radius = reach × (1 − bounding)

A capability's severity is its **reach** (what it can touch) discounted by its **bounding** (what constrains it):

- **Reach**: the raw power of the surface. Code/command execution and credential access have the highest reach; filesystem reads and resource use have the lowest.
- **Bounding**: what limits the reach in practice: invoked only on explicit user action, fixed/documented destinations, sandboxing, dropped privileges, egress allowlists, least-privilege tokens. Most bounding is hard to prove statically, so an engine that cannot prove it should list bounding factors as *attenuators* ("this is reduced if…") rather than asserting them.

Severity here is **blast radius, not malice**, and it is reported separately from **confidence** (how sure we are the capability exists at all). "Certainly network-capable" (high confidence) says nothing about whether that network reach is dangerous *here* (blast radius).

## Capability surfaces

The engine emits one `CAP-*` finding per surface present (the map), aggregated across the component:

| Surface (`CAP-*`) | Supporting atoms | Reach |
|---|---|---|
| `CAP-EXEC`: command / process execution | `EXEC.*` | high |
| `CAP-DYNLOAD`: dynamic code loading | `LOAD.*` | high |
| `CAP-CRED`: credential access | `CRED.*` | high |
| `CAP-PRIV`: privilege operations | `PRIV.*` | high |
| `CAP-PERSIST`: persistence | `PRST.*` | high |
| `CAP-NET`: outbound network reach | `NETW.*` | medium |
| `CAP-FS-WRITE`: filesystem mutation | `FSYS.WRITE`, `FSYS.DELETE` | medium |
| `CAP-INSTALL`: unsupervised install-time execution | `PKGM.INSTALL`, `PKGM.HOOK` | medium |
| `CAP-AGENT`: agent-directed content surface | `AITM.*` | medium |
| `CAP-FS-READ`: filesystem read / enumeration | `FSYS.READ`, `FSYS.ENUM`, `FSYS.SENSITIVE` | low |
| `CAP-RSRC`: resource consumption | `RSRC.*` | low |

See [indicators.md](indicators.md) for each surface's reach, amplifiers, and bounding factors.

## Composite blast radius

Individual surfaces compound. A `CR-PROFILE` finding rolls them up and flags the dangerous combinations, the places where reach multiplies:

- **Exfiltration-capable**: collection (`CAP-CRED`/`CAP-FS-READ`) + `CAP-NET`
- **Remote-execution-capable**: `CAP-NET` + (`CAP-EXEC`/`CAP-DYNLOAD`)
- **Self-modifying-capable**: `CAP-FS-WRITE` + (`CAP-EXEC`/`CAP-DYNLOAD`)
- **Install-time authority**: `CAP-INSTALL` + any active surface

See [compositions.md](compositions.md) for the full `CR-*` set.

## Why this matters for agents

An agent's danger is `affordances × manipulability`. The capability lens maps the **affordances half**: what the tool/agent/automation can reach. The [decisions lens](../decisions/) maps the **manipulability half**: where it can be steered. Composed, they answer the frontier question: *"what can this agent be tricked into doing?"* (the agentic-risk profile). For AI-generated / vibe-coded code you didn't write, the capability map is the first thing you need: it tells you the worst case before you decide whether to trust it.

## Output

- Per-surface `CAP-*` findings (severity = reach, confidence = certainty), each with bounding factors and **least-capability guardrails**.
- A `CR-PROFILE` summary: surfaces present, composite blast-radius label, and the dangerous combinations.
- A human **capability matrix** in the Markdown report; the full machine map in JSON.

## Mitigation philosophy: least capability

Capability findings prefer concrete blast-radius reduction over "fix the bug": remove unused surfaces, move risky behavior behind explicit approval, sandbox execution, restrict network destinations, scope credentials to least privilege, allowlist dynamic loading, add provenance to downloaded artifacts, separate build/release/runtime identities, monitor the surfaces you keep.
