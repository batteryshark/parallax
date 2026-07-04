# Tier 5: Immediate Response

## When to Use

The finding is confirmed malicious or the evidence is strong enough that waiting for further confirmation creates unacceptable risk. This is the highest escalation tier. It triggers containment, incident response, and potentially legal and law enforcement engagement.

Tier 5 is activated either through escalation from Tier 4 (an active monitoring alert fires) or directly when investigation reveals unambiguous malicious behavior demanding immediate action (e.g., a supply chain compromise with active credential exfiltration).

## Actions

### Containment (Immediate)

1. **Isolate affected systems.** Network isolation, segment quarantine, or shutdown depending on scope and blast radius.
2. **Block the malicious package or dependency.** Remove from internal registries, block at the proxy/firewall level, prevent further installations.
3. **Revoke potentially compromised credentials.** Any credential that may have been accessed by the malicious code should be rotated immediately: API keys, tokens, SSH keys, cloud credentials, certificates. Assume exposure until proven otherwise.
4. **Preserve evidence.** Before wiping or reimaging, capture forensic artifacts: logs, memory dumps, network captures, the malicious code itself. Evidence preservation is critical for both internal investigation and potential law enforcement engagement.

### Escalation (Immediate)

5. **Notify security leadership.** This is an active security incident, not a finding in a queue.
6. **Engage incident response.** Follow the organization's incident response plan. If MCD detection is the first indicator, the finding becomes the initial evidence for the IR investigation.
7. **Assess legal and regulatory obligations.** Depending on what data was accessed or exfiltrated, there may be breach notification requirements, regulatory reporting obligations, or contractual disclosure duties.
8. **Engage law enforcement if appropriate.** For confirmed attacks (supply chain compromises, credential theft, ransomware), law enforcement engagement may be warranted. This is a decision for legal and security leadership, not the MCD analyst, but the MCD program should surface the recommendation.

### Investigation (Parallel)

9. **Determine blast radius.** What systems ran the malicious code? What credentials were accessible? What data was exposed? Was lateral movement successful?
10. **Trace the attack chain.** Map the finding back to the composition. Use the ontology to systematically identify which atoms are present and reconstruct the full attack: entry vector, payload delivery, persistence, data access, exfiltration, lateral movement.
11. **Identify all affected versions.** If this is a supply chain compromise, determine which versions are malicious and which downstream consumers are affected.

### Recovery

12. **Roll back to known-good state.** Replace the malicious package version with a verified clean version. Redeploy from trusted sources.
13. **Verify containment.** Confirm that all instances of the malicious code have been removed and all compromised credentials have been rotated.
14. **Monitor for re-compromise.** The attacker may attempt to re-establish access. Maintain Tier 4 monitoring on the affected area for an extended period after recovery.

## Examples

- Active exfiltration of credentials to attacker-controlled infrastructure ([BP-CREDTHEFT](../compositions/BP-CREDTHEFT.md) confirmed). Immediate credential rotation and network isolation.
- Supply chain compromise detected in a widely-used internal dependency ([BP-SUPPLY](../compositions/BP-SUPPLY.md) confirmed). Immediate block of the compromised version across all internal registries, audit of all consuming services.
- Ransomware behavior detected in a production system ([BP-RANSOM](../compositions/BP-RANSOM.md) confirmed). Immediate isolation, backup verification, and incident response activation.
- Backdoor with active C2 communication ([BP-BACKDOOR](../compositions/BP-BACKDOOR.md) Variant A confirmed with live C2). Immediate network isolation, forensic capture, and law enforcement engagement.

## Post-Incident

After containment and recovery:

- **Conduct a post-incident review.** How was the malicious code introduced? Why wasn't it caught earlier? What detection gaps existed?
- **Update the ontology and MCD lens if needed.** If the attack used a technique not covered by existing atoms or compositions, propose additions.
- **Update monitoring.** Lessons from the incident should feed back into Tiers 1-4 monitoring for related patterns.
- **Publish findings if appropriate.** Contributing detection signatures, behavioral analysis, or anonymized case studies back to the security community strengthens collective defense. Coordinate with legal and communications teams.
