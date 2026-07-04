# MCD Lens: NETW (Network Communication) Indicators

> **Core MCD position:** Network communication is the primary channel through which stolen data leaves a system, secondary payloads arrive, and command-and-control instructions are received. In libraries and packages that do not have documented network functionality, any network communication is a significant finding.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `NETW.HTTP` | Context-dependent | Severity depends heavily on what is sent, where, and when in the lifecycle |
| `NETW.DNS` | Medium | Programmatic DNS (non-system resolver, data in queries) is unusual in most packages |
| `NETW.SOCKET` | Medium-High | Raw socket operations in library/package code are uncommon |
| `NETW.LISTEN` | High | A listening port in dependency code is a strong finding in most contexts |
| `NETW.IPC` | Low-Medium | Local IPC is common in plugin/orchestration architectures |
| `NETW.EMAIL` | Medium-High | Programmatic email in a non-email package is unusual |
| `NETW.FTP` | Medium | FTP in a non-file-transfer package is unusual |
| `NETW.WEBHOOK` | Medium-High | Webhook integration in packages that don't document messaging features is notable |
| `NETW.WS` | Medium-High | Persistent bidirectional connections in dependency/library code are unexpected |
| `NETW.GRPC` | Context-dependent | Severity depends on whether the package documents microservice functionality |
| `NETW.BROKER` | Context-dependent | Severity depends on whether the package documents messaging/event functionality |
| `NETW.SSE` | Medium | Persistent streaming connections in dependency code are notable |
| `NETW.DECENTRAL` | High | Decentralized network communication in non-blockchain packages is rare and high-severity |

## Escalation Factors

- **The package has no documented network functionality.** Any network communication in a utility, parser, formatter, or data-processing library is anomalous by definition. The package's stated purpose is the primary context for severity.
- **The destination is not recognized infrastructure.** The target is a personal domain, recently registered domain, dynamic DNS hostname (`*.duckdns.org`, `*.ngrok.io`), residential IP block, or bulletproof hosting provider. Contrast with legitimate telemetry contacting known vendor infrastructure.
- **The destination mimics a trusted service.** Typosquatted hostnames, attacker-controlled subdomains, and URL paths echoing legitimate API patterns (e.g., the Axios compromise used endpoints styled to resemble npm registry traffic).
- **Data sent includes secrets, credentials, or environment variables.** Any combination of `NETW.*` with `CRED.*`, environment variable reads, or filesystem reads of known secret locations is a strong escalation.
- **Communication is triggered at install, import, or startup, not at explicit runtime use.** Network calls in package lifecycle hooks (`postinstall`, `__init__.py` module-level, static initializers) execute before the user invokes any functionality. Very limited legitimate justification for install-time network calls.
- **Traffic is encoded, encrypted with a hardcoded key, or uses non-standard framing.** Base64-encoded POST bodies, custom binary framing over raw sockets, or DNS queries encoding data in subdomains indicate deliberate concealment of payload content.
- **A decentralized or censorship-resistant channel is used.** `NETW.DECENTRAL` in a standard software library or package has no common legitimate use case. These channels cannot be blocked by conventional network controls.
- **Communication occurs on non-standard ports or uses protocol mismatches.** HTTP traffic on unusual ports, DNS over non-standard resolvers, SMTP from code with no mail functionality.
- **A listener binds to `0.0.0.0` or an externally routable interface.** `NETW.LISTEN` on an external interface in a library is substantially more severe than a localhost listener.
- **The channel is persistent or polling.** WebSocket connections, SSE streams, or HTTP long-poll loops that remain open after the triggering operation suggest waiting for inbound data, continuous reception rather than one-time communication.

## De-escalation Factors

