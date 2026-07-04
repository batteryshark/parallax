# MCD Lens: FSYS (Filesystem Operations) Indicators

> **Core MCD position:** Filesystem operations are central to nearly every malicious behavior: credential theft reads files, droppers write files, ransomware modifies files, and reconnaissance enumerates them. The path being accessed, not the operation type, determines MCD severity.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `FSYS.READ` | Context-dependent | Entirely path-dependent, `~/.ssh/id_rsa` vs `./config.json` |
| `FSYS.WRITE` | Context-dependent | Depends on target path and subsequent operations |
| `FSYS.DELETE` | Low-Medium | Elevated when targeting logs, evidence, or security tools |
| `FSYS.ENUM` | Low-Medium | Elevated when targeting credential stores or non-application directories |
| `FSYS.PERM` | Medium | Elevated when targeting system files or removing visibility |
| `FSYS.LINK` | Low-Medium | Elevated when creating redirects to sensitive paths |
| `FSYS.TEMP` | Low | Nearly all software uses temp. Elevated only when combined with execution |
| `FSYS.ARCHIVE` | Low-Medium | Elevated when archiving user data directories |
| `FSYS.SENSITIVE` | High | Access to known sensitive paths is a strong finding in library code |
| `FSYS.HIDDEN` | Medium-High | Hidden storage in dependency code has narrow legitimate justification |
| `FSYS.CLIPBOARD` | Medium-High | Clipboard access in packages without UI functionality is notable |

## Escalation Factors

- **Sensitive path targeting.** Access to `~/.ssh/`, `~/.aws/credentials`, browser profiles, keychains, or OS credential stores elevates any FSYS atom to high regardless of operation type.
- **Write followed by execute.** `FSYS.WRITE` to a temp/writable directory immediately followed by execution is the canonical payload staging pattern (Axios: `/tmp/ld.py` → `nohup python3`). This combination is critical.
- **Archive creation targeting user data.** `FSYS.ARCHIVE` scoped to `~/Documents`, `~/Desktop`, database files, or source code is a pre-exfiltration indicator.
- **Enumeration of non-application directories.** `FSYS.ENUM` on SSH directories, credential stores, cloud configs, or other applications is suspicious. Enumeration of the package's own tree is expected.
- **Permission modification downgrading visibility.** Removing read or execute bits from logs, audit directories, or security tool binaries.
- **Deletion after anomalous write activity.** `FSYS.DELETE` sequenced after `FSYS.WRITE` or `FSYS.ARCHIVE` suggests cleanup. Standalone deletion of own temp files does not escalate.
- **Symlink creation outside the package tree.** Links redirecting sensitive paths or escaping sandbox boundaries.
- **Clipboard access with no user-initiated trigger.** Clipboard operations on import, in background threads, or on timers rather than in explicit user-invoked functions.
- **Cross-user or cross-privilege path access.** Reads/writes to paths belonging to other users or requiring elevated privilege.
- **Hardcoded absolute sensitive paths.** Sensitive paths as string literals rather than OS-API-constructed paths indicate deliberate targeting.
- **Hidden storage containing executable content or credentials.** ADS/xattrs storing scripts, binaries, keys, or exfiltrated data.
- **Hidden data attached to system files or other packages' files.** Piggybacking on trusted files.
- **Hidden storage read back and executed.** Data stored in hidden streams subsequently retrieved and passed to `LOAD.*`/`EXEC.*`.

## De-escalation Factors

- **Access limited to the package's declared install tree.** Reads/writes confined to package-manager-created paths are expected.
- **Temp file write paired with documented cache/build behavior.** Does not de-escalate write-then-execute patterns.
- **Archive operations on caller-supplied paths.** A compression library compressing what it's told to compress.
- **Permission changes on self-owned config at install time.** Standard hardening (e.g., `0600` on own config file).
- **Enumeration of standard directories for application data location.** Only when not extending to credential/security paths.
- **Hidden storage for documented OS metadata.** macOS quarantine xattrs, Finder metadata in Apple-namespaced attributes. Custom-namespaced xattrs with binary payloads do not de-escalate.
- **Hidden storage in backup/sync tools.** Tools that preserve file metadata may read/write ADS/xattrs as part of faithful reproduction. Only when the package's purpose is file management.

> **Caveat:** Filesystem operations are the broadest category. Always resolve the full path before assessing. A `FSYS.READ` of `~/.ssh/id_rsa` is fundamentally different from a `FSYS.READ` of the package's own `config.json`.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `FSYS.SENSITIVE` + `NETW.*` | Credential/config read → network exfiltration | Critical |
| `FSYS.WRITE` (temp) + `EXEC.*` | Payload staged in temp → executed, canonical dropper | Critical |
| `FSYS.ARCHIVE` + `NETW.*` | User data archived → transmitted, exfiltration staging | Critical |
| `FSYS.ENUM` + `FSYS.SENSITIVE` | Directory traversal locating credential targets | High |
| `FSYS.DELETE` + `EVSN.*` | Post-activity cleanup, anti-forensics | High |
| `FSYS.CLIPBOARD` + `NETW.*` | Clipboard content exfiltrated (passwords, seeds, tokens) | High |
| `FSYS.WRITE` + `FSYS.PERM` | File written then made executable, privilege setup | High |
| `FSYS.SENSITIVE` + `CRED.*` | Sensitive path confirmed as credential file | High-Critical |
| `FSYS.LINK` + `FSYS.WRITE` | Symlink redirect → write, path traversal attack | High |
| `FSYS.TEMP` + `XFRM.*` | Obfuscated content staged in temp, concealed payload | Critical |
| `FSYS.HIDDEN` + `EXEC.*`/`LOAD.*` | Hidden storage → retrieved → executed, invisible payload staging | Critical |
| `FSYS.HIDDEN` + `CRED.*` | Credentials in hidden storage, invisible credential cache | High |
| `FSYS.HIDDEN` + `PRST.*` | Hidden data as persistence, survives standard cleanup | High |

## MCD-Specific Disambiguation

### FSYS.SENSITIVE vs CRED: investigation priority
Through the MCD lens, when both apply, `CRED.*` drives the escalation priority and `FSYS.SENSITIVE` captures the method. The MCD investigation follows the data: was credential data read → was it encoded/archived → was it transmitted? The FSYS path is the starting point of that chain.

### FSYS.CLIPBOARD: targeting profile
Through the MCD lens, clipboard access targets include cryptocurrency addresses (substitution attacks replacing the user's address with the attacker's), passwords copied from password managers, session tokens, and seed phrases. The trigger mechanism is the primary severity driver: background monitoring is much higher severity than explicit function-call access.

### FSYS.TEMP: write-then-execute is the critical pattern
Through the MCD lens, temp file usage alone is not significant. The single highest-value MCD question for any `FSYS.TEMP` finding is: "is the temp file subsequently executed?" If yes, the finding is critical. The Axios compromise pattern (`NETW.HTTP` → `FSYS.WRITE` /tmp → `EXEC.PROC` nohup) is the reference example.
