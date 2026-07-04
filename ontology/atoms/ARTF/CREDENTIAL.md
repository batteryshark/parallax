# ARTF.CREDENTIAL: Embedded Credential Material

## Description

API keys, tokens, passwords, private keys, AWS access keys, or other authentication material embedded directly in source or binary as string literals or byte arrays. Identifiable by provider-specific formats: AWS access keys (`AKIA` prefix, 20 characters), GitHub tokens (`ghp_`, `gho_`, `ghs_` prefixes), Slack tokens (`xoxb-`, `xoxp-`, `xoxa-`), Stripe keys (`sk_live_`, `pk_live_`), PEM-encoded private keys (`-----BEGIN RSA PRIVATE KEY-----`), bearer tokens, basic auth strings, and generic high-entropy strings in authentication contexts. The artifact is the credential material itself, static authentication data embedded in the codebase.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | String literals matching provider key formats, PEM header/footer blocks, variables named `api_key`, `secret`, `password`, `token` assigned to string constants, hardcoded basic auth headers (`Authorization: Basic ...`), `.env` files committed to source |
| Static Binary | Yes | Provider-format key strings in data sections, PEM blocks, high-entropy ASCII strings near authentication API references |
| Runtime/Dynamic | Yes | Static credential strings passed to authentication APIs, used in HTTP authorization headers, submitted in login flows |

## Disambiguation

- **vs CRED.***: `ARTF.CREDENTIAL` is the static presence of credential material embedded in code or binary. `CRED.*` atoms describe runtime credential ACCESS behavior, reading credential stores, querying keychains, accessing browser databases. A hardcoded AWS key in source is `ARTF.CREDENTIAL`. Code that reads `~/.aws/credentials` at runtime is `CRED.CLOUD`. Both may co-occur when code contains embedded credentials AND accesses credential stores.
- **vs ARTF.HASH**: Credentials are authentication material used to prove identity or authorize access. Hash values are fixed-length digests used for comparison or integrity checking. An API key (`AKIA...`) is a credential. A SHA-256 digest used to verify file integrity is a hash. Some credential formats (certain tokens) may resemble high-entropy hash-like strings, provider-specific format patterns disambiguate.
- **vs XFRM.ENCODE**: Encoded credential material (a base64-encoded API key) presents both `ARTF.CREDENTIAL` (the credential, once decoded) and `XFRM.ENCODE` (the encoding operation). The credential is the semantic artifact; the encoding is the transformation applied to it.

## Structural Relationships

- **Often co-occurs with**: `NETW.HTTP` (credential used in API authentication), `XFRM.ENCODE` (credential encoded for transport or concealment), `PRST.*` (credential written to persistent storage), `CRED.*` (code that both embeds credentials and accesses credential stores)
- **May imply**: The code has a fixed authentication identity that does not depend on runtime credential retrieval or user input

## Notes

Provider-specific formats enable high-confidence identification. AWS access key IDs always start with `AKIA` (or `ASIA` for temporary credentials) followed by 16 alphanumeric characters. GitHub personal access tokens start with `ghp_` followed by 36 alphanumeric characters. These format signatures reduce false positives compared to generic high-entropy string detection. The presence of credential material in source versus binary versus configuration files carries different implications about the development process and exposure surface.
