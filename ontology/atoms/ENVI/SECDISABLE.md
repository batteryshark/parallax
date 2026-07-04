# ENVI.SECDISABLE: Security Control Modification

## Description

Disables, weakens, or reconfigures security mechanisms on the host system. Includes firewall rule manipulation (creating permissive inbound rules, disabling host firewalls), exploit mitigation disabling (turning off ASLR, DEP, Control Flow Guard, stack canaries), security tool exclusion injection (adding paths or processes to AV/EDR exclusion lists), security policy weakening (modifying AppLocker, SELinux, AppArmor, Gatekeeper, SIP, SmartScreen settings), and security status reporting suppression (spoofing security center status indicators). The mechanical behavior is modifying the configuration of active security controls.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Firewall rule creation/deletion commands, registry writes to security policy keys, `netsh advfirewall` / `iptables` / `pfctl` invocations, AV exclusion API calls, exploit mitigation configuration changes |
| Static Binary | Yes | Security tool configuration paths, firewall command strings, security policy registry key paths, AV exclusion list API references |
| Runtime/Dynamic | Yes | Firewall rule changes, security policy modifications, AV exclusion list additions, exploit mitigation state changes |

## Disambiguation

- **vs ENVI.LOG**: LOG targets event recording, the system's ability to observe and log activity. SECDISABLE targets active defensive controls, the system's ability to prevent or block activity. Disabling a firewall is SECDISABLE. Clearing the firewall's connection log is LOG.
- **vs CRPT.CERT**: Certificate operations (installing CAs, disabling TLS verification) specifically target the PKI trust model and are classified as CRPT.CERT. SECDISABLE covers other host-level security controls: firewalls, endpoint protection, exploit mitigations, OS security policy. When both certificate manipulation and broader security disabling occur together, both atoms apply.
- **vs PRIV.ELEVATE** (future): Privilege escalation acquires higher permissions. Security disabling modifies the configuration of controls that operate at the current privilege level. Disabling a user-mode security feature is SECDISABLE. Gaining root/admin access is privilege escalation. Both may be needed, escalate privileges to then disable a control that requires elevated access to modify.

## Structural Relationships

- **Often co-occurs with**: `ENVI.LOG` (suppress monitoring AND disable controls), `CRPT.CERT` (certificate manipulation as part of broader security weakening), operations that the disabled control would have blocked
- **May imply**: Active security controls on the host have been modified from their default or administrator-configured state

## Notes

The scope of the modification is key structural data. A rule targeting a specific program on a specific port differs from a blanket rule allowing any program on any port. An AV exclusion for a single file differs from excluding a directory tree. Whether the modification is restored after use or left permanent is also structurally relevant. The specific control being modified, the scope of the change, and the persistence of the change are the primary observations.
