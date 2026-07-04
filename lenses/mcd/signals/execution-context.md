# Execution Context Signals

| Signal | Description | Confidence Effect |
|---|---|---|
| **CI/CD environment targeting** | Code checks for CI/CD variables (`GITHUB_ACTIONS`, `CI`, `GITLAB_CI`, `JENKINS_URL`) before activating. CI/CD runners concentrate secrets: deployment keys, registry tokens, cloud credentials, publishing tokens. LiteLLM gated activation on `GITHUB_ACTIONS`. | Strong elevation: targeting environment where credentials are most concentrated |
| **Security tooling context** | Code executing within security scanning tools (SAST/DAST, vulnerability scanners, IaC scanners). Security tools have legitimate broad access by design; a compromised security tool is the ultimate wolf in sheep's clothing. The Trivy compromise: scanner's legitimate access became credential harvesting platform. | Critical elevation: pre-authorized access to exactly the secrets an attacker wants |
| **Privileged orchestration context** | Executing with Kubernetes cluster-admin, Docker socket access, or broad cloud IAM roles. Credential access and lateral movement atoms have dramatically higher blast radius. | Multiplies blast radius of any detected composition |

Relates to: `ENVI.ENVCHECK`, `SYSI.PROCMEM`, `PRIV.*` atom observations
