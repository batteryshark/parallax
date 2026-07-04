# ENVI.FORENSIC: Forensic Artifact Manipulation

## Description

Manipulates artifacts that would be used in post-incident analysis. Includes timestomping (setting file creation/modification times to false values), deleting or truncating log files and shell history, overwriting disk slack space, wiping recently-used file lists, modifying audit trails, and replacing artifacts with substitute content. The mechanical behavior is altering or destroying the historical record of system activity.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `os.utime()`, `SetFileTime()`, `touch -t`, shell history file manipulation, log file truncation, file replacement sequences (delete + rename) |
| Static Binary | Yes | Timestamp manipulation API imports, history file path strings, evidence file path references |
| Runtime/Dynamic | Yes | File timestamp changes inconsistent with actual modification, history file truncation, file replacement operations |

## Disambiguation

- **vs ENVI.LOG**: LOG suppresses ongoing event recording, preventing new evidence from being created. FORENSIC alters or destroys existing evidence, manipulating the historical record after events have occurred. Disabling an audit daemon is LOG. Clearing the audit log it already wrote is FORENSIC.
- **vs FSYS.WRITE / FSYS.DELETE**: FORENSIC involves filesystem operations but describes a specific behavior, manipulating artifacts for their evidentiary value. A generic file delete is FSYS.DELETE. Deleting a shell history file or replacing a previously-written file with a clean substitute targets the evidentiary record specifically. The distinction is the target: operational data vs. historical/forensic artifacts.
- **vs normal file operations**: Applications routinely create, modify, and delete files. ENVI.FORENSIC applies when the target is a forensic-relevant artifact (timestamps, logs, history files, audit trails) and the operation alters the historical record rather than performing an operational function.

## Structural Relationships

- **Often co-occurs with**: `ENVI.MASQ` (artifact replacement combined with identity disguise), `FSYS.WRITE` / `FSYS.DELETE` (underlying filesystem operations), `ENVI.TIMING` (delayed cleanup)
- **May imply**: Historical artifacts on the system are being altered to misrepresent what occurred

## Notes

Evidence replacement (substituting a convincing artifact for a malicious one) is structurally different from evidence deletion (removing the artifact entirely). Deletion leaves an observable absence. Replacement leaves a plausible artifact that passes existence checks. The type of manipulation and the specificity of the targeted artifacts are the key structural data points.
