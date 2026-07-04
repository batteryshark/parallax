# Decisions Lens

> **Core question:** *Where does this system decide who to trust, what to run, and whether to elevate, and how consequential is each of those decisions?*

Most code tooling views software as **lines** (style), **defects** (bugs), or **reachability** (control-flow graphs). The decisions lens views it as a set of **consequential decision points**: the places where the program commits to trusting an input, executing a payload, granting authority, or diverging its behavior based on a condition. Those points, not lines and not bugs, are where systems become dangerous, and they are exactly the surface an attacker (or a confused agent) steers.

This is the lens behind the project thesis: *view code as affordances and decisions, not lines and bugs.*

## What the decisions lens is (and is not)

- It is **interpretive**, like every lens. It assigns meaning to observations; it adds no new ontology. A decision point is recognized by **re-reading atoms and idioms the ontology already defines**.
- It is **not** a control-flow graph. A CFG tells you *which branches exist and what is reachable*. The decisions lens tells you *which branches are consequential and why*: a branch gated on an environment variable that changes whether a payload runs is a decision; a branch that picks a log format is not.
- It is **not** SAST. SAST asks "is this a vulnerability?" The decisions lens asks "where is the program placing trust, and on what?" A decision can be perfectly correct and still be the most important thing in the file to understand.

## The four decision categories

| Category | The decision being made | Recognized from (ontology) |
|---|---|---|
| **Trust** | "Do I treat this input/artifact as safe?" (verify a signature/cert or not; validate or deserialize untrusted data) | `CRPT.SIGN` / `CRPT.CERT` present *or absent*; `LOAD.DESER`; remote `NETW.*` whose result is used without an integrity check |
| **Authority** | "Under whose privileges / with what power does this run?" (elevate, drop, assume a role) | `PRIV.SUDO`, `PRIV.SUID`, `PRIV.CAP`, `PRIV.TOKEN`, `PRIV.ACCOUNT` |
| **Dispatch** | "What code do I run?" (let a runtime value choose the executed/loaded code) | `LOAD.EVAL`, dynamic `LOAD.IMPORT`, `EXEC.*` with a constructed command, `LOAD.CODEGEN` |
| **Environment gate** | "Do I behave differently *here* / *now*?" (diverge on environment, time, or config) | `ENVI.ENVCHECK`, `TIME.CMP`; branches that diverge on environment or time |

A decision point is most interesting when the **input to the decision is more tainted than the consequence assumes**, e.g., a dispatch decision (`LOAD.EVAL`) whose value is reachable from the network, or a trust decision that simply never happens (no signature check before executing fetched code).

## What makes a decision *consequential*

The lens ranks by **consequence × tainted-reachability of the decision's input**, not by severity-of-malice:

- **Consequence**: what the decision commits to: code execution > privilege change > data trust > behavioral divergence.
- **Input reachability**: can untrusted/external data reach the value the decision turns on? A decision on a compile-time constant is incidental; the same decision on attacker-influenced input is a trust boundary.
- **Absence as evidence**: a *missing* trust decision (no verification where verification was due) is itself a decision: the program decided to trust by default. The lens surfaces omissions, not just present checks.

## Why this matters for agents (and AI-generated code)

An agent's danger is `affordances × manipulability`. The decisions lens maps the **manipulability half**: every dispatch and trust decision is a place an agent can be *steered*, whether a tool whose arguments choose what executes, a fetch whose result is trusted, or an instruction surface that decides the next action. When you cannot be sure who wrote the code (model-generated, vibe-coded, agent-authored), the decision points are what you must understand to trust it. See the [capability lens](../capability/) for the affordance half and the agentic-risk profile for the composition.

## Components

- [indicators.md](indicators.md): how each atom/idiom is read as a decision point, and what raises/lowers its consequence.
- [compositions.md](compositions.md): named multi-observation decision patterns (e.g., *unverified-input drives execution*).

## Output

For each decision point the lens emits a finding with: the decision category, the claim (what is being trusted/run/elevated), severity (consequence) and confidence (separately), the evidence observations, **what would disprove it** (e.g., "the input is a closed allowlist"), and a verification step naming the method that would settle it. The aggregate is a **decision map**: where the system's trust boundaries actually are.
