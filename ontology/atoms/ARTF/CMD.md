# ARTF.CMD: Embedded Shell Command String

## Description

Complete or partial shell commands present as string literals in source or binary. Includes single commands (`curl`, `wget`, `powershell`), command pipelines (`cat /etc/passwd | grep root`), shell one-liners, PowerShell cmdlets, and command templates with placeholder substitution. May be passed to `exec`/`system` calls, used as templates for command construction, or assembled from fragments at runtime. The artifact is the command string itself, a static instruction intended for shell interpretation.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | String literals containing shell command syntax (`|`, `>`, `&&`, `;`), known command names (`curl`, `wget`, `chmod`, `powershell`, `cmd.exe`), command strings assigned to variables passed to `subprocess`, `os.system`, `exec`, `child_process.exec` |
| Static Binary | Yes | Shell command strings in data sections, command-line syntax patterns, shell metacharacters adjacent to executable names |
| Runtime/Dynamic | Yes | Command strings passed to process execution APIs, shell interpreters invoked with string arguments, command output captured |

## Disambiguation

- **vs EXEC.***: `ARTF.CMD` is the static presence of a command string in code or binary. `EXEC.*` atoms describe runtime command execution behavior. An embedded command string that is never executed is `ARTF.CMD` only. When code passes an embedded command to a shell or process API, both `ARTF.CMD` and the relevant `EXEC.*` atom apply. The command is the artifact; execution is the behavior.
- **vs XFRM.STRCON**: When command strings are assembled from fragments at runtime (e.g., `cmd = "cu" + "rl " + url`), the construction behavior is `XFRM.STRCON` and the resulting command is `ARTF.CMD`. If the fragments are individually identifiable as command components, each fragment may also qualify as `ARTF.CMD`.
- **vs ARTF.PATH**: A path to an executable (`/usr/bin/curl`) is both a path and a potential command component. In isolation, it is `ARTF.PATH`. Within a complete command string (`/usr/bin/curl -s http://...`), the full string is `ARTF.CMD` and the executable path within it is `ARTF.PATH`.

## Structural Relationships

- **Often co-occurs with**: `EXEC.SHELL` / `EXEC.PROC` (command string passed to execution primitive), `XFRM.STRCON` (command assembled from fragments), `XFRM.ENCODE` (command encoded to avoid detection), `ARTF.URL` / `ARTF.IP` (network targets within command strings), `ARTF.PATH` (filesystem targets within command strings)
- **May imply**: The code intends to invoke external processes or shell functionality, with the specific command determining what system interaction occurs

## Notes

Command content carries significant contextual information. Network-fetching commands (`curl`, `wget`, `Invoke-WebRequest`) indicate remote resource retrieval. Permission-modifying commands (`chmod`, `icacls`) indicate access control changes. System administration commands (`useradd`, `net user`, `schtasks`) indicate system modification. Piped commands indicate data flow between processes. Shell metacharacters (`|`, `>`, `&&`, `;`, backticks) indicate shell interpretation rather than direct process invocation. These are structural properties of the command string.
