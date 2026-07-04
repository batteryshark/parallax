# MCD Lens: CRED (Credential and Secret Access) Indicators

> **Core MCD position:** Credential theft is the objective of a large proportion of supply chain attacks. The attacker wants credentials, API keys, or session tokens. In dependency code, credential access without clear documented purpose is very high severity.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `CRED.KEYCHAIN` | Medium-High | OS credential store access in library code is unusual |
| `CRED.BROWSER` | High | Browser credential access is almost never a legitimate dependency behavior |
| `CRED.CLOUD` | High | Cloud credential file access in non-cloud packages is a strong signal |
| `CRED.SSH` | High | SSH key access in non-SSH-management packages is highly anomalous |
| `CRED.ENV` | Medium | Depends on which variables and whether targeted or bulk scanning |
| `CRED.TOKEN` | Medium-High | Token file access in packages with no auth management purpose |
| `CRED.CERT` | Medium | Certificate access is common in TLS-aware code; private key access is higher |

## Escalation Factors

- **Access at install or build time.** No install script legitimately reads `~/.aws/credentials`, queries the keychain, or enumerates SSH keys.
- **Multiple credential types accessed.** Sweeping across cloud, SSH, browser, and env credentials is systematic collection, not incidental access.
- **Credential access followed by network activity.** `CRED.*` → `NETW.*` is the canonical theft pattern. Webhook/messaging platform destinations escalate immediately.
- **Multi-platform path targeting.** Checking both `~/.aws/credentials` and `%USERPROFILE%\.aws\credentials` is writing a cross-platform harvester.
- **Preceded by reconnaissance.** `SYSI.OS` or `SYSI.USER` before `CRED.*` indicates environment profiling to select the right credential paths.
- **Credential material encoded/encrypted before transmission.** `XFRM.*` applied to harvested credentials conceals the stolen material.
- **No documented credential management purpose.** A date formatter or logging utility has no reason to read credential files.
- **Browser credential databases targeted.** Almost no legitimate library dependency needs `Login Data` or `Cookies`.
- **Broad env var pattern matching.** Iterating all env vars and filtering `*KEY*`, `*SECRET*`, `*TOKEN*` is systematic harvesting.
- **Certificate access combined with traffic interception.** `CRED.CERT` + `NETW.LISTEN` suggests MITM setup.

## De-escalation Factors

- **Documented credential management purpose.** An AWS SDK, password vault client, or SSH key management tool accessing its documented scope.
- **Access to package's own configuration.** A tool reading its own API key from its own config file.
- **Access driven by explicit user invocation.** Library code that accesses credentials only when called with explicit parameters, not on import/install.
- **Well-known SDK mediating access.** `boto3.Session()` vs. direct `open("~/.aws/credentials")`.

> **Caveat:** Credential access + network transmission is not de-escalatable. Even a well-known package has no legitimate reason to exfiltrate credentials.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `CRED.*` + `NETW.*` | Credential exfiltration, complete theft chain | Very High |
| `CRED.CLOUD` + `NETW.HTTP` | Cloud credential theft via HTTP, Axios pattern | Very High |
| `CRED.ENV` + `NETW.WEBHOOK` | Env secrets via messaging webhook | Very High |
| `CRED.*` + `XFRM.*` | Credential access concealed by transformation | High |
| `CRED.*` + `PKGM.INSTALL` | Credential access at install time | Very High |
| Multiple `CRED.*` subtypes | Multi-store credential sweep, systematic harvester | Very High |
| `SYSI.*` + `CRED.*` | Platform profiling → targeted credential access | High |
| `CRED.*` + `FSYS.ARCHIVE` | Credentials collected and packaged for bulk exfil | High |
| `CRED.CERT` + `NETW.LISTEN` | Certificate + listener, possible MITM setup | High |

## MCD-Specific Disambiguation

### CRED vs FSYS priority
When both `CRED.*` and `FSYS.SENSITIVE` apply, `CRED.*` drives MCD escalation priority. Follow the data: was credential data read → encoded → transmitted? FSYS captures the method; CRED captures what's being targeted.

### CRED.ENV: configuration vs harvesting
Through the MCD lens, reading `os.environ.get("MY_APP_LOG_LEVEL")` is not `CRED.ENV`. Reading `AWS_SECRET_ACCESS_KEY` is. Bulk-scanning all env vars for `*SECRET*/*KEY*/*TOKEN*` is systematic harvesting. The breadth of the pattern is the MCD signal.

### CRED.SSH: lateral movement risk
Through the MCD lens, SSH key theft paired with network reconnaissance expands blast radius beyond the compromised system. The stolen keys enable access to other systems, so the MCD investigation must assess the potential scope of lateral movement.
