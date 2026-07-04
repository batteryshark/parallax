# Network Analysis

Observation of actual network traffic produced by or directed at the software during execution.

## Capabilities

- **Actual destinations:** Where the code connects: resolved IPs, hostnames, ports, protocols
- **Protocol behavior:** HTTP methods, headers, TLS versions, DNS queries, custom protocols
- **Payload contents:** Request/response bodies, transmitted data, downloaded content (when not encrypted end-to-end)
- **Traffic patterns:** Connection frequency, data volume, timing patterns, beaconing behavior
- **DNS behavior:** Queries made, TTL values, NXDOMAIN responses, DNS-over-HTTPS usage, domain generation algorithm (DGA) patterns
- **TLS metadata:** Certificate chains, SNI values, cipher suites, certificate pinning behavior (even when payload is encrypted)
- **Lateral movement indicators:** Internal network scanning, connections to unexpected internal hosts, port sweeps

## Blind Spots

- **Code logic:** Cannot see why a connection is made, only that it was
- **Dormant capabilities:** Network code that doesn't execute during observation produces no traffic
- **Encrypted payloads:** End-to-end encrypted content (TLS, custom encryption) is opaque without key material or TLS interception
- **Timing-dependent behavior:** C2 with long sleep intervals, time-bombed beaconing, or trigger-based activation may not generate traffic during the observation window
- **Local-only behavior:** Filesystem operations, credential access, process manipulation: anything that doesn't touch the network

## Tools

Packet capture (tcpdump, Wireshark, tshark), network proxies (mitmproxy, Burp Suite), DNS logging, NetFlow/sFlow analysis, IDS/IPS (Suricata, Snort), sandbox network analysis modules, SSL/TLS interception proxies.

## When to Use

- **Destination verification:** When static analysis identifies network atoms (`NETW.*`) and you need to confirm actual traffic matches predicted behavior
- **Exfiltration detection:** When the investigation hypothesis involves data leaving the system, network analysis confirms or denies the channel
- **C2 identification:** When backdoor or remote access patterns are suspected, network analysis reveals beaconing, command polling, or interactive sessions
- **Traffic baselining:** Establishing what network behavior is normal for a package to detect deviation

## When to Transition Away

- **Unknown destinations identified:** When traffic goes to unexpected hosts → transition to **OSINT** (domain/IP reputation, registration history)
- **Encrypted traffic:** When payload inspection is needed but traffic is encrypted → transition to **environment scaffolding** (deploy TLS interception) + **dynamic analysis**
- **Code-level questions:** When traffic analysis reveals unexpected behavior and you need to understand why → transition to **static source/binary analysis**
- **Anti-analysis detected:** When traffic volume or patterns change based on analysis environment → transition to **environment scaffolding** (less detectable environment)

## Relationship to Dynamic Analysis

Network analysis and dynamic analysis are complementary and often co-deployed. Dynamic analysis observes behavior from inside the process (system calls, API calls, memory). Network analysis observes behavior from outside the process (traffic on the wire). Together they provide both the intent (code-level) and the effect (network-level) of network operations.

## Atom Categories Most Visible

NETW (all subtypes; this is the primary method for confirming network behavior), ARTF (destinations observed in traffic), CRED (credential material in payloads, when unencrypted)

## Atom Categories Least Visible

XFRM (transformation happens before traffic is generated), LOAD (code loading is process-internal), PRST (persistence is filesystem/registry), SYSI (system queries are local), ENVI (environment checks are local)
