# SYSI.NET: Network Configuration Query

## Description

Queries network interface configuration, IP addresses, routing tables, ARP caches, DNS configuration, or performs network topology discovery. APIs and mechanisms include `ifconfig` / `ipconfig` (interface listing), `getifaddrs()` (POSIX), `socket.gethostbyname()`, `socket.getaddrinfo()` (Python), `os.networkInterfaces()` (Node.js), `netstat` / `ss` (connection and route listing), `arp` / `arp -a` (ARP cache), `nslookup` / `dig` (DNS queries), `GetAdaptersInfo` / `GetAdaptersAddresses` (Windows API), `WMI Win32_NetworkAdapterConfiguration` queries, `/etc/resolv.conf` reads, and network scanning via port probes or ICMP. The code inspects network configuration state. It does not establish communication channels (which would be `NETW.*`).

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `ifconfig`/`ipconfig` subprocess calls, `socket.gethostbyname()`, `os.networkInterfaces()`, `getifaddrs()`, `netstat`/`ss` invocations, ARP table reads, `/etc/resolv.conf` reads, port scanning loops |
| Static Binary | Yes | Network enumeration API imports, interface listing command strings, IP address regex patterns, port range constants |
| Runtime/Dynamic | Yes | System calls for interface enumeration, subprocess execution of network commands, DNS resolution calls, sequential connection attempts to port ranges |

## Disambiguation

- **vs NETW.\***: `SYSI.NET` inspects network configuration state, what interfaces exist, what addresses are assigned, what routes are configured, what hosts are reachable. `NETW.*` atoms describe active network communication, establishing connections, sending data, receiving responses. Running `ipconfig` to list interfaces is `SYSI.NET`. Opening a TCP socket to send data to a remote host is `NETW.SOCKET`. Port scanning occupies a boundary: the probes are active network connections (`NETW.SOCKET`) used for the purpose of network topology discovery (`SYSI.NET`), both apply.
- **vs SYSI.HW**: MAC addresses can appear in both contexts. `SYSI.NET` queries network interface configuration including MAC addresses as part of network state. `SYSI.HW` queries MAC addresses as hardware identifiers for fingerprinting. When MAC addresses are collected alongside IP/routing information, `SYSI.NET` applies. When collected alongside serial numbers and CPU IDs for machine identification, `SYSI.HW` applies. Both may apply simultaneously.

## Structural Relationships

- **Often co-occurs with**: `NETW.*` (network state informs subsequent communication), `SYSI.OS` (combined system profiling), `SYSI.HW` (MAC addresses as hardware identifiers), other `SYSI.*` subtypes (aggregated system profile)
- **May imply**: The code needs to understand the network environment it operates in, for configuration, diagnostics, or reconnaissance

## Notes

Network configuration queries range from narrow (resolving the local hostname) to broad (full interface enumeration, ARP cache dumps, port scanning). The breadth of the query and the destination of collected data are the primary structural observations. Network scanning, systematically probing ports or hosts, is mechanically a series of connection attempts but functionally serves a discovery purpose, so both `SYSI.NET` and `NETW.SOCKET` apply.
