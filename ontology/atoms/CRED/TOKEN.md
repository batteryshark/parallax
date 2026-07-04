# CRED.TOKEN: Token / Session File Access

## Description

Reads authentication tokens, session files, OAuth token caches, JWT files, or API key files from known locations on disk. Targets files that store persistent authentication state outside of browser or cloud CLI contexts: GitHub CLI tokens (`~/.config/gh/`), npm auth tokens (`.npmrc`), Docker credentials (`~/.docker/config.json`), Slack tokens, and similar application-specific credential stores.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Token file path references (`.npmrc`, `~/.config/gh/hosts.yml`, `~/.docker/config.json`), token parsing code, bearer token extraction patterns |
| Static Binary | Yes | Token file path string literals, token format patterns |
| Runtime/Dynamic | Yes | File reads from token file locations, token string extraction and use |

## Disambiguation

- **vs CRED.CLOUD**: Cloud CLI credential files (AWS, GCP, Azure, K8s) are `CRED.CLOUD`. Non-cloud-CLI token files are `CRED.TOKEN`. The distinction is the credential store: cloud provider CLI vs. general application.
- **vs CRED.BROWSER**: Browser-managed credentials (password DB, cookies) are `CRED.BROWSER`. Standalone token files on disk are `CRED.TOKEN`.

## Structural Relationships

- **Often co-occurs with**: `FSYS.READ` (reading the token file), `FSYS.SENSITIVE` (token locations are sensitive paths), `NETW.*` (using or transmitting the token)
- **May imply**: The code knows the location and format of application-specific credential files

## Notes

Token files vary in format (JSON, YAML, INI, plaintext) and location (XDG config directories, home directory dotfiles, application-specific paths). The specificity of the path and the format parsing logic indicate the depth of the code's knowledge about the targeted credential store.
