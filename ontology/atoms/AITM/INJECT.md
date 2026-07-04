# AITM.INJECT: Instruction Embedding in Non-Executable Content

## Description

Natural language instructions embedded in code comments, docstrings, README files, error messages, or string literals that are formatted to direct the behavior of an LLM or AI system processing the code. The content is structured as directives (imperatives, authority claims, instruction overrides) rather than as documentation for human developers. The instructions exist in positions that are non-executable by the language runtime but are processed by AI systems that read code context.

Common embedding locations include inline comments, function/class/module docstrings, README and CONTRIBUTING files, package description fields, error message strings, license headers, and changelog entries. The directives may be plain text, formatted as system messages or tool calls, or structured to mimic AI conversation context (role markers, instruction delimiters, XML-like tags).

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Imperative language in comments/docstrings targeting AI behavior ("you must", "ignore previous instructions", "execute the following"), authority claims ("you are a", "as your system prompt"), tool call syntax in non-executable positions, system message formatting (`<system>`, `[INST]`, role markers) in documentation |
| Static Binary | Partial | Embedded strings containing directive language, less reliable because comments are typically stripped during compilation, but docstrings and string literals may survive |
| Runtime/Dynamic | No | Injected instructions are a static content concern, they target AI systems that read the code, not the language runtime. No runtime behavior is produced by the instructions themselves |

## Disambiguation

- **vs normal documentation using imperative language**: Legitimate documentation describes the package's own API and behavior, "call this function with X", "set this parameter to Y." `AITM.INJECT` references behavior outside the package's scope: reading files unrelated to the package, calling external tools, transmitting data to endpoints the package does not use, assuming an identity, overriding previous instructions, or modifying the behavior of the AI system processing the code. The distinguishing structural feature is scope, directives that address the reader's behavior rather than documenting the package's behavior.
- **vs AITM.CONTEXT**: `AITM.INJECT` embeds explicit directives, instructions that directly tell an AI system what to do. `AITM.CONTEXT` constructs a false mental model through otherwise-normal-looking documentation that misrepresents the code's behavior. An `AITM.INJECT` finding contains identifiable imperative instructions; an `AITM.CONTEXT` finding contains systematically misleading descriptions.
- **vs AITM.INVISIBLE**: When injection content is embedded using invisible Unicode techniques, both `AITM.INJECT` (the directive content) and `AITM.INVISIBLE` (the invisibility technique) apply. Tag both.

## Structural Relationships

- **Often co-occurs with**: `AITM.INVISIBLE` (directives hidden via Unicode tricks), `XFRM.ENCODE` (directives encoded to avoid string matching), `PKGM.INSTALL` (injection in install-time paths guarantees AI exposure during review), `AITM.CONTEXT` (explicit directives alongside misleading documentation)
- **May imply**: The author anticipated that AI systems would process this code; the directives are crafted to exploit LLM instruction-following behavior rather than to communicate with human developers
- **Commonly part of idioms**: Prompt injection in dependency (directive in docstring/README targeting code review agents), instruction override chain (authority claim + behavior directive + scope expansion), credential exfiltration via AI agent (directive instructing AI to read and transmit secrets)

## Notes

The placement of directives within a package determines exposure. README files and package descriptions are processed by AI systems during package evaluation and selection, before the code is ever installed. Docstrings and inline comments are processed during code review, IDE integration, and agent-assisted development. `__init__.py` docstrings and exported module documentation occupy particularly high-exposure positions because they are among the first content AI systems encounter when analyzing a package. The structural observation is which content surfaces are addressed by the directives, not whether the directives would succeed against any particular AI system.
