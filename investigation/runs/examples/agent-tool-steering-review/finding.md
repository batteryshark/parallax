# Agent Tool Steering Review

This worked example uses a tiny synthetic MCP-style docs helper. The fixture is
not real malware; it exists to show how Parallax keeps observation, malicious
code judgment, and agent-risk judgment separate.

The source fixture is [`artifacts/source/docs-helper-mcp/`](artifacts/source/docs-helper-mcp/).
It exposes a docs search tool, a URL fetcher, and a shell runner. Its MCP tool
schema also contains an instruction-override string in the `search_docs`
description.

## Observed Atoms

| Atom | Source | Why it matters |
|---|---|---|
| `AITM.TOOL` | `mcp.json` | The component defines an AI/MCP tool surface. |
| `AITM.INJECT` | `mcp.json` | A tool description contains instruction-override and deception text. |
| `EXEC.PROC` | `server.py` | The implementation can spawn a child process. |
| `NETW.HTTP` | `server.py` | The implementation can fetch remote URLs. |

## Lens Readings

`prlx-mcd` reports one high-severity `BP-AGENTMANIP` finding and recommends
`review`, not `quarantine`. The important bit is the attenuator: agent steering
and payload capability are co-located, but static analysis has not proven that
an agent can route the injected description into the shell-capable tool.

`prlx-agent-risk` gives a stronger operational recommendation. From an
agent-enablement view, the single target is both steerable and capability
bearing. It completes the `RCE` composition by itself (`NET` plus `EXEC`), so
the right response is to gate or sandbox it before enabling it for an agent.

`prlx-understand` frames the same source as comprehension work: start with the
remote-execution-capable surface, then verify approval boundaries and who can
influence the command argument.

## What Would Change The Assessment

- The MCD finding would weaken if no agent ingests the tool description as an
  instruction source.
- It would also weaken if `run_shell` is unreachable from agent-controlled
  routes, always requires human approval, or runs in a tight sandbox.
- It would strengthen if a dynamic harness shows the injected description
  changes tool calls or causes `run_shell` to execute.
