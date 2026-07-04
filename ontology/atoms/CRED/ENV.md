# CRED.ENV: Environment Variable Harvesting

## Description

Reads environment variables that contain or are likely to contain authentication material: API keys, access tokens, database connection strings with credentials, secret keys, and similar sensitive values. May read specific named variables (e.g., `AWS_SECRET_ACCESS_KEY`) or scan all environment variables with pattern matching against known secret-bearing naming conventions.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `os.environ` / `process.env` access, specific variable names (`AWS_SECRET_ACCESS_KEY`, `DATABASE_URL`, `API_KEY`), pattern-based filtering of environment keys |
| Static Binary | Yes | Environment variable name strings, environment access function imports |
| Runtime/Dynamic | Yes | Environment variable read system calls, access to specific variables |

## Disambiguation

- **vs normal configuration reading**: Every application reads environment variables. `CRED.ENV` applies when the target variables contain authentication material (keys, tokens, passwords, connection strings with credentials) or when the code systematically scans for variables matching secret-bearing patterns. Reading `LOG_LEVEL` is configuration. Reading `AWS_SECRET_ACCESS_KEY` is `CRED.ENV`.
- **vs CRED.CLOUD**: Environment variables containing cloud credentials (`AWS_ACCESS_KEY_ID`) are `CRED.ENV`. File-based cloud credentials (`~/.aws/credentials`) are `CRED.CLOUD`. Code that checks both sources accesses both atoms.

## Structural Relationships

- **Often co-occurs with**: `NETW.*` (transmitting harvested values), `CRED.CLOUD` (checking both env and file credential sources), `SYSI.*` (gathering system context alongside credentials)
- **May imply**: The code expects credentials to be available in the process environment

## Notes

The distinction between targeted reads (specific named variables) and bulk scanning (iterating all env vars with pattern matching on `*KEY*`, `*SECRET*`, `*TOKEN*`, `*PASS*`) is a structural observation. Targeted reads suggest knowledge of specific credential sources. Bulk scanning suggests systematic collection of whatever credentials are available.
