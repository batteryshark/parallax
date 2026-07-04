# Credential Store Sweep

## Description

Code iterates over a set of known credential storage locations, reads or attempts to read each, and aggregates the results. The distinguishing structural shape is the enumeration pattern, not a single credential file read, but a systematic sweep across multiple known stores. The locations may be hardcoded as a list, computed from environment variables (home directory expansion), or platform-switched (different paths for macOS/Windows/Linux). The sweep collects whatever is accessible rather than targeting a single known credential.

## Constituent Atoms

| Atom | Role | Notes |
|---|---|---|
| `CRED.*` (multiple) | Target identification | One or more CRED atoms identify what type of credential store is being accessed |
| `FSYS.READ` | Read operation | File content reading at each credential path |
| `FSYS.ENUM` | Path discovery (optional) | Directory listing to find credential files within known directories |
| `ARTF.PATH` | Path specification | Hardcoded known credential paths as string literals |
| `SYSI.OS` (optional) | Platform selection | OS detection to choose platform-appropriate credential paths |

## Structural Pattern

```
for each known_path in [credential_store_locations]:
    if path_exists(known_path):
        content = read(known_path)
        results.append(content)
```

The pattern may be literal iteration over a list, or may be a sequence of independent read attempts with error suppression (try/except, if-exists checks). The structural core is: multiple known credential locations → read attempt at each → aggregate accessible results.

## Variations

| Variation | Key Difference | Confidence Adjustment |
|---|---|---|
| **Explicit path list** | Hardcoded array of credential file paths, iterated directly | Strong match, the list of known paths is the clearest signal |
| **Platform-switched paths** | OS detection selects between macOS, Windows, and Linux credential locations | Strong match, cross-platform targeting increases coverage |
| **Directory enumeration** | Known credential directories (`.ssh/`, `.aws/`, browser profile dirs) are listed and all files read | Strong match, broader than path list, captures unknown filenames |
| **Environment-derived paths** | Home directory from env vars + known relative paths appended | Strong match, standard technique for cross-user portability |
| **Single-store deep read** | One credential store (e.g., browser password DB) accessed comprehensively | Weak match, depth without breadth is a CRED atom, not the sweep idiom |

## Confidence Spectrum

| Signal Strength | Indicators |
|---|---|
| **Strong match** | 3+ distinct credential store paths in a list or sequential reads; paths span multiple credential types (SSH + cloud + browser); error suppression per path (try/except or existence check) |
| **Moderate match** | 2 distinct credential store accesses in the same code path; paths are computed rather than listed |
| **Weak match** | Single credential store access (even if multiple files within it); credential path as configuration rather than hardcoded list |
| **Not this idiom** | Application reading its own credential configuration; single credential file read for documented authentication purpose; credential management tool accessing stores it's designed to manage |

## Notes

The sweep is distinguished from a single credential access by breadth, the code accesses multiple independent credential stores in a single execution path. A password manager legitimately reads its own credential database; the sweep idiom describes code that reads OTHER programs' credential stores across multiple categories. The aggregation step (collecting results rather than using each individually) reinforces the pattern, the code is gathering credentials, not authenticating with them.

The paths targeted are the primary structural data. Common high-value targets: `~/.ssh/id_rsa` and variants, `~/.aws/credentials`, `~/.config/gcloud/`, browser password databases (`Login Data`, `logins.json`), macOS Keychain files, `~/.npmrc`, `~/.docker/config.json`, and environment variables containing secrets.
