# ARTF.PATH: Embedded Filesystem Path

## Description

Absolute filesystem paths present as string literals in source or binary. Includes OS-specific path formats: Unix absolute paths (`/etc/passwd`, `/usr/local/bin/`), Windows paths with drive letters (`C:\Windows\System32\`) or UNC paths (`\\server\share`), macOS Library paths (`~/Library/Application Support/`), user home directory expansions (`~/.ssh/`, `%USERPROFILE%`), and Windows registry paths (`HKLM\SOFTWARE\`). The artifact is the path string itself, a fixed reference to a filesystem location embedded in the code.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | String literals starting with `/`, `C:\`, `\\`, `~`, or containing `%ENVVAR%` path expansions, `os.path.join` with absolute components, `Path("/absolute/...")` constructors, registry path constants |
| Static Binary | Yes | Absolute path strings in data sections, Windows-format paths with backslashes, Unix paths with forward slashes, environment variable references for path construction |
| Runtime/Dynamic | Yes | Path strings passed to file open/read/write calls, directory enumeration targets, path strings in error messages or log output |

## Disambiguation

- **vs FSYS.***: `ARTF.PATH` is the static presence of a path string in code or binary. `FSYS.*` atoms describe runtime filesystem operations (read, write, delete, enumerate). An embedded path may be a configuration default, a documentation reference, or an actual filesystem target. When code uses an embedded path in a filesystem operation, both `ARTF.PATH` and the relevant `FSYS.*` atom apply.
- **vs CRED.***: When an embedded path points to a known credential location (`~/.ssh/id_rsa`, `~/.aws/credentials`, `Login Data`), the path artifact is `ARTF.PATH` and any runtime access to that path for credential retrieval is `CRED.*`. The path names the target; the credential atom describes the access behavior.
- **vs ARTF.URL**: A `file://` URI is both a URL and a path reference. The `file://` prefix makes it `ARTF.URL`; the path component makes it `ARTF.PATH`. Standard filesystem paths without protocol scheme are `ARTF.PATH` only.

## Structural Relationships

- **Often co-occurs with**: `FSYS.READ` / `FSYS.WRITE` (path used as filesystem operation target), `CRED.*` (path pointing to credential store), `EXEC.SHELL` (path used as command target), `SYSI.OS` (OS detection selecting platform-specific paths), `XFRM.STRCON` (path assembled from components at runtime)
- **May imply**: The code targets specific filesystem locations, which may indicate assumptions about the target operating system, directory structure, or installed software

## Notes

Path targets carry contextual information. System directories (`/etc/`, `C:\Windows\System32\`), credential locations (`~/.ssh/`, `~/.aws/`), browser profile directories, temporary directories, and startup/persistence locations each indicate different operational concerns. Cross-platform path sets (both Unix and Windows variants for the same logical target) indicate platform-aware code. Registry paths indicate Windows-specific system configuration access. These are structural properties of the path, useful for characterization regardless of analytical lens.
