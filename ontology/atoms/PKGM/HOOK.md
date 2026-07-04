# PKGM.HOOK: Build System Hook Modification

## Description

Modifies build system configuration files (Makefile, `CMakeLists.txt`, Gradle build files, webpack config, `Cargo build.rs`, Bazel BUILD files) to inject code execution during the build process. The build system interprets these configuration files and executes the specified commands as part of compilation, linking, bundling, or other build phases. Distinguished from `PKGM.INSTALL` in that `PKGM.HOOK` covers the broader build toolchain beyond the language's native package manager hooks.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Makefile target additions or modifications, `CMakeLists.txt` `add_custom_command`/`execute_process` directives, Gradle task definitions with `exec`/`commandLine`, webpack plugin injection, `build.rs` content executing external commands, Bazel `genrule` commands |
| Static Binary | N/A | Build system hooks are source/configuration-level artifacts |
| Runtime/Dynamic | Yes | Unexpected process spawning during build, network activity during compilation, file writes outside the build output directory during build execution |

## Disambiguation

- **vs PKGM.INSTALL**: `PKGM.INSTALL` covers native package manager hooks (`postinstall` in `package.json`, `setup.py` execution, `extconf.rb`). These are mechanisms provided by the package manager itself. `PKGM.HOOK` covers broader build system injection (Makefiles, CMake, Gradle, webpack), which are build toolchain configuration files, not package manager metadata. A `postinstall` script that runs `make` involves both: `PKGM.INSTALL` (the package manager hook) triggers `PKGM.HOOK` (the Makefile execution).
- **vs PRST.HOOK**: `PRST.HOOK` registers persistent execution hooks in the OS or runtime environment, `LD_PRELOAD` entries, PATH manipulation, shell profile modifications, cron entries. These persist beyond the build and affect the system going forward. `PKGM.HOOK` modifies build system configuration files to execute during the build process. The distinction is build-time scope vs persistent system-level modification.

## Structural Relationships

- **Often co-occurs with**: `EXEC.SHELL` (build hooks invoke shell commands), `EXEC.PROC` (build hooks launch processes), `PKGM.INSTALL` (package manager hook triggers build system execution), `NETW.*` (build hook makes network calls), `FSYS.WRITE` (build hook writes files outside build output)
- **May imply**: The build process performs operations beyond compilation and linking; the build configuration is an active code execution surface

## Notes

Build system configuration files are a code execution surface that is frequently overlooked in security reviews. A Makefile target, a CMake custom command, or a Gradle task executes with the full privileges of the build process. In transitive dependencies, build hooks may execute without the consumer ever directly reviewing the build configuration. The structural observation is that the build configuration contains commands that will execute during the build. The content and behavior of those commands is described by co-occurring atoms.
