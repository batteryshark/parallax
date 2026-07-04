# Capability Lens: Indicators

How each ontology atom is read as a capability surface. **Reach** is the lens's severity axis (blast radius), reported separately from confidence. **Amplifiers** increase blast radius; **bounding factors** reduce it (and are what verification should look for).

## High-reach surfaces

### `CAP-EXEC`: command / process execution (`EXEC.*`)
Reach: can run shell commands or spawn processes, the maximal blast-radius primitive.
- **Amplifiers:** command string built from input (`XFRM.STRCON`); runs at install time; elevated privilege (`PRIV.*`).
- **Bounding:** fixed argv with no shell; no untrusted input reaches the arguments; sandboxed; capability dropped after use.
- **Guardrails:** sandbox; remove process-spawn ability; allowlist permitted commands.

### `CAP-DYNLOAD`: dynamic code loading (`LOAD.*`)
Reach: can load and run code chosen at runtime (`eval`, dynamic import, deserialization, codegen, reflection, native/WASM load).
- **Amplifiers:** the loaded value is reachable from network/user/env; decoded from `XFRM.ENCODE` before loading.
- **Bounding:** value is a compile-time constant or closed allowlist; safe deserializers only.
- **Guardrails:** disable eval / dynamic import; pin loadable modules.

### `CAP-CRED`: credential access (`CRED.*`)
Reach: can read credential or secret material (keychain, browser, cloud, SSH, env, tokens, certs).
- **Amplifiers:** co-located with `CAP-NET` (collection + egress); reads beyond what the component needs.
- **Bounding:** credential is user-supplied at call time and used only against its own service.
- **Guardrails:** least-privilege/short-lived tokens; rotate; avoid env-var secrets.

### `CAP-PRIV`: privilege operations (`PRIV.*`)
Reach: can request, assume, or exploit elevated privilege.
- **Amplifiers:** elevation wraps `CAP-EXEC`/`CAP-FS-WRITE`; broad or long-lived grant.
- **Bounding:** narrow, audited, dropped immediately.
- **Guardrails:** drop privileges; run with least authority.

### `CAP-PERSIST`: persistence (`PRST.*`)
Reach: can survive process exit, reboot, or session boundaries (startup, service, scheduler, hook, extension, boot).
- **Amplifiers:** combined with `CAP-EXEC`/`CAP-NET` (a durable foothold).
- **Bounding:** documented, user-visible autostart with an uninstall path.
- **Guardrails:** remove persistence hooks; monitor autostart locations.

## Medium-reach surfaces

### `CAP-NET`: outbound network reach (`NETW.*`)
Reach: can send and receive data over the network.
- **Amplifiers:** non-fixed/recently-registered destination; triggered at install/import; persistent/polling channel.
- **Bounding:** fixed, documented destination; downstream of explicit user action; payload observable and free of host/secret data.
- **Guardrails:** egress allowlist; pin destinations; block network at install time.

### `CAP-FS-WRITE`: filesystem mutation (`FSYS.WRITE`, `FSYS.DELETE`)
Reach: can create, modify, or delete files.
- **Amplifiers:** writes to executable/loadable paths (feeds self-modification); path derived from input.
- **Bounding:** confined to a temp/scoped directory; fixed paths.
- **Guardrails:** restrict writable paths; read-only filesystem where possible.

### `CAP-INSTALL`: unsupervised install-time execution (`PKGM.INSTALL`, `PKGM.HOOK`)
Reach: executes code at install time, before any explicit use, an unsupervised window in which other capabilities run.
- **Amplifiers:** the hook reaches `CAP-EXEC`/`CAP-NET`/`CAP-DYNLOAD`.
- **Bounding:** documented, reproducible build step; no network/exec.
- **Guardrails:** install with `--ignore-scripts`; review and vendor the dependency.

### `CAP-AGENT`: agent-directed content surface (`AITM.*`)
Reach: can shape what an AI agent reads, believes, or does (injected instructions, tool-description content, invisible unicode).
- **Amplifiers:** content is in a place an agent ingests by default (README, tool description, config).
- **Bounding:** content is inert documentation never fed to a model.
- **Guardrails:** treat as untrusted agent input; strip/sanitize agent-directed content.

## Low-reach surfaces

### `CAP-FS-READ`: filesystem read / enumeration (`FSYS.READ`, `FSYS.ENUM`, `FSYS.SENSITIVE`)
Reach: can read or enumerate files. Low alone; an amplifier for `CAP-NET` (exfiltration).
- **Guardrails:** restrict readable paths to needed directories.

### `CAP-RSRC`: resource consumption (`RSRC.*`)
Reach: can consume CPU, memory, disk, GPU, or network capacity.
- **Guardrails:** apply resource limits / cgroups.

## Cross-cutting

- **Reachability bounds blast radius.** A surface in dead/unreachable code has near-zero blast radius. An engine that cannot prove reachability should flag this as a disproof criterion instead.
- **Surfaces compound.** The dangerous combinations are in [compositions.md](compositions.md); a lone surface is rarely the story.
- **Reach ≠ confidence.** Report the power of the surface and the certainty it exists as two separate numbers, always.
