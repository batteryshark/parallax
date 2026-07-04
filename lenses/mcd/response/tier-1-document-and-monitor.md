# Tier 1: Document and Monitor

## When to Use

The finding is a real signal but is not actionable now. The code does something noteworthy (it accesses sensitive paths, performs crypto operations, or exhibits observations that could be part of a malicious composition), but investigation has not established malicious intent or confirmed benign purpose. The finding is ambiguous.

This tier also applies when the code is **close to a boundary**: the current state is technically benign, but the code is structured so that a small change could complete a malicious composition. A function that reads credential files but currently only logs metadata. A network module that constructs requests to an internal endpoint that could easily be repointed. Crypto operations that encrypt data locally but don't exfiltrate, yet.

## Actions

1. **Document the finding with full context.** What was observed, what the investigation found, and specifically what would escalate the finding if it changed.
2. **Flag the finding for code-level change monitoring.** The specific files, functions, or code paths involved should be watched for changes. This is diff-based surveillance:
   - Did someone modify the flagged function?
   - Did a new dependency appear in the same module?
   - Did the data flow change (e.g., a return value previously unused is now passed to a network call)?
   - Did a hardcoded target (URL, path, IP) change?
3. **Reassess on the next review cycle** or when a monitored change is detected, whichever comes first.

## Examples

- `CRED.ENV` reading environment variables with secret-bearing names, but no `NETW.*` exfiltration channel detected. One added HTTP call away from credential theft.
- `FSYS.SENSITIVE` accessing `~/.ssh/` in a deployment tool where SSH access is plausible but not clearly documented.
- `XFRM.ENCODE` with base64 encoding of configuration values: could be benign config handling or could be concealing operational strings.
- `CRPT.SYMENC` encrypting local data in a utility library where encryption is not a stated feature, but no exfiltration or file-overwrite behavior present.
- `XFRM.STRCON` assembling shell commands from fragments, but fragments are all hardcoded and the resulting command is benign. A change to any fragment could alter the command.

## Escalation Triggers

- A monitored code change removes a blocker (e.g., adds a network call near credential access).
- A monitored code change alters targets (e.g., URL changes from internal to external).
- A new dependency is added to the module containing the finding.
- Contextual signals change (e.g., new maintainer added to the package).
- The finding combines with new observations detected in a subsequent scan to form a composition match.

Escalation typically moves the finding to Tier 3 (Passive Monitoring) or Tier 4 (Active Monitoring) depending on the nature of the change.
