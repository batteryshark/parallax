# Package Metadata Signals

| Signal | Description | Confidence Effect |
|---|---|---|
| **New package** | Published recently with no track record | Elevates severity of any detected atoms |
| **New maintainer** | Ownership transferred or new maintainer added before suspicious release | High: mirrors XZ Utils attack pattern |
| **Download anomaly** | Download count inconsistent with age or purpose | Suggests typosquatting or compromise |
| **Version gap** | Published versions skip numbers or show irregular patterns | May indicate yanked malicious versions |
| **Metadata mismatch** | Description/README does not match actual code functionality | Suggests deception |
| **Provenance attestation downgrade** | Package that previously published via OIDC Trusted Publisher / Sigstore suddenly publishes without attestation (manual token, no `gitHead`, no CI binding). The Axios compromise was detectable by this signal alone: every legitimate 1.x release was via GitHub Actions OIDC; the malicious 1.14.1 was manual with a stolen npm token. | Very high: one of the strongest single indicators of account compromise |

Relates to: `PKGM.PUBLISH` atom observations
