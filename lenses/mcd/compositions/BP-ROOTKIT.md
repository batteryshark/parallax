# BP-ROOTKIT: Rootkit / Self-Modification

Modifies the operating environment to hide its presence or that of other malicious components. Operates below normal application code, intercepting system calls, modifying kernel structures, or altering inspection tools to report false information.

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | `PRST.HOOK` or `PRIV.EXPLOIT` | System-level modification capability |
| **Required** | `ENVI.LOG` or `ENVI.TAMPER` | Active concealment of presence |
| Supporting | `EXEC.INJECT` | Injecting into system processes |
| Supporting | `LOAD.DYLIB` | Loading interceptor libraries |
| Supporting | `FSYS.PERM` | Modifying file permissions to control visibility |
| Supporting | `PRIV.*` | Privilege escalation to gain modification access |

## Investigation Guidance

- **Verify:** What system components modified? What is being hidden? What access level required?
- **Escalates:** Kernel-level modifications. System call interception. Security tool modification.
- **De-escalates:** Hook is documented plugin mechanism. Modification to package's own files.
