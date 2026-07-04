# MCD Lens

*"Is this malicious?"*

The Malicious Code Detection lens evaluates software behaviors for indicators of malicious intent: supply chain attacks, backdoors, data exfiltration, credential theft, and related threats.

## Components

- **Indicators**: what ontology atoms and idioms suggest through the MCD lens (severity baselines, escalation/de-escalation factors)
- **Compositions**: behavioral patterns (BP-SUPPLY, BP-BACKDOOR, etc.) built from ontology terms with required and supporting elements
- **Confidence modifiers**: contextual signals specific to MCD (package metadata, dependency graph, temporal signals, network destination, etc.)
- **Verification playbooks**: investigation questions and method recommendations
- **Response framework**: tiers 0-5 from informational through immediate response

## Status

Complete as a first framework pass.

The MCD lens now contains:

- indicator files for all 16 ontology categories
- verification files for all 16 ontology categories
- 15 MCD composition files
- 6 contextual signal categories
- confidence parameterization
- response tiers 0-5

Executable tooling exists: in the [parallax](https://github.com/batteryshark/parallax) reference implementation, the engine emits ontology observations and the `prlx-mcd` product evaluates them into findings with confidence, disproof criteria, verification guidance, and response tier recommendations.
