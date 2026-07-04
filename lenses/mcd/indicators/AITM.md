# MCD Lens: AITM (AI-Directed Content) Indicators

> **Core MCD position:** AITM is a fundamentally new attack surface. An attacker no longer needs to trick a human reviewer; they need to trick the AI agent that reviews, approves, or acts on code on behalf of humans. Prompt injection in a dependency costs nothing to include and targets every AI system that reads the code. Through the MCD lens, AITM in a dependency is high severity by default because there is no benign technical explanation for embedding behavioral directives at an LLM inside a third-party library.

## Severity Baselines

| Atom | Baseline Severity | Notes |
|---|---|---|
| `AITM.INJECT` | High | Behavioral directives targeting AI systems in dependency code, no benign explanation in third-party library context |
| `AITM.INJECT` (targeting agentic actions) | Critical | Directives instructing AI to perform tool calls, file writes, network requests, or credential access, direct compromise of agent autonomy |
| `AITM.TOOL` | High | AI tool definitions in dependency context, declared capabilities and implementation routing require assessment against package purpose |
| `AITM.INVISIBLE` | High | Invisible content in dependency code, the invisibility itself is a strong structural signal; content that is hidden from human review but processed by AI has no benign dependency-context explanation |
| `AITM.CONTEXT` | High | Systematic security-relevant misrepresentation in newly written code, measured contradiction between documentation and implementation |

## Escalation Factors

The following conditions increase the MCD severity of any AITM finding:

- **Instructions target agentic or autonomous behavior.** Directives that instruct AI systems to make tool calls, write files, execute commands, modify configurations, or perform actions with side effects. The directive is not just informational, it attempts to cause the AI system to take action in the real world. This is the highest escalation factor for `AITM.INJECT`.
- **Placement in high-read paths.** Content in README files, `__init__.py` docstrings, exported API documentation, package description fields, or other surfaces that AI systems process early and with high priority. These locations maximize the probability and breadth of AI exposure.
- **Transitive dependency.** AITM content in a package that the consumer did not directly choose. Transitive dependencies receive less human review, and their documentation surfaces are processed by AI systems with the same priority as direct dependencies. The combination of reduced human scrutiny and full AI exposure makes transitive dependencies a high-value placement.
- **Combination with `XFRM.UNICODE` (invisible embedding).** Directives or misleading content embedded using invisible Unicode techniques. The content is designed to evade human review entirely while being processed by AI systems. Dual-channel attack: invisible to humans, visible to AI.
- **Payload contains exfiltration instructions.** Directives instruct the AI system to read credentials, environment variables, file contents, or other sensitive data and transmit it to an external endpoint or include it in output. Direct data exfiltration via AI agent.
- **Payload mimics legitimate policy or tool documentation.** Directives are formatted to resemble legitimate system prompts, security policies, tool definitions, or organizational guidelines. The formatting is designed to increase the probability that the AI system treats the content as authoritative.
- **Multiple files or locations.** AITM content appears across multiple files in the package: README, docstrings, comments, configuration files. Redundant placement increases the probability that at least one surface is processed by the target AI system.
- **References specific infrastructure or credentials.** Directives or tool definitions reference specific hostnames, IP addresses, API endpoints, credential paths, or environment variable names. Specificity indicates targeting rather than generic injection.
- **Content introduced in a recent version.** AITM content not present in previous versions. Version-level introduction follows the same pattern as other supply chain injection: a behavioral change in a recent release.

## De-escalation Factors

The following conditions reduce, but do not eliminate, MCD suspicion:

- **Package is an explicit AI/LLM utility library.** The package's stated purpose is to provide AI integration, prompt management, agent tooling, or LLM utility functions. AI-directed content is within the package's declared scope. `AITM.TOOL` findings in an MCP server library, `AITM.INJECT`-like patterns in a prompt engineering toolkit, or `AITM.CONTEXT` patterns in AI training/evaluation data are more consistent with stated purpose than the same findings in a date formatting library.
- **Finding isolated to test or example directories excluded from published artifact.** AITM content in `test/`, `examples/`, or `docs/` directories that are not included in the published package artifact. The content exists in the repository but is not distributed to consumers. Verify exclusion: check `.npmignore`, `MANIFEST.in`, or equivalent to confirm the directory is actually excluded from the published package.
- **Demonstrably AI-generated documentation noise (limited de-escalation).** Content that appears to be AI-generated documentation artifacts, generic imperative patterns produced by LLM-assisted documentation generation rather than targeted injection. This is a weak de-escalation because the boundary between AI-generated documentation noise and effective prompt injection is not reliably distinguishable, and an attacker can deliberately produce injection that resembles AI documentation artifacts.

