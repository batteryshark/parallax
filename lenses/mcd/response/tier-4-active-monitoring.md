# Tier 4: Active Monitoring and Alerting

## When to Use

The finding is high-confidence suspicious or the code has been observed exhibiting behaviors consistent with a malicious composition. The investigation has not yet definitively confirmed malicious intent, but the evidence is strong enough that execution of the flagged behavior should trigger an immediate alert with containment prepared.

This is also the appropriate tier when passive monitoring (Tier 3) has revealed concerning runtime behavior: the instrumentation showed something unexpected and the finding has escalated.

## Actions

1. **Deploy real-time detection and alerting.** Move beyond passive logging to active alerting:
   - Alert on execution of the flagged code path.
   - Alert on network connections to flagged destinations.
   - Alert on file access to flagged sensitive paths.
   - Alert on any behavior that completes a composition match that was previously partial.
2. **Prepare containment actions.** Define and stage, but do not yet execute, containment measures:
   - Network isolation of affected systems.
   - Blocking or quarantining the package or dependency.
   - Revoking credentials that may be compromised.
   - Rolling back to a known-good version.
3. **Continue code-level monitoring** with heightened scrutiny. Any code change to the flagged area should trigger immediate review, not wait for the next cycle.
4. **Brief relevant stakeholders.** Security leadership, the team that owns the affected code, and anyone who needs to be ready to act should be aware that a finding is at Tier 4.
5. **Define the trigger for Tier 5.** Be explicit: "If this alert fires, we execute containment plan X." The transition from Tier 4 to Tier 5 should not require a meeting. It should be a predefined action.

## Examples

- [BP-CREDTHEFT](../compositions/BP-CREDTHEFT.md) composition with all required atoms present (`CRED.CLOUD` + `NETW.HTTP`), confirmed by passive monitoring showing the code path executing, but the destination appears to be a legitimate analytics service. Active monitoring to alert if the destination changes or the request payload includes credential material.
- [BP-BACKDOOR](../compositions/BP-BACKDOOR.md) Variant A: pattern match with `NETW.LISTEN` + `EXEC.SHELL` in a package recently updated by a new maintainer. The listener has not been observed accepting connections, but the capability exists.
- A package where passive monitoring detected intermittent outbound connections to an IP not present in the source, suggesting dynamic resolution or a configuration change since the last static scan.
- Escalation from Tier 3 where instrumentation revealed a `TIME.CMP` condition will be met within days and the gated code path includes `NETW.HTTP` + `FSYS.READ`.

## Escalation Triggers

- An active alert fires: the flagged behavior has executed in a way consistent with the suspected malicious composition.
- New evidence confirms malicious intent (e.g., network destination confirmed as attacker infrastructure, exfiltrated data confirmed as credentials).
- Code changes remove remaining doubt.

Escalation moves immediately to Tier 5 (Immediate Response).

## De-escalation Triggers

- Extended active monitoring with no alerts firing.
- New evidence explains the behavior as benign (e.g., new maintainer is confirmed legitimate, network destination is confirmed as an authorized service).
- The flagged code is removed or refactored.

De-escalation moves the finding to Tier 3 (Passive Monitoring) or Tier 1 (Document and Monitor).
