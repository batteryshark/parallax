# Curiosity Lens: Indicators

Curiosity scores each observation for **interestingness**, then ranks. Interestingness is independent of severity and of confidence.

## Interestingness score

```
score = atom_rarity (1–5)  +  2 if the behavior is unexpected for the stated purpose
```

- **Unexpected** = the observation's capability category is *not* implied by the project's stated purpose.
- Filters that keep it quiet: an *expected* behavior that is also low-rarity is dropped (a network call in an API client is not interesting). When no stated purpose can be read, only rare atoms (rarity ≥ 4) are surfaced.

Label by score: **striking ≥ 6 · notable ≥ 4 · mild ≥ 3.**

## Atom rarity (how inherently "huh" a behavior is in dependency code)

| Rarity | Atoms | Why |
|---|---|---|
| 5 | `NETW.DECENTRAL` | blockchain/IPFS/ICP comms in normal software is almost never expected |
| 4 | `EXEC.*`, `LOAD.EVAL`, `LOAD.DESER`, `CRED.*`, `PKGM.INSTALL`, `PRST.*`, `PRIV.*`, `AITM.*` | execution, secret access, install-time code, persistence, privilege, agent-directed content |
| 3 | `NETW.*`, `LOAD.*`, `FSYS.DELETE` | network reach, dynamic loading, file deletion |
| 2 | `XFRM.ENCODE`, `FSYS.WRITE` | encoding, file writes; common, mildly notable in the wrong place |
| (skip) | `FSYS.READ`, `ARTF.*`, `RSRC.*` | too common to be interesting on their own |

## Purpose inference (what a stated purpose implies)

Keywords in the manifest/README map to expected capability categories. If a keyword is present, that category's behaviors are *expected* (and lose the inconsistency bonus):

| Category | Trigger keywords (substring match, lowercased) |
|---|---|
| network | client, api, http, fetch, request, download, server, webhook, sdk, scrape, crawl, url, rest, graphql, proxy, telemetry, analytics |
| exec | cli, shell, exec, build, compile, run, task, spawn, devtool, lint, transpile |
| fs | file, filesystem, read, write, parse, loader, bundle, watch, format, config, template |
| dynload | plugin, loader, dynamic, extension |
| install | native, binding, gyp, prebuilt, addon, postinstall |
| agent | mcp, agent, llm, assistant, tool, prompt |
| cred | auth, login, credential, token, secret, oauth, vault |
| persist | daemon, service, startup, scheduler, cron |
| encode | encode, base64, compress, serialize |

## Worked examples

- **"tiny string padding helper"** → purpose implies *nothing*. `EXEC.SHELL` (rarity 4 + unexpected 2 = **6, striking**), `NETW.HTTP` (3 + 2 = **5, notable**), `PKGM.INSTALL` (4 + 2 = **6, striking**). → "wait, it does THAT?"
- **"thin client for the exchangerate API"** → purpose implies *network*. `NETW.HTTP` (3, expected, < 4) → **dropped.** The lens stays quiet on legitimately network-shaped software.
- **"docs-search MCP server"** → purpose implies *network + agent*. `EXEC.PROC` (4 + unexpected 2 = **6, striking**; a docs search has no business running shell commands), `AITM.*` (4, expected) → notable.

## Cross-cutting

- **Interestingness is a router, not a verdict.** Striking findings should be escalated to MCD (malice) or capability (blast radius). The curiosity lens never claims something is bad.
- **The inconsistency bonus is the heart of it.** Rarity alone is generic; "rare *for what this claims to be*" is what produces genuine surprise, and what a purpose-blind scanner can't say.
