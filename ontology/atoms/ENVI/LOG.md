# ENVI.LOG: Audit and Logging Modification

## Description

Modifies, disables, redirects, or suppresses logging and monitoring systems. Includes clearing event logs, disabling audit trail generation, unhooking monitoring APIs, redirecting log output to null destinations, terminating or suspending monitoring processes, and modifying kernel audit rules or logging configuration. The mechanical behavior is altering the system's ability to record events.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Event log clearing APIs, service stop commands targeting monitoring processes, audit rule modification, log file truncation/deletion, output redirection to `/dev/null` |
| Static Binary | Yes | Imports for event log manipulation APIs, monitoring service name strings, audit subsystem references |
| Runtime/Dynamic | Yes | Event log entries disappearing, monitoring services stopping, audit rule changes, log file size changes |

## Disambiguation

- **vs ENVI.SECDISABLE**: LOG targets the recording of events, clearing logs, suppressing audit output, stopping monitoring processes. SECDISABLE targets active defensive controls, disabling firewalls, adding AV exclusions, weakening exploit mitigations. LOG affects whether events are observed after the fact. SECDISABLE affects whether security controls prevent or detect activity in real time.
- **vs ENVI.FORENSIC**: LOG suppresses ongoing monitoring and event recording. FORENSIC manipulates historical artifacts (timestamps, evidence files) after events have occurred. LOG prevents new evidence from being created. FORENSIC alters or destroys existing evidence.
- **vs normal log management**: Log rotation, compression, level-based filtering, and retention policy enforcement are standard operational practices. ENVI.LOG applies when suppression targets security-relevant output or named monitoring components, not routine log lifecycle management.

## Structural Relationships

- **Often co-occurs with**: Any atom whose activity the logging suppression would record, the suppressed monitoring would have captured the co-occurring behavior
- **May imply**: The system's event recording capability is being reduced

## Notes

The specificity of the suppression is key structural data. Reducing log verbosity is generic. Terminating a named monitoring process or clearing a specific audit category is targeted. The mechanical behavior is the same, modifying the logging/monitoring system, but the target specificity varies.
