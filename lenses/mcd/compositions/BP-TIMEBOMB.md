# BP-TIMEBOMB: Logic Bomb / Time Bomb

Remains dormant until a specific condition triggers activation: a date passes, a counter reaches a threshold, an environment variable appears, or a network signal is received. Passes all analysis during the dormant period.

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | `TIME.CMP` or `ENVI.ENVCHECK` | The trigger condition |
| **Required** | *Any payload atoms* | The behavior that activates when condition is met |
| Supporting | `ARTF.TIMESTAMP` | Hardcoded activation date |
| Supporting | `TIME.DELAY` | Delay before activation |
| Supporting | `XFRM.*` | Concealing trigger logic or payload |
| Supporting | `ENVI.TIMING` | Ensuring the bomb doesn't trigger during analysis |

## Investigation Guidance

- **Verify:** What is the trigger condition? What activates? Has the condition already been met?
- **Escalates:** Trigger is specific future date. Payload involves destruction, exfiltration, or backdoor. Trigger logic is transformed/concealed.
- **De-escalates:** Time comparison for cache expiration or rate limiting. Conditional gates a documented feature.
