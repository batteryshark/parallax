# MCD Response Framework

When the MCD lens produces a finding (an atom observation, a composition match, or a combination escalated by contextual signals), the next question is: **what do you do about it?**

This framework defines six response tiers, from closing a benign finding to engaging incident response on a confirmed compromise. Every finding should map to exactly one tier based on the investigation outcome. Tiers are not permanent. A finding can escalate or de-escalate as new evidence emerges or monitored code changes.

Response is entirely lens-specific. These tiers are the MCD lens's response framework. Other lenses define their own response actions (architecture: refactor/document debt/add tests; capability: restrict permissions/add guardrails).

## Response Tiers

| Tier | Name | Summary |
|---|---|---|
| 0 | [Informational / Close](tier-0-informational.md) | Investigated, confirmed benign. Document and close. |
| 1 | [Document and Monitor](tier-1-document-and-monitor.md) | Noted signal, not actionable now. Watch for code changes that would escalate. |
| 2 | [Engineering Referral](tier-2-engineering-referral.md) | Security flaw or dead code, not malicious. Route to engineering for remediation. |
| 3 | [Passive Monitoring](tier-3-passive-monitoring.md) | Add logging and instrumentation. Track execution and code changes. |
| 4 | [Active Monitoring and Alerting](tier-4-active-monitoring.md) | Real-time detection and alerting. Prepare containment. |
| 5 | [Immediate Response](tier-5-immediate-response.md) | Confirmed or high-confidence malicious. Contain, escalate, and respond. |

## Tier Selection

Tier selection is driven by two factors:

1. **Current state**: What does the evidence say right now? Is this benign, ambiguous, suspicious, or confirmed malicious?
2. **Proximity to harm**: How close is this code to being weaponized? A function that reads credentials but doesn't transmit them is one code change away from a credential theft composition. That proximity matters even if the current state is technically benign.

The MCD [confidence parameterization](../confidence/) maps severity and confidence levels to starting tiers:

| Severity | Low Confidence | Medium Confidence | High Confidence |
|---|---|---|---|
| Informational | Tier 0 | Tier 0 | Tier 0 |
| Low | Tier 0-1 | Tier 1 | Tier 1 |
| Medium | Tier 1 | Tier 1-3 | Tier 3 |
| High | Tier 3-4 | Tier 3-4 | Tier 4-5 |
| Critical | Tier 4-5 | Tier 4-5 | Tier 5 |

These are starting points, not rules. Practitioner judgment determines the final tier.

## Monitoring for Change

A core principle: **findings are not static.** Code changes. Dependencies update. Behaviors that are benign today can become malicious with a single commit.

Tiers 1 and 3 both include monitoring, but at different levels:

- **Tier 1** monitors at the **code level**: watching for diffs, new dependencies, function signature changes, or new code paths near the finding. This is static surveillance. The question: "did someone change this in a way that escalates the finding?"
- **Tier 3** monitors at both the **code level and runtime level**: instrumentation to detect whether the code path executes in production, combined with code-level change detection. The question: "is this executing, and is the code changing in ways that remove blockers preventing harm?"

A finding that is one code change away from being weaponized should never be Tier 0. Even if the current state is technically benign, proximity to harm demands at minimum Tier 1 with explicit change monitoring.