> **Caveat:** De-escalation for AITM is narrower than for other categories. The core question, "why does this dependency contain content targeting AI behavior?", has very few benign answers outside of explicit AI tooling. The de-escalation factors above reduce priority for investigation; they do not resolve the finding.

## Interpretive Combinations

| Combination | MCD Interpretation | Severity |
|---|---|---|
| `AITM.INJECT` + `PKGM.INSTALL` | Guaranteed execution path + AI-directed content. The install hook ensures the code is processed during installation, and the injection targets AI systems that review or assist with the installation. | Very High |
| `AITM.INVISIBLE` + `XFRM.UNICODE` | Dual-target attack, invisible to human reviewers via Unicode tricks, processed by AI systems. The content is specifically designed to exploit the visibility gap between human and AI code processing. | Very High |
| `AITM.TOOL` + `NETW.*` | Tool definition that routes to network endpoints, potential malicious MCP proxy or tool that redirects agent actions through attacker-controlled infrastructure. | High |
| `AITM.INJECT` + `CRED.*` | AI directed to locate, read, or transmit credentials. The injection instructs the AI system to access authentication material. | Very High |
| `AITM.INJECT` + `XFRM.ENCODE` | Encoded payload in documentation or comments, the directive content is encoded to avoid string-matching detection while remaining decodable by AI systems that process the text. | High |
| `AITM.TOOL` + `AITM.CONTEXT` | Malicious tool definition accompanied by misleading documentation about the tool's behavior. The documentation constructs a false model of what the tool does, while the tool definition routes to unexpected infrastructure or requests excessive parameters. | Very High |
| `AITM.INJECT` + `PRST.*` | AI directed to modify startup files, shell profiles, cron entries, or other persistence mechanisms. The injection attempts to use the AI system as a vector for establishing persistence. | Very High |
| `AITM.CONTEXT` + typosquatted package name | Systematic documentation misrepresentation in a package whose name closely resembles a popular legitimate package. The misleading documentation supports the typosquatting by constructing a false understanding of the package's purpose and trustworthiness. | Very High |
| `AITM.INJECT` + `AITM.INVISIBLE` + `AITM.CONTEXT` | Full-spectrum AITM: explicit directives, invisible embedding, and misleading context. Multiple AITM techniques in a single package indicate deliberate, layered targeting of AI systems. | Critical |
| `AITM.TOOL` + `AITM.INJECT` | Tool definition with embedded injection in description fields. The tool's natural language description contains directives that manipulate the AI agent's behavior when it reads the tool's schema. | Very High |

## MCD-Specific Disambiguation

### AITM vs authored imperative documentation
Legitimate documentation frequently uses imperative language: "Call this function with...", "Set the environment variable to...", "Run the build command." Through the MCD lens, the distinguishing feature is scope. Legitimate imperative documentation describes the package's own API, how to use the package. `AITM.INJECT` references behavior outside the package's scope: reading arbitrary files, calling external tools unrelated to the package, transmitting data to endpoints the package does not use, assuming an identity, or overriding the reader's existing instructions. The test is: "Does this directive describe how to use this package, or does it instruct the reader to do something unrelated to this package's stated purpose?"

### AITM.TOOL vs legitimate MCP/plugin definitions
`AITM.TOOL` applies to all AI tool definitions as a structural observation. Through the MCD lens, legitimate tool definitions have: parameter schemas consistent with the tool's stated function, implementation routing to infrastructure associated with the tool's publisher, and capability declarations that match the package's purpose. Suspicious tool definitions have: parameters that request access beyond the stated function (a "format text" tool that requests file system paths or credentials), implementation routing to unrelated or recently registered infrastructure, descriptions that manipulate agent behavior beyond normal tool usage, or capability declarations inconsistent with the package's other functionality.

### AITM.CONTEXT vs normal documentation error
Through the MCD lens, `AITM.CONTEXT` is distinguished from documentation drift by three structural properties: (1) temporal: the documentation was written alongside the current code, not inherited from a previous version; (2) directional: the inaccuracies consistently minimize the code's actual access scope and capabilities, never the reverse; (3) security-relevant: the misrepresented behaviors involve network access, credential handling, file system scope, or privilege level. Documentation that randomly drifts in both directions (sometimes overstating, sometimes understating capabilities) across a long-lived codebase is maintenance debt. Documentation that systematically understates security-relevant behavior in newly written code is `AITM.CONTEXT`.
