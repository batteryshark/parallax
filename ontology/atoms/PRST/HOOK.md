# PRST.HOOK: Execution Hook Registration

## Description

Installs hooks that intercept execution at the operating system, loader, or runtime level, outside the package's own process or scope. Includes shared library injection directives (`LD_PRELOAD` entries in `/etc/ld.so.preload`, `DYLD_INSERT_LIBRARIES` environment variable modification), PATH manipulation to shadow system binaries (placing a binary named `git` or `python` earlier in the PATH than the real binary), Python import hooks installed at the system level (`sitecustomize.py`, `.pth` files in `site-packages`), Git hooks in template directories (`~/.git-templates/hooks/`), and shell function overrides that shadow system commands. The hook causes code to execute whenever the intercepted operation occurs, across any process or user that triggers the hooked path.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Writes to `/etc/ld.so.preload`, `DYLD_INSERT_LIBRARIES` modification, PATH prepend operations, file writes to Git template hook directories, `.pth` file creation, `sitecustomize.py` modification, shell function definitions shadowing system commands |
| Static Binary | Yes | Preload configuration path strings, PATH manipulation patterns, hook directory path strings, `.pth` file content patterns |
| Runtime/Dynamic | Yes | Unexpected libraries loaded via preload, PATH resolution returning non-standard binary locations, Git hooks firing from template directories, Python import hooks intercepting module loads, shell functions overriding expected command behavior |

## Disambiguation

- **vs application-level hooks**: `PRST.HOOK` intercepts execution OUTSIDE the package's own process or scope, it affects other programs, other users, or system-wide behavior. Application-level hooks (Git hooks in a project's own `.git/hooks/`, framework lifecycle callbacks, event emitters, middleware registration) operate within the application's own scope and are normal programming patterns, not persistence mechanisms.
- **vs PRST.STARTUP**: `PRST.STARTUP` registers code to run at boot/login. `PRST.HOOK` registers code to run when a specific operation is performed (library load, command invocation, import, git operation). The trigger is an intercepted action, not a system lifecycle event.
- **vs ENVI.MASQ**: PATH shadowing involves both `PRST.HOOK` (the interception mechanism, placing a binary where it will be found first) and potentially `ENVI.MASQ` (if the shadow binary is named to impersonate the real binary). The hook is the interception; the masquerade is the identity disguise.

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (writing the hook binary or configuration), `ENVI.MASQ` (hook binary named to match the shadowed command), `CRED.*` (hook intercepts authentication flow to capture credentials), `EXEC.PROC` / `EXEC.SHELL` (hook executes additional code when triggered)
- **May imply**: Every invocation of the hooked operation (by any process, potentially by any user) will execute the hook code, creating a broad and persistent interception surface
- **Commonly part of idioms**: Credential interceptor (`LD_PRELOAD` library hooking authentication functions), command hijack (PATH shadow binary wrapping the real command with additional behavior), import interceptor (Python `.pth` file executing code on every Python invocation)

## Notes

The blast radius of an execution hook depends on its scope. A user-level `LD_PRELOAD` via shell profile affects that user's processes. A system-level `/etc/ld.so.preload` entry affects every dynamically-linked process on the system. A `.pth` file in a system `site-packages` directory runs on every Python invocation by any user. The scope of the hook (user-level vs. system-level) and the frequency of the intercepted operation (how often is the hooked command/library/import triggered) determine the effective blast radius.
