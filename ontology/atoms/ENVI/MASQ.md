# ENVI.MASQ: Runtime Artifact Identity Disguise

## Description

Renames, copies, or disguises runtime artifacts (files, binaries, processes, services, or network traffic) to resemble legitimate system components. Includes binary masquerading (copying a legitimate executable to a new name or placing a binary in a path that mimics OS conventions), process name manipulation (spawning processes with names that match system services), service registration with names mimicking legitimate services, and traffic pattern construction (crafting network requests that resemble legitimate traffic in structure or content). The mechanical behavior is making one artifact appear to be a different, typically well-known, artifact.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | File copy/rename operations targeting system paths, process name setting, service registration with system-like names, network request construction mimicking known patterns |
| Static Binary | Yes | System binary names as string constants, OS-convention path strings, service name strings matching known system services |
| Runtime/Dynamic | Yes | Files in system paths that don't match expected hashes, processes with system names running from unusual paths, network traffic with spoofed structural patterns |

## Disambiguation

- **vs XFRM.RENAME**: XFRM.RENAME transforms source-level identifiers (function names, variable names, class names), artifacts visible in code review and static analysis. ENVI.MASQ transforms runtime artifact identities (file names on disk, process names in task lists, service display names, network traffic patterns), artifacts visible during execution and post-execution analysis. The distinction is the artifact layer: source code vs. runtime.
- **vs FSYS.WRITE**: Writing a file is FSYS.WRITE. Writing a file with a name that mimics a legitimate system component to a location that mimics an OS convention path is FSYS.WRITE + ENVI.MASQ. The MASQ atom describes the identity mimicry aspect, not the filesystem operation itself.

## Structural Relationships

- **Often co-occurs with**: `ENVI.FORENSIC` (evidence replacement combined with artifact disguise), `FSYS.WRITE` (placing disguised files), `EXEC.PROC` (spawning disguised processes)
- **May imply**: Runtime artifacts on the system do not represent what their names suggest

## Notes

The fidelity of the disguise is a structural data point. Using a generic nonsense name is not ENVI.MASQ. Using a name that specifically matches a real signed OS component, placed in a path that follows the OS naming convention, is high-fidelity masquerading. The closeness of the match to a real component and whether the mimicked component actually exists on the system are key observations.
