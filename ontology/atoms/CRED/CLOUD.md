# CRED.CLOUD: Cloud Credential Files

## Description

Accesses cloud provider credential files at their canonical filesystem locations: AWS (`~/.aws/credentials`, `~/.aws/config`), GCP (`~/.config/gcloud/`), Azure (`~/.azure/`), Kubernetes (`~/.kube/config`), or equivalent cloud CLI credential stores. These files contain API keys, access tokens, session tokens, and service account credentials for cloud infrastructure.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Cloud credential path strings (`~/.aws/credentials`, `~/.config/gcloud/application_default_credentials.json`, `~/.kube/config`), file open/read targeting these paths |
| Static Binary | Yes | Cloud credential path literals in data sections |
| Runtime/Dynamic | Yes | File reads from cloud credential directories, parsing of credential file formats (INI for AWS, JSON for GCP) |

## Disambiguation

- **vs CRED.ENV**: Cloud credentials can be in files (CLOUD) or environment variables (ENV). `AWS_ACCESS_KEY_ID` in env is `CRED.ENV`. `~/.aws/credentials` file read is `CRED.CLOUD`. Both may be accessed in the same code path (checking multiple credential sources).
- **vs CRED.TOKEN**: `CRED.CLOUD` is for canonical cloud CLI credential locations specifically. Generic token files outside cloud CLI paths are `CRED.TOKEN`.

## Structural Relationships

- **Often co-occurs with**: `FSYS.READ` (reading the credential file), `FSYS.SENSITIVE` (cloud credential paths are sensitive), `NETW.HTTP` (using retrieved credentials for API calls or exfiltrating them), `CRED.ENV` (checking both file and env variable credential sources)
- **May imply**: The code is aware of cloud provider credential file formats and locations

## Notes

Cloud CLI tools follow documented credential resolution chains (e.g., AWS checks env vars, then `~/.aws/credentials`, then instance metadata). The distinction between using an SDK's credential chain (which implements this resolution) vs. directly reading the credential file is a structural observation, SDK usage goes through an abstraction layer; direct file reads operate on the raw credential data.
