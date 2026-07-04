# BP-TROJAN: Trojan / Disguised Payload

Presents a legitimate, useful interface while concealing malicious functionality. The package does what it claims, but also does something the user did not request. Harder to detect because legitimate functionality provides cover.

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | *Any malicious payload atom combination* | The hidden malicious behavior |
| **Required** | `XFRM.*` or *structural concealment* | Malicious behavior concealed within legitimate code |
| Supporting | `ENVI.ENVCHECK` | Activating only in specific environments |
| Supporting | `TIME.CMP` | Delaying activation to pass initial review |
| Supporting | `LOAD.EVAL` or `LOAD.IMPORT` | Dynamic loading of malicious component |

## Investigation Guidance

- **Verify:** Does the package do what it claims? What additional behaviors exist? Is malicious code loaded conditionally?
- **Escalates:** Hidden functionality targets specific victims/environments. Introduced in recent update by new contributor. Concealment is sophisticated.
- **De-escalates:** All code consistent with documented purpose. No concealment detected.
