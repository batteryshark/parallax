# BP-LATERAL: Lateral Movement

Once executing on one system, spreads presence to other systems within the same environment. Distinct from BP-WORM: worms propagate to external systems across network boundaries; lateral movement operates within an environment the attacker already has a foothold in.

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | `SYSI.NET` or `SYSI.PROC` or `SYSI.SW` | Discovery of lateral targets: other hosts, nodes, containers, services |
| **Required** | `CRED.*` or `PRIV.*` | Access mechanism: stolen credentials, escalated privileges, abused trust |
| **Required** | `EXEC.*` or `FSYS.WRITE` or `PRST.*` | Action on new target: commands, payloads, or persistence |
| Supporting | `CRED.SSH` | Stolen SSH keys for host-to-host movement |
| Supporting | `CRED.CLOUD` | Harvested cloud credentials for infrastructure access |
| Supporting | `CRED.TOKEN` | Kubernetes/API tokens for adjacent service access |
| Supporting | `SYSI.PROCMEM` | Reading process memory for runtime secrets |
| Supporting | `PRIV.EXPLOIT` | Container escape or privilege escalation |
| Supporting | `NETW.HTTP` | API-based orchestration interaction (Kubernetes API, cloud control planes) |
| Supporting | `PRST.SERVICE` | Persistence on each newly compromised node |

## Real-World Analogues

LiteLLM's Kubernetes lateral movement: enumerate nodes, create privileged pods per node, chroot to host filesystem, install systemd backdoor. Trivy's credential chain: harvest CI/CD secrets, publish malicious packages to other ecosystems.

## Investigation Guidance

- **Verify:** What infrastructure discovery? What credentials/access? What actions on each new target?
- **Escalates:** Automated loop targeting multiple systems. Privileged containers created. Persistence on each target. Harvested credentials used. Container escape.
- **De-escalates:** Consistent with documented orchestration/deployment tooling. Own legitimately scoped credentials. Limited to documented purpose.
