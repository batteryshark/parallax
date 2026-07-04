# MCD Lens: ARTF (Embedded Artifacts) Verification

Investigation questions for ARTF findings, organized for MCD triage. Questions tagged `[lens-neutral]` are applicable across multiple lenses and may be factored to the shared investigation framework later. Questions tagged `[MCD]` assume an MCD evaluation context.

## General: Any ARTF Atom

1. **Which ARTF subtypes are present?** Enumerate and document each distinct artifact: IPs, URLs, domains, paths, commands, credentials, hashes, email addresses, cryptocurrency addresses, timestamps. A complete artifact inventory is the foundation of ARTF analysis. `[lens-neutral]`

2. **Was the artifact introduced in a recent version?** Diff against previous versions. Artifacts that appear in a patch release or minor version bump by a known maintainer are less suspicious than those introduced by a new contributor or in an unexpected update. `[lens-neutral]`

3. **Who introduced the artifact?** Check commit history and author identity. Artifacts added by the original maintainer with a documented purpose differ from those added by a new contributor or in a compromised account scenario. `[lens-neutral]`

4. **Is the artifact reachable from an execution path?** Trace code paths from entry points (import, install hooks, exported functions) to the artifact. An unreachable artifact in dead code is structurally different from one on a hot path, though dead code can be activated by future changes. `[lens-neutral]`

5. **Is the artifact inside encoded or obfuscated content?** If the artifact was only discoverable after decoding/deobfuscation (`XFRM.*`), the author deliberately concealed it. Document what transformation was applied and what the artifact looks like before and after. `[lens-neutral]`

6. **Does the package's stated purpose explain this artifact's presence?** An HTTP client library may legitimately contain URL constants. A date formatting library should not contain IP addresses. Consistency between stated purpose and artifact content is the primary MCD evaluation context. `[MCD]`

7. **Do the artifacts cluster into an operational picture?** Multiple artifact types in the same code path (a URL, a path, a command, a timestamp) may describe a complete operation: fetch payload from URL, write to path, execute command, activate at timestamp. Assess whether isolated artifacts are actually components of a coordinated behavior. `[MCD]`

## ARTF.IP: Embedded IP Address

8. **Is the IP address public or private?** RFC 1918 (`10.*`, `172.16-31.*`, `192.168.*`), loopback (`127.0.0.1`), and documentation ranges (`192.0.2.*`, `198.51.100.*`, `203.0.113.*`) are structurally different from public routable addresses. `[lens-neutral]`

9. **Does the IP belong to known infrastructure?** Look up the IP. Does it resolve to a known cloud provider, CDN, or VPS service? Does it appear in threat intelligence feeds? Does it match the project's documented infrastructure? `[MCD]`

10. **Are there multiple IPs suggesting fallback infrastructure?** Multiple hardcoded IPs, especially with sequential connection attempts, suggest redundant command-and-control infrastructure. `[MCD]`

## ARTF.URL: Embedded URL / URI

11. **What is the domain age and registration details?** WHOIS lookup on the URL's domain. Recently registered domains (< 30 days) with privacy-protected registration are a strong signal. `[MCD]`

12. **Do the URL path components match known C2 patterns?** Paths like `/gate`, `/panel`, `/beacon`, `/upload`, `/cmd`, `/bot`, or random-looking alphanumeric paths. `[MCD]`

13. **Is the URL still live, and what does it serve?** If safely testable, what does the endpoint return? A legitimate API response, a binary payload, a redirect chain, or nothing? `[MCD]`

## ARTF.EMAIL: Embedded Email Address

14. **Does the email address belong to the project author or organization?** Check against package metadata, repository owner, and published maintainer contacts. `[lens-neutral]`

15. **Is it a free email provider or organizational domain?** Free providers (gmail, outlook, protonmail) versus organizational domains carry different contextual weight. Exfiltration to free email providers is a common pattern. `[MCD]`

## ARTF.CRYPTO_ADDR: Embedded Cryptocurrency Address

16. **Is this a cryptocurrency-related package?** A blockchain wallet library embedding addresses is expected. A logging utility embedding a Bitcoin address is not. `[lens-neutral]`

17. **What blockchain does the address belong to, and does it have transaction history?** Look up the address on a blockchain explorer. Active addresses with incoming transactions confirm operational use. `[MCD]`

## ARTF.CREDENTIAL: Embedded Credential Material

18. **Does the credential match a known provider format?** AWS (`AKIA`), GitHub (`ghp_`), Slack (`xoxb-`), Stripe (`sk_live_`), PEM headers: provider-specific formats enable high-confidence classification. `[lens-neutral]`

