# PKGM.INSTALL: Install-Time Code Execution

## Description

Code that executes during package installation through package manager hook mechanisms. npm `postinstall`/`preinstall` scripts, Python `setup.py`/`setup.cfg` execution, Ruby `extconf.rb`, Go `generate` directives that run at build time. The package manager invokes this code automatically as part of the installation process, no explicit consumer action beyond installing the package.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `postinstall`/`preinstall` fields in `package.json`, `setup.py` `cmdclass` entries, `extconf.rb` presence and execution logic, `build.rs` content, `go:generate` directives |
| Static Binary | N/A | Install hooks are source-level package metadata, binary analysis is not the typical detection surface |
| Runtime/Dynamic | Yes | Process spawning during `npm install` / `pip install` / `gem install`, unexpected network or filesystem activity during installation phase |

## Disambiguation

- **vs EXEC.\***: `PKGM.INSTALL` identifies the trigger mechanism, the package manager hook that causes code to run at install time. `EXEC.*` atoms identify the execution behavior itself (shell invocation, process spawning). Both typically apply: the install hook triggers execution. `PKGM.INSTALL` says *when* it runs; `EXEC.*` says *how* it runs.
- **vs PKGM.HOOK**: `PKGM.INSTALL` covers native package manager hooks, the mechanisms provided by npm, pip, gem, cargo, go for running code during package installation. `PKGM.HOOK` covers broader build system injection (Makefiles, CMakeLists.txt, Gradle tasks, webpack plugins) that is not a native package manager mechanism.

## Structural Relationships

- **Often co-occurs with**: `EXEC.SHELL` (install hook invokes shell commands), `EXEC.PROC` (install hook launches processes), `NETW.*` (install hook makes network calls), `FSYS.WRITE` (install hook writes files outside its own directory), `XFRM.*` (install hook decodes or deobfuscates content before execution)
- **May imply**: The package expects to perform operations beyond placing files in `node_modules`/`site-packages`/equivalent; the package has native extensions, build requirements, or active install-time behavior
- **Commonly part of idioms**: Supply chain dropper (install hook → network fetch → write → execute), install-time credential harvesting (install hook → read credentials → exfiltrate)

## Notes

Install-time code execution is the defining mechanism of supply chain attacks against package ecosystems. The npm `postinstall` hook is the single most abused vector in the JavaScript ecosystem; Python's `setup.py` execution serves the same role for PyPI packages. The structural observation is that the package contains code that the package manager will execute automatically. The content and behavior of that code is described by other atoms (`EXEC.*`, `NETW.*`, `CRED.*`, etc.). A package with an install hook that runs `echo "build complete"` and a package with an install hook that exfiltrates environment variables both carry `PKGM.INSTALL`; the difference is in the co-occurring atoms.
