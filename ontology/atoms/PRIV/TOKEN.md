# PRIV.TOKEN: Token / Identity Manipulation

## Description

Duplicates, impersonates, or forges access tokens within the current process or session. On Windows, this includes token manipulation APIs (`OpenProcessToken`, `DuplicateTokenEx`, `ImpersonateLoggedOnUser`, `CreateProcessWithTokenW`, `AdjustTokenPrivileges`). On Kerberos-authenticated systems, this includes ticket cache manipulation, ticket-granting operations, and golden/silver ticket construction. In federated identity systems, this includes SAML assertion forging and OAuth token manipulation. The mechanical behavior is modifying the effective identity or privilege set of the current execution context through token-level operations, without creating persistent identity records.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Windows token API calls (`DuplicateTokenEx`, `ImpersonateLoggedOnUser`, `CreateProcessWithTokenW`, `AdjustTokenPrivileges`), Kerberos library calls, ticket cache file path references (`/tmp/krb5cc_*`, `%LOCALAPPDATA%\krb5cc`), SAML/JWT construction code |
| Static Binary | Yes | Token API function imports, Kerberos library imports, ticket cache path strings, token privilege constant references (`SE_DEBUG_NAME`, `SE_IMPERSONATE_NAME`) |
| Runtime/Dynamic | Yes | Token API calls in API traces, impersonation level changes visible in thread context, new tickets appearing in credential caches, processes spawned under impersonated identity |

## Disambiguation

- **vs PRIV.ACCOUNT**: `PRIV.TOKEN` modifies the ephemeral in-process identity, the token exists only for the lifetime of the process or session. `PRIV.ACCOUNT` creates or modifies persistent OS identity records (user accounts, group memberships) that survive process termination and system reboot.
- **vs CRED.TOKEN**: `CRED.TOKEN` reads token/session files from disk (harvesting stored credentials). `PRIV.TOKEN` manipulates the active security context, duplicating, impersonating, or forging tokens for privilege change. The distinction is reading a credential file vs. modifying the execution identity.
- **vs PRIV.SUDO**: `PRIV.SUDO` uses an OS-provided elevation utility (sudo, runas) to launch a command under a different identity. `PRIV.TOKEN` manipulates the security token within the current process or thread context directly via API calls.

## Structural Relationships

- **Often co-occurs with**: `EXEC.PROC` (launching processes under impersonated token), `CRED.TOKEN` (reading tokens that are then used for impersonation), `SYSI.PROCMEM` (reading token from another process's memory)
- **May imply**: The code is transitioning its effective identity or privilege level through OS-level token operations

## Notes

Token manipulation scope varies from process-local to cross-process. Thread-level impersonation (`ImpersonateLoggedOnUser`, `SetThreadToken`) changes identity for the current thread only. Process-level token replacement affects all threads. `CreateProcessWithTokenW` creates a new process under the manipulated identity. The scope (whether the manipulated identity stays within the current process or spawns new processes) is a key structural observation.