- **The destination is documented vendor telemetry infrastructure with a known opt-out mechanism.** Crash reporters, update checkers, and analytics endpoints contacting named vendor infrastructure (Sentry, documented telemetry domains) are routine. They still warrant disclosure review but are not malware indicators.
- **Communication occurs only when the user explicitly invokes a network-facing feature.** An HTTP client library calling out when `client.get()` is invoked is expected behavior. The call must be causally downstream of explicit user action, not of import or initialization.
- **The payload is fully observable, documented, and does not include system data.** A health-check ping sending a static version string with no host identifiers, credentials, or environment context is low risk. If you cannot easily read the payload, you cannot de-escalate.
- **IPC channel is local-only and part of a documented plugin or service architecture.** `NETW.IPC` over a Unix domain socket in a process orchestrator that documents its IPC interface is expected. Confirm the socket path is non-guessable and no external network interface is involved.
- **Traffic pattern matches the package's stated purpose exactly.** An API client package making `NETW.HTTP` calls to the API it wraps, using user-supplied credentials passed at call time, is doing exactly what it should. The destination, payload, and trigger must all be consistent with the documented interface.

> **Caveat:** De-escalation based on documented purpose applies only when the network behavior is fully consistent with that purpose. A legitimate HTTP client that also makes undocumented calls to an unrelated endpoint is not de-escalated by the presence of legitimate calls.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `NETW.HTTP` + `CRED.*` | Credential exfiltration via HTTP, canonical supply chain theft pattern | Very High |
| `NETW.WEBHOOK` + `CRED.*` | Credentials posted to messaging platform, attacker owns receiving infrastructure with no personal hosting | Very High |
| `NETW.HTTP` + `XFRM.*` | Concealed HTTP communication, encoded POST bodies, dynamic URL construction | High |
| `NETW.DNS` + `XFRM.*` | DNS tunneling, data encoded into query subdomains or TXT payloads | High |
| `NETW.SOCKET` + `EXEC.*` | Reverse shell, raw socket with I/O redirected to shell | Very High |
| `NETW.LISTEN` + `EXEC.*` | Bind shell / backdoor, port listener that spawns a shell on connection | Very High |
| `NETW.DECENTRAL` + `EXEC.*` | Uncensorable C2, commands retrieved from blockchain/ICP/IPFS and executed | Very High |
| `NETW.WS` + `EXEC.*` | WebSocket C2, persistent bidirectional channel for command execution | Very High |
| `NETW.*` + `PKGM.INSTALL` | Network call during package installation, almost never legitimate | Very High |
| `NETW.*` + `PRST.*` | Network channel + persistence, durable communication channel survives reboot | Very High |
| `NETW.*` + `XFRM.*` + `CRED.*` | Full exfiltration kill chain, collection, concealment, transmission | Very High |
| `NETW.LISTEN` + `FSYS.*` | File server, listener serves filesystem contents on demand | High |
| `NETW.EMAIL` + `CRED.*` | Credential exfiltration via email, SMTP exfiltration | High |
| `NETW.BROKER` + `EXEC.*` | Pub-sub C2, commands received via message broker topic and executed | High |

## MCD-Specific Disambiguation

### NETW.LISTEN: Localhost vs. External Interface
Through the MCD lens, the bind address is the primary severity discriminator. Localhost listeners in development tools, local proxies, and plugin hosts have plausible non-malicious purpose. Listeners on `0.0.0.0` or external interfaces in a library package are core backdoor indicators.

### NETW.HTTP destination mimicry
The Axios compromise used endpoints styled to resemble npm registry traffic (`packages.npm.org/` prefix). Through the MCD lens, traffic patterns that deliberately mimic trusted services are a strong escalation signal: the attacker is attempting to make malicious traffic blend into expected network behavior.

### NETW.DECENTRAL takedown resistance
Through the MCD lens, the defining concern with decentralized channels is that conventional incident response (domain takedown, IP blocking, hosting provider reports) does not work. ICP canisters, IPFS content, and blockchain data persist as long as the network operates. This makes `NETW.DECENTRAL` uniquely high-severity for MCD because the response playbook is fundamentally different.
