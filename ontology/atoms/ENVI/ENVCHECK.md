# ENVI.ENVCHECK: Environment State Query

## Description

Queries runtime environment characteristics and branches on the result: environment variables, hostname, username, domain membership, geographic indicators (locale, timezone, IP geolocation), installed software profiles, or CI/build system indicators. The code inspects operational environment state (not analysis infrastructure, which is `ENVI.SANDBOX`) and executes different code paths depending on what it finds.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `os.environ` reads, `platform.node()`, `os.getlogin()`, `socket.gethostname()`, CI variable checks (`CI=true`, `GITHUB_ACTIONS`), locale/timezone queries |
| Static Binary | Yes | Environment variable name strings, hostname comparison values, known CI variable names |
| Runtime/Dynamic | Yes | Environment variable reads, hostname resolution calls, conditional branch taken based on environment state |

## Disambiguation

- **vs ENVI.SANDBOX**: Sandbox detection checks for analysis infrastructure (VMs, containers, specific sandbox products). Environment state queries check operational characteristics (hostnames, usernames, CI variables, geographic indicators). A check for `GITHUB_ACTIONS=true` is ENVI.ENVCHECK. A check for Cuckoo sandbox artifacts is ENVI.SANDBOX.
- **vs normal configuration**: Applications commonly read environment variables for configuration (database URLs, feature flags, log levels). ENVI.ENVCHECK applies when the environment query gates materially different behavior, not just configuration parameters but different execution paths. Reading `DATABASE_URL` to set a connection string is configuration. Reading `CI=true` to skip an entire code path is ENVI.ENVCHECK.

## Structural Relationships

- **Often co-occurs with**: `ENVI.SANDBOX` (combined environment profiling), any atom that the environment check gates (the checked condition controls whether subsequent behavior executes)
- **May imply**: The code has conditionally-activated behavior paths that depend on runtime environment state

## Notes

Environment checks range from broad (checking for any CI environment) to highly specific (checking for a named hostname or username). The specificity of the check and what it gates are the key structural data points. Additive checks (activate behavior when condition is true) and subtractive checks (suppress behavior when condition is true) are mechanically identical (both branch on environment state), but the distinction matters for interpretation.
