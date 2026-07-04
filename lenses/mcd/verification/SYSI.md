# MCD Lens: SYSI (System Inspection) Verification

## General: Any SYSI Atom

1. **What is the full set of SYSI subtypes present in this package?** Enumerate all system inspection behaviors across the codebase. A single OS query differs from OS + user + network + processes + hardware. The breadth of collection is itself a primary signal. `[lens-neutral]`

2. **When does collection execute?** Identify the execution trigger: install hook (`postinstall`, `setup.py`), module import (`__init__.py`, top-level module code), explicit function call, or deferred lazy initialization. Install-time and import-time collection have no user-initiated context. `[lens-neutral]`

3. **Where do collected values go? Trace the data flow.** Follow each collected value from the point of query to its final destination. Is it used locally (path selection, resource allocation), stored in a variable or file, serialized into a data structure, or passed to a network call? The local-to-remote boundary is the critical transition. `[lens-neutral]`

4. **Does any `NETW.*` atom co-occur anywhere in the package?** Search the entire package, not just the file containing SYSI code, for any network communication. Data may be collected in one module and transmitted from another. Trace whether collected SYSI data reaches any network egress point, including indirect paths through shared state or files. `[MCD]`

5. **Does the package's stated category create a plausible expectation for this inspection?** Build tools may query OS/architecture. Network utilities may query interfaces. Process managers may list processes. Evaluate whether the specific inspection behavior aligns with the package's functional purpose. A color formatting library querying hardware serial numbers has no category alignment. `[lens-neutral]`

## SYSI.PROC

6. **Are specific process names present in a checklist?** Search for hardcoded process name strings, especially names matching known AV products, EDR agents, sandbox components, debuggers, or security monitoring tools. Document the exact names. A generic `process_iter()` differs from one that checks results against `["wireshark", "procmon", "fiddler", "ollydbg"]`. `[lens-neutral]`

## SYSI.HW

7. **Which hardware attributes are collected, and do any map to VM detection primitives?** Identify the specific hardware fields queried. Flag: CPUID hypervisor bit, MAC OUI prefixes for virtual NICs (00:0C:29, 00:50:56, 08:00:27), DMI/SMBIOS strings checked against virtualization keywords, core/RAM thresholds used as VM heuristics. If present, `ENVI.SANDBOX` co-applies. `[lens-neutral]`

## SYSI.PROCMEM

8. **What is the target process, and what data is being extracted?** Identify the target process by name, PID selection method, or enumeration pattern. Determine what memory regions or data the code seeks: credentials, tokens, session data, encryption keys, or general memory dumps. The target determines severity: reading a process you own for debugging differs from reading `lsass.exe` or a browser process. `[lens-neutral]`

## SYSI.SW + SYSI.NET

9. **Are hardcoded values present in conditionals consuming SYSI output?** Search for string comparisons, regex matches, or lookup tables applied to collected system data. Hardcoded hostnames, usernames, IP ranges, software names, or version strings in conditionals indicate targeted logic: the code is looking for specific environments or configurations. `[MCD]`

## Version History

10. **When was the inspection code introduced, and has it changed?** Use `git log -S` or version diffs to identify when each SYSI behavior was added. System inspection present since v1.0 in a diagnostic tool is structurally different from system inspection introduced in a patch release of a utility library. Sudden introduction or expansion of collection scope in a maintenance update is a supply chain compromise indicator. `[lens-neutral]`
