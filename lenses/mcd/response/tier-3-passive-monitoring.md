# Tier 3: Passive Monitoring

## When to Use

The finding is suspicious enough to warrant instrumentation but not urgent enough to require real-time alerting. The investigation is inconclusive (the code could be benign or malicious), and the answer depends on whether the behavior actually executes in production and whether the code changes over time.

This tier bridges the gap between "we noticed something" (Tier 1) and "we need to respond now" (Tier 4). It adds runtime visibility to code-level monitoring: you're not just watching the code for changes; you're watching whether the code *runs* and what it does when it does.

## Actions

1. **Instrument the code path.** Add logging, tracing, or telemetry around the flagged functionality to capture:
   - Whether the code path is executed at all in production.
   - What data flows through it (inputs, outputs, targets).
   - How frequently it executes and under what conditions.
2. **Monitor for code changes** (same as Tier 1). Watch the flagged files and functions for diffs that alter the finding's risk profile. Specifically:
   - Addition of a network call near data access (completing an exfiltration composition).
   - Changed hardcoded targets (URLs, IPs, paths).
   - Addition of obfuscation (`XFRM.*`) to previously clear code.
   - New dependencies in the same module.
   - Removal of a blocker that was preventing harm.
3. **Review instrumentation data periodically.** Passive monitoring means collecting data, not acting on it in real time. Review on a defined cadence.
4. **Define explicit escalation criteria.** Before walking away, document what would move this to Tier 4. Make it concrete: "If this function is called with a non-internal IP as the target, escalate to Tier 4."

## Examples

- `CRED.SSH` + `FSYS.READ` in a deployment tool: reading SSH keys is plausible for its stated purpose, but add logging to confirm it only reads keys for documented hosts, not all keys in `~/.ssh/`.
- `NETW.HTTP` with a hardcoded URL to an external service: the service appears legitimate, but instrument the call to log request bodies and confirm no sensitive data is transmitted.
- Partial composition match for [BP-DROPPER](../compositions/BP-DROPPER.md): a package downloads a file during install, but the file appears to be a legitimate data resource. Instrument to confirm the downloaded content is consistent over time and is not replaced with an executable.
- `TIME.CMP` + `ARTF.TIMESTAMP`: a time comparison against a future date where the gated code path is unclear. Instrument to detect when the condition is met and what executes.

## Escalation Triggers

- Instrumentation reveals the code path is executing with unexpected inputs, targets, or frequency.
- Instrumentation reveals data exfiltration, credential access, or command execution not visible through static analysis.
- Code changes remove a blocker or alter the finding's risk profile.
- The finding combines with new evidence to complete a composition match.

Escalation moves the finding to Tier 4 (Active Monitoring) or directly to Tier 5 (Immediate Response) if instrumentation data reveals confirmed malicious behavior.

## De-escalation Triggers

- Instrumentation over a defined period shows the code path is never executed.
- Instrumentation confirms the behavior is consistent with the package's stated purpose.
- Code changes resolve the ambiguity (e.g., the suspicious function is refactored into something clearly benign).

De-escalation moves the finding to Tier 1 (continued code-level monitoring) or Tier 0 (close).
