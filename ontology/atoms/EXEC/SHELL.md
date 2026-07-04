# EXEC.SHELL: Shell Command Execution

## Description

Invokes a system shell interpreter (bash, sh, zsh, cmd.exe, powershell.exe) to execute a command string. The shell interprets the command (performing variable expansion, glob expansion, pipe construction, redirection, and other shell features) before executing the resulting operations. The command string is the input; the shell parses and executes it.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Shell invocation functions (`os.system()`, `subprocess.Popen(shell=True)`, `child_process.exec()`, `Runtime.exec("sh -c ...")`, backtick operators), command strings as arguments |
| Static Binary | Yes | Imported shell execution functions, shell path strings (`/bin/sh`, `cmd.exe`), command string arguments in data sections |
| Runtime/Dynamic | Yes | Shell process spawning, command-line arguments visible in process listings, shell-specific behaviors (pipe creation, variable resolution) |

## Disambiguation

- **vs EXEC.PROC**: `EXEC.SHELL` passes a command STRING to a shell interpreter for parsing. `EXEC.PROC` launches a binary directly by path with explicit arguments, without shell interpretation. `subprocess.Popen("ls -la", shell=True)` is `EXEC.SHELL`. `subprocess.Popen(["ls", "-la"])` is `EXEC.PROC`. The distinction is whether a shell interpreter is interposed, shell interpretation enables string-based construction, injection, and expansion that direct process spawning does not.
- **vs XFRM.STRCON → EXEC.SHELL**: When the command string is assembled from fragments before being passed to the shell, both `XFRM.STRCON` (the assembly) and `EXEC.SHELL` (the execution) apply. The construction and execution are separate observable behaviors.

## Structural Relationships

- **Often co-occurs with**: `XFRM.STRCON` (command string assembled from fragments), `XFRM.ENCODE` / `XFRM.ENCRYPT` (decoded content passed to shell), `NETW.SOCKET` (shell I/O bound to network, remote shell), `PKGM.INSTALL` (shell execution during install)
- **May imply**: The system has a shell interpreter available at the expected path
- **Commonly part of idioms**: Remote shell (network I/O ↔ shell I/O), decode-and-execute chain (decoded content executed via shell)

## Notes

Shell command execution adds a layer of string interpretation between the caller and the actual operations. The command string can contain pipes (`|`), redirects (`>`, `<`, `>&`), variable expansion (`$VAR`, `%VAR%`), subshells (`` `...` ``, `$(...)`), and conditional chains (`&&`, `||`). This means the actual operations performed may be significantly more complex than what appears in the command string literal.
