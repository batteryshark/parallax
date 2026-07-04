# BP-AGENTMANIP: Agent Manipulation

Content designed to manipulate AI agents that process, review, or act on the codebase. The target is not the machine running the code but the AI system analyzing it. The code does not need to execute; it only needs to be read by an agent with tool access.

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | `AITM.INJECT` or `AITM.TOOL` or `AITM.INVISIBLE` | AI-targeting content must be present |
| Supporting | `AITM.CONTEXT` | Misleading documentation supporting the manipulation |
| Supporting | `XFRM.UNICODE` | Unicode tricks to hide injection from human review |
| Supporting | `EXEC.*` | Commands the agent is being instructed to run |
| Supporting | `PKGM.*` | Package operations the agent is directed to approve |

## Investigation Guidance

- **Verify:** What instructions embedded? What AI system targeted? What would happen if an agent followed the instructions?
- **Escalates:** Instructions direct agent to execute commands, approve changes, or suppress findings. Hidden with Unicode. Multiple injection points reinforce same instruction.
- **De-escalates:** Legitimate documentation or comments. No executable instructions directed at AI systems.