19. **Is the credential still valid or has it been revoked?** If the credential can be safely tested against its provider's validation endpoint without authenticating, determine whether it is live. Active embedded credentials are an immediate security incident regardless of MCD context. `[MCD]`

20. **Is this a test/example credential or a production secret?** Check for patterns like `test`, `example`, `dummy`, `placeholder` in the credential or surrounding context. Well-known test credentials (AWS documentation examples) are structurally different from production secrets. `[lens-neutral]`

## ARTF.HASH: Embedded Hash Value

21. **What is being compared against this hash?** Trace the hash to its comparison operation. Is it checking file integrity, verifying a downloaded payload, comparing environment fingerprints, or validating a license? What the hash guards determines its significance. `[lens-neutral]`

22. **Does the hash match any known file or artifact?** Search the hash in VirusTotal, malware databases, or package registries. A hash that matches a known malicious binary is an immediate finding. `[MCD]`

23. **Is the hash used in a security-bypass or anti-tamper context?** Hashes used to detect debuggers, verify code integrity against modification, or gate behavior based on environment fingerprinting are structurally different from hashes used for data integrity. `[MCD]`

## ARTF.PATH: Embedded Filesystem Path

24. **Does the path point to a known credential or sensitive location?** `~/.ssh/`, `~/.aws/credentials`, browser `Login Data`, macOS Keychain, Windows Credential Manager paths. Credential-targeting paths escalate immediately. `[MCD]`

25. **Is the path cross-platform?** Both Unix and Windows variants for the same logical target (`~/.ssh/id_rsa` and `%USERPROFILE%\.ssh\id_rsa`) indicate deliberate multi-OS targeting. `[lens-neutral]`

26. **Does the path target a persistence or startup location?** Paths to cron directories, systemd units, Windows Run keys, LaunchAgents, or browser extension directories indicate persistence intent. `[MCD]`

## ARTF.CMD: Embedded Shell Command String

27. **What does the command do?** Parse the command: does it download content, modify permissions, create users, disable security, delete files, or exfiltrate data? The command content is the primary indicator. `[lens-neutral]`

28. **Does the command require elevated privileges?** Commands prefixed with `sudo`, `runas`, or targeting system directories imply the code expects or requests privilege escalation. `[lens-neutral]`

29. **Does the command contain network activity or data exfiltration?** `curl`, `wget`, `nc`, `Invoke-WebRequest`, piping data to remote endpoints: commands that move data off the system. `[MCD]`

## ARTF.DOMAIN: Embedded Domain Name

30. **What are the domain's registration details and age?** WHOIS lookup for creation date, registrar, registrant (if not privacy-protected). Recently registered domains are a strong escalation signal. `[MCD]`

31. **Does the domain use dynamic DNS or a suspicious TLD?** Dynamic DNS providers enable rapid IP changes. TLDs like `.xyz`, `.top`, `.tk`, `.ml` are disproportionately represented in malicious infrastructure. `[MCD]`

32. **What does the domain currently resolve to?** DNS lookup for current IP resolution. Does it resolve to known hosting infrastructure, sink-holed addresses, or parking pages? `[lens-neutral]`

## ARTF.TIMESTAMP: Embedded Date/Time Value

33. **Is the timestamp in the future relative to the package release date?** A future timestamp in conditional logic is a time-delayed activation trigger. Document the gap between release date and activation date. `[MCD]`

34. **Is the timestamp used in conditional logic?** Trace the timestamp to its use. Is it compared against `now()` in an `if` statement? Time-gated behavior is the structural concern. A timestamp used as a version marker is different from one used as an activation gate. `[lens-neutral]`

35. **Does the timestamp correlate with known events or campaigns?** Dates matching known vulnerability disclosures, supply chain attacks, or organizational events may indicate targeted timing. `[MCD]`

## Cross-Cutting

36. **Were any artifacts constructed rather than declared?** Artifacts assembled from fragments (`XFRM.STRCON`), decoded from encoded content (`XFRM.ENCODE`), or decrypted at runtime (`XFRM.ENCRYPT`) indicate deliberate evasion of static detection. Document the construction mechanism and the resulting artifact. `[lens-neutral]`

37. **Do the artifacts collectively describe attacker infrastructure?** Step back from individual artifacts and assess the full set. Do the IPs, domains, URLs, paths, and commands form a coherent operational picture: infrastructure for staging, delivery, execution, persistence, and exfiltration? `[MCD]`

38. **Are the artifacts consistent with the package's dependency graph?** A package that depends on `requests` having embedded URLs is structurally different from a pure computation library with embedded URLs. The dependency graph provides context for what artifacts are expected. `[lens-neutral]`
